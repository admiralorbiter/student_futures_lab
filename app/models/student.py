"""Student and response models — the only SQLite-backed data in v1."""

from datetime import datetime, timezone

from ..extensions import db


class Student(db.Model):
    """A student identified by a short self-chosen code. Not PII."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    cohort = db.Column(db.String(50), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    responses = db.relationship(
        "Response", backref="student", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.code}>"


class Response(db.Model):
    """A single saved input from one screen.

    Each row represents one field or selection on one screen for one student.
    Multiple rows per screen are normal (e.g., top_criteria, pathway_buckets,
    confidence, evidence_notes are each separate response rows for Screen 1).
    """

    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False, index=True
    )
    screen = db.Column(db.Integer, nullable=False)  # 1–5
    response_key = db.Column(db.String(100), nullable=False)  # e.g. "top_criteria"
    value = db.Column(db.Text, nullable=True)  # JSON-encoded for complex values
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        db.UniqueConstraint("student_id", "screen", "response_key", name="uq_response"),
    )

    def __repr__(self):
        return f"<Response s{self.screen} {self.response_key}>"
