from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
 

while True:
    try:
        conn = psycopg2.connect(
            host="localhost", database="fastapi", user='postgres', password="Obaid311", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Database connection failed due to {}".format(e))
        time.sleep(2)


my_posts = []


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Working!!!"}


@app.get("/sql")
def test_posts(db: Session = (Depends(get_db))):
    posts = db.query(models.Post).all()
    return {"posts": posts}


@app.get("/posts")
def get_posts(db: Session = (Depends(get_db))):
    posts = db.query(models.Post).all()
    return {"data": posts}

# title str, content str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = (Depends(get_db))):
    print(post)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_single_post(id: int,db: Session = (Depends(get_db))):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_post(id: int,db: Session = (Depends(get_db))):
    post = db.query(models.Post).filter(models.Post.id == id).first()    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_single_post(id: int, updated_post: Post,db: Session = (Depends(get_db))):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
