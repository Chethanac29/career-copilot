from pydantic import BaseModel, Field
from typing import Optional, List

# USER INFO MODELS

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    github: Optional[str] = None


class Education(BaseModel):
    degree: str
    institution: str
    duration: str
    score: Optional[str] = None


class Experience(BaseModel):
    role: str
    company: str
    duration: str
    location: Optional[str] = None
    responsibilities: List[str]


class Project(BaseModel):
    title: str
    description: str
    technologies: List[str]


class Skills(BaseModel):
    programming_languages: List[str]
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    other_relevant_technical_skills: List[str] = Field(default_factory=list)


class ResumeInput(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skills: Skills
    achievements: List[str] = Field(default_factory=list)
    extracurriculars: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
    raw_resume_text: Optional[str] = None

# JOB DESCRIPTION MODEL

class JobDescription(BaseModel):
    raw_text: str = Field(..., min_length=50)
    target_role: str

# RESUME REQUEST MODEL

class ResumeRequest(BaseModel):
    user_profile: ResumeInput
    job_description: JobDescription


class JDParsed(BaseModel):
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    other_relevant_technical_skills: List[str] = Field(default_factory=list)
    domain: Optional[str] = None
    seniority: Optional[str] = None
    key_responsibilities: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


# GENERATED PROJECT MODEL

class GeneratedProject(BaseModel):
    title: str
    description: str
    technologies: List[str]
    resume_bullets: List[str]
    github_query: str

class ProjectList(BaseModel):
    projects: List[GeneratedProject]

class BulletOutput(BaseModel):
    project_title: str
    bullets: List[str]
    