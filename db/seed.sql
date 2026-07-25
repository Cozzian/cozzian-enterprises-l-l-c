-- =============================================================================
-- Cozzian Enterprises LLC — Seed Data
-- 3 sample product lines: Vitamin C Serum, Probiotic Gummy, Protein Bar
-- =============================================================================

PRAGMA foreign_keys=ON;

-- -----------------------------------------------------------------------------
-- CLIENT PROJECTS
-- -----------------------------------------------------------------------------
INSERT INTO client_projects (project_name, client_company, contact_name, contact_email,
                             product_type, category, status, start_date, target_launch,
                             budget_usd, notes)
VALUES
    ('BrightC M2 Serum',
     'GlowAesthetic Labs',
     'Maria Chen',
     'm.chen@glowaesthetic.io',
     'cosmetic',
     'serum',
     'active',
     '2025-01-15',
     '2025-06-01',
     45000.00,
     'Stable 20% L-ascorbic acid serum with ferulic acid and vitamin E. Need airless packaging compatibility.'),

    ('ProbioGummy Plus',
     'GutWell Brands',
     'James Okafor',
     'j.okafor@gutwell.co',
     'nutraceutical',
     'gummy',
     'active',
     '2025-02-01',
     '2025-07-15',
     62000.00,
     '10B CFU/g shelf-stable probiotic gummy. Pectin-based, no gelatin. Stability 24 months at 25°C.'),

    ('LeanFuel Protein Bar',
     'Peak Nutrition Inc.',
     'Sofia Ramirez',
     's.ramirez@peaknutrition.com',
     'food_beverage',
     'bar',
     'active',
     '2025-03-01',
     '2025-08-30',
     78000.00,
     '20g plant protein bar, chocolate-coating enrobed. No sugar alcohols — use allulose + monk fruit.');

-- -----------------------------------------------------------------------------
-- FORMULATION RECIPES  (3–5 ingredients per product)
-- -----------------------------------------------------------------------------
-- Vitamin C Serum ingredients (project_id = 1)
INSERT INTO formulation_recipes (project_id, version, ingredient_name, percentage, weight_g,
                                 function_role, supplier, inci_name, cas_number, notes)
VALUES
    (1, 'v1.0', 'L-Ascorbic Acid',            20.0, 100.0, 'active',        'DSM',         'Ascorbic Acid',             '50-81-7',    'Stay at pH < 3.5 for stability'),
    (1, 'v1.0', 'Ferulic Acid',                0.5,   2.5, 'stabilizer',    'Sigma-Aldrich','Ferulic Acid',              '1135-24-6',  'Dissolve in ethanol first'),
    (1, 'v1.0', 'Tocopherol (Vitamin E)',      1.0,   5.0, 'antioxidant',   'BASF',        'Tocopherol',                '59-02-9',    'Oil-soluble; add after water phase cools'),
    (1, 'v1.0', 'Butylene Glycol',             3.0,  15.0, 'solvent',       'Jeen',        'Butylene Glycol',           '107-88-0',   'Helps dissolve LAA'),
    (1, 'v1.0', 'Purified Water (Aqua)',      75.5, 377.5, 'base',         'In-house',    'Aqua',                      '7732-18-5',  'Deionised, N2-purged');

-- Probiotic Gummy ingredients (project_id = 2)
INSERT INTO formulation_recipes (project_id, version, ingredient_name, percentage, weight_g,
                                 function_role, supplier, inci_name, cas_number, notes)
