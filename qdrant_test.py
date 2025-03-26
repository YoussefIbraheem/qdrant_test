from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import numpy as np

# Initialize client
client = QdrantClient(host="localhost", port=6333)

# Create a test collection
collection_name = "test_collection"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4, distance=Distance.COSINE)
)

# Insert test vectors
vectors = np.random.rand(10, 4).tolist()  # 10 random 4D vectors
client.upsert(
    collection_name=collection_name,
    points=[
        {"id": idx, "vector": vector}
        for idx, vector in enumerate(vectors)
    ]
)

# Perform a search
query_vector = np.random.rand(4).tolist()
results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3
)

print("🔍 Search Results:")
for result in results:
    print(f"- ID: {result.id}, Score: {result.score:.4f}")

# Clean up
client.delete_collection(collection_name)
print("\n✅ Qdrant is working correctly!")