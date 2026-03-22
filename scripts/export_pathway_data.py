"""Export pathway data from kc-industries into a read-only SQLite database.

Creates data/pathway_data.db with a curated subset of tables from
the kc-industries app.sqlite. This database is read-only at runtime —
students drill down into this data but never write to it.

Usage:
    python scripts/export_pathway_data.py

Source: C:\\Users\\admir\\Github\\kc-industries\\instance\\app.sqlite
Target: data/pathway_data.db
"""

import os
import sqlite3

SOURCE_DB = r"C:\Users\admir\Github\kc-industries\instance\app.sqlite"
TARGET_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pathway_data.db")


def parse_wage(wage_str):
    """Parse formatted wage string like '$206,420' to float."""
    if not wage_str:
        return None
    try:
        return float(str(wage_str).replace("$", "").replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def export():
    """Export curated tables from kc-industries to pathway_data.db."""
    if not os.path.exists(SOURCE_DB):
        print(f"ERROR: Source database not found: {SOURCE_DB}")
        return

    # Remove old export if it exists
    if os.path.exists(TARGET_DB):
        os.remove(TARGET_DB)
        print(f"Removed old {TARGET_DB}")

    os.makedirs(os.path.dirname(TARGET_DB), exist_ok=True)

    src = sqlite3.connect(SOURCE_DB)
    src.row_factory = sqlite3.Row
    dst = sqlite3.connect(TARGET_DB)

    # --- Programs with earnings data ---
    print("\n1. Exporting programs...")
    dst.execute("""
        CREATE TABLE programs (
            program_id INTEGER PRIMARY KEY,
            institution_id INTEGER,
            institution_name TEXT,
            program_name TEXT,
            credential_type TEXT,
            cip_code TEXT,
            completions INTEGER,
            median_earnings_1yr REAL,
            median_earnings_2yr REAL,
            median_earnings_4yr REAL,
            earnings_count INTEGER,
            description TEXT,
            url TEXT
        )
    """)

    rows = src.execute("""
        SELECT
            p.program_id,
            pv.provider_id AS institution_id,
            pv.name AS institution_name,
            p.name AS program_name,
            p.credential_type,
            p.cip AS cip_code,
            p.completions,
            se.median_earnings_1yr,
            se.median_earnings_2yr,
            se.median_earnings_4yr,
            se.count AS earnings_count,
            p.description,
            p.url
        FROM program p
        LEFT JOIN provider pv ON p.org_id = pv.provider_id
        LEFT JOIN scorecard_institution si ON pv.scorecard_unitid = si.unitid
        LEFT JOIN scorecard_earning se
            ON si.unitid = se.unitid
            AND REPLACE(p.cip, '.', '') LIKE REPLACE(se.cip_code, '.', '') || '%'
    """).fetchall()

    dst.executemany(
        "INSERT INTO programs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} program rows")

    # --- Institutions ---
    print("\n2. Exporting institutions...")
    dst.execute("""
        CREATE TABLE institutions (
            institution_id INTEGER PRIMARY KEY,
            name TEXT,
            institution_type TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            latitude REAL,
            longitude REAL,
            ownership TEXT,
            locale TEXT,
            website TEXT,
            scorecard_unitid INTEGER
        )
    """)

    rows = src.execute("""
        SELECT
            pv.provider_id,
            COALESCE(si.name, pv.name),
            pv.provider_type,
            si.city,
            si.state,
            si.zip_code,
            COALESCE(si.latitude, pv.latitude),
            COALESCE(si.longitude, pv.longitude),
            si.ownership,
            si.locale,
            pv.website,
            pv.scorecard_unitid
        FROM provider pv
        LEFT JOIN scorecard_institution si ON pv.scorecard_unitid = si.unitid
    """).fetchall()

    dst.executemany(
        "INSERT INTO institutions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} institution rows")

    # --- Occupations ---
    print("\n3. Exporting occupations...")
    dst.execute("""
        CREATE TABLE occupations (
            soc_code TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            group_type TEXT,
            education_required TEXT,
            experience_required TEXT,
            training_required TEXT,
            median_wage REAL,
            employment_current REAL,
            employment_projected REAL,
            projected_growth_pct REAL,
            projected_openings REAL
        )
    """)

    raw_rows = src.execute("""
        SELECT
            soc, title, description, group_type,
            education_required, experience_required, training_required,
            median_wage,
            employment_2024, employment_2034,
            projected_change_pct, projected_openings
        FROM occupation
        WHERE group_type = 'detailed'
    """).fetchall()

    # Parse the median_wage from formatted string to float
    parsed = []
    for r in raw_rows:
        row = list(r)
        row[7] = parse_wage(row[7])  # median_wage
        parsed.append(tuple(row))

    dst.executemany(
        "INSERT INTO occupations VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        parsed,
    )
    print(f"   {len(parsed)} occupation rows (detailed only)")

    # --- Program-Occupation links ---
    print("\n4. Exporting program-occupation links...")
    dst.execute("""
        CREATE TABLE program_occupations (
            id INTEGER PRIMARY KEY,
            program_id INTEGER,
            soc_code TEXT,
            confidence REAL,
            FOREIGN KEY (program_id) REFERENCES programs(program_id)
        )
    """)

    rows = src.execute("""
        SELECT id, program_id, soc, confidence
        FROM program_occupation
    """).fetchall()

    dst.executemany(
        "INSERT INTO program_occupations VALUES (?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} link rows")

    # --- Employers ---
    print("\n5. Exporting employers...")
    dst.execute("""
        CREATE TABLE employers (
            employer_id INTEGER PRIMARY KEY,
            name TEXT,
            naics_code TEXT,
            naics_sector TEXT,
            estimated_headcount INTEGER,
            employee_range TEXT,
            employer_type TEXT,
            city TEXT,
            state TEXT,
            latitude REAL,
            longitude REAL,
            county_fips TEXT,
            description TEXT,
            data_source TEXT
        )
    """)

    rows = src.execute("""
        SELECT
            org_id, name, naics, naics AS naics_sector,
            estimated_headcount, headcount_source,
            employer_type, city, state,
            latitude, longitude, county_fips,
            description, data_source
        FROM organization
        WHERE org_type = 'employer'
    """).fetchall()

    dst.executemany(
        "INSERT INTO employers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} employer rows")

    # --- Sector profiles ---
    print("\n6. Exporting sector profiles...")
    dst.execute("""
        CREATE TABLE sector_profiles (
            naics TEXT PRIMARY KEY,
            overview TEXT,
            unique_factors TEXT,
            risks TEXT,
            opportunities TEXT,
            watch_items TEXT
        )
    """)

    rows = src.execute("""
        SELECT naics, overview, unique_factors, risks, opportunities, watch_items
        FROM sector_profile
    """).fetchall()

    dst.executemany(
        "INSERT INTO sector_profiles VALUES (?,?,?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} sector profile rows")

    # --- Provider sectors ---
    print("\n7. Exporting institution sectors...")
    dst.execute("""
        CREATE TABLE institution_sectors (
            id INTEGER PRIMARY KEY,
            institution_id INTEGER,
            sector_code TEXT,
            sector_name TEXT,
            program_count INTEGER,
            total_completions INTEGER,
            primary_cip_family TEXT,
            FOREIGN KEY (institution_id) REFERENCES institutions(institution_id)
        )
    """)

    rows = src.execute("""
        SELECT id, org_id, sector_code, sector_name,
               program_count, total_completions, primary_cip_family
        FROM provider_sector
    """).fetchall()

    dst.executemany(
        "INSERT INTO institution_sectors VALUES (?,?,?,?,?,?,?)",
        [tuple(r) for r in rows],
    )
    print(f"   {len(rows)} institution-sector rows")

    # --- Create indexes ---
    print("\n8. Creating indexes...")
    dst.execute("CREATE INDEX idx_programs_cip ON programs(cip_code)")
    dst.execute("CREATE INDEX idx_programs_inst ON programs(institution_id)")
    dst.execute("CREATE INDEX idx_program_occ_prog ON program_occupations(program_id)")
    dst.execute("CREATE INDEX idx_program_occ_soc ON program_occupations(soc_code)")
    dst.execute("CREATE INDEX idx_employers_naics ON employers(naics_code)")
    dst.execute("CREATE INDEX idx_employers_county ON employers(county_fips)")
    dst.execute("CREATE INDEX idx_inst_sectors_inst ON institution_sectors(institution_id)")

    dst.commit()

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print(f"Export complete: {TARGET_DB}")
    print(f"Size: {os.path.getsize(TARGET_DB) / 1024:.0f} KB")
    print(f"{'=' * 60}")

    for table in ["programs", "institutions", "occupations",
                   "program_occupations", "employers", "sector_profiles",
                   "institution_sectors"]:
        count = dst.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:30s} {count:>6,} rows")

    dst.close()
    src.close()


if __name__ == "__main__":
    export()