VALUES
    (2, 'v1.0', 'Probiotic Blend (B. coagulans)', 2.0,  20.0, 'active',       'Deerland',   'Bacillus coagulans',        'N/A',         '10B CFU/g at overage 120%'),
    (2, 'v1.0', 'Pectin (Low Methoxyl)',           7.0,  70.0, 'gelling',     'CP Kelco',   'Pectin',                    '9000-69-5',  'LM type for sugar-reduced gummy'),
    (2, 'v1.0', 'Allulose',                       25.0, 250.0, 'sweetener',   'Tate & Lyle','Allulose',                   '551-68-8',   'Bulk sweetener, ~70% sucrose sweetness'),
    (2, 'v1.0', 'Monk Fruit Extract (50x)',         0.4,   4.0, 'sweetener',   'Layn',       'Siraitia grosvenorii fruit','N/A',         'High-intensity; adjust to taste'),
    (2, 'v1.0', 'Citric Acid',                     1.0,  10.0, 'acidulant',   'ADM',        'Citric Acid',               '77-92-9',    'pH ~3.8 for microbial stability'),
    (2, 'v1.0', 'Purified Water',                 64.6, 646.0, 'base',       'In-house',    'Aqua',                      '7732-18-5',  'Pre-heat to 80°C for pectin hydration');

-- Protein Bar ingredients (project_id = 3)
INSERT INTO formulation_recipes (project_id, version, ingredient_name, percentage, weight_g,
                                 function_role, supplier, inci_name, cas_number, notes)
VALUES
    (3, 'v1.0', 'Pea Protein Isolate (80%)',      30.0, 150.0, 'protein',     'Roquette',   'Pisum sativum protein',     'N/A',         'Nutralys S85F — high dispersibility'),
    (3, 'v1.0', 'Brown Rice Syrup',               32.0, 160.0, 'binder',      'Malt Products', 'Oryza sativa syrup',     'N/A',         'Humectant for soft texture'),
    (3, 'v1.0', 'Allulose',                       10.0,  50.0, 'sweetener',   'Tate & Lyle','Allulose',                   '551-68-8',   'Helps reduce water activity'),
    (3, 'v1.0', 'Cocoa Butter',                   14.0,  70.0, 'fat',         'Barry Callebaut','Theobroma cacao seed butter','8002-31-1','Coating enrobed later; 5% in bar'),
    (3, 'v1.0', 'Natural Chocolate Flavor',         1.5,   7.5, 'flavor',     'Firmenich',  'N/A',                       'N/A',         'Heat-stable at 60°C'),
    (3, 'v1.0', 'Salt (Sea)',                      0.5,   2.5, 'flavor',      'Morton Salt','Sodium Chloride',            '7647-14-5',  'Enhances sweetness perception'),
    (3, 'v1.0', 'Water',                          12.0,  60.0, 'processing aid','In-house', 'Aqua',                      '7732-18-5',  'Evaporates during baking');

-- -----------------------------------------------------------------------------
-- COMPLIANCE CHECKLISTS  (3–4 items per project)
-- -----------------------------------------------------------------------------
INSERT INTO compliance_checklists (project_id, checklist_item, category, required_by,
                                   is_met, due_date, assigned_to, evidence_ref, notes)
