from fastapi import FastAPI
from .routes.users import router as user_router

app = FastAPI(title="User Profile Service")

app.include_router(user_router)

@app.get("/")
def health():
    return {"status": "running"}
