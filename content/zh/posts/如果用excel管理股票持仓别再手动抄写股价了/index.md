---
title: "如果用Excel管理股票持仓，别再手动抄写股价了"
date: 2026-02-14
categories:
  - 公司估值
---

## 要解决的问题

如果你使用多个券商交易软件，并且持有的股票横跨多个交易所，用 Excel 管理投资组合是个简单且不失强大的工具。Excel有内置的股票数据源，可以自动更新包括股价在内的实时数据。但是，非常遗憾的是，对于A股来说，它一直以来只支持深交所的股票，没有上交所的股票数据。境外交易所来看，美股、港股都是支持的，但是日股也不支持。

如果你使用Excel管理持仓组合，每次更新持仓组合净值和收益，你不得不打开表格和行情软件，手动抄写那些无法自动更新的股票价格。持仓多的话，光抄价格就要好几分钟，而且容易抄错。

一个解决方案是使用金融终端或数据库提供的excel add-on插件，但这往往是收费服务的一部分。这里有一个免费的解决方案，还是使用excel：**用 VBA 宏调用 Yahoo Finance 的 API**。Yahoo Finance 覆盖全球几乎所有交易所，包括上证、深证和东京，而且完全免费。

## 最终效果

**一键更新，30 秒搞定。** 在 Excel 中运行一个宏，所有上证 A 股、B 股、日股的最新价格从 Yahoo Finance 自动写入表格，市值和盈亏自动计算。

更新流程：运行宏 → Yahoo Finance API → 股价写入「股价数据源」 → 持仓表市价自动更新 → 市值 & 盈亏自动计算

## 实现思路

整体架构很简单：

1. 新建一个「股价数据源」Sheet，A 列放 Yahoo Finance 股票代码，D 列放价格
2. 在持仓表中，用公式引用「股价数据源」的 D 列来获取当前股价，比如 `=股价数据源!D2`
3. VBA 宏遍历「股价数据源」的 A 列，逐个调用 Yahoo Finance API 获取最新价格，写入 D 列
4. Excel 公式自动完成后续的市值、盈亏计算

### Yahoo Finance 代码规则

| 市场 | 后缀 | 示例 |
|------|------|------|
| 上海证券交易所 | .SS | 600809.SS（山西汾酒） |
| 深圳证券交易所 | .SZ | 002293.SZ（罗莱生活） |
| 东京证券交易所 | .T | 8058.T（三菱商事） |
| 港股 | .HK | 0700.HK（腾讯） |
| 美股 | 无后缀 | GOOG（谷歌） |

这套代码理论上可以覆盖全球所有主要交易所。港股和美股如果你已经用 Excel 内置数据就不需要加进来。

## 设置步骤

### 第一步：准备「股价数据源」Sheet

在你的投资组合 Excel 中新建一个 Sheet，命名为「股价数据源」。A 列填 Yahoo Finance 代码，B 列填名称，D 列留给宏写入价格。

### 第二步：持仓表链接到数据源

在持仓表中，把原来手动填写市价的单元格改为公式引用「股价数据源」的对应行，比如 `=股价数据源!D2`。这样数据源一更新，所有持仓的市价联动更新。

### 第三步：另存为 .xlsm 格式

文件 → 另存为 → 格式选择 **Excel 启用宏的工作簿 (.xlsm)**。只有这个格式才能保存 VBA 宏。

### 第四步：打开 VBA 编辑器

- Mac: 工具 → 宏 → Visual Basic 编辑器（或按 `Option + F11`）
- Windows: 按 `Alt + F11`

### 第五步：插入模块并粘贴代码

在左侧项目面板中右键点击你的工作簿 → 插入 → 模块 → 粘贴下方的完整 VBA 代码。

### 第六步：运行！

保存，回到 Excel → 工具 → 宏 → 选择 `UpdateAllPrices` → 运行。首次运行 Mac 可能提示网络权限，允许即可。

## 完整 VBA 代码

以下是在 Mac 版 Excel 实测通过的完整代码。Windows 同样兼容，脚本内置了多层降级策略。

