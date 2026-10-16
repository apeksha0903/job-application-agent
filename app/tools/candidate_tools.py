import json
from agents import function_tool
from pydantic import ValidationError
from app.services.candidate_profile import load_candidate_profile


@function_tool
def get_candidate_name() -> str:
    """Return the candidate's name from the authoritative candidate profile."""
    try:
        profile = load_candidate_profile()
        return profile.identity.name
    except FileNotFoundError:
        return json.dumps({"error": "candidate.json not found. Ensure data/candidate.json exists."})
    except ValueError as exc:
        return json.dumps({"error": f"candidate.json has invalid JSON syntax: {exc}"})
    except ValidationError:
        return json.dumps({"error": "candidate.json structure does not match the expected profile format."})
    except Exception:
        return json.dumps({"error": "An unexpected error occurred while loading the candidate profile."})


@function_tool
def get_candidate_profile() -> str:
    """
    Retrieve the full authoritative candidate profile from data/candidate.json.

    This is the SINGLE SOURCE OF TRUTH for all verified candidate facts including:
    identity, contact, professional experience, education, skills, projects,
    research, certifications, achievements, career preferences, excluded domains,
    and job filtering rules.

    Always use this tool for candidate facts. Never fabricate information.
    """
    try:
        profile = load_candidate_profile()
        return profile.model_dump_json(indent=2)
    except FileNotFoundError:
        return json.dumps({"error": "candidate.json not found. Ensure data/candidate.json exists."})
    except ValueError as exc:
        return json.dumps({"error": f"candidate.json has invalid JSON syntax: {exc}"})
    except ValidationError:
        return json.dumps({"error": "candidate.json structure does not match the expected profile format."})
    except Exception:
        return json.dumps({"error": "An unexpected error occurred while loading the candidate profile."})
