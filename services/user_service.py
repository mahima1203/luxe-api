from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import models, schemas

def update_user_profile(user: models.User, update_data: schemas.UserUpdate, db: Session):
    if update_data.full_name is not None:
        user.full_name = update_data.full_name
    if update_data.phone_number is not None:
        user.phone_number = update_data.phone_number
    if update_data.gender is not None:
        user.gender = update_data.gender
        
    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(user: models.User, db: Session):
    user.is_deleted = True
    db.commit()

# ─── Cart Management ───────────────────────────────────────────────────────────

def get_cart(user_id: int, db: Session):
    return db.query(models.CartItem).options(joinedload(models.CartItem.product)).filter(models.CartItem.user_id == user_id).all()

def add_to_cart(user_id: int, data: schemas.CartItemCreate, db: Session):
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id, 
        models.CartItem.product_id == data.product_id
    ).first()
    
    if existing:
        existing.quantity += data.quantity
        db.commit()
        db.refresh(existing)
        return existing
        
    item = models.CartItem(user_id=user_id, product_id=data.product_id, quantity=data.quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_cart_item(user_id: int, item_id: int, data: schemas.CartItemUpdate, db: Session):
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
        
    if data.quantity <= 0:
        db.delete(item)
        db.commit()
        return None
        
    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    return item

def remove_from_cart(user_id: int, item_id: int, db: Session):
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()

# ─── Wishlist Management ───────────────────────────────────────────────────────

def get_wishlist(user_id: int, db: Session):
    return db.query(models.WishlistItem).options(joinedload(models.WishlistItem.product)).filter(models.WishlistItem.user_id == user_id).all()

def add_to_wishlist(user_id: int, data: schemas.WishlistItemCreate, db: Session):
    existing = db.query(models.WishlistItem).filter(
        models.WishlistItem.user_id == user_id, 
        models.WishlistItem.product_id == data.product_id
    ).first()
    
    if existing:
        return existing
        
    item = models.WishlistItem(user_id=user_id, product_id=data.product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_from_wishlist(user_id: int, item_id: int, db: Session):
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id, models.WishlistItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()

