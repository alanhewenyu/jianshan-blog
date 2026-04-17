---
title: "What's Your Stock Really Worth? DCF Tool ValueScope Just Got a Major Update"
date: 2026-03-13
categories:
  - Company Valuation
tags:
  - DCF
  - Value Investing
  - Buffett
  - Valuation
  - WACC
  - Hong Kong
  - A-shares
  - AI
summary: "ValueScope DCF valuation tool major update: web app now powered by DeepSeek R1 AI, supporting US, HK, A-share and Japan markets with both AI and custom valuation modes."
slug: "valuescope-dcf-tool-update"
aliases:
  - "/posts/你关注的股票值多少钱dcf估值工具valuescope更新了/"
---

I previously wrote a post called [*What's Your Stock Worth? Why Not Calculate It Yourself*](https://mp.weixin.qq.com/s?__biz=MzkwMTQ0ODE4NQ==&mid=2247484460&idx=1&sn=9ef051bb19a6da708815d3d9f0b06b24&scene=21#wechat_redirect), where I shared a DCF valuation tool called Valux. Since then, many friends have tried installing it and I've received lots of feedback.

I've kept all that feedback in mind. Recently I rebuilt the entire project from scratch, redesigned the web interface, gave it a new name — **ValueScope** — and registered a dedicated domain at **valuescope.app**. Feel free to check it out.

This post serves as an update note, and a chance to explain why I decided to rebuild the web version.

---

## The Web Version Now Has AI

In the previous version, AI valuation could only run in the terminal (CLI), and only models with CLI support — like Claude, Gemini, and Qwen — were available. Many friends aren't comfortable with the command line, and deploying the CLI version to the cloud had its own limitations, so the web version never got AI integration.

That's finally been fixed. The web version now uses DeepSeek R1's reasoning API. Since DeepSeek doesn't have built-in web search, I also integrated Serper (a Google Search API), creating a combination of Google search + domestic AI reasoning.

For web users, everything is pre-configured — you don't need to install anything. Just open the page and start using it.

---

## Custom Valuation

The web version retains the manual parameter selection feature for DIY valuations. Default parameters are based on historical averages; drag the sliders to adjust, and valuation results update instantly. This mode doesn't require AI reasoning, runs faster, and is completely free with unlimited use.

Both Custom Valuation and AI Quick Valuation run on the same underlying model — a standardized 10-year FCFF framework including WACC, terminal value, and sensitivity analysis. The only difference is where the parameters come from: AI reasoning vs. your own judgment. After AI valuation completes, you can still manually adjust parameters and see results update in real time.

---

## Supported Markets

Historical financial data for A-shares and Hong Kong stocks is built in — free to use, no API registration needed. If you're interested in US or Japanese stocks, you'll need an FMP (Financial Modeling Prep) API Key to access historical financial data.

FMP is a US-based financial data company that I've personally used for years. Their US stock data quality is solid, and the pricing is relatively affordable. FMP's data focuses primarily on equities, with particularly comprehensive financial data — ideal for quickly pulling financials and running valuations.

I recently secured a partnership discount. If you purchase through the referral link in the web app's "Financial Data API" section, you'll get a better price than the official site — and it helps support this project. You can also find FMP API usage instructions and the discount link in the GitHub project documentation.

---

## A Note on AI Quota

If you're a frequent AI user, you probably know that API calls are billed by usage — significantly more expensive than a flat subscription. For heavy users, running the terminal CLI version is more economical, though you won't have access to domestic models like DeepSeek since very few support CLI (currently only Qwen, among others). For light usage, the web version is more convenient. The web version's AI Quick Valuation currently runs on my personal API key, so it's available on a limited quota basis.

If you run out of quota and want to keep going, here are some options:

- Custom Valuation mode doesn't consume AI quota — it's free and unlimited, and the functionality is more than sufficient;
- Register your own DeepSeek and Serper APIs, enter them in the control panel to continue using the web version's AI features (each AI analysis costs roughly ¥0.1);
- If you prefer the terminal, clone the source code and run it locally with your own Claude / Gemini / Qwen subscription — these all have CLI versions, and monthly subscriptions are usually cheaper than API calls.

---

## Why I Built This Tool

ValueScope is entirely a personal passion project — I use this tool in my own investment workflow. The reason I wanted to make it public comes from a few core beliefs:

**🌐 Democratizing Technology** — In the AI era, each of us has the opportunity to turn ideas into products on our own. Professional-grade data modeling and valuation tools no longer belong exclusively to elite institutions. ValueScope aims to give every retail investor access to institutional-grade DCF valuation.

**🧱 First Principles** — After years of market ups and downs, as a veteran investor, I firmly believe in Buffett's philosophy: discounted cash flow is the cornerstone of value investing — estimating a company's true intrinsic value based on its future cash flows. This is the path to long-term survival in the stock market. If you're interested, check out my earlier post [*DCF Valuation Is the First Principle for Value Investors*](https://mp.weixin.qq.com/s?__biz=MzkwMTQ0ODE4NQ==&mid=2247484125&idx=1&sn=1a846af7252375e10078700a71fa41b6&scene=21#wechat_redirect).

**🏷️ Roughly Right > Precisely Wrong** — This might sound contradictory when it comes to DCF. Many people think valuation is pointless — too many variables, and small adjustments can lead to vastly different results. ValueScope doesn't aim for complex, detailed financial forecasting models. Instead, it focuses on capturing the most critical variables to produce a reasonable valuation range. This follows Damodaran's valuation methodology: focus on growth, margins, and reinvestment as core drivers, rather than chasing precise three-statement forecasts. More importantly, through DCF valuation and sensitivity analysis, you can think in reverse — what core assumptions does the current market price imply? Do you agree with the market's expectations? This process of reverse thinking is more valuable than arriving at a precise "target price."

---

Try it online: **valuescope.app** (desktop recommended)

Source code and project details: **github.com/alanhewenyu/ValueScope**

The project is fully open source. Feedback and contributions are welcome.

---

> 💡 **Want to try it yourself?** Use [ValueScope online valuation tool](https://valuescope.app/) — let AI analyze the parameters and calculate any stock's intrinsic value for free.
