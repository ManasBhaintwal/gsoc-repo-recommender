# main.py
from fastapi import FastAPI
from routes.users import router as users_router

app = FastAPI(title="user-profile-service")

app.include_router(users_router)

@app.get("/")
def root():
    return {"status": "user-profile-service ok"}
