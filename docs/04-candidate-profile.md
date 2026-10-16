# Master Candidate Profile

## 1. Overview & Purpose

The **Master Candidate Profile** serves as the **Single Source of Truth** for the AI Job Application Agent.

Before this milestone, candidate details were hard-coded directly inside individual tools. Moving forward, all candidate information (identity, skills, experience, projects, education, and career preferences) resides in a structured master profile (`data/candidate.json`) validated by Pydantic models (`app/models/candidate.py`).

This architecture ensures:
* Zero fabrication of candidate experience, skills, or achievements.
* Decoupled architecture separating data storage, validation, business logic, and LLM agent tool exposure.
* Consistent candidate representation across job evaluations, resume tailoring, and form filling.

---

## 2. Why JSON is the Source of Truth

* **Human-Readable & Editable**: JSON can be easily updated or maintained without code changes.
* **Portable & Interoperable**: Standard format easily consumed by Python, databases, or frontend dashboards.
* **Strict Structural Schema**: Easily mapped to Pydantic models for validation.

---

## 3. Why Pydantic Validation is Used

Pydantic guarantees data integrity before any agent tool processes candidate information:
* **Type Safety & Schema Validation**: Ensures required fields (e.g., degree, company, skills) are present and properly formatted.
* **Serialization & Parsing**: Converts JSON data directly into validated Python objects (`CandidateProfile`) and allows seamless conversion back into JSON for LLM tool consumption.

---

## 4. Profile Structure & Key Distinctions

The profile schema (`app/models/candidate.py`) is divided into distinct sections:

1. **`identity`**: Contact details (Name: Apeksha Morappanavar).
2. **`career_preferences`**: Target roles (Software Engineer, Backend Software Engineer, Full-Stack Software Engineer, Pure C++ Software Engineer) and domain exclusions (Embedded, Hardware, Automotive).
3. **`professional_experience`**: Magna International (Software Engineer, March 2025 – Present). Represented as continuous professional software engineering experience (1+ years).
4. **`projects`**: Approved projects (`MultiFlix`, `MERN-GPT`, `Breast Cancer Detection Using Few-Shot Learning`).
5. **`research`**: Conference research (`Breast Cancer Detection by Prototypical Networks Using Few-Shot Learning` presented at INCET 2024 / IEEE Bangalore).
6. **`education`**: B.E. in Computer Science and Engineering from KLE Technological University (2021–2025, CGPA: 9.44).
7. **`skills`**: Grouped into technical categories (Languages, Backend & Web, Databases, Testing & QA, Tools & Platforms, AI & Data Science, Domain Knowledge).
8. **`certifications` & `achievements`**: Verified non-fabricated credentials.

### Critical Distinction: Professional vs. Project vs. Research Experience
* **Professional Experience**: Solely verified employment (Magna International).
* **Project Experience**: Technologies used in academic/personal projects are kept strictly in the project section.
* **Rule**: Project technologies are never falsely claimed as professional work experience.

---

## 5. Strict Job Experience Filtering Rule

The candidate target profile specifies strict experience range boundaries for future job evaluation:

### Allowed Explicit Experience Ranges:
* `0–1 years`
* `0–2 years`
* `1 year`
* `1–2 years`

### Excluded Explicit Experience Ranges:
* `1–3 years`
* `2+ years`
* `2–3 years`
* `3+ years`
* `3–5 years`
* `5+ years`

> [!IMPORTANT]
> This filtering rule must be enforced deterministically in Python code during job ingestion rather than relying solely on LLM interpretation.

---

## 6. Support for Future Resume Tailoring

Different resume variants (e.g., backend-focused vs. pure software C++ focused) represent different *positioning strategies* of the **same single candidate identity**.

By centralizing all verified data in `data/candidate.json`, future resume generation modules will dynamically select relevant subsets of verified skills and achievements from this single source of truth without risking fabrication.

---

## 7. Data Flow Architecture

```text
data/candidate.json (Raw JSON data)
       ↓
app/services/candidate_profile.py (load_candidate_profile)
       ↓
app/models/candidate.py (Pydantic validation -> CandidateProfile object)
       ↓
app/tools/candidate_tools.py (get_candidate_profile @function_tool)
       ↓
Agent / LLM Context (Receives structured JSON context)
```
