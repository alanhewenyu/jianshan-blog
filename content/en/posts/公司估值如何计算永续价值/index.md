---
title: "Company Valuation: How to Calculate Terminal Value"
date: 2023-12-23
draft: false
slug: "公司估值如何计算永续价值"
categories: ["Company Valuation"]
tags: ["DCF", "ROIC", "Valuation", "WACC", "Consumer"]
summary: "Systematically explains terminal value calculation in the two-stage DCF model, including perpetual growth rate determination, the reinvestment-ROIC relationship, and how the terminal value formula is essentially a dividend discount model."
---

As discussed in previous articles, when valuing a company using discounted cash flow analysis, a two-stage cash flow model is typically employed, consisting of an explicit forecast period and a perpetuity period. The present value of the perpetuity-period cash flows is the company's terminal value.

*Terminal Value = NOPAT * (1 - Reinvestment Rate) / (WACC - g)*

- NOPAT represents the net operating profit after tax in the first year of the perpetuity period;
- g represents the growth rate during the perpetuity period;
- WACC represents the weighted average cost of capital.

NOPAT after deducting reinvestment can be thought of as the company's dividend payout. In essence, the formula above is fundamentally a Dividend Discount Model.

## Growth Rate

The perpetuity period assumes the company has entered a phase of long-term, stable growth. A company's long-term growth rate generally does not exceed the growth rate of the broader economy — put simply, a company cannot sustainably earn excess returns above the macroeconomic growth rate. Over the long run, the risk-free rate tends to converge with the economy's long-term growth rate. As a result, the risk-free rate is commonly used as a proxy for the company's long-term growth rate.

## Reinvestment Rate

Based on the relationship among the reinvestment rate, the growth rate (g), and the return on new invested capital (RONIC), the reinvestment rate used in the terminal value calculation can be estimated as follows:

*Reinvestment Rate = g / RONIC*

- RONIC represents the return on capital for reinvested (i.e., newly deployed) capital. The "N" distinguishes it from ROIC by specifically referring to returns on new capital rather than on total existing capital.

Accordingly, the terminal value formula can be rewritten as:

*Terminal Value = NOPAT * (1 - g / RONIC) / (WACC - g)*

## RONIC

The expected return on new invested capital (RONIC) should account for the company's competitive environment and competitive advantages. For most companies, the long run brings a reversion to the mean. Just as a company cannot sustain revenue growth above the macroeconomic growth rate, it is equally difficult to earn excess returns above the cost of capital (WACC) over time — meaning RONIC tends to approach or equal WACC.

When RONIC is close to the cost of capital, the terminal value becomes insensitive to the perpetuity growth rate, because the net present value of incremental investment approaches zero. Therefore, when RONIC = WACC, the terminal value formula simplifies further to:

*Terminal Value = NOPAT / WACC*

For companies operating in highly competitive industries where all excess profits are eroded by competition, the return on incremental investment ultimately converges to the cost of capital. In such cases, this simplified formula is appropriate.

Note that this does not imply the company ceases to grow in the long run — rather, growth no longer creates additional value.

Nor does it mean the company creates no value whatsoever during the perpetuity period. The reason for introducing RONIC as a distinct concept is that RONIC does not equate to the return on the company's total capital (both existing and newly invested). Capital invested prior to the perpetuity period continues to earn returns at the rates established during the explicit forecast period. In other words, the company's competitive advantages do not expire at the start of the perpetuity period — existing capital continues to generate excess returns.

## Can RONIC Exceed the Cost of Capital?

Although competition ultimately erodes excess returns on incremental investment, some companies do possess sustainable reinvestment advantages — particularly consumer brands with strong brand equity and unique intellectual property. In such cases, RONIC may exceed the cost of capital. However, as a matter of prudence, this excess return is typically capped at no more than 5%.
