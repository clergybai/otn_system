from .. import models, schemas
from ..database import get_api_db
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/')
def get_posts(db: Session = Depends(get_api_db)):
    return {"data": db.query(models.Post).all()}


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_api_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"post_detail": post}


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_api_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_api_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(get_api_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
