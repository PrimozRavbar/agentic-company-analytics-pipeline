from dataclasses import dataclass
import numpy as np


@dataclass
class Event:
    type: str
    ticker: str
    start_time: any
    end_time: any
    strength: float
    features: dict
    summary: str


def build_events_from_signal(
    df,
    ticker,
    signal_name,
    condition_fn,
    event_type
):
    events = []
    in_event = False
    start = None

    df = df.sort_values("date")

    for i, row in df.iterrows():

        active = condition_fn(row)

        if active and not in_event:
            start = row["date"]
            in_event = True

        elif in_event and (
            not active or i == df.index[-1]
        ):
            end = row["date"]

            segment = df[
                (df["date"] >= start) &
                (df["date"] <= end)
            ]

            if len(segment) < 2:
                in_event = False
                continue

            signal_mean = float(segment[signal_name].mean())
            length = len(segment)

            total_return = float(
                segment["close"].iloc[-1]
                / segment["close"].iloc[0]
                - 1
            )

            returns = segment["close"].pct_change().fillna(0)

            realized_vol = float(returns.std())

            max_drawdown = float(
                (
                    segment["close"]
                    / segment["close"].cummax()
                    - 1
                ).min()
            )

            strength = float(
                abs(signal_mean) * np.log1p(length)
            )

            events.append(
                Event(
                    type=event_type,
                    ticker=ticker,
                    start_time=start,
                    end_time=end,
                    strength=strength,
                    features={
                        f"mean_{signal_name}": signal_mean,
                        f"max_{signal_name}": float(
                            segment[signal_name].max()
                        ),
                        "length": length,
                        "total_return": total_return,
                        "realized_vol": realized_vol,
                        "max_drawdown": max_drawdown,
                    },
                    summary=(
                        f"{ticker} {event_type} "
                        f"({length}d, {total_return:.1%})"
                    )
                )
            )

            in_event = False

    return events


def summarize_events(events):
    summary = {}

    for event in events:
        summary[event.type] = (
            summary.get(event.type, 0) + 1
        )

    return summary


def generate_events(feature_df):
    events = []

    for ticker, df in feature_df.groupby("ticker"):

        df = df.sort_values("date")

        events += build_events_from_signal(
            df,
            ticker,
            "volatility",
            lambda r: (
                r["volatility"]
                > df["volatility"].mean()
                + df["volatility"].std() * 2
            ),
            "volatility_regime"
        )

        events += build_events_from_signal(
            df,
            ticker,
            "momentum",
            lambda r: (
                r["momentum"]
                < df["momentum"].mean()
                - df["momentum"].std() * 2
            ),
            "downtrend_regime"
        )

        events += build_events_from_signal(
            df,
            ticker,
            "zscore",
            lambda r: abs(r["zscore"]) > 2.5,
            "statistical_stress"
        )

    return events
