
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)


MODEL_NAME = "Qwen/Qwen3-1.7B"


def load_tokenizer(model_name=MODEL_NAME):
    return AutoTokenizer.from_pretrained(model_name)


def load_model(model_name=MODEL_NAME):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    return AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
    )


def format_messages(messages, tokenizer):
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )


def generate(model, tokenizer, messages, max_new_tokens=150):
    prompt = format_messages(messages, tokenizer)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    return tokenizer.decode(
        output[0],
        skip_special_tokens=False,
    )


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
