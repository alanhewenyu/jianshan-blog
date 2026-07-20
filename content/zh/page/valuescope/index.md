---
title: "ValueScope — 你的 AI 也能调用的 DCF 估值引擎"
layout: "page"
url: "/tools/valuescope/"
slug: "valuescope"
summary: "标准化 DCF 估值引擎：通过 MCP 接入 Claude / ChatGPT 等任意 AI，对话中完成 DCF 估值；网页控制台支持手动调参与敏感性分析。A股港股完全免费。"
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
.vs-mcp { padding: 1.6rem; border-radius: 12px; background: linear-gradient(90deg, rgba(139,92,246,0.08), rgba(37,99,235,0.08)); border: 1px solid rgba(139,92,246,0.25); margin: 2rem 0; }
.vs-mcp h4 { margin: 0 0 0.6rem; font-size: 1.1rem; }
.vs-mcp p { font-size: 0.92rem; color: var(--card-text-color-secondary); line-height: 1.7; margin: 0 0 0.6rem; }
.vs-mcp pre { font-size: 0.82rem; background: var(--card-background); border-radius: 8px; padding: 0.7rem 1rem; overflow-x: auto; margin: 0.6rem 0; }
.vs-pillars { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; margin: 2rem 0; }
.vs-pillar { padding: 1.4rem; border-radius: 12px; background: var(--card-background); box-shadow: var(--shadow-l1); }
.vs-pillar .pillar-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; }
.vs-pillar .pillar-icon { font-size: 1.6rem; }
.vs-pillar h4 { margin: 0; font-size: 1.05rem; }
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
</style>

<div class="vs-hero">
<h2>你的 AI 也能调用的 DCF 估值引擎</h2>
<p class="tagline">标准化 DCF · MCP 接入 Claude / ChatGPT / 任意 AI · 网页控制台手动分析</p>
<p class="sub">覆盖 A 股 / 港股 / 美股 / 日股，A股港股完全免费，无需注册</p>
<a href="https://valuescope.app/mcp" class="vs-cta" target="_blank">🔌 两分钟接入 MCP →</a>
<a href="https://valuescope.app/" class="vs-cta-secondary" target="_blank">打开网页版 →</a>
</div>

---

### 在你的 AI 里直接用

<div class="vs-mcp">
<h4>🔌 MCP 估值引擎</h4>
<p>AI 很擅长推理，但不擅长保持一致——今天算一次、下个月再算一次，数据来源和口径可能完全不同。ValueScope MCP 的分工：<strong>AI 负责前瞻判断</strong>（搜索业绩指引、推理假设参数），<strong>引擎负责数据和计算</strong>（标准化财务数据、DCF 模型、敏感性分析、反向 DCF）。同样的输入，永远得到同样的结果。</p>
<pre>claude mcp add valuescope --transport http https://mcp.valuescope.app/mcp</pre>
<p>接入后直接对你的 AI 说：<em>"给贵州茅台做个 DCF 估值"</em>。Claude 网页版 / Cherry Studio / ChatGPT 等客户端的配置方法见 <a href="https://valuescope.app/mcp" target="_blank">完整接入指南 →</a></p>
</div>

---

### 网页版：四大分析维度

<div class="vs-pillars">
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📊</span>
<h4>DCF 内在估值</h4>
</div>
<p>基于 Damodaran FCFF 框架的 10 年现金流折现模型，框架标准化、结果可复现。</p>
<ul>
<li>参数滑块实时重算，默认值来自 5 年历史均值</li>
<li>增长率 × EBIT 利润率双维度敏感性矩阵</li>
<li>完整预测表 + 估值桥 + 反向 DCF</li>
<li>Buffett Quick Valuation：股东盈余法自动估值</li>
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
<h4>把引擎接进你的 AI（可选）</h4>
<p>MCP 两分钟接入，在对话里让 AI 搜索指引、推理假设、完成估值</p>
</div>
</div>

<div class="vs-badges">
<span class="vs-badge">✅ 覆盖全球主要市场</span>
<span class="vs-badge">✅ MCP 接入任意 AI</span>
<span class="vs-badge">✅ A股港股完全免费</span>
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

### 关于 ValueScope

ValueScope 是一个标准化 DCF 估值引擎，底层是 Damodaran FCFF 框架（10 年现金流折现 + WACC + 终值），结合相对估值历史分位和四维评分体系。它有两种用法：**通过 MCP 接进你自己的 AI**，让 AI 负责搜索和推理、引擎负责数据和计算；或者**在网页版手动调参数、看敏感性、快速验证想法**。两种入口跑的是同一套引擎——AI 提供智能，ValueScope 提供框架和纪律，最终判断始终在你手上。

<div class="vs-bottom-cta">
<a href="https://valuescope.app/mcp" class="vs-cta" target="_blank">🔌 接入 MCP →</a>
<a href="https://valuescope.app/" class="vs-cta-secondary" target="_blank">打开网页版 →</a>
</div>