```vb
Public Sub UpdateAllPrices()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim ticker As String
    Dim price As Variant

    Set ws = ThisWorkbook.Sheets("股价数据源")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Application.ScreenUpdating = False
    Application.StatusBar = "正在更新股价..."

    Dim successCount As Long
    Dim failCount As Long
    successCount = 0
    failCount = 0

    For i = 2 To lastRow
        ticker = Trim(CStr(ws.Cells(i, 1).Value))
        If ticker = "" Or ticker = "代码" Then GoTo NextTicker

        Application.StatusBar = "正在更新: " & ws.Cells(i, 2).Value & _
            " (" & i - 1 & "/" & lastRow - 1 & ")"

        price = GetYahooPrice(ticker)

        If IsNumeric(price) Then
            ws.Cells(i, 4).Value = CDbl(price)
            ws.Cells(i, 5).Value = Now()
            successCount = successCount + 1
        Else
            ws.Cells(i, 4).Value = "ERROR"
            ws.Cells(i, 5).Value = CStr(price)
            failCount = failCount + 1
        End If

        Application.Wait Now + TimeValue("00:00:01")
NextTicker:
    Next i

    Application.StatusBar = False
    Application.ScreenUpdating = True

    MsgBox "股价更新完成！" & vbCrLf & _
        "成功: " & successCount & " 只" & vbCrLf & _
        "失败: " & failCount & " 只" & vbCrLf & _
        "更新时间: " & Format(Now(), "yyyy-mm-dd hh:mm:ss"), _
        vbInformation, "股价更新"
End Sub

Function GetYahooPrice(ticker As String) As Variant
    Dim url As String
    Dim response As String

    url = "https://query1.finance.yahoo.com/v8/finance/chart/" & _
        UrlEncode(ticker) & _
        "?range=1d&interval=1d"

    #If Mac Then
        On Error GoTo FinalError
        ' Mac: only use curl
        Dim scriptStr As String
        scriptStr = "do shell script ""curl -s -L " & _
            "-H 'User-Agent: Mozilla/5.0' " & _
            "'" & url & "'"""
        response = MacScript(scriptStr)
        GetYahooPrice = ParsePrice(response)
        Exit Function
    #Else
        On Error GoTo TryAlt
        ' Windows: XMLHTTP
        Dim http As Object
        Set http = CreateObject("MSXML2.XMLHTTP")
        http.Open "GET", url, False
        http.setRequestHeader "User-Agent", "Mozilla/5.0"
        http.Send

        If http.Status = 200 Then
            response = http.responseText
            GetYahooPrice = ParsePrice(response)
        Else
            GetYahooPrice = "HTTP " & http.Status
        End If
        Set http = Nothing
        Exit Function

    TryAlt:
        On Error GoTo FinalError
        ' Windows fallback: Microsoft.XMLHTTP
        Dim xmlhttp As Object
        Set xmlhttp = CreateObject("Microsoft.XMLHTTP")
        xmlhttp.Open "GET", url, False
        xmlhttp.setRequestHeader "User-Agent", "Mozilla/5.0"
        xmlhttp.Send

        If xmlhttp.Status = 200 Then
            response = xmlhttp.responseText
            GetYahooPrice = ParsePrice(response)
        Else
            GetYahooPrice = "HTTP " & xmlhttp.Status
        End If
        Set xmlhttp = Nothing
        Exit Function
    #End If

FinalError:
    GetYahooPrice = "Error: " & Err.Description
End Function

Function ParsePrice(jsonText As String) As Variant
    Dim searchKey As String
    Dim pos As Long
    Dim endPos As Long
    Dim priceStr As String

    searchKey = """regularMarketPrice"":"
    pos = InStr(1, jsonText, searchKey)

    If pos = 0 Then
        ParsePrice = "无法解析"
        Exit Function
    End If

    pos = pos + Len(searchKey)
    endPos = InStr(pos, jsonText, ",")
    If endPos = 0 Then endPos = InStr(pos, jsonText, "}")

    priceStr = Trim(Mid(jsonText, pos, endPos - pos))

    If IsNumeric(priceStr) Then
        ParsePrice = CDbl(priceStr)
    Else
        ParsePrice = "解析失败"
    End If
End Function

Function UrlEncode(ByVal s As String) As String
    Dim i As Long, ch As String, code As Integer
    Dim out As String

    For i = 1 To Len(s)
        ch = Mid$(s, i, 1)
        code = AscW(ch)
        Select Case code
            Case 48 To 57, 65 To 90, 97 To 122, 45, 46, 95, 126
                out = out & ch
            Case 32
                out = out & "%20"
            Case Else
                out = out & "%" & Right$("0" & Hex(code), 2)
        End Select
    Next i

    UrlEncode = out
End Function
```

脚本包含 4 个函数：`UpdateAllPrices`（主入口，遍历股票列表）、`GetYahooPrice`（调用 Yahoo Finance API，Mac 用 curl，Windows 用 XMLHTTP）、`ParsePrice`（从 JSON 中提取价格）、`UrlEncode`（URL 编码处理）。每次请求间隔 1 秒，避免触发频率限制。

## 日常使用

设置好之后，日常操作非常简单：

**每次更新只需一步：** 工具 → 宏 → `UpdateAllPrices` → 运行。等待约 30 秒（取决于股票数量），弹窗提示更新完成后，所有数据已是最新。

### 添加新股票

1. 在「股价数据源」Sheet 末尾新增一行，A 列填 Yahoo Finance 代码，B 列填名称
2. 在持仓表的市价单元格写公式引用 `=股价数据源!D{行号}`
3. 下次运行宏时自动覆盖

## 常见问题

**Q: Mac 上运行报错怎么办？**

确认文件已保存为 .xlsm 格式。在 Mac Excel 中：偏好设置 → 安全性 → 勾选「启用所有宏」。首次运行时允许网络访问权限。

**Q: 某只股票显示 ERROR？**

检查 A 列的 Yahoo Finance 代码是否正确。可以在 [finance.yahoo.com](https://finance.yahoo.com) 搜索股票名称来确认正确代码。

**Q: 可以自动定时运行吗？**

Excel VBA 本身不支持后台定时。但可以用 `Application.OnTime` 在 Excel 打开期间定时执行，或者用操作系统的定时任务来打开 Excel 并触发宏。对于投资组合跟踪来说，手动运行一次已经足够方便。

**Q: Yahoo Finance API 会收费吗？**

这里用的是 Yahoo Finance 的公开 chart API，免费且无需注册。价格有约 15 分钟延迟，对于投资组合日常跟踪完全够用。
