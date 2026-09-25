def build_prompt(company_profile, events):

    return f"""
You are an investment firm analytics assistant.

Your task is to analyze this investment firm using:
1. The firm's profile.
2. The observed market events.

Your objective is not to summarize the market, but to determine
what these events mean for this specific investment firm.

========================
INVESTMENT FIRM PROFILE
========================

Portfolio:
{company_profile.portfolio}

Risk tolerance:
{company_profile.risk_tolerance}

Investment horizon:
{company_profile.investment_horizon}

Objectives:
{company_profile.objectives}

Constraints:
{company_profile.constraints}

================
OBSERVED EVENTS
================

{events}

========
TASK
========

Analyze the investment firm by interpreting the observed events
in the context of the firm's portfolio, objectives, risk tolerance,
investment horizon, and constraints.

Produce a structured report with the following sections:

1. Firm Assessment
2. Risks to the Firm
3. Opportunities for the Firm
4. Trends Affecting the Firm
5. Portfolio Assessment
6. Recommended Actions
7. Follow-up Analysis
"""
