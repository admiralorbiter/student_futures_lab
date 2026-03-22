"""Pathway service — loads YAML mapping files and provides
read-only access to the pathway data database.

Two data sources:
  1. YAML files in data/mappings/ — curated editorial content (editable by PREP-KC)
  2. pathway_data.db — granular program, institution, occupation data (read-only)

Student responses go to a separate read-write database (via SQLAlchemy).
"""

import os
import sqlite3

import yaml
from flask import current_app


class PathwayService:
    """Loads and provides access to pathway data."""

    def __init__(self):
        self._data = {}
        self._db_path = None

    def init_app(self, app):
        """Load YAML files and connect to the pathway data database."""
        # --- YAML editorial data ---
        mappings_dir = app.config["MAPPINGS_DIR"]
        self._data = {}

        yaml_files = [
            "pathway_families",
            "pathway_summaries",
            "support_tags",
            "county_notes",
            "launch_points",
            "employer_context",
            "glossary",
            "plain_language_labels",
        ]

        for name in yaml_files:
            path = os.path.join(mappings_dir, f"{name}.yaml")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self._data[name] = yaml.safe_load(f)
                app.logger.info(f"Loaded {name}.yaml")
            else:
                self._data[name] = {}
                app.logger.warning(f"Missing {name}.yaml — using empty data")

        # --- Read-only database ---
        self._db_path = app.config.get("PATHWAY_DATA_DB")
        if self._db_path and os.path.exists(self._db_path):
            app.logger.info(f"Pathway data DB: {self._db_path}")
        else:
            app.logger.warning("No pathway_data.db found — granular queries disabled")
            self._db_path = None

        # Build lookup indexes from YAML
        self._build_indexes()

        # Build CIP-to-pathway lookup from families
        self._cip_to_pathway = {}
        for fam in self._data.get("pathway_families", {}).get("families", []):
            for prefix in fam.get("cip_prefixes", []):
                self._cip_to_pathway[prefix] = fam["id"]

    def _get_db(self):
        """Get a read-only database connection."""
        if not self._db_path:
            return None
        conn = sqlite3.connect(f"file:{self._db_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        return conn

    def _build_indexes(self):
        """Build fast-lookup dicts from the loaded YAML data."""
        self._pathway_index = {}
        for p in self._data.get("pathway_summaries", {}).get("pathways", []):
            self._pathway_index[p["id"]] = p

        self._family_index = {}
        for f in self._data.get("pathway_families", {}).get("families", []):
            self._family_index[f["id"]] = f

        self._county_index = {}
        for c in self._data.get("county_notes", {}).get("pathways", []):
            self._county_index[c["id"]] = c

        self._employer_index = {}
        for e in self._data.get("employer_context", {}).get("pathways", []):
            self._employer_index[e["id"]] = e

        self._launch_index = {}
        for lp in self._data.get("launch_points", {}).get("pathways", []):
            self._launch_index[lp["id"]] = lp

    # ──────────────────────────────────────────────
    # YAML-backed methods (curated editorial content)
    # ──────────────────────────────────────────────

    def get_families(self):
        """Return all pathway families in display order."""
        families = self._data.get("pathway_families", {}).get("families", [])
        return sorted(families, key=lambda f: f.get("display_order", 99))

    def get_pathway_summaries(self):
        """Return all pathway summaries in display order."""
        summaries = self._data.get("pathway_summaries", {}).get("pathways", [])
        for s in summaries:
            family = self._family_index.get(s["id"], {})
            s["display_order"] = family.get("display_order", 99)
        return sorted(summaries, key=lambda s: s.get("display_order", 99))

    def get_pathway(self, pathway_id):
        """Return a single pathway summary by ID."""
        return self._pathway_index.get(pathway_id)

    def get_county_notes(self, pathway_id):
        """Return county notes for a specific pathway."""
        return self._county_index.get(pathway_id)

    def get_employers(self, pathway_id):
        """Return curated top employers for a specific pathway (from YAML)."""
        entry = self._employer_index.get(pathway_id, {})
        return entry.get("employers", [])

    def get_launch_points(self, pathway_id):
        """Return curated launch points for a specific pathway (from YAML)."""
        entry = self._launch_index.get(pathway_id, {})
        return entry.get("launch_points", [])

    def get_support_tags(self):
        """Return barrier and support tag definitions."""
        tags = self._data.get("support_tags", {})
        return {
            "barriers": tags.get("barriers", []),
            "supports": tags.get("supports", []),
        }

    def get_glossary(self):
        """Return glossary terms."""
        return self._data.get("glossary", {}).get("terms", [])

    def get_label(self, field_name):
        """Return the plain-language label for a technical field name."""
        labels = self._data.get("plain_language_labels", {}).get("labels", {})
        return labels.get(field_name, field_name)

    def get_additional_fields(self, visible_only=True):
        """Return additional (unmapped) fields of study."""
        fields = self._data.get("pathway_families", {}).get("additional_fields", [])
        if visible_only:
            fields = [f for f in fields if f.get("visible", True)]
        return fields

    # ──────────────────────────────────────────────
    # Database-backed methods (granular drill-down)
    # ──────────────────────────────────────────────

    def get_programs_by_pathway(self, pathway_id):
        """Return all programs in a pathway, with earnings data."""
        db = self._get_db()
        if not db:
            return []
        family = self._family_index.get(pathway_id, {})
        prefixes = family.get("cip_prefixes", [])
        if not prefixes:
            return []
        placeholders = ",".join("?" for _ in prefixes)
        rows = db.execute(
            f"""
            SELECT * FROM programs
            WHERE substr(replace(cip_code, '.', ''), 1, 2) IN ({placeholders})
            ORDER BY institution_name, program_name
            """,
            prefixes,
        ).fetchall()
        db.close()
        return [dict(r) for r in rows]

    def get_programs_by_institution(self, institution_id):
        """Return all programs at an institution."""
        db = self._get_db()
        if not db:
            return []
        rows = db.execute(
            "SELECT * FROM programs WHERE institution_id = ? ORDER BY program_name",
            (institution_id,),
        ).fetchall()
        db.close()
        return [dict(r) for r in rows]

    def get_institution(self, institution_id):
        """Return a single institution's details."""
        db = self._get_db()
        if not db:
            return None
        row = db.execute(
            "SELECT * FROM institutions WHERE institution_id = ?",
            (institution_id,),
        ).fetchone()
        db.close()
        return dict(row) if row else None

    def get_all_institutions(self):
        """Return all institutions."""
        db = self._get_db()
        if not db:
            return []
        rows = db.execute(
            "SELECT * FROM institutions ORDER BY name"
        ).fetchall()
        db.close()
        return [dict(r) for r in rows]

    def get_linked_occupations(self, program_id):
        """Return occupations linked to a program via SOC code crosswalk."""
        db = self._get_db()
        if not db:
            return []
        rows = db.execute(
            """
            SELECT o.*, po.confidence
            FROM program_occupations po
            JOIN occupations o ON po.soc_code = o.soc_code
            WHERE po.program_id = ?
            ORDER BY po.confidence DESC
            """,
            (program_id,),
        ).fetchall()
        db.close()
        return [dict(r) for r in rows]

    def get_employers_by_naics(self, naics_code):
        """Return employers in a specific NAICS sector."""
        db = self._get_db()
        if not db:
            return []
        rows = db.execute(
            """
            SELECT * FROM employers
            WHERE naics_code = ?
            ORDER BY estimated_headcount DESC
            """,
            (naics_code,),
        ).fetchall()
        db.close()
        return [dict(r) for r in rows]

    def get_data_stats(self):
        """Return summary stats for the data layer (for debugging/display)."""
        db = self._get_db()
        if not db:
            return {"db_available": False}
        stats = {"db_available": True}
        for table in ["programs", "institutions", "occupations",
                       "program_occupations", "employers", "sector_profiles"]:
            stats[table] = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        db.close()
        return stats


# Singleton instance — initialized in the app factory
pathway_service = PathwayService()
