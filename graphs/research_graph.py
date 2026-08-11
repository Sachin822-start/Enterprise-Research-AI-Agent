from langgraph.graph import StateGraph, END
from models.state import ResearchState
from agents.planner import planner_node
from agents.search_agent import search_node
from agents.scraper_agent import scraper_node
from agents.retriever_agent import retriever_node
from agents.evidence_agent import evidence_analysis_node
from agents.intelligence_agent import intelligence_node


builder = StateGraph(ResearchState)

# Nodes
builder.add_node("planner",planner_node)
builder.add_node("search",search_node)
builder.add_node("scraper",scraper_node)
builder.add_node("retriever",retriever_node)
builder.add_node("evidence_analysis",evidence_analysis_node)
builder.add_node("intelligence",intelligence_node)

# Entry Point
builder.set_entry_point("planner")

# Workflow
builder.add_edge("planner","search")
builder.add_edge("search","scraper")
builder.add_edge("scraper","retriever")
builder.add_edge("retriever","evidence_analysis")
builder.add_edge("evidence_analysis","intelligence")
builder.add_edge("intelligence",END)

# Compile Graph
graph = builder.compile()