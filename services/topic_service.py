import json
import os
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer

TOPIC_DB = "data/research_topics.json"
os.makedirs("data", exist_ok=True)

if not os.path.exists(TOPIC_DB):
    with open(TOPIC_DB, "w") as f:
        json.dump([], f)

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_topics():
    if not os.path.exists(TOPIC_DB):
        return []
    try:
        with open(TOPIC_DB, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []

def save_topics(data):
    with open(TOPIC_DB, "w") as f:
        json.dump(data, f, indent=4)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def store_topic(topic):
    topics = load_topics()
    embedding = model.encode(topic).tolist()
    topics.append({
        "id": str(uuid.uuid4()),
        "topic": topic,
        "embedding": embedding
    })

    save_topics(topics)

def find_similar_topic(topic,threshold=0.80):
    topics = load_topics()
    if len(topics) == 0:
        return None
    query = model.encode(topic)
    best = None
    best_score = 0
    for item in topics:
        score = cosine_similarity(
            query,
            item["embedding"]
        )

        if score > best_score:
            best_score = score
            best = item

    if best_score >= threshold:
        return {
            "topic": best["topic"],
            "score": float(best_score)

        }
    return None

def list_topics():
    return load_topics()