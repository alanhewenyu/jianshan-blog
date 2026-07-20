---
title: "ValueScope — The DCF Valuation Engine Your AI Can Call"
layout: "page"
url: "/en/tools/valuescope/"
slug: "valuescope"
summary: "A standardized DCF valuation engine: connect it to Claude / ChatGPT / any AI via MCP and run valuations in chat, or use the web console for manual analysis. A-shares & HK completely free."
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
<h2>The DCF Valuation Engine Your AI Can Call</h2>
<p class="tagline">Standardized DCF · MCP server for Claude / ChatGPT / any AI · Web console for manual analysis</p>
<p class="sub">Covers US, HK, A-shares & Japan — A-shares & HK completely free, no signup required</p>
<a href="https://valuescope.app/mcp" class="vs-cta" target="_blank">🔌 Connect via MCP in 2 Minutes →</a>
<a href="https://valuescope.app/" class="vs-cta-secondary" target="_blank">Open Web Console →</a>
</div>

---

### Use It Inside Your AI

<div class="vs-mcp">
<h4>🔌 The MCP Valuation Engine</h4>
<p>AI is great at reasoning but bad at staying consistent — run a DCF today and again next month, and the data sources and methodology may differ completely. ValueScope MCP splits the work: <strong>your AI handles the forward-looking judgment</strong> (searching guidance, reasoning about assumptions) while <strong>the engine owns the data and the math</strong> (standardized financials, the DCF model, sensitivity analysis, reverse DCF). Same inputs, same result, every time.</p>
<pre>claude mcp add valuescope --transport http https://mcp.valuescope.app/mcp</pre>
<p>Once connected, just ask your AI: <em>"Value Tencent with a DCF."</em> Setup for Claude web, Cherry Studio, ChatGPT and other clients: <a href="https://valuescope.app/mcp" target="_blank">full setup guide →</a></p>
</div>

---

### Web Console: Four Analysis Dimensions

<div class="vs-pillars">
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📊</span>
<h4>DCF Intrinsic Valuation</h4>
</div>
<p>A standardized 10-year FCFF model based on the Damodaran framework — fixed methodology, reproducible results.</p>
<ul>
<li>Parameter sliders with instant recalculation, defaults from 5-year historical averages</li>
<li>Growth Rate × EBIT Margin dual-dimension sensitivity matrix</li>
<li>Full forecast table + valuation bridge + reverse DCF</li>
<li>Buffett Quick Valuation: automated Owner Earnings estimate</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📈</span>
<h4>Relative Valuation</h4>
</div>
<p>Is the current price expensive? Compare it against the stock's own history to find out.</p>
<ul>
<li>Current PE / PB / PS / EV/EBITDA multiples</li>
<li>3 / 5 / 10-year historical percentile visualization</li>
<li>Percentile bars: current value, mean, min/max at a glance</li>
<li>Historical PE & PB trend charts</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">🎯</span>
<h4>4-Dimension Scoring</h4>
</div>
<p>Valuation, Quality, Growth, and Momentum — four dimensions condensed into one radar chart.</p>
<ul>
<li>Valuation: PE/PB percentile + mean-reversion signals</li>
<li>Quality: ROIC, ROE, asset efficiency</li>
<li>Growth: Revenue growth, earnings growth trajectory</li>
<li>Momentum: Price trends & technical indicators</li>
<li>Transparent sub-factors with adjustable weights</li>
</ul>
</div>
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">🔎</span>
<h4>Financial Overview</h4>
</div>
<p>The first screen you see — build a complete picture in seconds.</p>
<ul>
<li>5-year PE / PB percentile cards</li>
<li>Revenue & growth, EBIT margin, ROIC & ROE, FCF — four-chart grid</li>
<li>Balance sheet highlights: cash, debt, leverage ratio</li>
<li>Full historical financials table</li>
</ul>
</div>
</div>

---

### Three Steps to Start

<div class="vs-how">
<div class="vs-step">
<div class="step-num">1</div>
<h4>Enter a Ticker</h4>
<p>US (AAPL), HK (0700.HK), A-shares (600519), Japan (7203.T)</p>
</div>
<div class="vs-step">
<div class="step-num">2</div>
<h4>Browse Four Dimensions</h4>
<p>Overview, DCF, Relative Valuation, Scoring — switch with one click</p>
</div>
<div class="vs-step">
<div class="step-num">3</div>
<h4>Connect Your AI (Optional)</h4>
<p>Two-minute MCP setup — let your AI research guidance, reason about assumptions, and run the valuation in chat</p>
</div>
</div>

<div class="vs-badges">
<span class="vs-badge">✅ Global market coverage</span>
<span class="vs-badge">✅ MCP for any AI client</span>
<span class="vs-badge">✅ A-shares & HK completely free</span>
<span class="vs-badge">✅ No signup required</span>
<span class="vs-badge">✅ Open source</span>
</div>

---

### Popular Stocks

<div class="vs-stocks">
<a href="https://valuescope.app/stock/AAPL">🍎 Apple</a>
<a href="https://valuescope.app/stock/NVDA">🖥️ NVIDIA</a>
<a href="https://valuescope.app/stock/MSFT">💻 Microsoft</a>
<a href="https://valuescope.app/stock/GOOGL">🔍 Google</a>
<a href="https://valuescope.app/stock/0700.HK">💬 Tencent</a>
<a href="https://valuescope.app/stock/600519.SS">🥃 Moutai</a>
<a href="https://valuescope.app/stock/PDD">🛒 PDD</a>
<a href="https://valuescope.app/stock/7203.T">🚗 Toyota</a>
</div>

---

### Screenshot

<div class="vs-screenshot">

![ValueScope Web Interface](screenshot.png)

</div>

---

### About ValueScope

ValueScope is a standardized DCF valuation engine built on the Damodaran FCFF framework (10-year discounted cash flow + WACC + terminal value), combined with relative-valuation historical percentiles and a 4-dimension scoring system. Use it two ways: <strong>connect it to your own AI via MCP</strong> — the AI researches and reasons, the engine owns the data and the math — or <strong>work the parameters by hand in the web console</strong> to test ideas and explore sensitivities. Both run the same engine. The AI brings the intelligence, ValueScope brings the framework and discipline — and the final judgment is always yours.

<div class="vs-bottom-cta">
<a href="https://valuescope.app/mcp" class="vs-cta" target="_blank">🔌 Connect via MCP →</a>
<a href="https://valuescope.app/" class="vs-cta-secondary" target="_blank">Open Web Console →</a>
</div>
