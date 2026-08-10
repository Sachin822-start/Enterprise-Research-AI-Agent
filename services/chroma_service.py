import chromadb
from chromadb.utils import embedding_functions

# Chroma Client

client = chromadb.PersistentClient(
    path="knowledge_base"
)

embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="research_documents",
    embedding_function=embedding_model
)

# Store Document
def store_document(document):
    url = document["url"]

    if document_exists(url):
        return

    collection.add(
        ids=[url],
        documents=[document["text"]],
        metadatas=[
            {
                "title": document["title"],
                "url": document["url"],
                "source": document["url"].split("/")[2],
                "topic": document["topic"]
            }
        ]
    )

# Retrieve
def retrieve_documents(query, top_k=10):

    result = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = []

    if len(result["documents"]) == 0:
        return documents

    docs = result["documents"][0]
    metas = result["metadatas"][0]

    for doc, meta in zip(docs, metas):
        documents.append(
            {
                "title": meta["title"],
                "url": meta["url"],
                "source": meta["source"],
                "topic": meta["topic"],
                "text": doc
            }
        )

    return documents
# Exists
def document_exists(url):
    result = collection.get(
        ids=[url]
    )
    return len(result["ids"]) > 0

# Delete
def delete_documents():
    global collection
    client.delete_collection(
        "research_documents"
    )
    collection = client.get_or_create_collection(
        name="research_documents",
        embedding_function=embedding_model
    )