from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./playlist.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)
    mood = Column(String)
    genre = Column(String, nullable=True)
    youtube_url = Column(String)
    mood_score = Column(Float)

# Initialize DB
def init_db():
    Base.metadata.create_all(bind=engine)
