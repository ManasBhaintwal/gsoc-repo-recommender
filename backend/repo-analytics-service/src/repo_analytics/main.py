from fastapi import FastAPI
from repo_analytics.routers import repos

app = FastAPI(title="Repo Analytics Service", version="1.0.0")

app.include_router(repos.router)

@app.get("/")
def root():
    return {"message": "Repo Analytics Service Running"}
