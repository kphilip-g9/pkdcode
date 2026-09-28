import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.problem import Problem, TestCase
from app.models.submission import Submission

Base.metadata.create_all(bind=engine)
db = SessionLocal()

PROBLEMS = [
    {
        "title": "Sum of Two Numbers",
        "statement": "Given two integers A and B on one line separated by a space, print their sum.",
        "difficulty": "Easy",
        "test_cases": [
            {"input": "1 2",   "expected_output": "3",  "is_sample": True},
            {"input": "10 20", "expected_output": "30", "is_sample": True},
        ]
    },
    {
        "title": "Reverse a String",
        "statement": "Given a string S, print it reversed.",
        "difficulty": "Easy",
        "test_cases": [
            {"input": "hello", "expected_output": "olleh", "is_sample": True},
            {"input": "world", "expected_output": "dlrow", "is_sample": True},
        ]
    },
    {
        "title": "Count Even Numbers",
        "statement": "Given N integers on the second line, count how many are even.\nFirst line is N.",
        "difficulty": "Easy",
        "test_cases": [
            {"input": "5\n1 2 3 4 5", "expected_output": "2", "is_sample": True},
            {"input": "4\n2 4 6 8",   "expected_output": "4", "is_sample": True},
        ]
    },
]

for p_data in PROBLEMS:
    p = Problem(
        title      = p_data["title"],
        statement  = p_data["statement"],
        difficulty = p_data["difficulty"],
        source     = "custom",
    )
    db.add(p)
    db.flush()  # gets the id before commit
    for tc in p_data["test_cases"]:
        db.add(TestCase(
            problem_id      = p.id,
            input           = tc["input"],
            expected_output = tc["expected_output"],
            is_sample       = tc["is_sample"],
        ))

db.commit()
print("✅ Seeded 3 problems.")
db.close()