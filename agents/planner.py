from langchain_ollama import ChatOllama
from models.state import ResearchState
import json

llm = ChatOllama(
    model="llama3.2:1b",   # change to 1b if you don't have 3b
    temperature=0
)

def planner_node(state: ResearchState):
    print("\n" + "=" * 60)
    print("PLANNER AGENT")
    print("=" * 60)

    topic = state["topic"]
    prompt = f"""
You are an Enterprise Research Planner.
Given the research topic below:
{topic}

Generate:
1. A concise research goal.
2. Exactly 3 research questions.
3. Exactly 3 optimized web search queries.

Return ONLY valid JSON.

Example:
{{
    "research_goal":"Understand how AI is transforming retail.",

    "research_questions":[
        "Question 1",
        "Question 2",
        "Question 3"
    ],

    "search_queries":[
        "Search Query 1",
        "Search Query 2",
        "Search Query 3"
    ]
}}
Return JSON only.
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Remove markdown if model returns it
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()
    data = json.loads(content)
    state["research_goal"] = data["research_goal"]
    state["research_questions"] = data["research_questions"]
    state["search_queries"] = data["search_queries"]
    print("\nResearch Goal")
    print("-" * 60)
    print(state["research_goal"])
    print("\nResearch Questions")
    print("-" * 60)
    for q in state["research_questions"]:
        print("•", q)
    print("\nSearch Queries")
    print("-" * 60)
    for q in state["search_queries"]:
        print("•", q)

    return state