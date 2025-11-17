from fastapi import APIRouter

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/")
def get_repos():
    return {"status": "ok", "data": []}
    