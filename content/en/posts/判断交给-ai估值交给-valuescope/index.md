---
title: "Leave the Judgment to AI, the Valuation to ValueScope"
date: 2026-07-13
draft: false
slug: "判断交给-ai估值交给-valuescope"
categories: ["Company Valuation"]
tags: ["MCP", "DCF", "Reverse DCF", "AI Valuation", "Sensitivity Analysis"]
summary: "ValueScope now ships an MCP server, letting AI assistants like Claude run standardized DCF valuations directly."
---

Back in March I published the [ValueScope DCF valuation tool](https://mp.weixin.qq.com/s?__biz=MzcxMDI2MjQwMg==&mid=2247484323&idx=1&sn=7944dd83014d8055768ee9b49a60a21f&scene=21#wechat_redirect) on my WeChat account, and quite a few readers asked: **can AI call this model directly to run a valuation?**

Now it can.

And behind this update is a rethinking of where the product should go. For a while I'd been working on how to embed AI features into the ValueScope website. But lately I've become increasingly convinced that this direction may no longer matter much. Because when people have a question these days, their first instinct is already to just ask AI.

If that's the case, then perhaps the best home for a valuation tool isn't an AI button on a web page — it's becoming a capability of the AI itself. So this update makes a change of direction: **instead of having you call AI through the website, we let AI call ValueScope.**

## From "an AI valuation button on a website" to "a valuation tool inside AI"

What's launching this time is ValueScope's MCP service.

MCP (Model Context Protocol) can be thought of as the universal interface standard of the AI world. Through MCP, AI assistants like Claude and ChatGPT can safely call external tools. Once ValueScope is connected, your AI gains a new capability: **valuing stocks with a standardized DCF engine.**

Some might ask: can't Claude or ChatGPT already do a DCF valuation directly? Why do you need a dedicated tool?

The problem is that AI is great at reasoning but bad at staying consistent. Ask AI to run a DCF on Tencent today and again next month, and the two runs may use different data sources, different accounting conventions, different model frameworks, even different parameter definitions. In the end you see the valuation change but you don't know: did the company's fundamentals change, or did the AI itself change? For someone tracking dozens of companies over the long run, that's a problem.

ValueScope MCP divides the labor this way:

- **AI handles forward-looking judgment**: searching for the latest guidance and analyst expectations, and reasoning through future growth rates, margins, and capital efficiency in light of industry logic;
- **ValueScope handles data and computation**: standardized financial data, the DCF model, sensitivity analysis, reverse DCF, and every concrete calculation step.

The same inputs always produce the same result. In other words: **AI provides the intelligence, ValueScope provides the framework and the discipline.**

This split has one very practical benefit as well: speed. Previously, when AI built a DCF from scratch, it had to search for financial data itself, understand the structure of the statements, set up a model framework, and then work through the calculations step by step — essentially assembling a financial model on the fly. That's slow, and the token cost is high.

With ValueScope MCP, the data pipeline, model framework, and calculation logic are already in place. AI no longer has to spend time shuffling numbers and doing arithmetic; it spends its time where it actually adds value — analysis and judgment. A valuation typically finishes in a second or two, and re-running it with adjusted assumptions is nearly instantaneous.

MCP is an open protocol, so any MCP-capable client can connect to ValueScope. Today that includes Claude Code, Claude Desktop, Claude Web, ChatGPT, Cherry Studio, and other MCP-supporting clients. Valuation quality ultimately still depends on the underlying model's reasoning ability and its web-search capability. From my own use, Claude still gives the best experience.

## What it actually looks like in use

Once connected, you just talk to your AI the way you normally would.

For example: run a DCF valuation on Tencent Holdings.

The AI will automatically call the ValueScope engine and work through the whole process. It first pulls five years of historical financials and computes the historical ranges of each valuation parameter — trends in revenue growth, margins, and capital efficiency, for example. Then, following the analytical framework built into the model, it searches the web for the latest guidance, analyst consensus, and industry information. Next it reasons through each key assumption independently and explains its rationale. Finally it calls the valuation engine to produce the result.

The output includes the valuation conclusion, a table of key assumptions, historical trend analysis, value composition, sensitivity analysis, and a reverse DCF. More valuable than "what's the target price," I've always thought, is the question: what assumptions does the current market price imply? And do you agree with them? That's why I've always been fond of reverse DCF.

You can go further and ask for separate valuations under optimistic, neutral, and pessimistic scenarios, or simply look at the historical trend charts for margins and revenue growth. Throughout the process, all you have to do is ask questions and make judgments — data retrieval, model computation, and organizing the results are all handled by the engine.

## How to connect (two minutes)

### Claude Code

```
claude mcp add valuescope --transport http https://mcp.valuescope.app/mcp
```

### Claude web / mobile app

Settings → Connectors → Add custom connector

Enter:

```
https://mcp.valuescope.app/mcp
```

### Cherry Studio

In the MCP server configuration, choose the HTTP type and enter the address above.

## Supported markets and data sources

A-shares and Hong Kong stocks are completely free — no API registration needed, just connect and go.

Data for US and Japanese stocks comes from FMP (Financial Modeling Prep), which requires an API key. If you already set things up per "How to connect" above (without a key) and want to add one, just remove the old entry and add it again:

```
claude mcp remove valuescope
claude mcp add valuescope --transport http https://mcp.valuescope.app/mcp --header "X-FMP-Key: your-key"
```

In the Connectors section of the web / mobile app, you add a custom request header under the advanced options when adding the connector — name it `X-FMP-Key` and set the value to your key.

Once configured, every conversation will carry the key automatically, with no need to mention it again. (If you just want a quick test, that works too — simply say in the chat, "my FMP key is xxx, value NVIDIA for me." But that only applies to the current conversation; for long-term use, configure it as described above.)

FMP's financial data quality is solid, and its subscription pricing is relatively cheap. Signing up and subscribing through the referral link below (the valuescope coupon code is already included) gets you a better price than the official site:

```
https://site.financialmodelingprep.com/pricing-plans?couponCode=valuescope
```

## About the web version

The web version at valuescope.app will continue to be maintained, and it got an upgrade this time as well: page load speed is noticeably faster, and each tab now has its own link, making sharing and citing much easier.

The web version will return to the role it's best suited for: **a DCF workbench for manually tuning parameters, running sensitivity analysis, and quickly testing ideas.**

## Still the same original intent

ValueScope remains a personal side project, and it remains the investing tool I use every day.

That March article mentioned three founding beliefs: technology should be democratized; discounted cash flow is the first principle of value investing; and vaguely right beats precisely wrong. This MCP update is, at heart, an extension of the same idea.

In the past, professional tools tended to require users to learn their way of working. Now I increasingly believe: **a good tool shouldn't ask you to change your habits to accommodate it — it should fit itself into your workflow.**

If your workflow has already become "ask AI first," then the most sensible place for a valuation tool is inside the AI. ValueScope MCP is a step in that direction.

---

Finally, both addresses in one place, for easy copying:

**MCP endpoint**:

```
https://mcp.valuescope.app/mcp
```

**Web version**:

```
https://valuescope.app
```

Try it out and let me know what you think.

**Disclaimer: All ValueScope output is the result of model computation, intended for research reference only, and does not constitute investment advice.**

---

> 💡 **Want to run the numbers yourself?** Use the [ValueScope online valuation tool](https://valuescope.app/) — AI helps you analyze the parameters, and you can compute any stock's intrinsic value for free.
