# Candidate Document Knowledge Base & Semantic RAG Layer

## 1. Overview & Architecture

The AI Job Application Agent cleanly separates authoritative candidate facts from supporting source-document context:

```text
Candidate Profile                                Candidate Documents
       │                                                 │
       ▼                                                 ▼
 data/candidate.json                        knowledge/resumes/*.pdf
       │                                                 │
       ▼                                                 ▼
Authoritative Structured Facts                      OpenAI Vector Store
       │                                                 │
       ▼                                                 ▼
get_candidate_profile()                          OpenAI File Search
       │                                                 │
       │                                                 ▼
       │                                    search_candidate_knowledge()
       │                                                 │
       └────────────────────┬────────────────────────────┘
                            ▼
                         AI Agent
```

---

## 2. Source-of-Truth Boundary: `candidate.json` vs. Candidate RAG

| Dimension | Structured Profile (`data/candidate.json`) | Candidate RAG (`knowledge/resumes/`) |
| :--- | :--- | :--- |
| **Role** | **Authoritative Single Source of Truth** | **Supporting Source-Document Context** |
| **Data Scope** | Verified facts, identity, current role, education, target roles, allowed experience ranges, excluded domains | Historical resume wording, bullet point phrasing, technical highlights, project narratives |
| **Tool Exposed** | `get_candidate_profile()`, `get_candidate_name()` | `search_candidate_knowledge()`, `search_candidate_documents()` |
| **Storage / Backend** | Validated JSON / Pydantic schema | OpenAI Vector Store & File Search |
| **Precedence** | **Authoritative (Highest)** | **Supporting (Lower)** |

### Conflict Resolution Rule:
* `candidate.json` is the sole authoritative source for verified candidate information.
* If a retrieved resume passage contains conflicting phrasing, preliminary titles, or unverified claims, **`candidate.json` always wins**.
* Candidate RAG does **not** replace `candidate.json`.

---

## 3. The Three Resumes as Historical Variants

The resume files located in `knowledge/resumes/` are:
* `Apeksha_Morappanavar_Resume.pdf`
* `Apeksha_Morappanavar_Scoutit.pdf`
* `Apeksha_Morappanavar_UiPath.pdf`

### Key Principles:
1. **Same Candidate, Multiple Tailoring Angles**: These three PDFs are historical variants of the **same single candidate** with different positioning and emphasis (e.g., backend/full-stack focus vs. systems/C++ focus).
2. **Not Separate Profiles**: They must never be treated or merged into separate candidate identities.
3. **Phrasing Evidence**: They serve as a rich repository of previously tested resume phrasing, metric formulations, and technical bullet points for future resume tailoring.

---

## 4. Indexing vs. Retrieval Operations

The RAG layer explicitly decouples one-time indexing from regular runtime retrieval to avoid repeated file uploads.

### A. Indexing / Ingestion (One-Time / Periodic Setup)
Performed via `CandidateKnowledgeBase.index_candidate_documents()`:
1. Creates or connects to an OpenAI Vector Store (`create_candidate_vector_store`).
2. Uploads all PDF documents in `knowledge/resumes/` in a single batch.
3. Polls until vector store processing completes (`upload_and_poll`).
4. Persists the `vector_store_id` to `data/knowledge_base_config.json` or respects `CANDIDATE_VECTOR_STORE_ID`.

### B. Retrieval (Normal Agent Runtime)
Performed via `CandidateKnowledgeBase.search_candidate_documents()`:
1. Receives a natural language query from an agent or tool.
2. Reuses the existing vector store ID without uploading files.
3. Executes OpenAI File Search.
4. Returns structured results containing:
   - `file_name`: Name of the source document (preserving provenance).
   - `score`: Relevance score from the vector search.
   - `text`: Relevant text passage retrieved.

---

## 5. Provenance Preservation & Raw Content

The retrieval layer preserves the exact source document name and text returned by the OpenAI API:
* Enables the agent to identify which specific resume variant a bullet point or project description originated from.
* Content is retrieved directly as present in the indexed PDF documents without ad-hoc text manipulation.
