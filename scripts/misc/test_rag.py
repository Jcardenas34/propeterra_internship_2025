import chromadb
import numpy as np
from chromadb.config import Settings
from sklearn.metrics.pairwise import cosine_similarity
from propeterra_internship_2025.utils.helpers import timing_function


# Load Chroma DB
chroma_client = chromadb.Client(Settings(
    persist_directory="/Users/chiral/git_projects/dissertation_RAG/chroma_db/",  # where chroma.sqlite3 lives
    anonymized_telemetry=False
))

# List collections
print("Collections:", chroma_client.list_collections())

# Load a specific collection
# collection = chroma_client.get_collection(name="your_collection_name")

# # Fetch all
# results = collection.get(include=["embeddings", "documents"])

# # Embed a query (example with OpenAI, but needs actual embedding):
# from openai import OpenAIEmbeddings
# query = "How do pets behave indoors?"
# query_embedding = OpenAIEmbeddings().embed_query(query)  # or use your own method

# # Similarity
# embedding_matrix = np.array(results["embeddings"])
# scores = cosine_similarity([query_embedding], embedding_matrix)[0]
# top_k_idx = np.argsort(scores)[-5:][::-1]

# for i in top_k_idx:
#     print(f"{results['documents'][i]} (Score: {scores[i]:.4f})")
