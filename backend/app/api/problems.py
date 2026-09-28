from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.problem import Problem

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("")
def list_problems(db: Session = Depends(get_db)):
    problems = db.query(Problem).all()
    return [
        {"id": p.id, "title": p.title, "difficulty": p.difficulty}
        for p in problems
    ]

@router.get("/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {
        "id":         problem.id,
        "title":      problem.title,
        "statement":  problem.statement,
        "difficulty": problem.difficulty,
        "source_url": problem.source_url,
        "test_cases": [
            {"input": tc.input, "expected_output": tc.expected_output}
            for tc in problem.test_cases if tc.is_sample
        ]
    }