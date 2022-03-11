from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils, OAuth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional, List


router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)



@router.get("/", response_model=List[schemas.PostResponseWithVote])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    #Get all posts of authenticated user's own posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    #retrive the new post 
    db.refresh(new_post) 
    
    return new_post
    

    
@router.get("/{id}", response_model=schemas.PostResponseWithVote)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
     
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    # Get a single post of authenticated user's only post by post id    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
        
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
 
    return post