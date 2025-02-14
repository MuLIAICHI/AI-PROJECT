from typing import Dict, Any, List
from pathlib import Path
# Create a wrapper class to make APSW compatible with sqlite3 interface
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb
from chromadb.config import Settings


class VectorStore:
    """Manages embeddings and similarity search for SEO data."""

    def __init__(self):
        """Initialize the ChromaDB vector store with persistence."""
        # Define persistence directory
        persist_dir = Path(__file__).parent.parent.parent / 'knowledge' / 'embeddings'
        persist_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

        # Initialize ChromaDB with correct settings
        try:
            self.client = chromadb.PersistentClient(path=str(persist_dir))
            self.collection = self.client.get_or_create_collection("seo_embeddings")
            print("✅ VectorStore Initialized Successfully")
        except Exception as e:
            print(f"❌ Error initializing ChromaDB: {e}")
            self.collection = None  # Prevent operations on a failed initialization

    def add_embeddings(self, data: Dict[str, Any], category: str):
        """Add new embeddings to the store."""
        if not self.collection:
            print("⚠️ ChromaDB collection not initialized!")
            return

        documents = self._prepare_documents(data)
        if not documents:
            print("⚠️ No valid documents to store in embeddings!")
            return

        metadatas = [{"category": category} for _ in documents]
        ids = [f"{category}_{i}" for i in range(len(documents))]

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Successfully added {len(documents)} embeddings to ChromaDB")
        except Exception as e:
            print(f"❌ Error adding embeddings: {e}")

    def find_similar(self, query_data: Dict[str, Any], n_results: int = 5) -> List[Dict[str, Any]]:
        """Find similar cases based on query data."""
        if not self.collection:
            print("⚠️ ChromaDB collection not initialized!")
            return []

        query = self._prepare_query(query_data)
        if not query:
            print("⚠️ Query data is empty, cannot find similar cases!")
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return self._process_results(results)
        except Exception as e:
            print(f"❌ Error querying embeddings: {e}")
            return []

    def _prepare_documents(self, data: Dict[str, Any]) -> List[str]:
        """Convert data dictionary into a list of string documents for embedding."""
        documents = []
        for key, value in data.items():
            if isinstance(value, dict):
                documents.extend(self._prepare_documents(value))
            elif isinstance(value, (str, int, float)):
                documents.append(f"{key}: {value}")
        return documents

    def _prepare_query(self, data: Dict[str, Any]) -> str:
        """Convert query dictionary into a formatted query string."""
        query_parts = []
        for key, value in data.items():
            if isinstance(value, dict):
                query_parts.extend(self._prepare_query(value).split('\n'))
            elif isinstance(value, (str, int, float)):
                query_parts.append(f"{key}: {value}")
        return '\n'.join(query_parts)

    def _process_results(self, results: Dict) -> List[Dict[str, Any]]:
        """Process and format similarity search results."""
        if not results or not results.get('documents', []):
            print("⚠️ No results found in ChromaDB")
            return []

        processed_results = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            processed_results.append({
                'content': doc,
                'category': metadata.get('category', 'Unknown'),
                'similarity_score': round(1 - distance, 3),  # Convert distance to similarity score
                'rank': i + 1
            })

        print(f"🔍 Found {len(processed_results)} similar cases.")
        return processed_results
