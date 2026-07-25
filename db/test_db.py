"""
# ============================================================================================
# Cozzian Enterprises LLC — Test Suite for Database Layer
# ============================================================================================
# Tests: table existence, foreign key cascades, seed data counts, edge cases
# Run with: python -m pytest db/test_db.py -v
#
# NOTE: Cascade-delete tests mutate the database permanently. Run them last
#       (they are grouped at the end of the file) or re-seed the DB afterward.
# ============================================================================================
"""

import sqlite3
from pathlib import Path

DB_DIR = Path("db")
DB_PATH = DB_DIR / "cozzian.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SEED_PATH = DB_DIR / "seed.sql"

EXPECTED_TABLES = {
    "client_projects",
    "formulation_recipes",
    "compliance_checklists",
    "batch_test_results",
}


# ====================================================================
# Helpers
# ====================================================================

def db_connect():
    """Return an open SQLite connection for the cozzian.db database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def reseed_database():
    """Drop and recreate the database from schema.sql and seed.sql (data mutation tests use this)."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    seed_sql = SEED_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(schema_sql)
    conn.executescript(seed_sql)
    conn.commit()
    conn.close()


def ensure_project_exists(conn):
    """Return a valid project id, reseeding the DB if no projects exist."""
    row = conn.execute("SELECT id FROM client_projects LIMIT 1").fetchone()
    if row is not None:
        return row[0]
    # No projects — reseed and try again with a fresh connection
    reseed_database()
    conn.close()
    fresh = db_connect()
    row = fresh.execute("SELECT id FROM client_projects LIMIT 1").fetchone()
    assert row is not None, "Reseeded but still no projects"
    return row[0]


# ====================================================================
# 1. Connect to cozzian.db  (pytest fixture)
# ====================================================================

def test_db_path_exists():
    """cozzian.db must exist in the db/ directory."""
    assert DB_PATH.exists(), f"Database file not found: {DB_PATH}"
    assert DB_PATH.stat().st_size > 0, f"Database file is empty: {DB_PATH}"


# ====================================================================
# 2. Test that all 4 tables exist
# ====================================================================

