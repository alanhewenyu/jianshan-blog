---
title: "ValueScope — AI 智能估值工具"
layout: "page"
url: "/tools/valuescope/"
slug: "valuescope"
summary: "免费 AI 股票估值与分析平台：DCF 内在估值、相对估值分位、四维评分雷达，覆盖 A 股、港股、美股。"
---

<style>
.vs-hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.vs-hero h2 { font-size: 2rem; margin-bottom: 0.6rem; font-weight: 800; }
.vs-hero .tagline { font-size: 1.15rem; color: var(--card-text-color-secondary); margin-bottom: 0.6rem; }
.vs-hero .sub { font-size: 0.95rem; color: var(--card-text-color-secondary); opacity: 0.8; margin-bottom: 1.5rem; }
.vs-cta { display: inline-block; background: #2563eb; color: #fff !important; padding: 0.75rem 2rem; border-radius: 8px; font-size: 1.1rem; font-weight: 600; text-decoration: none !important; transition: background 0.2s; }
.vs-cta:hover { background: #1d4ed8; }
.vs-cta-secondary { display: inline-block; color: #2563eb !important; padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 1rem; font-weight: 500; text-decoration: none !important; border: 1.5px solid #2563eb; margin-left: 0.8rem; transition: background 0.2s; }
.vs-cta-secondary:hover { background: rgba(37,99,235,0.06); }
.vs-pillars { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; margin: 2rem 0; }
.vs-pillar { padding: 1.4rem; border-radius: 12px; background: var(--card-background); box-shadow: var(--shadow-l1); }
.vs-pillar .pillar-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; }
.vs-pillar .pillar-icon { font-size: 1.6rem; }
.vs-pillar h4 { margin: 0; font-size: 1.05rem; }
.vs-pillar .pillar-tag { font-size: 0.7rem; background: #dbeafe; color: #1e40af; padding: 0.15rem 0.5rem; border-radius: 10px; font-weight: 600; }
.vs-pillar p { font-size: 0.9rem; color: var(--card-text-color-secondary); margin: 0 0 0.5rem; line-height: 1.6; }
.vs-pillar ul { margin: 0; padding-left: 1.2rem; font-size: 0.85rem; color: var(--card-text-color-secondary); line-height: 1.8; }
.vs-badges { display: flex; gap: 1.2rem; justify-content: center; flex-wrap: wrap; margin: 1.5rem 0; }
.vs-badge { font-size: 0.92rem; color: var(--card-text-color-secondary); }
.vs-how { display: flex; gap: 1rem; margin: 2rem 0; flex-wrap: wrap; justify-content: center; }
.vs-step { flex: 1; min-width: 180px; max-width: 240px; text-align: center; padding: 1.2rem 1rem; border-radius: 12px; background: var(--card-background); box-shadow: var(--shadow-l1); position: relative; }
.vs-step .step-num { display: inline-block; width: 28px; height: 28px; line-height: 28px; border-radius: 50%; background: #2563eb; color: #fff; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem; }
.vs-step h4 { margin: 0.3rem 0; font-size: 0.95rem; }
.vs-step p { font-size: 0.82rem; color: var(--card-text-color-secondary); margin: 0; }
.vs-stocks { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin: 1.5rem 0; }
.vs-stocks a { display: inline-block; padding: 0.4rem 1rem; border-radius: 20px; background: var(--card-background); box-shadow: var(--shadow-l1); text-decoration: none !important; font-size: 0.9rem; color: var(--card-text-color-main) !important; transition: box-shadow 0.2s; }
.vs-stocks a:hover { box-shadow: var(--shadow-l2); }
.vs-screenshot { text-align: center; margin: 2rem 0; }
.vs-screenshot img { max-width: 100%; border-radius: 12px; box-shadow: var(--shadow-l2); }
.vs-bottom-cta { text-align: center; padding: 2rem 0; }
.vs-compare { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.88rem; }
.vs-compare th { text-align: left; padding: 0.6rem 0.8rem; border-bottom: 2px solid var(--card-text-color-secondary); font-weight: 600; }
.vs-compare td { padding: 0.5rem 0.8rem; border-bottom: 1px solid rgba(128,128,128,0.15); }
.vs-compare tr td:first-child { font-weight: 500; }
</style>

<div class="vs-hero">
<h2>一个工具，看透一只股票</h2>
<p class="tagline">DCF 内在估值 · 相对估值分位 · 四维评分雷达 · AI 深度分析</p>
<p class="sub">覆盖 A 股 / 港股 / 美股 / 日股，免费使用，无需注册</p>
<a href="https://valuescope.app/" class="vs-cta" target="_blank">开始分析 →</a>
<a href="https://github.com/alanhewenyu/ValueScope" class="vs-cta-secondary" target="_blank">GitHub</a>
</div>

---

### 四大分析维度

<div class="vs-pillars">
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📊</span>
<h4>DCF 内在估值</h4>
<span class="pillar-tag">AI 加持</span>
</div>
<p>基于 Damodaran FCFF 框架的 10 年现金流折现模型，框架标准化、结果可复现。</p>
<ul>
<li>AI 一键生成全部估值参数（DeepSeek R1 + 网络搜索）</li>
<li>增长率 × EBIT 利润率双维度敏感性矩阵</li>
<li>Gap 分析：AI 对比估值与市价差异并归因</li>
<li>完整预测表 + 估值桥 + BUY / HOLD / SELL 判定</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📈</span>
<h4>相对估值</h4>
</div>
<p>当前价格贵不贵？放到自身历史里一看便知。</p>
<ul>
<li>PE / PB / PS / EV/EBITDA 当前倍数</li>
<li>3 / 5 / 10 年历史分位可视化</li>
<li>分位条一目了然：当前值、均值、极值</li>
<li>PE、PB 历史走势图</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">🎯</span>
<h4>四维评分</h4>
</div>
<p>估值、质量、成长、动量——四个维度浓缩为一张雷达图。</p>
<ul>
<li>估值维度：PE/PB 分位 + 均值回归信号</li>
<li>质量维度：ROIC、ROE、资产效率</li>
<li>成长维度：营收增速、盈利增速趋势</li>
<li>动量维度：价格趋势与技术指标</li>
<li>子因子透明可查，权重可调</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">🔎</span>
<h4>财务总览</h4>
</div>
<p>进入个股页第一眼就能快速建立全局印象。</p>
<ul>
<li>5 年 PE / PB 分位卡片</li>
<li>营收增长、EBIT 利润率、ROIC & ROE、自由现金流四宫格</li>
<li>资产负债表关键指标：现金、债务、杠杆率</li>
<li>历史财务数据完整表格</li>
</ul>
</div>
</div>

---

### 三步开始

<div class="vs-how">
<div class="vs-step">
<div class="step-num">1</div>
<h4>输入股票代码</h4>
<p>A 股（600519）、港股（0700.HK）、美股（AAPL）、日股（7203.T）</p>
</div>
<div class="vs-step">
<div class="step-num">2</div>
<h4>浏览四个分析维度</h4>
<p>总览、DCF 估值、相对估值、四维评分一键切换</p>
</div>
<div class="vs-step">
<div class="step-num">3</div>
<h4>AI 深度分析（可选）</h4>
<p>一键让 AI 搜索基本面数据，生成估值参数并完成 DCF</p>
</div>
</div>

<div class="vs-badges">
<span class="vs-badge">✅ 覆盖全球主要市场</span>
<span class="vs-badge">✅ DeepSeek R1 深度推理</span>
<span class="vs-badge">✅ 完全免费</span>
<span class="vs-badge">✅ 无需注册</span>
<span class="vs-badge">✅ 开源透明</span>
</div>

---

### 热门股票快捷入口

<div class="vs-stocks">
<a href="https://valuescope.app/stock/600519.SS">🥃 茅台</a>
<a href="https://valuescope.app/stock/0700.HK">💬 腾讯</a>
<a href="https://valuescope.app/stock/AAPL">🍎 苹果</a>
<a href="https://valuescope.app/stock/NVDA">🖥️ 英伟达</a>
<a href="https://valuescope.app/stock/PDD">🛒 拼多多</a>
<a href="https://valuescope.app/stock/3690.HK">🍜 美团</a>
<a href="https://valuescope.app/stock/9988.HK">🛍️ 阿里巴巴</a>
<a href="https://valuescope.app/stock/MSFT">💻 微软</a>
</div>

---

### 产品截图

<div class="vs-screenshot">

![ValueScope 网页版界面](screenshot.png)

</div>

---

### 和同类工具对比

<table class="vs-compare">
<tr><th>功能</th><th>ValueScope</th><th>同花顺/雪球</th><th>GuruFocus</th></tr>
<tr><td>DCF 估值</td><td>✅ 完整 FCFF 模型</td><td>❌</td><td>✅ 简化版</td></tr>
<tr><td>AI 参数估算</td><td>✅ DeepSeek + 网络搜索</td><td>❌</td><td>❌</td></tr>
<tr><td>敏感性分析</td><td>✅ 双维度矩阵</td><td>❌</td><td>❌</td></tr>
<tr><td>相对估值分位</td><td>✅ 3/5/10 年</td><td>部分</td><td>✅</td></tr>
<tr><td>多维评分雷达</td><td>✅ 四维透明评分</td><td>❌</td><td>部分</td></tr>
<tr><td>A 股 / 港股</td><td>✅</td><td>✅</td><td>部分</td></tr>
<tr><td>免费使用</td><td>✅ 完全免费</td><td>部分</td><td>💰 $450/年</td></tr>
<tr><td>开源</td><td>✅</td><td>❌</td><td>❌</td></tr>
</table>

---

### 关于 ValueScope

ValueScope 是一个开源的 AI 驱动股票分析平台。底层是标准化的 Damodaran FCFF 估值框架（10 年现金流折现 + WACC + 终值），结合相对估值历史分位和四维评分体系，帮助你从多个角度理解一只股票的价值。AI 层负责搜索和分析，但最终判断始终在你手上。

项目完全开源：[GitHub](https://github.com/alanhewenyu/ValueScope)

<div class="vs-bottom-cta">
<a href="https://valuescope.app/" class="vs-cta" target="_blank">立即免费试用 →</a>
</div>
