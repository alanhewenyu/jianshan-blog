---
title: "Stop Manually Copying Stock Prices into Your Excel Portfolio"
date: 2026-02-14
draft: false
slug: "如果用excel管理股票持仓别再手动抄写股价了"
categories: ["Company Valuation"]
tags: ["Excel", "VBA", "Yahoo Finance", "Portfolio Management"]
summary: "Provides a free Excel VBA macro solution that calls the Yahoo Finance API to automatically update global stock prices, eliminating tedious manual data entry for portfolio management."
---

## The Problem

If you use multiple brokerage accounts with stocks across different exchanges, Excel is a simple yet powerful tool for managing your investment portfolio. Excel has built-in stock data types that can automatically update prices and other real-time data. Unfortunately, for China's A-shares, it has only ever supported Shenzhen-listed stocks — Shanghai Stock Exchange data is missing. For international markets, U.S. and Hong Kong stocks are supported, but Japanese stocks are not.

If you manage your portfolio in Excel, every time you update net asset value and returns, you have to open both your spreadsheet and a trading app, manually copying prices for stocks that can't auto-update. With a larger portfolio, just copying prices takes several minutes — and mistakes are easy to make.

One solution is using Excel add-ins from financial terminals or databases, but these typically come as part of paid services. Here's a free alternative that stays within Excel: **use VBA macros to call the Yahoo Finance API**. Yahoo Finance covers virtually every exchange worldwide, including Shanghai, Shenzhen, and Tokyo — completely free.

## End Result

**One click, 30 seconds.** Run a macro in Excel, and all Shanghai A-shares, B-shares, and Japanese stock prices are automatically fetched from Yahoo Finance and written into your spreadsheet. Market values and P&L calculate automatically.

Update flow: Run macro → Yahoo Finance API → Prices written to "Price Data Source" sheet → Portfolio prices auto-update → Market value & P&L auto-calculate

## Implementation

The architecture is straightforward:

1. Create a "Price Data Source" sheet — Column A for Yahoo Finance ticker symbols, Column D for prices
2. In your portfolio sheet, use formulas referencing Column D of the data source, e.g., `=PriceDataSource!D2`
3. The VBA macro iterates through Column A, calls Yahoo Finance API for each ticker, and writes prices to Column D
4. Excel formulas handle all downstream market value and P&L calculations

### Yahoo Finance Ticker Conventions

| Market | Suffix | Example |
|--------|--------|---------|
| Shanghai Stock Exchange | .SS | 600809.SS (Shanxi Fenjiu) |
| Shenzhen Stock Exchange | .SZ | 002293.SZ (Luolai Lifestyle) |
| Tokyo Stock Exchange | .T | 8058.T (Mitsubishi Corp) |
| Hong Kong | .HK | 0700.HK (Tencent) |
| U.S. | None | GOOG (Google) |

This code theoretically covers all major global exchanges. If you already use Excel's built-in data for U.S. and HK stocks, you don't need to include them.

## Setup Steps

### Step 1: Prepare the "Price Data Source" Sheet

Create a new sheet in your portfolio Excel file named "Price Data Source." Fill Column A with Yahoo Finance tickers, Column B with names, and leave Column D for the macro to write prices.

### Step 2: Link Your Portfolio to the Data Source

In your portfolio sheet, replace manually entered prices with formula references to the corresponding rows in the data source, e.g., `=PriceDataSource!D2`. Once the data source updates, all portfolio prices update automatically.

### Step 3: Save as .xlsm Format

File → Save As → Choose **Excel Macro-Enabled Workbook (.xlsm)**. Only this format can save VBA macros.

### Step 4: Open the VBA Editor

- Mac: Tools → Macro → Visual Basic Editor (or press `Option + F11`)
- Windows: Press `Alt + F11`

### Step 5: Insert Module and Paste Code

In the left project panel, right-click your workbook → Insert → Module → Paste the complete VBA code below.

### Step 6: Run!

