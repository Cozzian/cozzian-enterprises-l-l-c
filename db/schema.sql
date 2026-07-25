-- =============================================================================
-- Cozzian Enterprises LLC — Database Schema
-- Formulation Science & R&D Prototyping
-- =============================================================================
-- Tables: client_projects, formulation_recipes, compliance_checklists,
--         batch_test_results
-- =============================================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- -----------------------------------------------------------------------------
-- 1. client_projects — each brand engagement / R&D project
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS client_projects (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name    TEXT    NOT NULL,
    client_company  TEXT    NOT NULL,
    contact_name    TEXT,
    contact_email   TEXT,
    product_type    TEXT    NOT NULL,          -- e.g. 'cosmetic', 'nutraceutical', 'pharmaceutical', 'food_beverage'
    category        TEXT,                     -- e.g. 'serum', 'gummy', 'bar', 'cream', 'capsule'
    status          TEXT    NOT NULL DEFAULT 'active',   -- active | on_hold | completed | cancelled
    start_date      DATE    NOT NULL,
    target_launch   DATE,
    budget_usd      REAL,
    notes           TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 2. formulation_recipes — every recipe iteration per project
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS formulation_recipes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL REFERENCES client_projects(id) ON DELETE CASCADE,
    version         TEXT    NOT NULL DEFAULT 'v1.0',  -- e.g. v1.0, v2.1
    ingredient_name TEXT    NOT NULL,
    percentage      REAL    NOT NULL,            -- percentage of total formula
    weight_g        REAL,                       -- actual grams in this batch size
    function_role   TEXT,                       -- e.g. 'active', 'emulsifier', 'preservative', 'binder'
    supplier        TEXT,
    lot_number      TEXT,
    cas_number      TEXT,                       -- Chemical Abstracts Service number
    inci_name       TEXT,                       -- International Nomenclature of Cosmetic Ingredients
    notes           TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 3. compliance_checklists — regulatory readiness per project
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS compliance_checklists (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL REFERENCES client_projects(id) ON DELETE CASCADE,
    checklist_item  TEXT    NOT NULL,
    category        TEXT    NOT NULL DEFAULT 'general',   -- general | labeling | safety | claims | import_export
    required_by     TEXT,                                -- e.g. 'FDA', 'EU Cos Regulation', 'FTC'
    is_met          INTEGER NOT NULL DEFAULT 0,          -- 0 = not met, 1 = met
    due_date        DATE,
    assigned_to     TEXT,
    evidence_ref    TEXT,                                -- link or filename of supporting doc
    notes           TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 4. batch_test_results — lab-test outcomes per batch / recipe version
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batch_test_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL REFERENCES client_projects(id) ON DELETE CASCADE,
    recipe_id       INTEGER REFERENCES formulation_recipes(id) ON DELETE SET NULL,
    batch_number    TEXT    NOT NULL,
    test_date       DATE    NOT NULL,
    test_type       TEXT    NOT NULL,            -- e.g. 'pH', 'viscosity', 'potency', 'microbiology', 'stability'
    result_value    REAL,
    result_unit     TEXT,                        -- e.g. 'pH', 'cP', 'CFU/g', '%', 'mg/g'
    specification   TEXT,                        -- e.g. '4.5–5.5', '<100 CFU/g'
    passed          INTEGER NOT NULL DEFAULT 1,  -- 0 = fail, 1 = pass
    tested_by       TEXT,
    lab_notes       TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_formulation_project ON formulation_recipes(project_id);
CREATE INDEX IF NOT EXISTS idx_compliance_project  ON compliance_checklists(project_id);
CREATE INDEX IF NOT EXISTS idx_batch_project       ON batch_test_results(project_id);
CREATE INDEX IF NOT EXISTS idx_batch_recipe        ON batch_test_results(recipe_id);