def test_all_tables_exist():
    """Verify that the four core tables exist in the database."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    found = {row[0] for row in cursor.fetchall()}
    conn.close()

    missing = EXPECTED_TABLES - found
    assert not missing, f"Missing tables: {missing}"
    assert len(found) >= 4, f"Expected at least 4 tables, found {len(found)}: {found}"


# ====================================================================
# 3. Test seed data row counts
# ====================================================================

def test_seed_client_projects_count():
    """client_projects must have at least 3 rows (BrightC, ProbioGummy, LeanFuel)."""
    conn = db_connect()
    count = conn.execute("SELECT COUNT(*) FROM client_projects").fetchone()[0]
    conn.close()
    assert count >= 3, f"Expected >= 3 client_projects, got {count}"


def test_seed_formulation_recipes_count():
    """formulation_recipes: ≥15 (5+6+7 ingredients across 3 products)."""
    conn = db_connect()
    count = conn.execute("SELECT COUNT(*) FROM formulation_recipes").fetchone()[0]
    conn.close()
    assert count >= 15, f"Expected >= 15 formulation_recipes, got {count}"


def test_seed_compliance_checklists_count():
    """compliance_checklists must have at least 10 rows."""
    conn = db_connect()
    count = conn.execute("SELECT COUNT(*) FROM compliance_checklists").fetchone()[0]
    conn.close()
    assert count >= 10, f"Expected >= 10 compliance_checklists, got {count}"


def test_seed_batch_test_results_count():
    """batch_test_results must have at least 6 rows."""
    conn = db_connect()
    count = conn.execute("SELECT COUNT(*) FROM batch_test_results").fetchone()[0]
    conn.close()
    assert count >= 6, f"Expected >= 6 batch_test_results, got {count}"


# ====================================================================
# 4. Test nullable optional fields (edge cases)
# ====================================================================

def test_client_projects_nullable_fields():
    """
    client_projects allows NULL on: contact_name, contact_email, category,
    target_launch, budget_usd, notes.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO client_projects
            (project_name, client_company, product_type, status, start_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Null Test Project", "NullCo", "cosmetic", "active", "2025-06-01"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT * FROM client_projects WHERE id = ?", (new_id,)
    ).fetchone()

    assert row["contact_name"] is None, "contact_name should be nullable"
    assert row["contact_email"] is None, "contact_email should be nullable"
    assert row["category"] is None, "category should be nullable"
    assert row["target_launch"] is None, "target_launch should be nullable"
    assert row["budget_usd"] is None, "budget_usd should be nullable"
    assert row["notes"] is None, "notes should be nullable"

    cursor.execute("DELETE FROM client_projects WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


def test_formulation_recipes_nullable_fields():
    """
    formulation_recipes allows NULL on: weight_g, function_role, supplier,
    lot_number, cas_number, inci_name, notes.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO formulation_recipes
            (project_id, ingredient_name, percentage)
        VALUES (?, ?, ?)
        """,
        (project_id, "Mystery Ingredient X", 5.0),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT * FROM formulation_recipes WHERE id = ?", (new_id,)
    ).fetchone()

    assert row["weight_g"] is None, "weight_g should be nullable"
    assert row["function_role"] is None, "function_role should be nullable"
    assert row["supplier"] is None, "supplier should be nullable"
    assert row["lot_number"] is None, "lot_number should be nullable"
    assert row["cas_number"] is None, "cas_number should be nullable"
    assert row["inci_name"] is None, "inci_name should be nullable"
    assert row["notes"] is None, "notes should be nullable"

    cursor.execute("DELETE FROM formulation_recipes WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


def test_compliance_checklists_nullable_fields():
    """
    compliance_checklists allows NULL on: required_by, due_date, assigned_to,
    evidence_ref, notes.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO compliance_checklists
            (project_id, checklist_item, category)
        VALUES (?, ?, ?)
        """,
        (project_id, "Null field item", "general"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT * FROM compliance_checklists WHERE id = ?", (new_id,)
    ).fetchone()

    assert row["required_by"] is None, "required_by should be nullable"
    assert row["due_date"] is None, "due_date should be nullable"
    assert row["assigned_to"] is None, "assigned_to should be nullable"
    assert row["evidence_ref"] is None, "evidence_ref should be nullable"
    assert row["notes"] is None, "notes should be nullable"

    cursor.execute("DELETE FROM compliance_checklists WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


def test_batch_test_results_nullable_fields():
    """
    batch_test_results allows NULL on: recipe_id, result_value, result_unit,
    specification, tested_by, lab_notes.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO batch_test_results
            (project_id, batch_number, test_date, test_type)
        VALUES (?, ?, ?, ?)
        """,
        (project_id, "NULL-BATCH-001", "2025-07-01", "null_field_test"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT * FROM batch_test_results WHERE id = ?", (new_id,)
    ).fetchone()

    assert row["recipe_id"] is None, "recipe_id should be nullable (SET NULL)"
    assert row["result_value"] is None, "result_value should be nullable"
    assert row["result_unit"] is None, "result_unit should be nullable"
    assert row["specification"] is None, "specification should be nullable"
    assert row["tested_by"] is None, "tested_by should be nullable"
    assert row["lab_notes"] is None, "lab_notes should be nullable"

    cursor.execute("DELETE FROM batch_test_results WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


# ====================================================================
# 5. Test NOT NULL constraint enforcement
# ====================================================================

def test_client_projects_requires_project_name():
    """project_name is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO client_projects
                (client_company, product_type, start_date)
            VALUES (?, ?, ?)
            """,
            ("TestCo", "cosmetic", "2025-06-01"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing project_name, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_client_projects_requires_client_company():
    """client_company is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO client_projects
                (project_name, product_type, start_date)
            VALUES (?, ?, ?)
            """,
            ("No Company Project", "cosmetic", "2025-06-01"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing client_company, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_client_projects_requires_product_type():
    """product_type is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO client_projects
                (project_name, client_company, start_date)
            VALUES (?, ?, ?)
            """,
            ("No ProductType", "TestCo", "2025-06-01"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing product_type, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_client_projects_requires_start_date():
    """start_date is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO client_projects
                (project_name, client_company, product_type)
            VALUES (?, ?, ?)
            """,
            ("No Date Project", "TestCo", "cosmetic"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing start_date, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_formulation_recipes_requires_ingredient_name():
    """ingredient_name is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO formulation_recipes
                (project_id, percentage)
            VALUES (?, ?)
            """,
            (project_id, 10.0),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing ingredient_name, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_formulation_recipes_requires_percentage():
    """percentage is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO formulation_recipes
                (project_id, ingredient_name)
            VALUES (?, ?)
            """,
            (project_id, "Phantom Ingredient"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing percentage, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_compliance_checklists_requires_checklist_item():
    """checklist_item is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO compliance_checklists
                (project_id, category)
            VALUES (?, ?)
            """,
            (project_id, "general"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing checklist_item, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_compliance_checklists_requires_category():
    """category is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO compliance_checklists
                (project_id, checklist_item)
            VALUES (?, ?)
            """,
            (project_id, "Required category test"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing category, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_batch_test_results_requires_batch_number():
    """batch_number is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO batch_test_results
                (project_id, test_date, test_type)
            VALUES (?, ?, ?)
            """,
            (project_id, "2025-07-01", "pH"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing batch_number, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_batch_test_results_requires_test_date():
    """test_date is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO batch_test_results
                (project_id, batch_number, test_type)
            VALUES (?, ?, ?)
            """,
            (project_id, "BATCH-NODATE", "pH"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing test_date, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_batch_test_results_requires_test_type():
    """test_type is NOT NULL; inserting without it must raise IntegrityError."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]
    try:
        cursor.execute(
            """
            INSERT INTO batch_test_results
                (project_id, batch_number, test_date)
            VALUES (?, ?, ?)
            """,
            (project_id, "BATCH-NOTYPE", "2025-07-01"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for missing test_type, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


# ====================================================================
# 6. Test referential integrity — orphan rows rejected
# ====================================================================

def test_orphan_formulation_recipe_rejected():
    """Inserting a formulation_recipe with a non-existent project_id must fail."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO formulation_recipes
                (project_id, ingredient_name, percentage)
            VALUES (?, ?, ?)
            """,
            (99999, "Ghost Ingredient", 1.0),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for non-existent project_id, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_orphan_compliance_checklist_rejected():
    """Inserting a compliance_checklist with a non-existent project_id must fail."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO compliance_checklists
                (project_id, checklist_item, category)
            VALUES (?, ?, ?)
            """,
            (99999, "Ghost Checklist", "general"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for non-existent project_id, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


def test_orphan_batch_test_result_rejected():
    """Inserting a batch_test_result with a non-existent project_id must fail."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO batch_test_results
                (project_id, batch_number, test_date, test_type)
            VALUES (?, ?, ?, ?)
            """,
            (99999, "GHOST-BATCH", "2025-07-01", "pH"),
        )
        conn.commit()
        assert False, (
            "Expected IntegrityError for non-existent project_id, but insert succeeded"
        )
    except sqlite3.IntegrityError:
        pass  # Expected
    finally:
        conn.close()


# ====================================================================
# 7. Test foreign key CASCADE deletes  (run these LAST — they mutate DB)
# ====================================================================

def test_formulation_recipes_cascade_on_project_delete():
    """
    Deleting a client_project must CASCADE-delete all its formulation_recipes.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, project_name FROM client_projects LIMIT 1")
    project = cursor.fetchone()
    assert project is not None, "No projects exist to test cascade"
    project_id = project[0]
    project_name = project[1]

    cursor.execute(
        "SELECT COUNT(*) FROM formulation_recipes WHERE project_id = ?",
        (project_id,),
    )
    before_count = cursor.fetchone()[0]
    assert before_count > 0, f"Project {project_name} has no recipes to cascade"

    cursor.execute("DELETE FROM client_projects WHERE id = ?", (project_id,))
    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM formulation_recipes WHERE project_id = ?",
        (project_id,),
    )
    after_count = cursor.fetchone()[0]
    assert after_count == 0, (
        f"CASCADE failed: {before_count} formulation_recipes for project "
        f"{project_name} still exist"
    )

    conn.close()


def test_compliance_checklists_cascade_on_project_delete():
    """
    Deleting a client_project must CASCADE-delete all its compliance_checklists.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, project_name FROM client_projects LIMIT 1")
    project = cursor.fetchone()
    assert project is not None
    project_id = project[0]

    cursor.execute(
        "SELECT COUNT(*) FROM compliance_checklists WHERE project_id = ?",
        (project_id,),
    )
    before_count = cursor.fetchone()[0]
    assert before_count > 0

    cursor.execute("DELETE FROM client_projects WHERE id = ?", (project_id,))
    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM compliance_checklists WHERE project_id = ?",
        (project_id,),
    )
    after_count = cursor.fetchone()[0]
    assert after_count == 0, (
        f"CASCADE failed: {before_count} compliance_checklists still exist"
    )

    conn.close()


def test_batch_test_results_cascade_on_project_delete():
    """
    Deleting a client_project must CASCADE-delete all its batch_test_results.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, project_name FROM client_projects LIMIT 1")
    project = cursor.fetchone()
    assert project is not None
    project_id = project[0]

    cursor.execute(
        "SELECT COUNT(*) FROM batch_test_results WHERE project_id = ?",
        (project_id,),
    )
    before_count = cursor.fetchone()[0]
    assert before_count > 0

    cursor.execute("DELETE FROM client_projects WHERE id = ?", (project_id,))
    conn.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM batch_test_results WHERE project_id = ?",
        (project_id,),
    )
    after_count = cursor.fetchone()[0]
    assert after_count == 0, (
        f"CASCADE failed: {before_count} batch_test_results still exist"
    )

    conn.close()


def test_batch_test_results_set_null_on_recipe_delete():
    """
    Deleting a formulation_recipe must SET NULL the recipe_id in batch_test_results.
    """
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()

    # Find a recipe that has batch test results pointing to it
    cursor.execute(
        "SELECT DISTINCT btr.recipe_id FROM batch_test_results btr "
        "WHERE btr.recipe_id IS NOT NULL LIMIT 1"
    )
    row = cursor.fetchone()

    # If no direct link exists in seed data, insert one manually
    if row is None:
        cursor.execute("SELECT id FROM client_projects LIMIT 1")
        pid = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM formulation_recipes WHERE project_id = ? LIMIT 1", (pid,))
        recipe_row = cursor.fetchone()
        assert recipe_row is not None, "No recipes exist to test SET NULL"
        recipe_id = recipe_row[0]

        cursor.execute(
            """
            INSERT INTO batch_test_results
                (project_id, recipe_id, batch_number, test_date, test_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (pid, recipe_id, "SETNULL-BATCH", "2025-07-01", "set_null_test"),
        )
        conn.commit()
    else:
        recipe_id = row[0]

    # Count how many batch results reference it
    cursor.execute(
        "SELECT COUNT(*) FROM batch_test_results WHERE recipe_id = ?",
        (recipe_id,),
    )
    affected_count = cursor.fetchone()[0]
    assert affected_count > 0

    # Delete the recipe
    cursor.execute("DELETE FROM formulation_recipes WHERE id = ?", (recipe_id,))
    conn.commit()

    # Verify recipe_id is now NULL for those rows
    cursor.execute(
        "SELECT COUNT(*) FROM batch_test_results WHERE recipe_id = ?",
        (recipe_id,),
    )
    remaining = cursor.fetchone()[0]
    assert remaining == 0, (
        f"SET NULL failed: {remaining} batch_test_results still reference "
        f"deleted recipe_id {recipe_id}"
    )

    conn.close()


# ====================================================================
# 8. Test default values
# ====================================================================

def test_client_projects_default_status():
    """status defaults to 'active' when not specified."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO client_projects
            (project_name, client_company, product_type, start_date)
        VALUES (?, ?, ?, ?)
        """,
        ("Default Status Project", "StatusCo", "cosmetic", "2025-06-01"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT status FROM client_projects WHERE id = ?", (new_id,)
    ).fetchone()
    assert row["status"] == "active", f"Expected default status='active', got '{row['status']}'"

    cursor.execute("DELETE FROM client_projects WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


def test_compliance_checklists_default_category():
    """category defaults to 'general' when not specified."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO compliance_checklists
            (project_id, checklist_item)
        VALUES (?, ?)
        """,
        (project_id, "Default category test"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT category FROM compliance_checklists WHERE id = ?", (new_id,)
    ).fetchone()
    assert row["category"] == "general", f"Expected default category='general', got '{row['category']}'"

    cursor.execute("DELETE FROM compliance_checklists WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()


def test_batch_test_results_default_passed():
    """passed defaults to 1 (True) when not specified."""
    reseed_database()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM client_projects LIMIT 1")
    project_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO batch_test_results
            (project_id, batch_number, test_date, test_type)
        VALUES (?, ?, ?, ?)
        """,
        (project_id, "DEFAULT-PASS", "2025-07-01", "default_test"),
    )
    new_id = cursor.lastrowid
    conn.commit()

    row = cursor.execute(
        "SELECT passed FROM batch_test_results WHERE id = ?", (new_id,)
    ).fetchone()
    assert row["passed"] == 1, f"Expected default passed=1, got {row['passed']}"

    cursor.execute("DELETE FROM batch_test_results WHERE id = ?", (new_id,))
    conn.commit()
    conn.close()