Save, return to Excel → Tools → Macro → Select `UpdateAllPrices` → Run. On first run, Mac may prompt for network permissions — allow it.

## Complete VBA Code

The following code has been tested on Mac Excel. Windows is also compatible, with built-in multi-layer fallback strategies.

```vb
Public Sub UpdateAllPrices()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim ticker As String
    Dim price As Variant

    Set ws = ThisWorkbook.Sheets("Price Data Source")
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Application.ScreenUpdating = False
    Application.StatusBar = "Updating prices..."

    Dim successCount As Long
    Dim failCount As Long
    successCount = 0
    failCount = 0

    For i = 2 To lastRow
        ticker = Trim(CStr(ws.Cells(i, 1).Value))
        If ticker = "" Then GoTo NextTicker

        Application.StatusBar = "Updating: " & ws.Cells(i, 2).Value & _
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

    MsgBox "Price update complete!" & vbCrLf & _
        "Success: " & successCount & vbCrLf & _
        "Failed: " & failCount & vbCrLf & _
        "Updated: " & Format(Now(), "yyyy-mm-dd hh:mm:ss"), _
        vbInformation, "Price Update"
End Sub

Function GetYahooPrice(ticker As String) As Variant
    Dim url As String
    Dim response As String

    url = "https://query1.finance.yahoo.com/v8/finance/chart/" & _
        UrlEncode(ticker) & _
        "?range=1d&interval=1d"

    #If Mac Then
        On Error GoTo FinalError
        Dim scriptStr As String
        scriptStr = "do shell script ""curl -s -L " & _
            "-H 'User-Agent: Mozilla/5.0' " & _
            "'" & url & "'"""
        response = MacScript(scriptStr)
        GetYahooPrice = ParsePrice(response)
        Exit Function
    #Else
        On Error GoTo TryAlt
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
        ParsePrice = "Parse failed"
        Exit Function
    End If

    pos = pos + Len(searchKey)
    endPos = InStr(pos, jsonText, ",")
    If endPos = 0 Then endPos = InStr(pos, jsonText, "}")

    priceStr = Trim(Mid(jsonText, pos, endPos - pos))

    If IsNumeric(priceStr) Then
        ParsePrice = CDbl(priceStr)
    Else
        ParsePrice = "Parse failed"
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

The script contains 4 functions: `UpdateAllPrices` (main entry point, iterates through the stock list), `GetYahooPrice` (calls Yahoo Finance API — curl on Mac, XMLHTTP on Windows), `ParsePrice` (extracts price from JSON), and `UrlEncode` (URL encoding). Each request is spaced 1 second apart to avoid rate limiting.

## Daily Usage

Once set up, daily operation is simple:

**One step per update:** Tools → Macro → `UpdateAllPrices` → Run. Wait about 30 seconds (depending on stock count), and a dialog confirms completion with all data refreshed.

### Adding New Stocks

1. Add a new row at the bottom of the "Price Data Source" sheet — Column A for Yahoo Finance ticker, Column B for name
2. In the portfolio sheet, add a formula referencing `=PriceDataSource!D{row}`
3. The next macro run will automatically include it

## FAQ

**Q: Getting errors on Mac?**

Ensure the file is saved as .xlsm format. In Mac Excel: Preferences → Security → Check "Enable all macros." Allow network access on first run.

**Q: A stock shows ERROR?**

Verify the Yahoo Finance ticker in Column A is correct. Search the stock name on [finance.yahoo.com](https://finance.yahoo.com) to confirm the correct ticker.

**Q: Can it run on a schedule?**

Excel VBA doesn't support background scheduling natively. You can use `Application.OnTime` for in-session scheduling, or use OS-level scheduled tasks to open Excel and trigger the macro. For portfolio tracking, a manual run is usually convenient enough.

**Q: Will Yahoo Finance API start charging?**

This uses Yahoo Finance's public chart API — free with no registration required. Prices have approximately 15-minute delay, which is perfectly adequate for daily portfolio tracking.
