# Agentic Company Analytics Pipeline

An agentic framework for answering analytic questions about a company using internal and external data, structured events, company profiles, retrieval, and a local LLM.

## Pipeline

```text
                         ┌─────────────────────┐
                         │   Internal &        │
                         │   External Data     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Signals        │
                         │  Derived features   │
                         │    & indicators     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Events        │
                         │ Structured findings │
                         │     from data       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                 ┌────────────────────────────────────┐
                 │          Agent / Harness            │
                 │                                    │
                 │  ┌──────────────┐                  │
                 │  │   Company    │                  │
                 │  │    Profile   │                  │
                 │  └──────┬───────┘                  │
                 │         │                          │
                 │         ▼                          │
                 │  ┌──────────────┐                  │
                 │  │    Local     │                  │
                 │  │     LLM      │                  │
                 │  └──────┬───────┘                  │
                 │         │                          │
                 │   Retrieval Request                │
                 │         │                          │
                 │         ▼                          │
                 │  ┌──────────────┐                  │
                 │  │  Retrieval   │◄──── Data/Events │
                 │  └──────┬───────┘                  │
                 │         │                          │
                 │         ▼                          │
                 │      New Context                    │
                 │         │                          │
                 │         └──────────► LLM            │
                 │                      │              │
                 │                      ▼              │
                 │               Further Request?      │
                 │                 │          │        │
                 │                Yes         No        │
                 │                 │          │        │
                 │                 └─── loop   ▼        │
                 │                         Analysis     │
                 │                         / Answer      │
                 └────────────────────────────────────┘
```

## Development Plan

### 1. Personalized Retrieval

Make retrieval dynamic rather than fixed. The agent should select relevant information based on the company's portfolio, risk tolerance, objectives, investment horizon, constraints, and other company-specific characteristics.

### 2. Dynamic Company Profile

Replace the current simulated profile with a richer, dynamic representation of the company, including the characteristics needed to personalize the analysis and retrieval process.

### 3. Agentic Harness

Build the orchestration layer that maintains state and context, interacts with the local LLM, issues retrieval requests, incorporates retrieved information, and iterates until sufficient information is available to answer the question.
