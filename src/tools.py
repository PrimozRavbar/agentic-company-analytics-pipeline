
from pydantic import BaseModel
from smolagents import tool

from src.retrieval import EventStore


class RetrievalRequest(BaseModel):
    tickers: list[str] | None = None
    event_types: list[str] | None = None
    start_time: str | None = None
    end_time: str | None = None
    reason: str


class RetrievedEvent(BaseModel):
    type: str
    ticker: str
    start_time: str
    end_time: str
    strength: float
    features: dict
    summary: str


def retrieve_company_events(
    event_store: EventStore,
    request: RetrievalRequest,
) -> list[RetrievedEvent]:

    retrieved = event_store.retrieve(request)

    return [
        RetrievedEvent(
            type=e.type,
            ticker=e.ticker,
            start_time=str(e.start_time),
            end_time=str(e.end_time),
            strength=e.strength,
            features=e.features,
            summary=e.summary,
        )
        for e in retrieved
    ]


def build_retrieve_company_events_tool(event_store: EventStore):

    @tool
    def retrieve_company_events_tool(
        tickers: list[str] | None = None,
        event_types: list[str] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        reason: str = "",
    ) -> list[dict]:
        """Retrieve company events matching the requested criteria.

        Args:
            tickers: Stock tickers to retrieve events for.
            event_types: Types of events to retrieve.
            start_time: Earliest event date to include.
            end_time: Latest event date to include.
            reason: Explanation of why the retrieval is needed.
        """
        request = RetrievalRequest(
            tickers=tickers,
            event_types=event_types,
            start_time=start_time,
            end_time=end_time,
            reason=reason,
        )

        retrieved = retrieve_company_events(event_store, request)

        return [event.model_dump() for event in retrieved]

    return retrieve_company_events_tool
