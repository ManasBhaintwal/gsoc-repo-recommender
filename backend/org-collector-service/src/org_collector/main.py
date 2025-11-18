from fastapi import FastAPI
from .routers import orgs

app = FastAPI(title="Org Collector Service", version="1.0.0")

app.include_router(orgs.router)

@app.get("/")
def root():
    return {"message": "Org Collector Service Running"}
