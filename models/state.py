from typing import TypedDict, List

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


class ResearchState(TypedDict):
    topic: str
    research_goal: str
    research_questions: List[str]
    search_queries: List[str]
    search_results: list
    documents: List[Document]
    retrieved_documents: List[Document]
    findings: List[Finding]
    report: str