from graphs.research_graph import graph
from services.topic_service import (find_similar_topic,store_topic)
from agents.retriever_agent import retriever_node
from agents.intelligence_agent import intelligence_node


def run_existing_research(topic):
    print("\n" + "=" * 70)
    print("SIMILAR RESEARCH FOUND")
    print("=" * 70)

    state = {
        "topic": topic,
        "research_goal": topic,
        "research_questions": [],
        "search_queries": [],
        "search_results": [],
        "documents": [],
        "retrieved_documents": [],
        "findings": [],
        "report": ""
    }
    state = retriever_node(state)
    state = intelligence_node(state)
    return state

topic = input("\nResearch Topic : ").strip()
similar = find_similar_topic(topic)

if similar:
    print(f"\nMatched Topic : {similar['topic']}")
    print(f"Similarity    : {similar['score']:.3f}")
    result = run_existing_research(
        similar["topic"]
    )
else:
    print("\nNew Research Topic\n")
    result = graph.invoke(
        {
            "topic": topic,
            "research_goal": "",
            "research_questions": [],
            "search_queries": [],
            "search_results": [],
            "documents": [],
            "retrieved_documents": [],
            "findings": [],
            "report": ""
        }
    )
    store_topic(topic)

print("\n")
print("=" * 90)
print("ENTERPRISE AI RESEARCH REPORT")
print("=" * 90)
print(result["report"])
print("\n")
print("=" * 90)
print("PIPELINE SUMMARY")
print("=" * 90)
print(f"Topic                 : {result['topic']}")
print(f"Research Questions    : {len(result['research_questions'])}")
print(f"Search Queries        : {len(result['search_queries'])}")
print(f"Documents Scraped     : {len(result['documents'])}")
print(f"Knowledge Retrieved   : {len(result['retrieved_documents'])}")
print("\nCompleted Successfully.")