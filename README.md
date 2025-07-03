# 🗂️ Gestionnaire de Tâches Web

## 📌 Description

**Gestionnaire de Tâches Web** est une application collaborative permettant de créer, suivre, et organiser des tâches avec des priorités, des statuts et une attribution à des utilisateurs.  
Ce projet a été réalisé dans le cadre d’un travail collaboratif pour appliquer les concepts de **Git**, **CI/CD**, **tests automatisés**, et **DevOps**.

---

## 🚀 Fonctionnalités Principales

- ✏️ Création, modification, suppression de tâches
- 👥 Attribution de tâches à des utilisateurs
- 📊 Système de statuts et de priorités
- 🌐 Interface responsive (React)
- 🧩 API REST (Express.js)
- 🧪 Tests automatisés (unitaires, intégration, E2E avec Selenium)
- ⚙️ Pipeline CI/CD (GitHub Actions)
- 📈 Monitoring basique

---

## 📁 Structure du projet

```
projet-gestionnaire-taches/
├── frontend/         # Application React
├── backend/          # API Node.js/Express
├── tests/            # Tests Selenium / Jest
├── .github/          # Workflows GitHub Actions
├── README.md         # Ce fichier
└── package.json      # Configuration racine
```

---

## 🔧 Commandes à exécuter pour démarrer le projet

### 📂 Cloner le dépôt
```bash
git clone https://github.com/Nisseya/proj_cicd.git
cd gestionnaire-taches-web
```

### 🌳 Créer une branche pour travailler
```bash
git checkout -b dev
```

### 💻 Initialiser le frontend
```bash
cd frontend
npm install
npm start
```

### 🖥️ Initialiser le backend
```bash
cd ../backend
npm install
npm run dev
```

### 🧪 Lancer les tests E2E (Selenium)
```bash
cd ../tests
pytest tests/test_selenium.py --html=report.html --self-contained-html
```

### 🧪 Linter le code React
```bash
cd ../frontend
npx eslint .
```

---

## 🧪 Tests & Qualité

- ✅ **Tests E2E** avec Selenium + Pytest
- ✅ **Linting** du code frontend avec ESLint
- ✅ **Tests unitaires** frontend (Jest)
- ✅ **Rapports HTML automatisés** via GitHub Actions
- ❓ *(Optionnel)* : tests backend via Jest/Supertest

---

## 🔁 Intégration Continue & Déploiement (CI/CD)

- **GitHub Actions** :
  - ✅ Tests automatisés (frontend, Selenium)
  - ✅ Lint automatique
  - ✅ Génération de rapports
  - ✅ Build frontend
  - ✅ Déploiement GitHub Pages (`frontend/build`)
- **Backend** déployé manuellement sur **Render**

---

## ⚙️ Installation & Lancement

### 📦 Backend (Node.js / Express)
```bash
cd backend
npm install
npm run dev
```

### 💻 Frontend (React)
```bash
cd frontend
npm install
npm start
```

---

## 🔐 Accès par défaut

```text
Username : admin@test.com
Password : password
```

---

## 🧠 Technologies utilisées

- React (Frontend)
- Express (Backend)
- MongoDB (si utilisé)
- Selenium + Pytest (Tests E2E)
- Jest (Tests unitaires)
- GitHub Actions (CI/CD)
- Render / GitHub Pages (Déploiement)

---

## 👥 Équipe projet

| Nom        | Rôle             |
|------------|------------------|
| Membre 1   | Dev Frontend     |
| Membre 2   | Dev Backend      |
| Membre 3   | DevOps / QA      |

---

## 📈 Suivi & Innovation

- Utilisation des branches `main`, `dev` avec protection
- Suivi via GitHub Issues et Projets
- Idées proposées :
  - Vue calendrier
  - Drag & Drop des tâches
  - Notifications par email

---

## 📄 Licence

Ce projet est sous licence [ISC](./LICENSE)

---

## 🙌 Remerciements

Projet réalisé dans le cadre du module **DevOps / CI/CD**.


---

## 🧪 Détail des tests automatisés

### 📸 Tests End-to-End (E2E) avec Selenium

Les tests Selenium simulent une vraie interaction utilisateur avec l'interface frontend (`localhost:3000`). Exemple :

- Inscription d'un utilisateur avec un email aléatoire
- Connexion avec ce compte
- Vérification de la redirection vers le tableau de bord (`/dashboard`)

```python
driver.get("http://localhost:3000/register")
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.TAG_NAME, "form").submit()
assert "/dashboard" in driver.current_url
```

Ces tests sont exécutés en mode headless avec Chrome et intégrés dans le pipeline CI.

### 🔗 Tests API avec Pytest + Requests

Ces tests valident le bon fonctionnement des endpoints de l’API backend (`localhost:3001`), dont :

- `/api/auth/register` et `/api/auth/login` pour la création d'un compte
- `/api/tasks` pour la création, la lecture, la mise à jour et la suppression de tâches
- `/api/users` pour la récupération de la liste des utilisateurs

Exemple de test :
```python
def test_create_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task = {"title": "Tâche testée", "description": "...", "priority": "high"}
    res = requests.post(f"{BASE_URL}/api/tasks", json=task, headers=headers)
    assert res.status_code == 201
```

Ces tests sont automatisés et peuvent être exécutés avec :
```bash
pytest tests/
```

### 🔗 Tests avec Selenium

Ces tests valident le bon fonctionnement des endpoints de l’API backend (`localhost:3001`), dont :

- `/api/auth/register` et `/api/auth/login` pour la création d'un compte
- `/api/tasks` pour la création, la lecture, la mise à jour et la suppression de tâches
- `/api/users` pour la récupération de la liste des utilisateurs

Exemple de test :
```python
def test_create_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task = {"title": "Tâche testée", "description": "...", "priority": "high"}
    res = requests.post(f"{BASE_URL}/api/tasks", json=task, headers=headers)
    assert res.status_code == 201
```

Ces tests sont automatisés et peuvent être exécutés avec :
```bash
pytest tests/
```


---