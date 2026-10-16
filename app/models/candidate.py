from typing import List, Optional
from pydantic import BaseModel


class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class ProfessionalExperience(BaseModel):
    company: str
    role: str
    period: str
    experience_level: Optional[str] = None
    responsibilities: List[str]
    achievements: List[str]
    technologies: Optional[List[str]] = None


class Project(BaseModel):
    title: str
    description: str
    technologies: List[str]
    highlights: List[str]
    link: Optional[str] = None


class Research(BaseModel):
    title: str
    publication: str
    year: str
    summary: str


class Education(BaseModel):
    degree: str
    institution: str
    period: str
    cgpa: Optional[float] = None


class Certification(BaseModel):
    title: str
    issuer: str


class Achievement(BaseModel):
    title: str
    description: str


class Skills(BaseModel):
    languages: List[str]
    backend_and_web: List[str]
    databases: List[str]
    testing_and_qa: List[str]
    tools_and_platforms: List[str]
    ai_and_data_science: List[str]
    domain_knowledge: List[str]


class JobFilterRules(BaseModel):
    allowed_experience_ranges: List[str]
    excluded_keywords: List[str]
    rule: Optional[str] = None


class CareerPreferences(BaseModel):
    target_roles: List[str]
    excluded_domains: List[str]
    job_filter_rules: JobFilterRules


class ResumeTailoringContext(BaseModel):
    note: str
    master_principle: str
    document_principle: Optional[str] = None


class CandidateProfile(BaseModel):
    identity: ContactInfo
    career_preferences: CareerPreferences
    professional_experience: List[ProfessionalExperience]
    projects: List[Project]
    research: List[Research]
    education: List[Education]
    skills: Skills
    certifications: List[Certification]
    achievements: List[Achievement]
    resume_tailoring_context: ResumeTailoringContext
