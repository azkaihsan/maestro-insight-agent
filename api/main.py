"""
Maestro Insight Agent — Mock Student Mastery REST API

A FastAPI application that serves structured student mastery data
including misconceptions, difficulty scores, and learning progress.
"""

import json
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Student Mastery API",
    description="Mock API for retrieving student learning diagnostics, misconceptions, and mastery profiles.",
    version="1.0.0",
)

# Load student data from JSON file
DATA_PATH = Path(__file__).parent.parent / "data" / "students.json"


def load_students() -> list[dict]:
    """Load student data from the JSON file."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


STUDENTS: list[dict] = load_students()


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "Student Mastery API",
        "status": "running",
        "total_students": len(STUDENTS),
    }


@app.get("/students")
def list_students():
    """
    List all students with summary info (id, name, grade, subject, overall_mastery).
    """
    return [
        {
            "student_id": s["student_id"],
            "name": s["name"],
            "grade": s["grade"],
            "subject": s["subject"],
            "overall_mastery": s["overall_mastery"],
            "last_assessment_date": s["last_assessment_date"],
        }
        for s in STUDENTS
    ]


@app.get("/students/search")
def search_students(name: Optional[str] = Query(None, description="Partial name to search for")):
    """
    Search students by name (case-insensitive partial match).
    """
    if not name:
        raise HTTPException(status_code=400, detail="Query parameter 'name' is required.")

    matches = [
        s for s in STUDENTS if name.lower() in s["name"].lower()
    ]

    if not matches:
        return {"message": f"No students found matching '{name}'.", "results": []}

    return {
        "message": f"Found {len(matches)} student(s) matching '{name}'.",
        "results": matches,
    }


@app.get("/students/{student_id}")
def get_student_profile(student_id: str):
    """
    Get the full mastery profile for a specific student by ID.
    Returns all topics, misconceptions, difficulty scores, and mastery levels.
    """
    student = next((s for s in STUDENTS if s["student_id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found.")
    return student


@app.get("/students/{student_id}/misconceptions")
def get_student_misconceptions(student_id: str):
    """
    Get only the misconceptions for a specific student, grouped by topic.
    """
    student = next((s for s in STUDENTS if s["student_id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found.")

    misconceptions_by_topic = []
    for topic in student["topics"]:
        if topic["misconceptions"]:
            misconceptions_by_topic.append(
                {
                    "topic": topic["topic"],
                    "misconceptions": topic["misconceptions"],
                    "difficulty_score": topic["difficulty_score"],
                }
            )

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "subject": student["subject"],
        "misconceptions": misconceptions_by_topic,
        "total_misconceptions": sum(
            len(t["misconceptions"]) for t in misconceptions_by_topic
        ),
    }


@app.get("/students/{student_id}/struggling-topics")
def get_struggling_topics(student_id: str):
    """
    Get topics where the student is struggling (status = 'struggling').
    """
    student = next((s for s in STUDENTS if s["student_id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found.")

    struggling = [t for t in student["topics"] if t["status"] == "struggling"]

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "subject": student["subject"],
        "struggling_topics": struggling,
        "total_struggling": len(struggling),
    }
