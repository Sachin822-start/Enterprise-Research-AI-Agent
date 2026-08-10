from langchain_ollama import ChatOllama
from models.state import ResearchState

llm = ChatOllama(
    model="llama3.2:1b",   # use 1b if that's what you have
    temperature=0
)


def intelligence_node(state: ResearchState):
    print("\n" + "=" * 60)
    print("ENTERPRISE INTELLIGENCE AGENT")
    print("=" * 60)
    context = ""
    for i, doc in enumerate(state["retrieved_documents"], start=1):
        context += f"""
Document {i}
Title:
{doc['title']}
Source:
{doc['url']}
Content:
{doc['text'][:4000]}
"""

    prompt = f"""
You are an Enterprise AI Research Analyst.
Research Topic:
{state["topic"]}
Research Goal:
{state["research_goal"]}
Using ONLY the supplied evidence, generate a professional enterprise report.
Return the report using exactly these headings.
# Executive Summary
# Key Findings
# Evidence Comparison
Mention agreements and contradictions between sources.
# Business Challenges
# Recommendations
# References
List every source URL.
# Final Conclusion
Do not invent facts.
Return only plain text.
"""
    print("Generating Executive Report...")
    response = llm.invoke(
        prompt + "\n\nEvidence:\n" + context
    )
    state["report"] = response.content
    print("Report Generated Successfully.\n")
    return state