from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.submission import Submission

router = APIRouter(prefix="/submissions", tags=["submissions"])

class SubmissionRequest(BaseModel):
    problem_id: int
    language:   str
    code:       str

@router.post("")
def create_submission(body: SubmissionRequest, db: Session = Depends(get_db)):
    submission = Submission(
        problem_id = body.problem_id,
        language   = body.language,
        code       = body.code,
        verdict    = "QUEUED"
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return {"submission_id": submission.id, "verdict": submission.verdict}