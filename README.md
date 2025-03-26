 (Due to technical issues, the search service is temporarily unavailable.)

# **Qdrant Docker Test Instructions**  
**A simple guide to verify Qdrant is working correctly using Docker**  

---

## **Prerequisites**  
✅ **Docker** must be installed:  
- [Download Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows/Mac)  
- Linux: Install via package manager (e.g., `sudo apt install docker.io`)  

Verify Docker works:  
```bash
docker --version
# Should show Docker version (e.g., "Docker version 24.0.6")
```

---

## **Step 1: Run Qdrant in Docker**  
Execute this command in a terminal:  
```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```
**What this does:**  
- Starts Qdrant with HTTP API on port **6333** and gRPC on **6334**  
- Creates a local `qdrant_storage` folder to persist data  

---

## **Step 2: Verify Qdrant is Running**  
### **Check Docker Container**  
Open a **new terminal** and run:  
```bash
docker ps
```
✅ **Expected Output:**  
```
CONTAINER ID   IMAGE          COMMAND      STATUS       PORTS                                       NAMES
abc123def456   qdrant/qdrant  "./qdrant"   Up 5 mins    0.0.0.0:6333-6334->6333-6334/tcp   qdrant
```

### **Test the HTTP API**  
```bash
curl http://localhost:6333
```
✅ **Expected Response:**  
```json
{"title":"qdrant - vector search engine","version":"1.x.x"}
```

---

## **Step 3: Test with Python (Optional but Recommended)**  
### **1. Install Required Packages**  
```bash
pip install qdrant-client numpy
```

### **2. Run the Test Script**  
Save the following as `test_qdrant.py`:  

```python
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
    points=[{"id": idx, "vector": vec} for idx, vec in enumerate(vectors)]
)

# Search test
query_vector = np.random.rand(4).tolist()
results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3
)

print("🔍 Search Results:")
for result in results:
    print(f"- ID: {result.id}, Score: {result.score:.4f}")

# Cleanup
client.delete_collection(collection_name)
print("\n✅ Qdrant is working correctly!")
```

Run it:  
```bash
python test_qdrant.py
```

✅ **Expected Output:**  
```
🔍 Search Results:
- ID: 3, Score: 0.7821
- ID: 7, Score: 0.7565
- ID: 1, Score: 0.7324

✅ Qdrant is working correctly!
```

---

## **Troubleshooting**  
| Issue | Solution |
|-------|----------|
| **Port 6333 in use** | Change host port: `-p 6335:6333` |
| **Docker permission denied** | Run: `sudo usermod -aG docker $USER` (Linux) |
| **`curl` fails** | Check if Qdrant is running (`docker ps`) |
| **Python script fails** | Ensure `qdrant-client` is installed (`pip install qdrant-client numpy`) |

---

## **Next Steps**  
- Explore the **Qdrant Web UI**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)  
- Try loading real-world datasets  
- Experiment with different vector dimensions  

---

**🎉 Success!** Qdrant is now correctly set up and verified.  
Let me know if you encounter any issues! 🚀
