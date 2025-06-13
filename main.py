from fastapi import FastAPI, HTTPException, Query, Response, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import random
import os
from sqlalchemy import create_engine, Column, String, Integer, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json

app = FastAPI(title="Code Snippet Search and Share API")

# Database setup
DATABASE_URL = "sqlite:///./snipshare.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SnippetDB(Base):
    __tablename__ = "snippets"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    code = Column(Text)
    language = Column(String, index=True)
    tags = Column(Text)  # Store as JSON string
    upvotes = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class Snippet(BaseModel):
    id: str
    title: str
    code: str
    language: str
    tags: List[str] = []
    upvotes: int = 0

class SnippetCreate(BaseModel):
    title: str
    code: str
    language: str
    tags: Optional[List[str]] = []

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@app.get("/dev", response_class=HTMLResponse)
def serve_overlay():
    overlay_path = os.path.join(os.path.dirname(__file__), "overlay.html")
    with open(overlay_path, "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

@app.post("/snippets", response_model=Snippet)
def add_snippet(snippet: SnippetCreate, db: Session = Depends(get_db)):
    snippet_id = str(uuid4())
    db_snippet = SnippetDB(
        id=snippet_id,
        title=snippet.title,
        code=snippet.code,
        language=snippet.language,
        tags=json.dumps(snippet.tags or []),
        upvotes=0
    )
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return Snippet(
        id=db_snippet.id,
        title=db_snippet.title,
        code=db_snippet.code,
        language=db_snippet.language,
        tags=json.loads(db_snippet.tags),
        upvotes=db_snippet.upvotes
    )

@app.get("/snippets", response_model=List[Snippet])
def search_snippets(query: Optional[str] = Query(None), language: Optional[str] = None, tag: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(SnippetDB)
    if query:
        q = q.filter((SnippetDB.title.ilike(f"%{query}%")) | (SnippetDB.code.ilike(f"%{query}%")))
    if language:
        q = q.filter(SnippetDB.language.ilike(language))
    results = q.all()
    snippets = []
    for s in results:
        tags = json.loads(s.tags)
        if tag and tag.lower() not in [t.lower() for t in tags]:
            continue
        snippets.append(Snippet(
            id=s.id,
            title=s.title,
            code=s.code,
            language=s.language,
            tags=tags,
            upvotes=s.upvotes
        ))
    return snippets

@app.get("/snippets/random", response_model=Snippet)
def get_random_snippet(db: Session = Depends(get_db)):
    snippets = db.query(SnippetDB).all()
    if not snippets:
        raise HTTPException(status_code=404, detail="No snippets available.")
    s = random.choice(snippets)
    return Snippet(
        id=s.id,
        title=s.title,
        code=s.code,
        language=s.language,
        tags=json.loads(s.tags),
        upvotes=s.upvotes
    )

@app.post("/snippets/{snippet_id}/upvote", response_model=Snippet)
def upvote_snippet(snippet_id: str, db: Session = Depends(get_db)):
    snippet = db.query(SnippetDB).filter(SnippetDB.id == snippet_id).first()
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found.")
    snippet.upvotes += 1
    db.commit()
    db.refresh(snippet)
    return Snippet(
        id=snippet.id,
        title=snippet.title,
        code=snippet.code,
        language=snippet.language,
        tags=json.loads(snippet.tags),
        upvotes=snippet.upvotes
    )
