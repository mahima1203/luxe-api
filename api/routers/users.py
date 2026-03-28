from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from core.security import get_current_user
from services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=schemas.UserProfile)
def get_user_profile(user: models.User = Depends(get_current_user)):
    return user

@router.put("/me", response_model=schemas.UserProfile)
def update_user_profile(schema: schemas.UserUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.update_user_profile(user, schema, db)

@router.delete("/me")
def soft_delete_user(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user_service.soft_delete_user(user, db)
    return {"message": "User soft deleted successfully"}

# ─── Cart ─────────────────────────────────────────────────────────────────────

@router.get("/cart", response_model=list[schemas.CartItemResponse])
def get_cart(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.get_cart(user.id, db)

@router.post("/cart", response_model=schemas.CartItemResponse)
def add_to_cart(data: schemas.CartItemCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.add_to_cart(user.id, data, db)

@router.put("/cart/{item_id}", response_model=schemas.CartItemResponse)
def update_cart_item(item_id: int, data: schemas.CartItemUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.update_cart_item(user.id, item_id, data, db)

@router.delete("/cart/{item_id}", status_code=204)
def remove_from_cart(item_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user_service.remove_from_cart(user.id, item_id, db)

# ─── Wishlist ─────────────────────────────────────────────────────────────────

@router.get("/wishlist", response_model=list[schemas.WishlistItemResponse])
def get_wishlist(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.get_wishlist(user.id, db)

@router.post("/wishlist", response_model=schemas.WishlistItemResponse)
def add_to_wishlist(data: schemas.WishlistItemCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return user_service.add_to_wishlist(user.id, data, db)

@router.delete("/wishlist/{item_id}", status_code=204)
def remove_from_wishlist(item_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user_service.remove_from_wishlist(user.id, item_id, db)

