---
title: "Python and Automated Data Processing"
date: 2024-04-25
draft: false
slug: "python与自动化数据处理"
categories: ["Company Valuation"]
tags: ["DCF", "Value Investing", "Financial Statements", "Valuation", "Moutai", "Tencent", "Alibaba", "Meituan", "AI"]
summary: ""
toc: true
---

In this article, I'd like to share some personal reflections on learning Python and automated data processing. As a non-computer science professional, my explanations may not be the most technically precise, but I hope that by sharing these experiences, more people can appreciate the role of Python in data processing. For example, when it comes to the company valuation topics we've previously discussed, automated data processing with Python allows us to quickly estimate a company's fair intrinsic value in just one minute -- all you need is to input a few key valuation parameters. The foundational data used in the earlier valuation demonstration of Kweichow Moutai was entirely generated through automation.

But before we talk about Python, let's first explore the importance of historical financial data in company valuation.

## Valuation and Historical Financial Data

When we set out to calculate a DCF valuation for a listed company, the first step is to review historical financial data. Historical financial data is critically important for valuation, primarily for the following reasons:

### **Income Statement: The Starting Point for Projections**

Financial forecasting typically begins with sales projections, because revenue has far-reaching implications -- it directly affects the forecasting of expenses, working capital, and other items. As the foundation of DCF valuation, Free Cash Flow to the Firm (FCFF) projections are no exception; the starting point is revenue and its growth rate. Therefore, a company's growth profile is one of the most important factors in valuation.

### **Balance Sheet: The Basis for Calculating Equity Value**

The DCF valuation derived from FCFF reflects the value created by a company's normal operating activities. After this initial calculation, two additional adjustments are needed. The first is adding back the company's non-operating assets, such as excess cash reserves and equity investments in other companies. These assets are not essential to ongoing operations and are not captured in the initial FCFF calculation.

In reality, many companies hold massive cash reserves and equity investments, which have a significant impact on equity value assessment. Take China's internet giants, for example -- whether it's Tencent, Alibaba, or Meituan, all of them carry substantial cash and equity investments on their books. Tencent, in particular, holds equity investments exceeding RMB 900 billion.

The second adjustment is deducting interest-bearing debt and minority interests to arrive at the company's equity value. Recall the FCFF formula we introduced earlier -- it starts with after-tax operating profit. This tells us that FCFF belongs to the entire firm, and the difference between FCFF and ultimate equity value is accounted for by interest-bearing debt and minority interests.

### Historical Data as a Mirror: Learning from the Past to Predict the Future

A company's short-term financial data can be easily distorted by economic cycles and industry cycles. Only by extending the historical timeframe can we gain a clearer picture of a company's financial performance. For value-oriented investments -- companies that may not be growing rapidly but deliver consistent results -- DCF valuation tends to be more accurate, because stable historical data yields higher predictability. For high-growth companies, historical data has limited predictive value. Regardless of the type of company, if historical data is highly volatile and unstable, forecasting the future based on that data becomes extremely difficult. Such companies carry significant investment risk, and their valuations are hard to pin down.

## Python and Data Automation

Given the importance of historical data and the need for data spanning multiple years, the ability to retrieve this data automatically can dramatically improve valuation efficiency. There are quite a few professional financial data providers in China, and downloading financial data through Excel is something anyone can do. An even better approach is to use the API interfaces offered by financial data providers to retrieve data programmatically, which requires writing code.

We are in the midst of an exciting new era of artificial intelligence. With the help of ChatGPT, writing programs has become easier than ever before. In earlier articles, I demonstrated how ChatGPT can automatically generate code. While ChatGPT has replaced much of what programmers used to do, this doesn't mean you can skip learning to code. The premise that anyone can become a programmer is that everyone understands programs and knows how to write code. Understanding code allows us to better leverage the efficiency gains brought by ChatGPT and the broader AI revolution.

There are many programming languages, with the lowest level being machine language, which directly manipulates the computer's 0s and 1s. Above that are assembly language and various high-level programming languages such as C++ and Java. We don't need a deep understanding of every language -- we just need to know that compared to high-level languages like C++, Python is a scripting language that is very close to natural language. As a scripting language, Python has relatively simple syntax and structure, making it easy to get started. Of course, as a scripting language, Python's drawback is obvious: it runs slower. However, for handling everyday tasks, this difference in speed is barely noticeable.

The ecosystem around Python is enormous. Common applications include: data processing (encompassing data cleaning, analysis, and visualization), web development and web scraping, and -- most notably -- artificial intelligence, which is a key reason why Python has become increasingly popular.

## Reflections on Learning Programming

### Programming Is a Simulation of the Real World

This is my biggest takeaway from self-learning Python. For example, when you first start learning to code, you begin with Lists and Dicts (dictionaries). Converting real-world objects and relationships into lists and dictionaries -- lists within dictionaries, dictionaries within lists -- this elegantly simple treatment can represent the vast complexity of human society as structured, clear data.

Another example is the concept of a Class in programming, which has a distinctly Platonic philosophical flavor. Plato believed that everything begins with an ideal Form, and the physical world is merely a shadow of those Forms. He used the analogy of a painter painting a table to illustrate the relationship between Forms and specific things: a carpenter builds a table according to a pre-existing ideal, and a painter then paints based on the carpenter's table. Thus, the painter's table is three steps removed from reality -- it is a copy of a copy of the Form. Plato's concept of the Form is very much like a Class in programming, and the depiction of the real world is like an Object (instance) under that Class.

In short, by opening the door to programming, you'll suddenly realize how programs describe the world -- and how simple and elegant their language is.

### Making Computer Operations Fun

Although computers are becoming increasingly powerful, for most non-professionals, a computer is basically a web browser plus an office suite. However, the truly interesting aspect of computing lies in human-computer interaction. During the process of learning to program, when you type your first command `print("Hello, World!")` into the terminal and receive a response, you'll discover that a computer can be your interactive partner. When you can write a small piece of code to accomplish a minor task, you'll experience the joy of that sense of control.

## How to Self-Learn Python

There are many Python courses online, varying widely in quality and difficulty. In fact, self-learning Python isn't hard. My recommendation is to read books, combining them with problems you encounter at work or interests in your daily life. Approaching the material with a specific problem to solve in mind helps you quickly get started on small projects, accelerating the learning process with immediately visible results. For instance, finance professionals frequently face data processing and transformation tasks, as well as the challenge of automating data workflows to improve efficiency.

Here, targeting professionals in finance, data analysis, and investment, I'd like to recommend two classic introductory books (not advertisements):

The first is *Python Crash Course* (published by Posts and Telecom Press in China). This book consistently receives high ratings online and has been a bestseller. As an introductory text, its content is concise with approachable examples -- truly an excellent fit for beginners.

The second is *Python for Data Analysis* (published by China Machine Press). The indispensable Python library for data analysis is pandas, and those who frequently work with Excel will find pandas easy to pick up, since its data structures resemble Excel's two-dimensional table format. This book was written by the creator of pandas himself, and it is widely regarded as the definitive guide for learning data analysis.
