"""Import curated IPEDS institution_profiles.csv into pathway_data.db as ipeds_profiles table."""
import csv
import sqlite3
import sys

DB_PATH = "data/pathway_data.db"
CSV_PATH = "data/ipeds-report/institution_profiles.csv"

def safe_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v.replace(",", ""))
    except (ValueError, AttributeError):
        return None

def safe_int(v):
    f = safe_float(v)
    return int(f) if f is not None else None

def main():
    # Read CSV
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Read {len(rows)} institutions from CSV")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Drop & recreate ipeds_profiles table
    c.execute("DROP TABLE IF EXISTS ipeds_profiles")
    c.execute("""
        CREATE TABLE ipeds_profiles (
            unitid INTEGER PRIMARY KEY,
            institution_name TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            county TEXT,
            distance_from_kc REAL,
            tier INTEGER,
            tier_label TEXT,
            control TEXT,
            level TEXT,
            sector TEXT,
            institution_size TEXT,
            degree_granting TEXT,
            locale TEXT,
            hbcu TEXT,
            website TEXT,

            -- Completions
            total_completions INTEGER,
            unique_programs INTEGER,
            top_cip_family TEXT,
            top_cip_completions INTEGER,
            cert_completions INTEGER,
            assoc_completions INTEGER,
            bach_completions INTEGER,
            master_completions INTEGER,
            doctoral_completions INTEGER,

            -- Enrollment
            total_enrollment INTEGER,
            undergrad_enrollment INTEGER,
            grad_enrollment INTEGER,
            ft_enrollment INTEGER,
            pt_enrollment INTEGER,
            ft_pct REAL,
            male_enrollment INTEGER,
            female_enrollment INTEGER,

            -- Demographics
            pct_white REAL,
            pct_black REAL,
            pct_hispanic REAL,
            pct_asian REAL,
            pct_aian REAL,
            pct_nhpi REAL,
            pct_two_plus REAL,
            pct_unknown REAL,
            pct_nonresident REAL,

            -- Graduation & Outcomes
            yield_rate REAL,
            gr_cohort_type TEXT,
            gr_cohort_size INTEGER,
            gr_completers INTEGER,
            graduation_rate REAL,
            om_adjusted_cohort INTEGER,
            award_rate_4yr REAL,
            award_rate_6yr REAL,
            award_rate_8yr REAL,
            still_enrolled_8yr REAL,
            awards_4yr INTEGER,
            awards_6yr INTEGER,
            awards_8yr INTEGER,
            cert_8yr INTEGER,
            assoc_8yr INTEGER,
            bach_8yr INTEGER,

            -- Financial Aid
            sfa_ug_students INTEGER,
            sfa_ftft_students INTEGER,
            ftft_pct_ug REAL,
            any_aid_pct REAL,
            any_aid_count INTEGER,
            any_grant_pct REAL,
            any_grant_count INTEGER,
            avg_grant_amount REAL,
            pell_grant_pct REAL,
            pell_grant_count INTEGER,
            avg_pell_amount REAL,
            fed_loan_pct REAL,
            fed_loan_count INTEGER,
            avg_fed_loan REAL,
            avg_total_grant_ftft REAL,
            avg_fed_grant_ftft REAL,
            avg_state_grant_ftft REAL,
            avg_institutional_grant_ftft REAL,
            avg_loan_ftft REAL,
            avg_fed_loan_ftft REAL
        )
    """)

    # Map CSV column names → table columns
    col_map = {
        "UNITID": ("unitid", safe_int),
        "Institution Name": ("institution_name", str),
        "City": ("city", str),
        "State": ("state", str),
        "ZIP": ("zip_code", str),
        "County": ("county", str),
        "Distance from KC (mi)": ("distance_from_kc", safe_float),
        "Tier": ("tier", safe_int),
        "Tier Label": ("tier_label", str),
        "Control": ("control", str),
        "Level": ("level", str),
        "Sector": ("sector", str),
        "Institution Size": ("institution_size", str),
        "Degree-Granting": ("degree_granting", str),
        "Locale": ("locale", str),
        "HBCU": ("hbcu", str),
        "Website": ("website", str),
        "Total Completions (2024)": ("total_completions", safe_int),
        "Unique Programs (2024)": ("unique_programs", safe_int),
        "Top CIP Family (2024)": ("top_cip_family", str),
        "Top CIP Family Completions (2024)": ("top_cip_completions", safe_int),
        "Certificate Completions (2024)": ("cert_completions", safe_int),
        "Associate's Completions (2024)": ("assoc_completions", safe_int),
        "Bachelor's Completions (2024)": ("bach_completions", safe_int),
        "Master's Completions (2024)": ("master_completions", safe_int),
        "Doctoral Completions (2024)": ("doctoral_completions", safe_int),
        "12-Mo Total Enrollment": ("total_enrollment", safe_int),
        "12-Mo Undergraduate": ("undergrad_enrollment", safe_int),
        "12-Mo Graduate": ("grad_enrollment", safe_int),
        "12-Mo Full-Time": ("ft_enrollment", safe_int),
        "12-Mo Part-Time": ("pt_enrollment", safe_int),
        "Full-Time %": ("ft_pct", safe_float),
        "12-Mo Total Male": ("male_enrollment", safe_int),
        "12-Mo Total Female": ("female_enrollment", safe_int),
        "Enrl % White": ("pct_white", safe_float),
        "Enrl % Black": ("pct_black", safe_float),
        "Enrl % Hispanic": ("pct_hispanic", safe_float),
        "Enrl % Asian": ("pct_asian", safe_float),
        "Enrl % AIAN": ("pct_aian", safe_float),
        "Enrl % NHPI": ("pct_nhpi", safe_float),
        "Enrl % Two+": ("pct_two_plus", safe_float),
        "Enrl % Unknown": ("pct_unknown", safe_float),
        "Enrl % Nonresident": ("pct_nonresident", safe_float),
        "Yield Rate (%)": ("yield_rate", safe_float),
        "GR Cohort Type": ("gr_cohort_type", str),
        "GR Cohort Size": ("gr_cohort_size", safe_int),
        "GR Completers (150%)": ("gr_completers", safe_int),
        "Graduation Rate (%)": ("graduation_rate", safe_float),
        "OM Adjusted Cohort": ("om_adjusted_cohort", safe_int),
        "Award Rate 4yr (%)": ("award_rate_4yr", safe_float),
        "Award Rate 6yr (%)": ("award_rate_6yr", safe_float),
        "Award Rate 8yr (%)": ("award_rate_8yr", safe_float),
        "Still Enrolled 8yr (%)": ("still_enrolled_8yr", safe_float),
        "Awards at 4yr": ("awards_4yr", safe_int),
        "Awards at 6yr": ("awards_6yr", safe_int),
        "Awards at 8yr": ("awards_8yr", safe_int),
        "Cert at 8yr": ("cert_8yr", safe_int),
        "Assoc at 8yr": ("assoc_8yr", safe_int),
        "Bach at 8yr": ("bach_8yr", safe_int),
        "SFA UG Students": ("sfa_ug_students", safe_int),
        "SFA FTFT Students": ("sfa_ftft_students", safe_int),
        "FTFT % of UG": ("ftft_pct_ug", safe_float),
        "Any Aid (%)": ("any_aid_pct", safe_float),
        "Any Aid Count": ("any_aid_count", safe_int),
        "Any Grant (%)": ("any_grant_pct", safe_float),
        "Any Grant Count": ("any_grant_count", safe_int),
        "Avg Grant Amount": ("avg_grant_amount", safe_float),
        "Pell Grant (%)": ("pell_grant_pct", safe_float),
        "Pell Grant Count": ("pell_grant_count", safe_int),
        "Avg Pell Amount": ("avg_pell_amount", safe_float),
        "Federal Loan (%)": ("fed_loan_pct", safe_float),
        "Federal Loan Count": ("fed_loan_count", safe_int),
        "Avg Federal Loan": ("avg_fed_loan", safe_float),
        "Avg Total Grant (FTFT)": ("avg_total_grant_ftft", safe_float),
        "Avg Federal Grant (FTFT)": ("avg_fed_grant_ftft", safe_float),
        "Avg State Grant (FTFT)": ("avg_state_grant_ftft", safe_float),
        "Avg Institutional Grant (FTFT)": ("avg_institutional_grant_ftft", safe_float),
        "Avg Loan (FTFT)": ("avg_loan_ftft", safe_float),
        "Avg Federal Loan (FTFT)": ("avg_fed_loan_ftft", safe_float),
    }

    inserted = 0
    for row in rows:
        record = {}
        for csv_col, (db_col, converter) in col_map.items():
            raw = row.get(csv_col, "")
            if converter == str:
                record[db_col] = raw if raw else None
            else:
                record[db_col] = converter(raw)

        if not record.get("unitid"):
            continue

        cols = list(record.keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        c.execute(
            f"INSERT OR REPLACE INTO ipeds_profiles ({col_names}) VALUES ({placeholders})",
            [record[col] for col in cols],
        )
        inserted += 1

    conn.commit()

    # Verify: match our institutions table to ipeds_profiles via scorecard_unitid
    matched = c.execute("""
        SELECT i.institution_id, i.name, i.scorecard_unitid, ip.total_enrollment, ip.graduation_rate, ip.pell_grant_pct
        FROM institutions i
        JOIN ipeds_profiles ip ON i.scorecard_unitid = ip.unitid
    """).fetchall()
    print(f"\nInserted {inserted} IPEDS profiles")
    print(f"Matched {len(matched)} of our existing institutions:")
    for m in matched:
        print(f"  id={m[0]} | {m[1]} | unitid={m[2]} | enroll={m[3]} | grad_rate={m[4]} | pell={m[5]}%")

    conn.close()

if __name__ == "__main__":
    main()
