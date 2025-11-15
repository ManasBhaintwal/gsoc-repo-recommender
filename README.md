# 📦 **gsoc-repo-recommender**

**An AI-powered platform to help students find the best open-source repositories to contribute to for Google Summer of Code (GSoC).**
This **monorepo** contains both backend microservices and the frontend web application.
The system intelligently analyzes GSoC organizations, GitHub repositories, your skill profile, and historical data to recommend the most suitable projects — maximizing your chances of selection.

---

## 🚀 **Features**

### 🔎 Smart Repository Recommendations

* ML-based scoring system
* Matches your skills to repository tech stack
* Predicts probability of an organization returning next year
* Weighted ranking of repositories based on:

  * repo health
  * contribution friendliness
  * documentation quality
  * skill match
  * GSoC participation history

### 🧠 AI + RAG Assistant

* Searches repo docs, issues, ideas lists
* Generates proposal guidance
* Personalized suggestions

### 📊 Repo Analytics Dashboard

* Commit activity
* Issue trends
* PR merge time
* Contributor growth
* Overall health score

### 👤 Student Profile System

* Add skills, experience, interests
* Save favorite repos/orgs
* GitHub integration

---

# 🏗 **Architecture Overview**

This is a **microservices-based monorepo** with independent backend services and a shared frontend.

### **Backend Services**

| Service                               | Description                                             |
| ------------------------------------- | ------------------------------------------------------- |
| `org-collector-service`               | Scrapes and stores GSoC organizations + project history |
| `repo-analytics-service`              | Analyzes GitHub repos and calculates metrics            |
| `scoring-ml-service`                  | ML engine for repo suitability + org return probability |
| `embeddings-rag-service`              | Vector search, embeddings, and AI assistant             |
| `user-profile-service`                | User accounts, skills, preferences                      |
| `recommendation-orchestrator-service` | API gateway, service aggregator                         |

### **Frontend**

| Folder             | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `frontend-web-app` | Next.js UI for recommendations, dashboards, and AI assistant |

---

# 🧬 **Tech Stack**

### **Backend**

* Python (FastAPI)
* Node.js / NestJS (for auth/user/orchestrator services)
* PostgreSQL
* Qdrant (Vector DB)
* Redis (Caching)
* Celery / Cron (Background jobs)
* Docker & Docker Compose

### **Frontend**

* Next.js
* React
* TailwindCSS
* Shadcn/UI
* Chart.js

---

# 📁 **Monorepo Structure**

```
gsoc-repo-recommender/
│
├── backend/
│   ├── org-collector-service/
│   ├── repo-analytics-service/
│   ├── scoring-ml-service/
│   ├── embeddings-rag-service/
│   ├── user-profile-service/
│   ├── recommendation-orchestrator-service/
│   └── shared/
│
├── frontend/
│   └── frontend-web-app/
│
├── docker/
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
│
├── docs/
│   ├── architecture.md
│   ├── api-specs/
│   └── ml-models/
│
├── LICENSE
└── README.md
```

---

# 📦 **Installation & Setup**

### **Prerequisites**

* Python 3.10+
* Node.js 18+
* Docker
* GitHub API Token
* Postgres + Qdrant + Redis

---

### 🐳 **Run Using Docker Compose**

Inside the repo root:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This will start:

* all backend microservices
* vector DB
* Postgres
* Redis
* frontend app

---

### 🛠 **Manual Setup (Backend)**

Example: Run the org collector service

```bash
cd backend/org-collector-service
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 🛠 **Manual Setup (Frontend)**

```bash
cd frontend/frontend-web-app
npm install
npm run dev
```

---

# 🧪 **Testing**

Each service includes its own test suite.

Run backend tests:

```bash
pytest
```

Run frontend tests:

```bash
npm run test
```

---

# 🤝 **Contributing**

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Submit a PR with detailed description

Follow the monorepo conventions outlined in `/docs/architecture.md`.

---

# 📄 **License**

This project is licensed under the **Apache License 2.0**.
See the full license in the `LICENSE` file.

---

# ⭐ **Acknowledgements**

This project exists to help students get into open-source and successfully participate in **Google Summer of Code**.
Thanks to the open-source community and the many GSoC organizations who publish high-quality resources.

---
