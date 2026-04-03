from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, HttpUrl
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()

# ----- DATA EN MÉMOIRE -----
portfolios: List["Portfolio"] = []


# ----- MODELS -----
class Skill(BaseModel):
    name: str
    level: Optional[int] = None  # facultatif


class Project(BaseModel):
    name: str
    description: str
    technologies: Optional[List[str]] = []
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None


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


# ----- EXEMPLE -----
example_portfolio = Portfolio(
    full_name="Alexandre Dupont",
    title="Développeur Full Stack",
    email="alex.dupont@example.com",
    phone="+33 6 12 34 56 78",
    location="Paris, France",
    bio="Passionné par le développement web et les technologies modernes, je crée des applications performantes et intuitives.",
    skills=[
        Skill(name="Python"),
        Skill(name="JavaScript"),
        Skill(name="React"),
        Skill(name="Django"),
        Skill(name="SQL"),
        Skill(name="Docker"),
    ],
    projects=[
        Project(
            name="Gestionnaire de tâches",
            description="Application web pour organiser ses tâches quotidiennes avec notifications et calendrier intégré.",
            technologies=["Python", "Django", "React", "PostgreSQL"],
            github_url="https://github.com/alexdupont/task-manager",
            demo_url="https://taskmanager.example.com",
        ),
        Project(
            name="Portfolio interactif",
            description="Mon portfolio personnel pour présenter mes projets et compétences.",
            technologies=["HTML", "CSS", "JavaScript", "React"],
            github_url="https://github.com/alexdupont/portfolio",
            demo_url="https://alexdupont.dev",
        ),
    ],
    experiences=[
        Experience(
            title="Développeur Full Stack",
            company="Tech Solutions",
            start_date="2022-01",
            end_date="2023-12",
            description="Développement d'applications web pour des clients internationaux, intégration de solutions cloud et maintenance des systèmes existants.",
        ),
        Experience(
            title="Stagiaire Développeur Web",
            company="Web Agency",
            start_date="2021-06",
            end_date="2021-12",
            description="Participation au développement front-end de sites clients avec React et optimisation SEO.",
        ),
    ],
    education=[
        Education(
            degree="Master Informatique",
            school="Université de Paris",
            start_date="2019-09",
            end_date="2021-06",
            description="Spécialisation en développement web et intelligence artificielle.",
        ),
        Education(
            degree="Licence Informatique",
            school="Université de Lyon",
            start_date="2016-09",
            end_date="2019-06",
        ),
    ],
    social_links=[
        SocialLink(platform="LinkedIn", url="https://www.linkedin.com/in/alexdupont"),
        SocialLink(platform="GitHub", url="https://github.com/alexdupont"),
        SocialLink(platform="Twitter", url="https://twitter.com/alexdupont"),
    ],
)

portfolios.append(example_portfolio)


# ----- ROUTES PORTFOLIO -----
@app.post("/portfolios")
def create_portfolio(portfolio: Portfolio):
    portfolios.append(portfolio)
    return {"message": "Portfolio created", "portfolio_id": len(portfolios) - 1}


@app.get("/portfolios")
def get_portfolios():
    return portfolios


@app.get("/portfolio/{portfolio_id}", response_class=HTMLResponse)
def read_portfolio(request: Request, portfolio_id: int):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        return HTMLResponse(content="Portfolio not found", status_code=404)

    portfolio = portfolios[portfolio_id]
    return templates.TemplateResponse(
        "portfolio.html",
        {"request": request, "portfolio": portfolio.dict()},  # <-- converti en dict
    )


@app.put("/portfolios/{portfolio_id}")
def update_portfolio(portfolio_id: int, portfolio: Portfolio):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolios[portfolio_id] = portfolio
    return {"message": "Portfolio updated"}


@app.delete("/portfolios/{portfolio_id}")
def delete_portfolio(portfolio_id: int):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolios.pop(portfolio_id)
    return {"message": "Portfolio deleted"}


# ----- ROUTES PROJECTS -----
@app.post("/portfolios/{portfolio_id}/projects")
def add_project(portfolio_id: int, project: Project):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolios[portfolio_id].projects.append(project)
    return {
        "message": "Project added",
        "project_id": len(portfolios[portfolio_id].projects) - 1,
    }


@app.put("/portfolios/{portfolio_id}/projects/{project_id}")
def update_project(portfolio_id: int, project_id: int, project: Project):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if project_id >= len(portfolios[portfolio_id].projects) or project_id < 0:
        raise HTTPException(status_code=404, detail="Project not found")
    portfolios[portfolio_id].projects[project_id] = project
    return {"message": "Project updated"}


@app.delete("/portfolios/{portfolio_id}/projects/{project_id}")
def delete_project(portfolio_id: int, project_id: int):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if project_id >= len(portfolios[portfolio_id].projects) or project_id < 0:
        raise HTTPException(status_code=404, detail="Project not found")
    portfolios[portfolio_id].projects.pop(project_id)
    return {"message": "Project deleted"}


# ----- ROUTES SKILLS -----
@app.post("/portfolios/{portfolio_id}/skills")
def add_skill(portfolio_id: int, skill: Skill):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolios[portfolio_id].skills.append(skill)
    return {
        "message": "Skill added",
        "skill_id": len(portfolios[portfolio_id].skills) - 1,
    }


@app.put("/portfolios/{portfolio_id}/skills/{skill_id}")
def update_skill(portfolio_id: int, skill_id: int, skill: Skill):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if skill_id >= len(portfolios[portfolio_id].skills) or skill_id < 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    portfolios[portfolio_id].skills[skill_id] = skill
    return {"message": "Skill updated"}


@app.delete("/portfolios/{portfolio_id}/skills/{skill_id}")
def delete_skill(portfolio_id: int, skill_id: int):
    if portfolio_id >= len(portfolios) or portfolio_id < 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if skill_id >= len(portfolios[portfolio_id].skills) or skill_id < 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    portfolios[portfolio_id].skills.pop(skill_id)
    return {"message": "Skill deleted"}
