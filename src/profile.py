from dataclasses import dataclass
from typing import List
import random


TICKERS = [
    "AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","BRK-B","JPM","V",
    "UNH","XOM","MA","AVGO","PG","HD","LLY","MRK","COST","PEP",
    "ADBE","CSCO","KO","CRM","WMT","BAC","NFLX","TMO","DIS","ABT"
]

RISK_LEVELS = ["low", "medium", "high"]

HORIZONS = [
    "short_term",
    "medium_term",
    "long_term"
]

OBJECTIVES = [
    "capital_preservation",
    "steady_growth",
    "income_generation",
    "aggressive_growth"
]


@dataclass
class CompanyProfile:
    portfolio: List[str]
    risk_tolerance: str
    investment_horizon: str
    objectives: List[str]
    constraints: List[str]


def random_profile():
    return CompanyProfile(
        portfolio=random.sample(
            TICKERS,
            k=random.randint(5, 10)
        ),
        risk_tolerance=random.choice(RISK_LEVELS),
        investment_horizon=random.choice(HORIZONS),
        objectives=random.sample(OBJECTIVES, k=2),
        constraints=[]
    )
