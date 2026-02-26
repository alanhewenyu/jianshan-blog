---
title: "Company Valuation: Free Cash Flow to the Firm (FCFF)"
date: 2023-12-21
draft: false
slug: "公司估值自由现金流fcff"
categories: ["Company Valuation"]
tags: ["DCF", "Value Investing", "ROIC", "Buffett", "Financial Statements", "Valuation", "WACC"]
summary: ""
ShowToc: true
TocOpen: false
---

As discussed in a previous article, a company's free cash flow to the firm (FCFF) is the residual amount after deducting the capital investment (reinvestment) required to maintain and grow the business from net operating profit after tax (NOPAT).

## Net Operating Profit After Tax

Net operating profit after tax is not a standard financial statement line item but rather the earnings measure that corresponds to a company's total invested capital (IC). For ease of calculation, practitioners typically start with earnings before interest and taxes (EBIT) from the financial statements and compute the applicable income tax on that basis:

*NOPAT = EBIT x (1 - Effective Tax Rate)*

The advantage of using EBIT is that it is a widely available metric, much easier to obtain from financial statements compared to NOPAT. The effective tax rate reflects the company's actual income tax burden, which is usually lower than the statutory tax rate, primarily due to reconciling items between tax filings and financial statements.

Given that interest expenses are tax-deductible, the tax computed on EBIT will be higher than the company's actual tax payment, meaning NOPAT may be slightly understated. However, there is no need for concern -- the NOPAT formula intentionally ignores the tax shield from interest expenses because that benefit is captured in the calculation of the cost of capital (WACC). In other words, when discounting cash flows, the discount rate in the denominator is also reduced accordingly.

## Reinvestment

Reinvestment is essential for sustaining a company's growth. If all after-tax profits were distributed to shareholders, and without additional external financing, the company would cease to grow. Recall the formula from a previous discussion:

*NOPAT Growth Rate = ROIC x Reinvestment Rate*

A company's reinvestment is reflected on the left side of the balance sheet. Upon closer examination, capital investments can broadly be categorized into two types: working capital and long-term assets.

### Working Capital Investment

Working capital is the net amount of current assets minus non-interest-bearing current liabilities (NWC). An important point to note is that, unlike the operating nature of working capital, excess cash and investment securities are not required for normal business operations and do not form part of working capital. Such non-operating investment assets should be valued separately.

### Long-Term Asset Investment

Long-term asset investment typically refers to a company's expenditure on fixed assets and intangible assets, which is also reflected in the investing activities section of the cash flow statement. It is important to note that depreciation is a non-cash expense and must be added back to EBIT when calculating cash flow.

If we view (capital expenditure - depreciation) as a single item, it can be understood as follows: a company's capital expenditure must first cover the impact of depreciation on fixed assets, and the portion net of depreciation represents the incremental capital expenditure. This is how it works in practice -- machinery and facilities are not typically replaced all at once at the end of their useful life but are continuously maintained and upgraded.

Ongoing investment in long-term assets is often essential for maintaining a company's competitiveness, especially in capital-intensive industries with rapid technological change, such as the semiconductor industry. In contrast, some companies have annual capital expenditures roughly equal to depreciation, with minimal incremental capital spending. These companies resemble Buffett's beloved See's Candies -- requiring very little incremental capital expenditure while maintaining market competitiveness and generating consistent cash flow.

## How to Calculate Free Cash Flow

Summarizing the above, a company's free cash flow can be expressed as:

*FCFF = EBIT x (1 - Effective Tax Rate) - Delta NWC - (Capital Expenditure - Depreciation)*

Since changes in working capital and long-term asset investment both constitute reinvestment, when expressed as a percentage of NOPAT, this gives us the reinvestment rate:

*Reinvestment Rate = (Capital Expenditure - Depreciation + Delta NWC) / NOPAT*

Therefore, a company's free cash flow can be written as:

*FCFF = EBIT (1 - Effective Tax Rate) x (1 - Reinvestment Rate)*

A company's reinvestment typically maintains a relatively stable relationship with revenue, meaning the input-output ratio tends to be fairly consistent. Looking at EBIT, its growth depends on revenue growth and operating profit margins -- that is, business expansion and improvements in operational efficiency. Revenue growth and operating profit margins are thus the core drivers of a company's free cash flow and intrinsic value, consistent with the conclusions from the earlier article analyzing the key drivers of equity investment returns.

## An Alternative Method for Calculating Free Cash Flow

In practice, the most common approach to calculating FCFF starts from the cash flow statement, subtracting capital expenditures (from investing activities) from operating cash flow. This method is obviously much simpler than the approach discussed above.

At first glance, the method discussed earlier resembles the indirect method of preparing the cash flow statement -- starting from EBIT and treating non-cash expenses (depreciation) and changes in working capital as adjustments. So are the two approaches equivalent, and can we simply use the cash flow statement method?

In reality, two types of expenses are treated differently between the two methods, which can lead to significant distortions in the FCFF calculated from the cash flow statement.

### Interest Expenses

The indirect method of the cash flow statement typically starts from net income, which means that, compared to EBIT, operating cash flow has already deducted financial expenses. If we are calculating free cash flow to equity (FCFE), this is not an issue. However, as discussed earlier, free cash flow to the firm (FCFF) is more commonly used. Consequently, deriving FCFF from the cash flow statement will understate the true free cash flow.

### Stock-Based Compensation

While stock-based compensation is part of employee remuneration, it differs in that it is a non-cash expense. As such, it appears as a reconciling item in the indirect method of the cash flow statement, thereby increasing operating cash flow. However, the FCFF formula discussed earlier does not treat stock-based compensation as a reconciling item.

Does it seem like there is an error in the formula? Quite the opposite -- although stock-based compensation is not a cash expense, it should indeed be deducted from free cash flow. This may seem counterintuitive from a typical cash flow perspective, but stock-based compensation effectively surrenders the company's cash earnings.

Here is how Aswath Damodaran, the renowned professor of finance and valuation in the United States, puts it:

> "Stock-based compensation is simply a case where a company has used a barter system to get around the cash flow effect. In other words, if the company had issued the options and restricted stock (that it plans to give to employees) to the market, and then used the cash proceeds to pay employees, we would have treated it as a cash expense."

Therefore, although stock-based compensation cannot be reflected as a cash expense on the financial statements, it essentially surrenders the company's cash earnings.