VALUES
    -- Vitamin C Serum
    (1, 'Stability testing: 3 months at 40°C / 75% RH',        'safety',       'FDA 21 CFR 700',         1, '2025-04-15', 'R&D Lab',     'STB-001-25.pdf', 'Passed accelerated; colour stable'),
    (1, 'pH verification report (target 3.0–3.5)',              'safety',       'FDA 21 CFR 700',         1, '2025-03-01', 'QC Team',     'pH-001-25.pdf',  'pH 3.2 at T=0, 3.4 at 40°C/2wk'),
    (1, 'INCI ingredient listing + EU allergen declaration',    'labeling',     'EU Reg 1223/2009',       0, '2025-05-01', 'Regulatory',  NULL,             'Awaiting final fragrance spec'),
    (1, 'Preservation efficacy test (USP 51 / EP 5.1.1)',       'safety',       'USP <51>',               0, '2025-04-30', 'Micro Lab',   NULL,             'Need to challenge with E. coli + S. aureus'),

    -- Probiotic Gummy
    (2, 'Probiotic viability at T=0, 3, 6, 12, 18, 24 months', 'safety',       'FDA DSHEA / USP',        1, '2025-06-01', 'R&D Lab',     'VIA-001-25.pdf', '10.8B CFU/g at T=0 (8% overage)'),
    (2, 'Nutrition facts panel — moisture & water activity',    'labeling',     'FDA 21 CFR 101',         0, '2025-05-15', 'QC Team',     NULL,             'Aw < 0.60 target; need Aw measurement'),
    (2, 'Heavy metals (Pb, As, Cd, Hg) ICP-MS screen',         'safety',       'USP <232>/<233>',        1, '2025-03-10', '3rd Party',   'HM-089-25.pdf',  'All below 50% of limits'),
    (2, 'EU Novel Food dossier readiness',                     'import_export','EU Reg 2015/2283',        0, '2025-09-01', 'Regulatory',  NULL,             'B. coagulans not yet authorised in EU'),

    -- Protein Bar
    (3, 'Microbiology: APC, Yeast, Mold, Coliforms (CMMEF)',   'safety',       'FDA 21 CFR 110',         1, '2025-04-01', 'Micro Lab',   'MB-022-25.pdf',  'APC < 1000 CFU/g, no coliforms'),
    (3, 'Nutritional label validation — protein % by Kjeldahl', 'labeling',    'FDA 21 CFR 101.9',       0, '2025-06-01', 'QC Team',     NULL,             'Target 20g/serving; Kjeldahl scheduled'),
    (3, 'Allergen cross-contact risk assessment',              'safety',       'FDA FALCPA 2004',        1, '2025-03-20', 'Ops Team',    'ALLERGEN-RA.pdf','Shared line with soy; CIP validated'),
    (3, 'Organic / Non-GMO Project verification paperwork',    'labeling',     'USDA NOP / Non-GMO Proj',0, '2025-07-01', 'Regulatory',  NULL,             'Supplier docs for pea protein pending');

-- -----------------------------------------------------------------------------
-- BATCH TEST RESULTS  (2–3 per project)
-- -----------------------------------------------------------------------------
INSERT INTO batch_test_results (project_id, recipe_id, batch_number, test_date, test_type,
                                result_value, result_unit, specification, passed, tested_by, lab_notes)
VALUES
    -- Vitamin C Serum Batch
    (1, 1, 'BCH-VC-001', '2025-02-10', 'pH',              3.2, 'pH',   '3.0–3.5', 1, 'L. Tran', 'Within spec; LAA fully dissolved'),
    (1, 1, 'BCH-VC-001', '2025-02-10', 'Viscosity',    150.0, 'cP',   '100–300 cP', 1, 'L. Tran', 'Good spreadability at 25°C'),
    (1, 1, 'BCH-VC-001', '2025-02-10', 'LAA Potency (HPLC)', 19.8, '%', '≥19.0%', 1, 'HPLC Lab', '99% of label claim; within spec'),

    -- Probiotic Gummy Batch
    (2, 6, 'BCH-PG-001', '2025-03-05', 'Probiotic Viability', 10.8, 'B CFU/g', '≥10.0 B CFU/g', 1, 'A. Kim', 'Overage of 8% provides margin'),
    (2, 6, 'BCH-PG-001', '2025-03-05', 'Water Activity',     0.58, 'Aw',       '≤0.60 Aw',       1, 'A. Kim', 'Target met; good microbial barrier'),
    (2, 6, 'BCH-PG-001', '2025-03-05', 'pH',                 3.8, 'pH',       '3.5–4.0',        1, 'A. Kim', 'Optimal for pectin gel and microbial control'),

    -- Protein Bar Batch
    (3, 9, 'BCH-PB-001', '2025-04-02', 'Protein (Kjeldahl)', 20.4, 'g/serving', '≥20.0 g/serving', 1, 'J. Park', 'Exceeds label claim by 2%'),
    (3, 9, 'BCH-PB-001', '2025-04-02', 'Water Activity',      0.52, 'Aw',        '≤0.60 Aw',        1, 'J. Park', 'Low Aw ensures 12-month shelf life'),
    (3, 9, 'BCH-PB-001', '2025-04-02', 'Hardness (TA.XT2)', 1800, 'g-force',  '1500–2200 g-force',1, 'J. Park', 'Textural profile ideal for enrobing');