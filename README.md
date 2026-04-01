# myEportfolio
Générateur de CV/Eportfolio
1)Description

Ce projet consiste à créer une application web permettant de générer un ePortfolio dynamique.

L’objectif est de permettre à un utilisateur de :

créer un portfolio
ajouter des projets
ajouter des compétences
afficher son portfolio sous forme de page web

Le backend est développé avec FastAPI, et le frontend sera géré via templates HTML (Jinja2).

Stack technique
Python
FastAPI
Pydantic (validation des données)
Jinja2 (templates HTML)
(plus tard) Base de données SQL d'aprés ce que le prof a dis.

2)Structure du projet (actuelle)
myEportfolio/
│
├── main.py          # routes FastAPI
├── models.py        # modèles Pydantic
├── templates/       # templates HTML (à venir)
└── README.md

3)Modélisation des données

Nous utilisons des classes Pydantic pour structurer les données.

Exemple :
class Skill(BaseModel):
    name: str
    level: Optional[int] = None

Ces modèles permettent :
validation automatique
typage clair
communication propre entre frontend et backend

4)Routes API (V1)
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
