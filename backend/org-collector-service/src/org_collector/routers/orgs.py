

# backend/org-collector-service/src/org_collector/routers/orgs.py
from database.connect import get_conn
from fastapi import APIRouter, BackgroundTasks
from org_collector.services.sync_pipeline import sync_master_then_yearly_then_projects

router = APIRouter(prefix="/orgs", tags=["orgs"])

@router.get("/")
def get_orgs():
    return {"status": "ok", "data": []}

@router.post("/sync")
def sync_orgs(
    background_tasks: BackgroundTasks,
    master: bool = True,
    yearly: bool = True,
    projects: bool = True
):    # run in background to avoid blocking request
    background_tasks.add_task(
        sync_master_then_yearly_then_projects,
        master,
        yearly,
        projects
    )
    return {
        "status": "sync_started",
        "modes": {
            "master": master,
            "yearly": yearly,
            "projects": projects
        }
    }

@router.get("/count")
def count_orgs():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM orgs;")
        n = cur.fetchone()[0]
    conn.close()
    return {"orgs": n}

@router.get("/projects/count")
def count_projects():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM org_projects;")
        n = cur.fetchone()[0]
    conn.close()
    return {"projects": n}

@router.get("/last-sync")
def last_sync():
    from org_collector.services.sync_status import get_sync_status
    ts = get_sync_status("org_sync")
    return {"last_synced_at": ts}
