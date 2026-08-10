from models.state import ResearchState
from services.chroma_service import retrieve_documents


def retriever_node(state: ResearchState):
    print("\n" + "=" * 60)
    print("RETRIEVER AGENT")
    print("=" * 60)
    print("\nSearching Enterprise Knowledge Base...")
    docs = retrieve_documents(
        query=state["research_goal"],
        top_k=10
    )
    state["retrieved_documents"] = docs
    print(f"\nRetrieved {len(docs)} relevant documents.\n")

    for i, doc in enumerate(docs, start=1):
        print(f"{i}.{doc['title']}")
        print(f"{doc['url']}")
    return state