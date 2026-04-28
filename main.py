import json
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from schemas import (
    PortfolioModel,
    SkillModel,
    ProjectModel,
    ExperienceModel,
    EducationModel,
    SocialLinkModel,
)
from models import Portfolio, Skill, Project, Experience, Education, SocialLink

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_portfolio_or_404(portfolio_id: int, db: Session) -> PortfolioModel:
    portfolio = db.get(PortfolioModel, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@app.get("/")
def root():
    return RedirectResponse(url="/portfolios/1")


@app.post("/portfolios")
def create_portfolio(portfolio: Portfolio, db: Session = Depends(get_db)):
    db_portfolio = PortfolioModel(
        full_name=portfolio.full_name,
        title=portfolio.title,
        email=portfolio.email,
        phone=portfolio.phone,
        location=portfolio.location,
        bio=portfolio.bio,
    )
    db.add(db_portfolio)
    db.flush()

    for skill in portfolio.skills:
        db.add(
            SkillModel(name=skill.name, level=skill.level, portfolio_id=db_portfolio.id)
        )

    for project in portfolio.projects:
        db.add(
            ProjectModel(
                name=project.name,
                description=project.description,
                technologies=json.dumps(project.technologies),
                github_url=project.github_url,
                demo_url=project.demo_url,
                portfolio_id=db_portfolio.id,
            )
        )

    for exp in portfolio.experiences:
        db.add(
            ExperienceModel(
                title=exp.title,
                company=exp.company,
                start_date=exp.start_date,
                end_date=exp.end_date,
                description=exp.description,
                portfolio_id=db_portfolio.id,
            )
        )

    for edu in portfolio.education:
        db.add(
            EducationModel(
                degree=edu.degree,
                school=edu.school,
                start_date=edu.start_date,
                end_date=edu.end_date,
                description=edu.description,
                portfolio_id=db_portfolio.id,
            )
        )

    for link in portfolio.social_links:
        db.add(
            SocialLinkModel(
                platform=link.platform,
                url=str(link.url),
                portfolio_id=db_portfolio.id,
            )
        )

    db.commit()
    db.refresh(db_portfolio)
    return {"message": "Portfolio created", "portfolio_id": db_portfolio.id}


@app.get("/portfolios")
def get_portfolios(db: Session = Depends(get_db)):
    return db.query(PortfolioModel).all()


@app.get("/portfolios/{portfolio_id}", response_class=HTMLResponse)
def read_portfolio(request: Request, portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = get_portfolio_or_404(portfolio_id, db)
    return templates.TemplateResponse(
        request=request,
        name="portfolio.html",
        context={"portfolio": portfolio},
    )


@app.put("/portfolios/{portfolio_id}")
def update_portfolio(
    portfolio_id: int, portfolio: Portfolio, db: Session = Depends(get_db)
):
    db_portfolio = get_portfolio_or_404(portfolio_id, db)
    db_portfolio.full_name = portfolio.full_name
    db_portfolio.title = portfolio.title
    db_portfolio.email = portfolio.email
    db_portfolio.phone = portfolio.phone
    db_portfolio.location = portfolio.location
    db_portfolio.bio = portfolio.bio
    db.commit()
    return {"message": "Portfolio updated"}


@app.delete("/portfolios/{portfolio_id}")
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    db_portfolio = get_portfolio_or_404(portfolio_id, db)
    db.delete(db_portfolio)
    db.commit()
    return {"message": "Portfolio deleted"}


@app.post("/portfolios/{portfolio_id}/projects")
def add_project(portfolio_id: int, project: Project, db: Session = Depends(get_db)):
    get_portfolio_or_404(portfolio_id, db)
    db_project = ProjectModel(
        name=project.name,
        description=project.description,
        technologies=json.dumps(project.technologies),
        github_url=project.github_url,
        demo_url=project.demo_url,
        portfolio_id=portfolio_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return {"message": "Project added", "project_id": db_project.id}


@app.put("/portfolios/{portfolio_id}/projects/{project_id}")
def update_project(
    portfolio_id: int, project_id: int, project: Project, db: Session = Depends(get_db)
):
    get_portfolio_or_404(portfolio_id, db)
    db_project = db.get(ProjectModel, project_id)
    if not db_project or db_project.portfolio_id != portfolio_id:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.name = project.name
    db_project.description = project.description
    db_project.technologies = json.dumps(project.technologies)
    db_project.github_url = project.github_url
    db_project.demo_url = project.demo_url
    db.commit()
    return {"message": "Project updated"}


@app.delete("/portfolios/{portfolio_id}/projects/{project_id}")
def delete_project(portfolio_id: int, project_id: int, db: Session = Depends(get_db)):
    get_portfolio_or_404(portfolio_id, db)
    db_project = db.get(ProjectModel, project_id)
    if not db_project or db_project.portfolio_id != portfolio_id:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}


@app.post("/portfolios/{portfolio_id}/skills")
def add_skill(portfolio_id: int, skill: Skill, db: Session = Depends(get_db)):
    get_portfolio_or_404(portfolio_id, db)
    db_skill = SkillModel(name=skill.name, level=skill.level, portfolio_id=portfolio_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return {"message": "Skill added", "skill_id": db_skill.id}


@app.put("/portfolios/{portfolio_id}/skills/{skill_id}")
def update_skill(
    portfolio_id: int, skill_id: int, skill: Skill, db: Session = Depends(get_db)
):
    get_portfolio_or_404(portfolio_id, db)
    db_skill = db.get(SkillModel, skill_id)
    if not db_skill or db_skill.portfolio_id != portfolio_id:
        raise HTTPException(status_code=404, detail="Skill not found")
    db_skill.name = skill.name
    db_skill.level = skill.level
    db.commit()
    return {"message": "Skill updated"}


@app.delete("/portfolios/{portfolio_id}/skills/{skill_id}")
def delete_skill(portfolio_id: int, skill_id: int, db: Session = Depends(get_db)):
    get_portfolio_or_404(portfolio_id, db)
    db_skill = db.get(SkillModel, skill_id)
    if not db_skill or db_skill.portfolio_id != portfolio_id:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(db_skill)
    db.commit()
    return {"message": "Skill deleted"}
