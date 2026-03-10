---
title: "ValueScope — AI 智能估值工具"
layout: "page"
url: "/tools/valuescope/"
slug: "valuescope"
summary: "免费在线 DCF 估值工具，AI 驱动参数分析，覆盖 A 股、港股、美股，一键计算股票内在价值。"
---

<style>
.vs-hero { text-align: center; padding: 2rem 0 1.5rem; }
.vs-hero h2 { font-size: 1.8rem; margin-bottom: 0.5rem; }
.vs-hero p { font-size: 1.1rem; color: var(--card-text-color-secondary); margin-bottom: 1.5rem; }
.vs-cta { display: inline-block; background: #2563eb; color: #fff !important; padding: 0.75rem 2rem; border-radius: 8px; font-size: 1.1rem; font-weight: 600; text-decoration: none !important; transition: background 0.2s; }
.vs-cta:hover { background: #1d4ed8; }
.vs-steps { display: flex; gap: 1.5rem; margin: 2rem 0; flex-wrap: wrap; justify-content: center; }
.vs-step { flex: 1; min-width: 200px; max-width: 280px; text-align: center; padding: 1.2rem; border-radius: 12px; background: var(--card-background); box-shadow: var(--shadow-l1); }
.vs-step .icon { font-size: 2rem; margin-bottom: 0.5rem; }
.vs-step h4 { margin: 0.3rem 0; }
.vs-step p { font-size: 0.9rem; color: var(--card-text-color-secondary); margin: 0; }
.vs-badges { display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap; margin: 1.5rem 0; }
.vs-badge { font-size: 0.95rem; color: var(--card-text-color-secondary); }
.vs-features { display: flex; gap: 1.5rem; margin: 2rem 0; flex-wrap: wrap; justify-content: center; }
.vs-feature { flex: 1; min-width: 250px; max-width: 320px; padding: 1.2rem; border-radius: 12px; background: var(--card-background); box-shadow: var(--shadow-l1); }
.vs-feature h4 { margin: 0 0 0.5rem; }
.vs-feature p { font-size: 0.9rem; color: var(--card-text-color-secondary); margin: 0; }
.vs-stocks { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin: 1.5rem 0; }
.vs-stocks a { display: inline-block; padding: 0.4rem 1rem; border-radius: 20px; background: var(--card-background); box-shadow: var(--shadow-l1); text-decoration: none !important; font-size: 0.9rem; color: var(--card-text-color-main) !important; transition: box-shadow 0.2s; }
.vs-stocks a:hover { box-shadow: var(--shadow-l2); }
.vs-screenshot { text-align: center; margin: 2rem 0; }
.vs-screenshot img { max-width: 100%; border-radius: 12px; box-shadow: var(--shadow-l2); }
.vs-bottom-cta { text-align: center; padding: 2rem 0; }
</style>

<div class="vs-hero">
<h2>用 AI 算出一只股票值多少钱</h2>
<p>覆盖 A 股 / 港股 / 美股，免费在线 DCF 估值，AI 自动搜索分析</p>
<a href="https://valuescope.streamlit.app/" class="vs-cta" target="_blank">开始估值 →</a>
</div>

---

### 三步完成估值

<div class="vs-steps">
<div class="vs-step">
<div class="icon">📝</div>
<h4>输入股票代码</h4>
<p>支持 A 股（600519）、港股（0700.HK）、美股（AAPL）</p>
</div>
<div class="vs-step">
<div class="icon">🤖</div>
<h4>AI 搜索分析</h4>
<p>自动搜索业绩指引、分析师预期，给出参数建议</p>
</div>
<div class="vs-step">
<div class="icon">📊</div>
<h4>得出内在价值</h4>
<p>DCF 估值结果 + 敏感性分析 + 买入/卖出判定</p>
</div>
</div>

<div class="vs-badges">
<span class="vs-badge">✅ 覆盖全球主要市场</span>
<span class="vs-badge">✅ DeepSeek R1 深度推理</span>
<span class="vs-badge">✅ A 股港股免费</span>
<span class="vs-badge">✅ 无需注册</span>
</div>

---

### 功能亮点

<div class="vs-features">
<div class="vs-feature">
<h4>🤖 AI 一键估值</h4>
<p>Cloud AI（DeepSeek R1）自动搜索公司业绩指引、分析师预期和行业数据，一键生成所有 DCF 参数建议并完成估值。</p>
</div>
<div class="vs-feature">
<h4>📊 2D 敏感性矩阵</h4>
<p>增长率 × 利润率双维度敏感性分析，加上 WACC 敏感性，找到你的安全边际。这是竞品都没有的独创功能。</p>
</div>
<div class="vs-feature">
<h4>🔍 Gap 分析</h4>
<p>AI 对比 DCF 估值与当前市价，搜索分析师目标价，分析差异原因——是市场情绪溢价，还是你的假设偏保守？</p>
</div>
<div class="vs-feature">
<h4>📝 自定义估值</h4>
<p>拖动滑块手动设置每个参数，历史数据实时参考，估值结果即时更新。完全免费，不限次数。</p>
</div>
<div class="vs-feature">
<h4>📈 估值判定</h4>
<p>一目了然的 BUY / HOLD / SELL 判定徽章，显示内在价值、当前市价和安全边际百分比。</p>
</div>
<div class="vs-feature">
<h4>📥 Excel 导出</h4>
<p>估值结果、历史财务数据、AI 分析报告，一键导出 Excel 文件，方便存档和回顾。</p>
</div>
</div>

---

### 热门股票快捷入口

<div class="vs-stocks">
<a href="https://valuescope.streamlit.app/?ticker=600519.SS">🥃 茅台</a>
<a href="https://valuescope.streamlit.app/?ticker=0700.HK">💬 腾讯</a>
<a href="https://valuescope.streamlit.app/?ticker=AAPL">🍎 苹果</a>
<a href="https://valuescope.streamlit.app/?ticker=NVDA">🖥️ 英伟达</a>
<a href="https://valuescope.streamlit.app/?ticker=PDD">🛒 拼多多</a>
<a href="https://valuescope.streamlit.app/?ticker=3690.HK">🍜 美团</a>
<a href="https://valuescope.streamlit.app/?ticker=000858.SZ">🍶 五粮液</a>
<a href="https://valuescope.streamlit.app/?ticker=9988.HK">🛍️ 阿里巴巴</a>
</div>

---

### 产品截图

<div class="vs-screenshot">

![ValueScope 网页版界面](screenshot.png)

</div>

---

### 关于 ValueScope

ValueScope 是一个开源的 AI 驱动 DCF 估值工具，底层是标准化的 10 年现金流折现模型（FCFF + WACC + 终值 + 敏感性分析），框架固定、结果可复现。AI 层帮助分析公司基本面并建议估值参数，最终决定权始终在你手上。

项目完全开源：[GitHub](https://github.com/alanhewenyu/ValueScope)

<div class="vs-bottom-cta">
<a href="https://valuescope.streamlit.app/" class="vs-cta" target="_blank">立即免费试用 →</a>
</div>
