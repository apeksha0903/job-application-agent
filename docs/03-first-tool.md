# First Agent Tool — Function Tool Integration

## 1. What Was Built

In this milestone, we extended the initial AI Job Application Agent by registering its first **tool**: `get_candidate_name()`.

Instead of relying solely on prompt text or static instructions, the agent can now dynamically execute custom Python code when it needs specific external or candidate data.

### Created / Modified Files:
* `app/tools/candidate_tools.py` — Defines the `get_candidate_name()` function decorated with `@function_tool`.
* `app/first_agent.py` — Imports `get_candidate_name`, registers it under `tools=[get_candidate_name]` in the `Agent` configuration, and updates instructions to enforce tool use when candidate details are required.
* `docs/03-first-tool.md` — Architectural documentation for this milestone.

---

## 2. Why Tools Are Needed

LLMs alone have fundamental limitations:
1. **No direct access to runtime environment or private data**: LLMs only process the context provided in the prompt.
2. **Hallucination risks**: If asked for specific private information (e.g., candidate name, skills, resume details) without a tool, an LLM might guess or fabricate information.
3. **No execution capability**: LLMs produce text, but cannot directly query databases, fetch web pages, or read files without tools.

By equipping agents with tools, the LLM acts as the **decision engine** (determining *when* and *which* tool to call), while Python functions execute the actual logic deterministically.

---

## 3. Key Concepts

### `@function_tool`
The `@function_tool` decorator from the OpenAI Agents SDK converts a standard Python function into an agent-compatible tool definition. It inspects:
* **Function Signature & Type Hints**: Defines the parameters and return type.
* **Docstring**: Communicates to the LLM *what* the tool does and *when* it should be invoked.

```python
from agents import function_tool

@function_tool
def get_candidate_name() -> str:
    """Return the candidate's name."""
    return "Apeksha"
```

### `tools=[get_candidate_name]`
Passing a list of function tools to `Agent(..., tools=[...])` makes these tools available to the LLM during conversation turns. The SDK formats the tool declarations into JSON schemas that are sent alongside the prompt to the model API.

---

## 4. Execution Architecture & Flow

```text
User ("What is my name?")
  ↓
Agent / Runner
  ↓
LLM (inspects query + tool schemas & decides get_candidate_name tool is needed)
  ↓
Tool Call Request (emitted by LLM)
  ↓
Python Function (get_candidate_name() executes and returns "Apeksha")
  ↓
Tool Result ("Apeksha" sent back to LLM context)
  ↓
LLM (synthesizes final answer)
  ↓
Final Response ("Your name is Apeksha.")
```

---

## 5. How the Agent Decides Tool Relevance

The LLM evaluates every user request against:
1. **System Instructions**: Explicit rules (e.g., *"Always use the get_candidate_name tool whenever you need the candidate's name"*).
2. **Tool Docstrings & Schemas**: The description inside `get_candidate_name()`.
3. **User Query**:
   * For `"What is my name?"`, the LLM sees a match with the tool docstring and issues a tool call.
   * For `"What is 25 multiplied by 4?"`, the LLM recognizes that candidate information is irrelevant, skips the tool call entirely, and answers directly (`100`).

---

## 6. Comparison: Milestone 1 vs. Milestone 2

| Feature | Milestone 1 (First Agent) | Milestone 2 (First Tool) |
| :--- | :--- | :--- |
| **Architecture** | User → Agent → LLM → Response | User → Agent → LLM → Tool → Tool Result → LLM → Response |
| **External Capabilities** | None (Text completion only) | Python Function Execution (`@function_tool`) |
| **Data Retrieval** | Rely on LLM pre-trained knowledge | Dynamic lookup via Python functions |
| **Tool Selection** | N/A | Selective (Calls tools only when relevant) |

---

## 7. Current Hard-coding & Next Steps

### What is currently hard-coded:
* The candidate's name (`"Apeksha"`) is hard-coded as a static string directly inside `get_candidate_name()`.

### What will be improved in the next milestone:
* Move from hard-coded values to a structured **Candidate Profile** (e.g., JSON / Pydantic schema or database) from which tools will dynamically load verified candidate data.
