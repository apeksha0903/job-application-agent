import json
from agents import function_tool
from app.knowledge_base import CandidateKnowledgeBase

_knowledge_base = CandidateKnowledgeBase()


@function_tool
def search_candidate_knowledge(query: str) -> str:
    """
    Search supporting candidate source documents (historical resume PDF variants)
    for specific project wording, resume bullet phrasing, and detailed context.

    Note: This tool provides supporting document context for resume-tailoring tasks.
    Authoritative candidate facts (identity, contact, official experience, target roles,
    and strict job filtering rules) must ALWAYS come from the candidate profile, not from this tool.
    If there is any conflict, candidate.json takes precedence.
    """
    results = _knowledge_base.search_candidate_documents(query=query)
    return json.dumps(results, indent=2)
