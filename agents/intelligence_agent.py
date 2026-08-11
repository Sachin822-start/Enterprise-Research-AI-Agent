import json

from langchain_ollama import ChatOllama
from models.state import ResearchState


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


def intelligence_node(state: ResearchState):

    print("\n" + "=" * 60)
    print("ENTERPRISE INTELLIGENCE AGENT")
    print("=" * 60)

    # --------------------------------------------------
    # Get structured evidence analysis
    # --------------------------------------------------

    findings = state.get(
        "findings",
        []
    )

    evidence_analysis = state.get(
        "evidence_analysis",
        {}
    )

    comparisons = evidence_analysis.get(
        "comparisons",
        []
    )

    contradictions = state.get(
        "contradictions",
        []
    )

    # --------------------------------------------------
    # Convert structured data to readable JSON
    # --------------------------------------------------

    findings_context = json.dumps(
        findings,
        indent=2
    )

    comparisons_context = json.dumps(
        comparisons,
        indent=2
    )

    contradictions_context = json.dumps(
        contradictions,
        indent=2
    )

    # --------------------------------------------------
    # Enterprise Intelligence Prompt
    # --------------------------------------------------

    prompt = f"""
You are an Enterprise AI Research Analyst.

Research Topic:
{state["topic"]}

Research Goal:
{state["research_goal"]}

You must generate an enterprise research report using
ONLY the structured evidence provided below.

Do NOT use your own external knowledge.

Do NOT invent facts.

Do NOT create sources that are not provided.

Every important finding must remain traceable to its
supporting source.

If sources disagree, explicitly mention the disagreement.

==================================================
STRUCTURED FINDINGS
==================================================

{findings_context}


==================================================
EVIDENCE COMPARISONS
==================================================

{comparisons_context}


==================================================
CONTRADICTIONS DETECTED
==================================================

{contradictions_context}


==================================================
REPORT FORMAT
==================================================

Return the report using exactly these headings:

# Executive Summary

Provide a concise summary of the research.

# Key Findings

Present the major findings.

For each important finding include:

- Finding
- Classification
- Confidence
- Supporting Source

# Evidence Comparison

Compare evidence across sources.

Mention areas where sources agree.

Mention areas where sources differ.

# Contradictions

If contradictions were detected, explain:

- The claim
- Source A
- Source B
- The difference
- Any available resolution/context

If there are no contradictions, state:

"No significant contradictions were identified
in the retrieved evidence."

# Business Challenges

Describe business challenges supported by
the retrieved evidence.

# Recommendations

Provide recommendations based ONLY on the
identified findings and evidence.

# Final Conclusion

Provide a concise conclusion based ONLY on
the analyzed evidence.

# References

List the source title and URL for every source
used in the findings.

IMPORTANT:

- Do not invent information.
- Do not introduce unsupported claims.
- Do not hide contradictory evidence.
- Maintain source traceability.
- Keep the report professional and enterprise-oriented.

Return only the report text.
"""

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    print(
        "Generating Executive Report..."
    )

    try:

        response = llm.invoke(
            prompt
        )

        state["report"] = response.content

        print(
            "Report Generated Successfully."
        )

    except Exception as error:

        print(
            f"Report generation failed: {error}"
        )

        state["report"] = (
            "Unable to generate the research report."
        )

    return state