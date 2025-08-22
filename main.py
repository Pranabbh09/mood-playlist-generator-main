from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Song
from state import SongCreate, SongOut

app = FastAPI()
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/songs/", response_model=SongOut)
def add_song(song: SongCreate, db: Session = Depends(get_db)):
    db_song = Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/songs/", response_model=list[SongOut])
def get_all_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()
