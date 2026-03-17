---
title: "ValueScope — AI-Powered Stock Valuation"
layout: "page"
url: "/en/tools/valuescope/"
slug: "valuescope"
summary: "Free AI stock analysis platform: DCF intrinsic valuation, relative valuation percentiles, 4-dimension scoring radar. Covers US, HK, A-shares & global stocks."
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
</style>

<div class="vs-hero">
<h2>One Tool to Understand Any Stock</h2>
<p class="tagline">DCF Intrinsic Valuation · Relative Valuation Percentiles · 4-Dimension Scoring · AI Analysis</p>
<p class="sub">Covers US, HK, A-shares, Japan & global markets — free, no signup required</p>
<a href="https://valuescope.app/" class="vs-cta" target="_blank">Start Analyzing →</a>
<a href="https://github.com/alanhewenyu/ValueScope" class="vs-cta-secondary" target="_blank">GitHub</a>
</div>

---

### Four Analysis Dimensions

<div class="vs-pillars">
<div class="vs-pillar">
<div class="pillar-header">
<span class="pillar-icon">📊</span>
<h4>DCF Intrinsic Valuation</h4>
<span class="pillar-tag">AI-POWERED</span>
</div>
<p>A standardized 10-year FCFF model based on the Damodaran framework — fixed methodology, reproducible results.</p>
<ul>
<li>AI generates all DCF parameters in one click (DeepSeek R1 + web search)</li>
<li>Growth Rate × EBIT Margin dual-dimension sensitivity matrix</li>
<li>Gap Analysis: AI explains valuation-vs-market-price discrepancies</li>
<li>Full forecast table + valuation bridge + BUY / HOLD / SELL verdict</li>
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
<h4>AI Deep Analysis (Optional)</h4>
<p>Let AI search fundamentals, generate DCF parameters, and complete the valuation</p>
</div>
</div>

<div class="vs-badges">
<span class="vs-badge">✅ Global market coverage</span>
<span class="vs-badge">✅ DeepSeek R1 deep reasoning</span>
<span class="vs-badge">✅ Completely free</span>
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

ValueScope is an open-source AI-powered stock analysis platform. The foundation is the Damodaran FCFF valuation framework (10-year discounted cash flow + WACC + terminal value), combined with relative valuation historical percentiles and a 4-dimension scoring system to help you understand a stock's value from multiple angles. The AI layer handles research and analysis, but the final judgment is always yours.

Fully open source: [GitHub](https://github.com/alanhewenyu/ValueScope)

<div class="vs-bottom-cta">
<a href="https://valuescope.app/" class="vs-cta" target="_blank">Try It Free →</a>
</div>
