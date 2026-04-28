# Générateur de CV / ePortfolio

## Description

Ce projet consiste à créer une application web permettant de générer un ePortfolio dynamique.

L'objectif est de permettre à un utilisateur de :

- créer un portfolio ;
- ajouter des projets ;
- ajouter des compétences ;
- afficher son portfolio sous forme de page web ;
- conserver ses données de manière persistante.

Le backend est développé avec FastAPI, et le frontend est géré via des templates HTML avec Jinja2.

---

## Stack technique

- Python
- FastAPI
- Pydantic (validation des données)
- Jinja2 (templates HTML)
- SQLAlchemy (ORM - mapping objet-relationnel)
- SQLite (base de données locale)

---

## Structure du projet

```bash
myEportfolio/
│
├── main.py          # Routes FastAPI et point d'entrée
├── models.py        # Modèles Pydantic (validation des données entrantes)
├── schemas.py       # Modèles SQLAlchemy (tables de la base de données)
├── database.py      # Configuration de la connexion et de la session SQLAlchemy
├── templates/
│   └── portfolio.html  # Template HTML Jinja2
├── portfolio.db     # Base de données SQLite (générée automatiquement)
├── requirements.txt
└── README.md
```

---

## Modélisation des données

Nous utilisons deux types de modèles distincts.

**Modèles Pydantic** (models.py) — valident les données qui arrivent via l'API :

```python
class Skill(BaseModel):
    name: str
    level: Optional[int] = None
```

Ces modèles permettent :
- validation automatique des données entrantes
- typage clair
- communication propre entre frontend et backend

**Modèles SQLAlchemy** (schemas.py) — représentent les tables de la base de données :

```python
class SkillModel(Base):
    __tablename__ = "skills"
    id           = Column(Integer, primary_key=True)
    name         = Column(String, nullable=False)
    level        = Column(Integer, nullable=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
```

Ces modèles permettent :
- persistance des données dans SQLite
- relations entre les tables via les clés étrangères
- suppression en cascade (supprimer un portfolio supprime ses compétences, projets, etc.)

---

## Base de données

Nous avons ajouté SQLAlchemy comme ORM (Object Relational Mapper) afin de remplacer le stockage en mémoire (liste Python) par une vraie base de données SQLite.

**Pourquoi SQLAlchemy ?**
- les données persistent entre les redémarrages du serveur
- on manipule des objets Python au lieu d'écrire du SQL brut
- les relations entre tables (portfolio → skills, projects...) sont gérées automatiquement

**Comment ça fonctionne ?**
Requête HTTP entrante
↓
validée par Pydantic (models.py)
↓
convertie en SQLAlchemy (schemas.py)
↓
sauvegardée dans SQLite (portfolio.db)
↓
affichée via Jinja2 (portfolio.html)
↓
Page HTML

La base de données `portfolio.db` est créée automatiquement au premier démarrage grâce à :

```python
Base.metadata.create_all(bind=engine)
```

---

## Routes API (V1)

### Portfolio
- POST `/portfolios` → créer un portfolio
- GET `/portfolios` → récupérer tous les portfolios
- GET `/portfolios/{id}` → afficher un portfolio en HTML
- PUT `/portfolios/{id}` → modifier un portfolio
- DELETE `/portfolios/{id}` → supprimer un portfolio

### Projets
- POST `/portfolios/{id}/projects` → ajouter un projet
- PUT `/portfolios/{id}/projects/{project_id}` → modifier un projet
- DELETE `/portfolios/{id}/projects/{project_id}` → supprimer un projet

### Compétences
- POST `/portfolios/{id}/skills` → ajouter une compétence
- PUT `/portfolios/{id}/skills/{skill_id}` → modifier une compétence
- DELETE `/portfolios/{id}/skills/{skill_id}` → supprimer une compétence

---

## Feuille de route

- [x] API REST avec FastAPI
- [x] Validation des données avec Pydantic
- [x] Stockage persistant SQLite avec SQLAlchemy
- [x] Page portfolio HTML avec Jinja2
- [ ] HTMX pour les interactions dynamiques sans rechargement
- [ ] Authentification utilisateur (JWT)
- [ ] Inscription, connexion et gestion du portfolio par l'utilisateur
