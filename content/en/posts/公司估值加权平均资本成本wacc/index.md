---
title: "Company Valuation: Weighted Average Cost of Capital (WACC)"
date: 2024-01-05
draft: false
slug: "公司估值加权平均资本成本wacc"
categories: ["Company Valuation"]
tags: ["DCF", "Valuation", "WACC"]
summary: ""
---

When discounting a company's free cash flow to the firm (FCFF), the discount rate used is the Weighted Average Cost of Capital (WACC). Since a company's cost of capital comprises both equity and debt, the weighting reflects the company's capital structure.

*WACC = E/V*ke + D/V*kd*(1-Tm)*

- D/V = Target proportion of debt at market value relative to total firm value
- E/V = Target proportion of equity at market value relative to total firm value
- kd = Cost of debt
- ke = Cost of equity
- Tm = Marginal tax rate on the company's income

This article does not intend to provide a comprehensive guide to calculating WACC; instead, it focuses on a few commonly misunderstood aspects.

## Industry Effects

WACC represents an opportunity cost — the return investors could earn by investing their capital elsewhere at a comparable level of risk.

The ability of investors to diversify their portfolios means that only non-diversifiable risk affects the cost of capital. Since non-diversifiable risk generally impacts all companies within the same industry, the industry in which a company operates is the primary driver of its cost of capital. As a result, companies in the same industry tend to have similar costs of capital.

## Cost of Equity

The cost of equity is typically estimated using the Capital Asset Pricing Model (CAPM):

*Cost of Equity = Risk-Free Rate + β * Equity Risk Premium*

For the beta (β), the industry-level beta is commonly used — that is, the industry average beta based on the company's line of business, adjusted for differences in financial leverage.

## Cost of Debt

The cost of debt reflects the company's underlying default risk. If the company has publicly traded bonds, the yield on the most recently issued bonds can be used directly. If no directly observable public data is available, the implied default spread corresponding to the company's credit rating can serve as a reference. If no credit rating exists, the cost can be estimated based on the company's existing debt, with adjustments for liquidity and debt coverage capacity.

Because interest on debt is tax-deductible, the after-tax cost should be used. A company's effective tax rate is often lower than its statutory rate. The tax rate used in this calculation should be the company's marginal tax rate, which is typically higher than the effective tax rate.

## Weighting

The weights are based on the market values of equity and debt, not book values. For publicly listed companies, the market value of equity is readily available. Estimating the market value of debt is generally more difficult, but since the market value of debt typically does not deviate significantly from its book value, book value is commonly used as an approximation.

Why use market values rather than book values for the weights? As noted above, the cost of capital is an opportunity cost. Consider the following scenario: if the company were to distribute all capital earmarked for reinvestment as dividends, investors could deploy that capital elsewhere to earn a return. To keep the capital structure unchanged, the company would need to either repay debt or issue new shares — both of which must be done at market prices.

Since cash flow projections are long-term in nature, the weights should reflect the target capital structure. If the weights based on the current market values of equity and debt are expected to change materially over time, they should be adjusted toward the target capital structure.
