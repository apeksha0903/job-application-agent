import json
from pathlib import Path

from app.models.candidate import CandidateProfile

# Path pointing to data/candidate.json from the project root
DATA_DIR = Path(__file__).parent.parent.parent / "data"
PROFILE_FILE = DATA_DIR / "candidate.json"


def load_candidate_profile(file_path: Path = PROFILE_FILE) -> CandidateProfile:
    """Load, parse, and validate the candidate profile from JSON.

    Raises:
        FileNotFoundError: data/candidate.json does not exist.
        ValueError: The file contains invalid JSON syntax.
        ValidationError: The JSON does not match the CandidateProfile schema.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            "Candidate profile not found. Ensure data/candidate.json exists."
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"candidate.json contains invalid JSON syntax: {exc.msg} "
            f"(line {exc.lineno}, column {exc.colno})."
        ) from exc

    return CandidateProfile(**data)
