from typing import Literal, TypedDict

class AgentState(TypedDict, total=False):
    query: str
    session_id: str
    route: Literal["retrieve", "direct"]
    context: str
    sources: list
    answer: str
