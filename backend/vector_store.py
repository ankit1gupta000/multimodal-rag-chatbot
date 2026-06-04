"""Simple in-memory vector store with JSON persistence"""
import json
import os
from typing import List, Dict, Any
import math


class VectorStore:
    """Simple vector store for embeddings with cosine similarity search"""
    
    def __init__(self, store_file: str = "vectors.json"):
        self.store_file = store_file
        self.vectors: Dict[str, Dict[str, Any]] = {}
        self.load()
    
    def load(self):
        """Load vectors from file if it exists"""
        if os.path.exists(self.store_file):
            try:
                with open(self.store_file, 'r') as f:
                    self.vectors = json.load(f)
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vectors = {}
    
    def save(self):
        """Save vectors to file"""
        try:
            with open(self.store_file, 'w') as f:
                json.dump(self.vectors, f)
        except Exception as e:
            print(f"Error saving vector store: {e}")
    
    def upsert(self, vector_id: str, embedding: List[float], text: str, doc_type: str = "document"):
        """Store or update a vector"""
        self.vectors[vector_id] = {
            "embedding": embedding,
            "text": text,
            "type": doc_type
        }
        self.save()
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors using cosine similarity"""
        if not self.vectors:
            return []
        
        # Calculate cosine similarity
        results = []
        for vec_id, vec_data in self.vectors.items():
            similarity = self._cosine_similarity(query_embedding, vec_data["embedding"])
            results.append({
                "id": vec_id,
                "score": similarity,
                "metadata": {
                    "text": vec_data["text"],
                    "type": vec_data["type"]
                }
            })
        
        # Sort by similarity and return top-k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def clear(self):
        """Clear all vectors"""
        self.vectors = {}
        self.save()


# Global instance
vector_store = VectorStore()


def store_vector(vector_id: str, embedding: List[float], text: str, doc_type: str = "document"):
    """Store a vector in the global store"""
    vector_store.upsert(vector_id, embedding, text, doc_type)


def search_vector(embedding: List[float], top_k: int = 5):
    """Search the global vector store"""
    results = vector_store.search(embedding, top_k)
    
    # Return in a format compatible with the old Pinecone interface
    class SearchResults:
        def __init__(self, matches):
            self.matches = matches
    
    # Convert to match objects
    matches = []
    for result in results:
        class Match:
            def __init__(self, metadata):
                self.metadata = metadata
        
        matches.append(Match(result["metadata"]))
    
    return SearchResults(matches)
