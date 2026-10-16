import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_RESUMES_DIR = PROJECT_ROOT / "knowledge" / "resumes"
CONFIG_FILE = PROJECT_ROOT / "data" / "knowledge_base_config.json"

class CandidateKnowledgeBase:
    """
    Candidate Document Knowledge Base using OpenAI Vector Stores and File Search.

    Manages indexing and semantic search over supporting candidate documents
    (such as historical resume PDF variants).
    """

    def __init__(
        self,
        vector_store_id: Optional[str] = None,
        resumes_dir: Path = DEFAULT_RESUMES_DIR,
        config_path: Path = CONFIG_FILE,
    ):
        self.client = OpenAI()
        self.resumes_dir = resumes_dir
        self.config_path = config_path
        self.vector_store_id = vector_store_id or self._load_vector_store_id()

    def _load_vector_store_id(self) -> Optional[str]:
        """Load vector store ID from environment variable or local config file."""
        env_vs_id = os.getenv("CANDIDATE_VECTOR_STORE_ID")
        if env_vs_id:
            return env_vs_id

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("vector_store_id")
            except Exception:
                return None
        return None

    def _save_vector_store_id(self, vector_store_id: str) -> None:
        """Persist vector store ID to local configuration file."""
        self.vector_store_id = vector_store_id
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump({"vector_store_id": vector_store_id}, f, indent=2)

    def create_candidate_vector_store(self, name: str = "Candidate Resumes Knowledge Base") -> str:
        """Create a new OpenAI vector store."""
        vector_store = self.client.vector_stores.create(name=name)
        self._save_vector_store_id(vector_store.id)
        return vector_store.id

    def index_candidate_documents(self) -> Dict[str, Any]:
        """
        One-time / batch indexing operation:
        Uploads resume PDFs to OpenAI and attaches them to the vector store.
        """
        if not self.resumes_dir.exists():
            raise FileNotFoundError(f"Resumes directory not found: {self.resumes_dir}")

        pdf_files = list(self.resumes_dir.glob("*.pdf"))
        if not pdf_files:
            return {
                "status": "error",
                "message": f"No PDF files found in {self.resumes_dir}",
                "indexed_files": [],
            }

        # Ensure vector store exists
        if not self.vector_store_id:
            self.create_candidate_vector_store()

        file_streams = []
        try:
            for pdf_path in pdf_files:
                file_streams.append(open(pdf_path, "rb"))

            # Upload batch to vector store and poll until indexing completes
            # Use small chunks so search returns focused resume sections
            # rather than entire documents
            file_batch = self.client.vector_stores.file_batches.upload_and_poll(
                vector_store_id=self.vector_store_id,
                files=file_streams,
                chunking_strategy={
                    "type": "static",
                    "static": {
                        "max_chunk_size_tokens": 200,
                        "chunk_overlap_tokens": 50,
                    },
                },
            )

            indexed_names = [p.name for p in pdf_files]
            return {
                "status": file_batch.status,
                "vector_store_id": self.vector_store_id,
                "file_counts": {
                    "total": file_batch.file_counts.total,
                    "completed": file_batch.file_counts.completed,
                    "failed": file_batch.file_counts.failed,
                },
                "indexed_files": indexed_names,
            }
        finally:
            for stream in file_streams:
                stream.close()

    def search_candidate_documents(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search the candidate vector store semantically using OpenAI File Search.

        Preserves provenance (file name and document metadata) from the OpenAI API response.
        Returns the actual content indexed without manual text normalization.
        """
        if not self.vector_store_id:
            return [
                {
                    "error": "Vector store not configured. Please index candidate documents first or set CANDIDATE_VECTOR_STORE_ID."
                }
            ]

        try:
            response = self.client.vector_stores.search(
                vector_store_id=self.vector_store_id,
                query=query,
                max_num_results=max_results,
            )

            results = []
            for item in getattr(response, "data", []):
                filename = getattr(item, "filename", "Unknown Document")
                # Extract text content from chunks preserving original source text
                chunks = getattr(item, "content", [])
                text_parts = []
                for chunk in chunks:
                    chunk_text = getattr(chunk, "text", "")
                    if chunk_text:
                        text_parts.append(chunk_text)

                combined_text = "\n".join(text_parts) if text_parts else str(getattr(item, "text", ""))

                results.append({
                    "file_name": filename,
                    "score": getattr(item, "score", None),
                    "text": combined_text,
                })

            if not results:
                return [
                    {
                        "message": f"No relevant content found in candidate documents for query: '{query}'",
                        "query": query,
                    }
                ]

            return results
        except Exception as e:
            return [
                {
                    "error": f"Error performing semantic search: {str(e)}",
                    "vector_store_id": self.vector_store_id,
                }
            ]
