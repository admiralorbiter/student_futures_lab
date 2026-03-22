"""Routes for the guided inquiry flow."""

from datetime import datetime, timezone

from flask import (
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from ...extensions import db
from ...models.student import Response, Student
from ...services.pathway_service import pathway_service
from . import bp

# Screen metadata — drives the progress bar and navigation
SCREENS = {
    1: {"title": "Pathway Explorer", "question": "What looks strongest on paper?"},
    2: {"title": "Hickman Mills Lens", "question": "Would this still look strong for Hickman Mills students?"},
    3: {"title": "Launch Points", "question": "Where could someone realistically start?"},
    4: {"title": "My Pathway Reality Check", "question": "What does this mean for me?"},
    5: {"title": "Recommendation Builder", "question": "What should PREP-KC do?"},
}


def _get_student_code():
    """Get the current student code from cookie, or None for anonymous."""
    return request.cookies.get(current_app.config["STUDENT_CODE_COOKIE"])


def _get_or_create_student(code):
    """Find or create a student record for the given code."""
    student = Student.query.filter_by(code=code).first()
    if not student:
        student = Student(code=code)
        db.session.add(student)
        db.session.commit()
    return student


def _load_saved_responses(student_code, screen_num):
    """Load saved responses for a student on a screen as a dict."""
    if not student_code:
        return {}
    student = Student.query.filter_by(code=student_code).first()
    if not student:
        return {}
    responses = Response.query.filter_by(
        student_id=student.id, screen=screen_num
    ).all()
    return {r.response_key: r.value for r in responses}


def _load_cross_screen_responses(student_code, screen_num, key_prefix=None):
    """Load saved responses from a *different* screen.

    Optionally filter by key prefix (e.g. 'pathway_bucket_').
    Returns dict of {response_key: value}.
    """
    if not student_code:
        return {}
    student = Student.query.filter_by(code=student_code).first()
    if not student:
        return {}
    query = Response.query.filter_by(student_id=student.id, screen=screen_num)
    if key_prefix:
        query = query.filter(Response.response_key.startswith(key_prefix))
    return {r.response_key: r.value for r in query.all()}


def _get_screen1_top_pathways(student_code):
    """Return list of pathway IDs the student marked 'strongest' on Screen 1.

    Falls back to all 7 pathway IDs if no saved data exists.
    Students can override this on Screen 2.
    """
    all_ids = ["healthcare", "business", "manufacturing", "logistics",
               "tech", "education", "law_public"]
    buckets = _load_cross_screen_responses(student_code, 1, "pathway_bucket_")
    if not buckets:
        return all_ids  # No saved data — show all

    strongest = [
        key.replace("pathway_bucket_", "")
        for key, val in buckets.items()
        if val == "strongest"
    ]
    # If fewer than 3 strongest, also include "mixed" pathways
    if len(strongest) < 3:
        mixed = [
            key.replace("pathway_bucket_", "")
            for key, val in buckets.items()
            if val == "mixed"
        ]
        strongest.extend(mixed)

    return strongest[:5] if strongest else all_ids  # Cap at 5, fallback to all


def _save_responses(student_code, screen_num, form_data):
    """Save form data as response rows. Upserts by (student, screen, key)."""
    if not student_code:
        return
    student = _get_or_create_student(student_code)

    for key, value in form_data.items():
        value = value.strip() if value else ""
        if not value:
            continue  # Don't save empty values

        existing = Response.query.filter_by(
            student_id=student.id, screen=screen_num, response_key=key
        ).first()

        if existing:
            existing.value = value
            existing.updated_at = datetime.now(timezone.utc)
        else:
            resp = Response(
                student_id=student.id,
                screen=screen_num,
                response_key=key,
                value=value,
            )
            db.session.add(resp)

    db.session.commit()


@bp.route("/")
def landing():
    """Landing page — project intro and optional code entry."""
    student_code = _get_student_code()
    return render_template("landing.html", student_code=student_code)


@bp.route("/save-code", methods=["POST"])
def save_code():
    """Save a student code to cookie and create/find the student record."""
    code = request.form.get("code", "").strip()
    if not code:
        return redirect(url_for("main.landing"))

    # Create or find the student
    _get_or_create_student(code)

    # Set cookie and redirect to Screen 1
    response = make_response(redirect(url_for("main.screen", screen_num=1)))
    response.set_cookie(
        current_app.config["STUDENT_CODE_COOKIE"],
        code,
        max_age=current_app.config["STUDENT_CODE_MAX_AGE"],
        httponly=True,
        samesite="Lax",
    )
    return response


@bp.route("/clear-code", methods=["POST"])
def clear_code():
    """Clear the saved student code (return to anonymous)."""
    response = make_response(redirect(url_for("main.landing")))
    response.delete_cookie(current_app.config["STUDENT_CODE_COOKIE"])
    return response


@bp.route("/screen/<int:screen_num>")
def screen(screen_num):
    """Render one of the 5 inquiry screens."""
    if screen_num not in SCREENS:
        return redirect(url_for("main.landing"))

    student_code = _get_student_code()
    screen_info = SCREENS[screen_num]
    saved = _load_saved_responses(student_code, screen_num)

    # Screen-specific data injection
    extra = {}
    if screen_num == 1:
        extra["pathways"] = pathway_service.get_pathway_summaries()
        extra["additional_fields"] = pathway_service.get_additional_fields()
        extra["pathway_stats"] = pathway_service.get_pathway_stats()
        extra["chart_data"] = pathway_service.get_pathway_chart_data()

    elif screen_num == 2:
        all_pathways = pathway_service.get_pathway_summaries()
        top_ids = _get_screen1_top_pathways(student_code)
        # Build per-pathway context dicts
        county_notes = {}
        employers = {}
        for p in all_pathways:
            county_notes[p["id"]] = pathway_service.get_county_notes(p["id"]) or {}
            employers[p["id"]] = pathway_service.get_employers(p["id"])

        extra["pathways"] = all_pathways
        extra["top_pathway_ids"] = top_ids
        extra["county_notes"] = county_notes
        extra["employers"] = employers
        extra["support_tags"] = pathway_service.get_support_tags()
        extra["pathway_stats"] = pathway_service.get_pathway_stats()
        extra["chart_data"] = pathway_service.get_pathway_chart_data()
        # Pass Screen 1 buckets so template can show "(Strongest)", "(Mixed)", etc.
        extra["screen1_buckets"] = _load_cross_screen_responses(
            student_code, 1, "pathway_bucket_"
        )

    return render_template(
        f"screens/screen_{screen_num}.html",
        screen_num=screen_num,
        screen=screen_info,
        screens=SCREENS,
        student_code=student_code,
        saved=saved,
        prev_screen=screen_num - 1 if screen_num > 1 else None,
        next_screen=screen_num + 1 if screen_num < 5 else None,
        **extra,
    )


@bp.route("/screen/<int:screen_num>/submit", methods=["POST"])
def screen_submit(screen_num):
    """Handle form submission for a screen."""
    if screen_num not in SCREENS:
        return redirect(url_for("main.landing"))

    student_code = _get_student_code()

    # Collect all form fields into a dict
    form_data = {}
    for key in request.form:
        form_data[key] = request.form[key]

    # Save if student has a code
    _save_responses(student_code, screen_num, form_data)

    # Redirect to next screen
    next_num = screen_num + 1 if screen_num < 5 else None
    if next_num:
        return redirect(url_for("main.screen", screen_num=next_num))
    return redirect(url_for("main.landing"))
