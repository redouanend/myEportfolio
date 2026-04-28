import json
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PortfolioModel(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(Text, nullable=False)

    skills = relationship(
        "SkillModel", back_populates="portfolio", cascade="all, delete"
    )
    projects = relationship(
        "ProjectModel", back_populates="portfolio", cascade="all, delete"
    )
    experiences = relationship(
        "ExperienceModel", back_populates="portfolio", cascade="all, delete"
    )
    education = relationship(
        "EducationModel", back_populates="portfolio", cascade="all, delete"
    )
    social_links = relationship(
        "SocialLinkModel", back_populates="portfolio", cascade="all, delete"
    )


class SkillModel(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    portfolio = relationship("PortfolioModel", back_populates="skills")


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    technologies = Column(Text, default="[]")
    github_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    portfolio = relationship("PortfolioModel", back_populates="projects")

    @property
    def technologies_list(self):
        return json.loads(self.technologies or "[]")


class ExperienceModel(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    portfolio = relationship("PortfolioModel", back_populates="experiences")


class EducationModel(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String, nullable=False)
    school = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    portfolio = relationship("PortfolioModel", back_populates="education")


class SocialLinkModel(Base):
    __tablename__ = "social_links"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)
    url = Column(String, nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    portfolio = relationship("PortfolioModel", back_populates="social_links")
