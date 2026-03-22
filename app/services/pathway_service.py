"""Pathway service — loads YAML mapping files at app startup.

All pathway data is read-only in v1. No runtime database queries needed
for pathway, institution, or employer data.
"""

import os

import yaml
from flask import current_app


class PathwayService:
    """Loads and provides access to all YAML mapping data."""

    def __init__(self):
        self._data = {}

    def init_app(self, app):
        """Load all YAML files from the mappings directory."""
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

        # Build lookup indexes
        self._build_indexes()

    def _build_indexes(self):
        """Build fast-lookup dicts from the loaded data."""
        # Pathway summaries by ID
        self._pathway_index = {}
        summaries = self._data.get("pathway_summaries", {})
        for p in summaries.get("pathways", []):
            self._pathway_index[p["id"]] = p

        # Pathway families by ID
        self._family_index = {}
        families = self._data.get("pathway_families", {})
        for f in families.get("families", []):
            self._family_index[f["id"]] = f

        # County notes by pathway ID
        self._county_index = {}
        county = self._data.get("county_notes", {})
        for c in county.get("pathways", []):
            self._county_index[c["id"]] = c

        # Employer context by pathway ID
        self._employer_index = {}
        employer = self._data.get("employer_context", {})
        for e in employer.get("pathways", []):
            self._employer_index[e["id"]] = e

        # Launch points by pathway ID
        self._launch_index = {}
        launch = self._data.get("launch_points", {})
        for lp in launch.get("pathways", []):
            self._launch_index[lp["id"]] = lp

    # --- Public API ---

    def get_families(self):
        """Return all pathway families in display order."""
        families = self._data.get("pathway_families", {}).get("families", [])
        return sorted(families, key=lambda f: f.get("display_order", 99))

    def get_pathway_summaries(self):
        """Return all pathway summaries in display order."""
        summaries = self._data.get("pathway_summaries", {}).get("pathways", [])
        # Merge in family info
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
        """Return employer context for a specific pathway."""
        entry = self._employer_index.get(pathway_id, {})
        return entry.get("employers", [])

    def get_launch_points(self, pathway_id):
        """Return launch points for a specific pathway."""
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
        """Return additional (unmapped) fields of study.

        These are CIP areas outside the 7 pathway families but still
        shown to students so they can see the full landscape.
        """
        fields = self._data.get("pathway_families", {}).get("additional_fields", [])
        if visible_only:
            fields = [f for f in fields if f.get("visible", True)]
        return fields


# Singleton instance — initialized in the app factory
pathway_service = PathwayService()
