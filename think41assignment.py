from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
   # Have to create the following files.
# from database import Base, engine, SessionLocal
# from models import Poll, PollOption, VoteLog
# from schemas import PollCreate, PollStatusUpdate, VoteRequest

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/polls")
def create_poll(poll: PollCreate, db: Session = Depends(get_db)):
    if db.query(Poll).filter_by(poll_str_id=poll.poll_str_id).first():
        raise HTTPException(400, detail="Poll ID already exists")

    new_poll = Poll(poll_str_id=poll.poll_str_id, question=poll.question)
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)

    for option in poll.options:
        db.add(PollOption(option_str_id=option.option_str_id, text=option.text, poll_id=new_poll.id))

    db.commit()
    return {"status": "poll created", "poll_id": poll.poll_str_id}

@app.post("/polls/{poll_str_id}/vote")
def vote(poll_str_id: str, vote: VoteRequest, db: Session = Depends(get_db)):
    poll = db.query(Poll).filter_by(poll_str_id=poll_str_id).first()
    if not poll:
        raise HTTPException(404, detail="Poll not found")

    if poll.status == "closed":
        return {"status": "error", "message": "Poll is closed. Voting is not allowed."}

    option = db.query(PollOption).filter_by(option_str_id=vote.option_str_id, poll_id=poll.id).first()
    if not option:
        raise HTTPException(404, detail="Option not found")

    if vote.user_identifier:
        existing_vote = db.query(VoteLog).filter_by(poll_id=poll.id, user_identifier=vote.user_identifier).first()
        if existing_vote:
            return {"status": "already_voted", "message": "You have already voted in this poll."}
        db.add(VoteLog(poll_id=poll.id, user_identifier=vote.user_identifier))

    option.votes += 1
    db.commit()

    return {"status": "vote_counted", "message": "Thank you for voting!"}

@app.get("/polls/{poll_str_id}/results")
def get_results(poll_str_id: str, db: Session = Depends(get_db)):
    poll = db.query(Poll).filter_by(poll_str_id=poll_str_id).first()
    if not poll:
        raise HTTPException(404, detail="Poll not found")

    results = [
        {
            "option_str_id": opt.option_str_id,
            "text": opt.text,
            "votes": opt.votes
        } for opt in poll.options
    ]

    return {
        "poll_str_id": poll.poll_str_id,
        "question": poll.question,
        "results": results
    }

@app.get("/polls/active")
def list_active_polls(db: Session = Depends(get_db)):
    polls = db.query(Poll).filter_by(status="active").all()
    return [{"poll_str_id": p.poll_str_id, "question": p.question} for p in polls]

@app.put("/polls/{poll_str_id}/status")
def update_poll_status(poll_str_id: str, body: PollStatusUpdate, db: Session = Depends(get_db)):
    poll = db.query(Poll).filter_by(poll_str_id=poll_str_id).first()
    if not poll:
        raise HTTPException(404, detail="Poll not found")
    poll.status = body.status
    db.commit()
    return {"poll_str_id": poll.poll_str_id, "status": poll.status, "message": f"Poll status updated to {poll.status}"}
