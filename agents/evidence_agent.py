import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

load_dotenv()


# ============================================================
# Configuration
# ============================================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


# ============================================================
# Structured Output Models
# ============================================================

class EvidenceItem(BaseModel):
    title: str = Field(
        description="Title of the source supporting the finding."
    )

    url: str = Field(
        description="URL of the source."
    )

    support: str = Field(
        description="Short explanation of how the source supports the finding."
    )


class FindingOutput(BaseModel):
    finding: str = Field(
        description="A factual finding directly supported by the provided sources."
    )

    classification: str = Field(
        description="Must be positive, negative, neutral, or mixed."
    )

    confidence: str = Field(
        description="Must be high, medium, or low."
    )

    evidence: List[EvidenceItem] = Field(
        description="Sources that directly support this finding."
    )


class ComparisonOutput(BaseModel):
    topic: str = Field(
        description="Topic or issue being compared across sources."
    )

    comparison: str = Field(
        description="How the sources agree, differ, or provide complementary evidence."
    )


class ContradictionOutput(BaseModel):
    claim: str = Field(
        description="The claim for which sources disagree."
    )

    source_a: str = Field(
        description="First source involved in the disagreement."
    )

    source_b: str = Field(
        description="Second source involved in the disagreement."
    )

    explanation: str = Field(
        description="Explanation of how the two sources differ."
    )


class EvidenceAnalysisOutput(BaseModel):

    findings: List[FindingOutput] = Field(
        default_factory=list
    )

    comparisons: List[ComparisonOutput] = Field(
        default_factory=list
    )

    contradictions: List[ContradictionOutput] = Field(
        default_factory=list
    )


# ============================================================
# LLM
# ============================================================

base_llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0
)


# IMPORTANT:
# Use Ollama's JSON Schema structured output.
structured_llm = base_llm.with_structured_output(
    EvidenceAnalysisOutput,
    method="json_schema"
)


# ============================================================
# Evidence Analysis Node
# ============================================================

def evidence_analysis_node(state):

    print("\n" + "=" * 70)
    print("EVIDENCE ANALYSIS AGENT")
    print("=" * 70)

    documents = state.get(
        "retrieved_documents",
        []
    )

    if not documents:

        print(
            "\nNo retrieved documents available."
        )

        state["findings"] = []
        state["contradictions"] = []
        state["evidence_analysis"] = {}

        return state

    print(
        f"\nAnalyzing {len(documents)} retrieved documents..."
    )

    # ========================================================
    # Prepare Evidence
    # ========================================================

    evidence_context = ""

    # Analyze only the most relevant 5 documents.
    # This keeps the context manageable for the local 3B model.
    documents_to_analyze = documents[:5]

    for index, document in enumerate(
        documents_to_analyze,
        start=1
    ):

        evidence_context += f"""

SOURCE {index}

Title:
{document.get("title", "")}

URL:
{document.get("url", "")}

Content:
{document.get("text", "")[:2500]}

==================================================
"""

    # ========================================================
    # Prompt
    # ========================================================

    prompt = f"""
You are an Enterprise Research Evidence Analyst.

Research Topic:
{state["research_goal"]}

Analyze ONLY the sources provided below.

Your responsibilities are:

1. Extract important factual findings.
2. Compare evidence between sources.
3. Classify findings.
4. Detect genuine contradictions.

IMPORTANT GROUNDING RULES:

- Use ONLY information present in the supplied sources.
- Do NOT use your own background knowledge.
- Do NOT invent facts.
- Do NOT invent companies, products, statistics, studies,
  URLs, or examples.
- Every finding must be supported by at least one supplied source.
- Every finding must include its source URL.
- If the sources do not provide enough evidence, do not create
  the finding.
- Different wording does NOT automatically mean contradiction.
- Only report a contradiction when two sources make materially
  different claims about the same issue.

Classification values:

positive
negative
neutral
mixed

Confidence values:

high
medium
low

The final structured response must contain:

- findings
- comparisons
- contradictions

Research Evidence:

{evidence_context}
"""

    # ========================================================
    # Call Structured LLM
    # ========================================================

    try:

        print(
            "\nRunning structured evidence analysis..."
        )

        result = structured_llm.invoke(
            prompt
        )

        print(
            "\nStructured evidence analysis received."
        )

        # ====================================================
        # Convert Pydantic result
        # ====================================================

        findings = []

        for finding in result.findings:

            findings.append(
                {
                    "finding": finding.finding,
                    "source": (
                        finding.evidence[0].title
                        if finding.evidence
                        else ""
                    ),
                    "classification": finding.classification,
                    "confidence": finding.confidence,
                    "evidence": [
                        evidence.model_dump()
                        for evidence in finding.evidence
                    ]
                }
            )

        contradictions = []

        for contradiction in result.contradictions:

            contradictions.append(
                {
                    "contradiction_id": (
                        f"C{len(contradictions) + 1}"
                    ),
                    "claim": contradiction.claim,

                    "source_a": {
                        "title": contradiction.source_a,
                        "url": ""
                    },

                    "source_b": {
                        "title": contradiction.source_b,
                        "url": ""
                    },

                    "resolution": (
                        contradiction.explanation
                    )
                }
            )

        comparisons = [
            comparison.model_dump()
            for comparison in result.comparisons
        ]

        # ====================================================
        # Save into LangGraph State
        # ====================================================

        state["findings"] = findings

        state["contradictions"] = contradictions

        state["evidence_analysis"] = {
            "findings": findings,
            "comparisons": comparisons,
            "contradictions": contradictions
        }

    except Exception as error:

        print(
            "\nEvidence analysis failed:"
        )

        print(
            repr(error)
        )

        state["findings"] = []

        state["contradictions"] = []

        state["evidence_analysis"] = {}

        return state

    # ========================================================
    # Results
    # ========================================================

    print(
        f"\nFindings extracted: "
        f"{len(findings)}"
    )

    print(
        f"Evidence comparisons: "
        f"{len(comparisons)}"
    )

    print(
        f"Contradictions detected: "
        f"{len(contradictions)}"
    )

    print(
        "\nEvidence analysis completed."
    )

    return state