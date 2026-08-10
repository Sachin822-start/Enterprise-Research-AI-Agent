import streamlit as st
from graphs.research_graph import graph
from services.topic_service import (find_similar_topic,store_topic)
from agents.retriever_agent import retriever_node
from agents.intelligence_agent import intelligence_node

st.set_page_config(
    page_title="Enterprise AI Research Agent",
    page_icon="",
    layout="wide"
)
st.title("Enterprise AI Research Agent")
st.markdown(
"""
Reusable Enterprise Research Knowledge Base
Built with
- LangGraph
- Ollama
- ChromaDB
- Tavily
- Sentence Transformers
"""
)

topic = st.text_input(
    "Enter Research Topic"
)

if st.button("Start Research"):
    if topic == "":
        st.warning("Please enter a topic.")
        st.stop()
    progress = st.progress(0)
    status = st.empty()

    # -------------------------------------------------------
    status.write("Checking existing research...")
    progress.progress(10)
    similar = find_similar_topic(topic)

    # -------------------------------------------------------

    if similar:
        st.success(
            f"Found Similar Topic ({similar['score']:.2f})"
        )
        state = {
            "topic": similar["topic"],
            "research_goal": similar["topic"],
            "research_questions": [],
            "search_queries": [],
            "search_results": [],
            "documents": [],
            "retrieved_documents": [],
            "findings": [],
            "report": ""
        }
        status.write("Retrieving Knowledge Base...")
        progress.progress(40)
        state = retriever_node(state)
        progress.progress(70)
        status.write("Generating Executive Report...")
        state = intelligence_node(state)
        progress.progress(100)
        result = state
    else:
        status.write("Running Research Pipeline...")
        progress.progress(20)
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
        progress.progress(100)
    status.empty()
    st.success("Research Completed")
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Questions",
        len(result["research_questions"])
    )
    col2.metric(
        "Documents",
        len(result["retrieved_documents"])
    )
    col3.metric(
        "Search Queries",
        len(result["search_queries"])
    )
    st.divider()
    st.subheader("Executive Report")
    st.markdown(result["report"])
    st.divider()
    with st.expander("Research Questions"):
        for q in result["research_questions"]:
            st.write("•", q)
    with st.expander("Search Queries"):
        for q in result["search_queries"]:
            st.write("•", q)

    with st.expander("Knowledge Base Documents"):
        for doc in result["retrieved_documents"]:
            st.markdown(f"### {doc['title']}")
            st.write(doc["url"])
            st.write(doc["text"][:500] + "...")
            st.divider()