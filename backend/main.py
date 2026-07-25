import sqlite3
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# Cozzian Enterprises LLC -- Formulation Science & R&D Prototyping API
# ---------------------------------------------------------------------------

app = FastAPI(title="Cozzian Enterprises - LabSync API", version="1.0.0")

# ---------------------------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
DATABASE_PATH = Path(__file__).resolve().parent.parent / "db" / "cozzian.db"


def get_db():
    """Return a per-request SQLite connection (avoids THREAD staleness)."""
    conn = sqlite3.connect(str(DATABASE_PATH), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/api/health", tags=["health"])
async def health_check():
    """Returns database and server health status."""
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        db_status = "online"
        row_counts = {}
        for table in ["client_projects", "formulation_recipes",
                       "compliance_checklists", "batch_test_results"]:
            row_counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
        conn.close()
        return {
            "status": "ok",
            "database": db_status,
            "tables": row_counts,
            "version": "1.0.0",
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# ---------------------------------------------------------------------------
# GET /api/projects -- list all client projects
# ---------------------------------------------------------------------------
@app.get("/api/projects", tags=["projects"])
async def get_projects():
    """Return all client projects from the database."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM client_projects ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# GET /api/projects/{project_id} -- single project with recipes & compliance
# ---------------------------------------------------------------------------
@app.get("/api/projects/{project_id}", tags=["projects"])
async def get_project(project_id: int):
    """Return a single project by ID, including its recipes and compliance."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    proj_row = conn.execute(
        "SELECT * FROM client_projects WHERE id = ?", (project_id,)
    ).fetchone()
    if proj_row is None:
        conn.close()
        return {"detail": "Project not found"}
        # In production raise HTTPException; returning dict for simplicity
    proj = dict(proj_row)
    proj["recipes"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM formulation_recipes WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        ).fetchall()
    ]
    proj["compliance_checklists"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM compliance_checklists WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        ).fetchall()
    ]
    conn.close()
    return proj


# ---------------------------------------------------------------------------
# GET /api/recipes -- list all recipes, optional ?project_id=N
# ---------------------------------------------------------------------------
@app.get("/api/recipes", tags=["recipes"])
async def get_recipes(project_id: int = Query(None)):
    """Return all formulation recipes, optionally filtered by project_id."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    if project_id is not None:
        rows = conn.execute(
            "SELECT * FROM formulation_recipes WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM formulation_recipes ORDER BY created_at"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# GET /api/compliance_checklists -- list all, optional ?project_id=N
# ---------------------------------------------------------------------------
@app.get("/api/compliance_checklists", tags=["compliance"])
async def get_compliance_checklists(project_id: int = Query(None)):
    """Return all compliance checklists, optionally filtered by project_id."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    if project_id is not None:
        rows = conn.execute(
            "SELECT * FROM compliance_checklists WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM compliance_checklists ORDER BY created_at"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# GET /api/batch_tests -- list all batch tests, optional ?project_id=N
# ---------------------------------------------------------------------------
@app.get("/api/batch_tests", tags=["batch-tests"])
async def get_batch_tests(project_id: int = Query(None)):
    """Return batch test results, optionally filtered by project_id."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    if project_id is not None:
        rows = conn.execute(
            "SELECT * FROM batch_test_results WHERE project_id = ? ORDER BY created_at",
            (project_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM batch_test_results ORDER BY created_at"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")