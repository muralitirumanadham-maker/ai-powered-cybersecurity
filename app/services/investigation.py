from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.services.llm import gemini_summary


class InvestigationState(TypedDict, total=False):
    result: dict
    summary: str
    investigation_status: str


def build_graph():
    def summarize(state: InvestigationState):
        return {
            "summary": gemini_summary(state["result"]),
            "investigation_status": "completed",
        }

    graph = StateGraph(InvestigationState)
    graph.add_node("summarize", summarize)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", END)
    return graph.compile()


GRAPH = build_graph()


def investigate(result: dict):
    output = GRAPH.invoke({"result": result})
    return output["summary"]
