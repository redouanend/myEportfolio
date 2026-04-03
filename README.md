# Générateur de CV / ePortfolio

## Description

Ce projet consiste à créer une application web permettant de générer un ePortfolio dynamique.

L’objectif est de permettre à un utilisateur de :

- créer un portfolio ;
- ajouter des projets ;
- ajouter des compétences ;
- afficher son portfolio sous forme de page web.

Le backend est développé avec FastAPI, et le frontend est géré via des templates HTML avec Jinja2.

---

## Stack technique

- Python
- FastAPI
- Pydantic (validation des données)
- Jinja2 (templates HTML)
- Base de données SQL (à venir)

---

## Structure du projet

```bash
myEportfolio/
│
├── main.py        # Routes FastAPI
├── models.py      # Modèles Pydantic
├── templates/     # Templates HTML
└── README.md
```

---

## Modélisation des données

Nous utilisons des classes Pydantic pour structurer les données.

Exemple :
class Skill(BaseModel):
    name: str
    level: Optional[int] = None

Ces modèles permettent :
validation automatique
typage clair
communication propre entre frontend et backend


---


## Routes API (V1)
Portfolio
POST /portfolios → créer un portfolio
GET /portfolios → récupérer tous les portfolios
GET /portfolios/{id} → récupérer un portfolio
PUT /portfolios/{id} → modifier un portfolio
DELETE /portfolios/{id} → supprimer un portfolio
Projects
POST /portfolios/{id}/projects → ajouter un projet
PUT /portfolios/{id}/projects/{project_id} → modifier un projet
DELETE /portfolios/{id}/projects/{project_id} → supprimer un projet
Skills
POST /portfolios/{id}/skills → ajouter une compétence
PUT /portfolios/{id}/skills/{skill_id} → modifier une compétence
DELETE /portfolios/{id}/skills/{skill_id} → supprimer une compétence
