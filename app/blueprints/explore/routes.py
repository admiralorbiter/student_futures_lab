"""Explore blueprint routes — data explorer views with charts."""

from flask import render_template

from . import bp
from ...services.pathway_service import pathway_service


@bp.route("/")
def hub():
    """Data Explorer hub — card grid linking to views."""
    bls = pathway_service.get_bls_employment()
    proj = pathway_service.get_bls_projections()

    total_workers = sum(d.get("employment", 0) for d in bls.values())
    total_employers = sum(d.get("employers", 0) for d in bls.values())
    total_openings = sum(d.get("total_openings", 0) for d in proj.values())
    total_occupations = sum(d.get("occupation_count", 0) for d in proj.values())

    stats = pathway_service.get_pathway_stats()
    total_programs = sum(s.get("program_count", 0) for s in stats.values())

    return render_template(
        "explore/hub.html",
        total_workers=total_workers,
        total_employers=total_employers,
        total_openings=total_openings,
        total_occupations=total_occupations,
        total_programs=total_programs,
    )


@bp.route("/labor-market")
def labor_market():
    """KC Labor Market Overview — aggregate charts across all 7 pathways."""
    bls = pathway_service.get_bls_employment()
    proj = pathway_service.get_bls_projections()
    pathways = pathway_service.get_pathway_summaries()

    # Build chart-ready data sorted by pathway order
    chart_data = []
    for p in pathways:
        pid = p["id"]
        emp = bls.get(pid, {})
        prj = proj.get(pid, {})
        chart_data.append({
            "name": p["name"],
            "id": pid,
            "employment": emp.get("employment", 0),
            "employers": emp.get("employers", 0),
            "avg_weekly_wage": emp.get("avg_weekly_wage", 0),
            "annual_wage": emp.get("annual_wage", 0),
            "oty_employment_pct_chg": emp.get("oty_employment_pct_chg", 0),
            "oty_wage_pct_chg": emp.get("oty_wage_pct_chg", 0),
            "total_openings": prj.get("total_openings", 0),
            "total_net_growth": prj.get("total_net_growth", 0),
            "avg_growth_pct": prj.get("avg_growth_pct", 0),
        })

    county_data = pathway_service.get_bls_county_breakdown()

    return render_template(
        "explore/labor_market.html",
        chart_data=chart_data,
        county_data=county_data,
        pathways=pathways,
    )


@bp.route("/pathway/<pathway_id>")
def pathway_detail(pathway_id):
    """Pathway Deep Dive — per-pathway detail with charts."""
    pathways = pathway_service.get_pathway_summaries()

    # Find the matching pathway
    pathway = None
    for p in pathways:
        if p["id"] == pathway_id:
            pathway = p
            break
    if not pathway:
        return render_template("explore/hub.html"), 404

    bls = pathway_service.get_bls_employment().get(pathway_id, {})
    proj = pathway_service.get_bls_projections().get(pathway_id, {})
    stats = pathway_service.get_pathway_stats().get(pathway_id, {})
    chart_data = pathway_service.get_pathway_chart_data().get(pathway_id, {})
    county_data = pathway_service.get_bls_county_breakdown_for_pathway(pathway_id)

    return render_template(
        "explore/pathway_detail.html",
        pathway=pathway,
        bls=bls,
        proj=proj,
        stats=stats,
        chart_data=chart_data,
        county_data=county_data,
        families=pathways,  # used for tab selector
        family=pathway,     # current pathway (tab selector uses family.id)
    )
