"""Routes for the guided inquiry flow."""

from flask import (
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from ...extensions import db
from ...models.student import Student
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

    return render_template(
        f"screens/screen_{screen_num}.html",
        screen_num=screen_num,
        screen=screen_info,
        screens=SCREENS,
        student_code=student_code,
        prev_screen=screen_num - 1 if screen_num > 1 else None,
        next_screen=screen_num + 1 if screen_num < 5 else None,
    )
