"""Analyze kc-industries data to build pathway aggregates for YAML seed files."""
import csv
import json
from collections import defaultdict

CSV_PATH = r"C:\Users\admir\Github\kc-industries\data\exports\kc_program_pathways.csv"
EMP_PATH = r"C:\Users\admir\Github\kc-industries\data\processed\major_employers_geocoded.json"

# CIP 2-digit prefix to pathway family mapping
CIP_TO_PATHWAY = {
    "51": "healthcare", "26": "healthcare",
    "52": "business", "27": "business",
    "14": "manufacturing", "15": "manufacturing",
    "46": "manufacturing", "47": "manufacturing", "48": "manufacturing",
    "49": "logistics",
    "11": "tech", "10": "tech",
    "13": "education",
    "22": "law_public", "43": "law_public", "44": "law_public",
}

# NAICS to pathway mapping for employers
NAICS_TO_PATHWAY = {
    "62": "healthcare",
    "52": "business", "53": "business", "55": "business",
    "31-33": "manufacturing", "23": "manufacturing",
    "42": "logistics", "48-49": "logistics",
    "51": "tech", "54": "tech",
    "61": "education",
    "92": "law_public", "56": "law_public",
}


def analyze_programs():
    rows = list(csv.DictReader(open(CSV_PATH, "r")))
    pw = defaultdict(lambda: {"wages": [], "employment": [], "growth": [],
                               "openings": [], "programs": 0, "cips": set()})
    unmapped = defaultdict(int)

    for r in rows:
        cip = r.get("cip_code", "")[:2]
        pathway = CIP_TO_PATHWAY.get(cip)
        if not pathway:
            unmapped[cip] += 1
            continue
        pw[pathway]["programs"] += 1
        pw[pathway]["cips"].add(cip)
        try:
            pw[pathway]["wages"].append(float(r["linked_local_median_wage"]))
        except (ValueError, KeyError):
            pass
        try:
            pw[pathway]["employment"].append(float(r["linked_local_employment"]))
        except (ValueError, KeyError):
            pass
        try:
            pw[pathway]["growth"].append(float(r["linked_projected_growth_pct"]))
        except (ValueError, KeyError):
            pass
        try:
            pw[pathway]["openings"].append(float(r["linked_projected_openings_k"]))
        except (ValueError, KeyError):
            pass

    print("PATHWAY AGGREGATES FROM PROGRAM DATA:")
    print("-" * 80)
    for name, d in sorted(pw.items(), key=lambda x: -x[1]["programs"]):
        avg_wage = sum(d["wages"]) / len(d["wages"]) if d["wages"] else 0
        avg_growth = sum(d["growth"]) / len(d["growth"]) if d["growth"] else 0
        total_emp = sum(d["employment"]) if d["employment"] else 0
        avg_open = sum(d["openings"]) / len(d["openings"]) if d["openings"] else 0
        print(f"  {name:20s} | {d['programs']:3d} programs | "
              f"avg wage ${avg_wage:>8,.0f} | growth {avg_growth:>5.1f}% | "
              f"openings {avg_open:>6.1f}k | CIPs: {sorted(d['cips'])}")

    print(f"\nUnmapped CIPs ({sum(unmapped.values())} programs):")
    for c, n in sorted(unmapped.items(), key=lambda x: -x[1]):
        print(f"  CIP {c}: {n} programs")


def analyze_employers():
    with open(EMP_PATH, "r") as f:
        data = json.load(f)
    emps = data.get("employers", [])

    pw_emps = defaultdict(list)
    unmapped_naics = defaultdict(int)

    for e in emps:
        naics = e.get("naics", "")
        pathway = NAICS_TO_PATHWAY.get(naics)
        if not pathway:
            unmapped_naics[naics] += 1
            continue
        pw_emps[pathway].append({
            "name": e["name"],
            "city": e.get("city", ""),
            "headcount": e.get("estimated_headcount", 0),
            "naics": naics,
            "geocoded": bool(e.get("latitude")),
        })

    print("\n\nEMPLOYER AGGREGATES BY PATHWAY:")
    print("-" * 80)
    for name, emps_list in sorted(pw_emps.items(), key=lambda x: -len(x[1])):
        top = sorted(emps_list, key=lambda x: -(x["headcount"] or 0))[:5]
        top_names = ", ".join(f"{e['name']} ({e['city']})" for e in top)
        print(f"  {name:20s} | {len(emps_list):3d} employers | Top: {top_names}")

    print(f"\nUnmapped NAICS ({sum(unmapped_naics.values())} employers):")
    for n, c in sorted(unmapped_naics.items(), key=lambda x: -x[1])[:10]:
        print(f"  NAICS {n}: {c}")


if __name__ == "__main__":
    analyze_programs()
    analyze_employers()
