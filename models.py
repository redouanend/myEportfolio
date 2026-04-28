from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class Skill(BaseModel):
    name: str
    level: Optional[int] = None


class Project(BaseModel):
    name: str
    description: str
    technologies: Optional[List[str]] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: str


class Education(BaseModel):
    degree: str
    school: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None


class SocialLink(BaseModel):
    platform: str
    url: HttpUrl


class Portfolio(BaseModel):
    full_name: str
    title: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: str
    skills: List[Skill] = []
    projects: List[Project] = []
    experiences: List[Experience] = []
    education: List[Education] = []
    social_links: List[SocialLink] = []
