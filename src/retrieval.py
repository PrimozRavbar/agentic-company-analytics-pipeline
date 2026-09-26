
import pandas as pd
from collections import defaultdict


class EventStore:
    def __init__(self, events):
        self.events = events

    def retrieve(self, request):
        return retrieve_events(
            self.events,
            **request.model_dump()
        )


def retrieve_events(
    events,
    tickers=None,
    event_types=None,
    start_time=None,
    end_time=None,
    reason=None
):
    if start_time is not None:
        start_time = pd.Timestamp(start_time)

    if end_time is not None:
        end_time = pd.Timestamp(end_time)

    retrieved = []

    for event in events:

        if (
            tickers is not None
            and event.ticker not in tickers
        ):
            continue

        if (
            event_types is not None
            and event.type not in event_types
        ):
            continue

        if (
            start_time is not None
            and event.end_time < start_time
        ):
            continue

        if (
            end_time is not None
            and event.start_time > end_time
        ):
            continue

        retrieved.append(event)

    return retrieved


def reduce_events(events, k=30):
    by_type = defaultdict(list)

    for event in events:
        by_type[event.type].append(event)

    type_weight = {
        event_type: sum(
            event.strength for event in group
        )
        for event_type, group in by_type.items()
    }

    total_weight = sum(type_weight.values())

    reduced = []

    for event_type, group in by_type.items():
        share = max(
            1,
            int(k * type_weight[event_type] / total_weight)
        )

        group_sorted = sorted(
            group,
            key=lambda event: event.strength,
            reverse=True
        )

        reduced.extend(group_sorted[:share])

    return sorted(
        reduced,
        key=lambda event: event.strength,
        reverse=True
    )[:k]
