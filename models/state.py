from typing import TypedDict, List, Dict, Any


class SearchQuery(TypedDict):
    query: str


class Document(TypedDict):
    title: str
    url: str
    text: str
    topic: str


class Finding(TypedDict):
    finding: str
    source: str
    classification: str
    confidence: str
    evidence: List[Dict[str, str]]


class Contradiction(TypedDict):
    contradiction_id: str
    claim: str
    source_a: Dict[str, str]
    source_b: Dict[str, str]
    resolution: str


class ResearchState(TypedDict):
    topic: str
    research_goal: str
    research_questions: List[str]
    search_queries: List[str]
    search_results: list
    documents: List[Document]
    retrieved_documents: List[Document]
    findings: List[Finding]
    contradictions: List[Contradiction]
    evidence_analysis: Dict[str, Any]
    report: str