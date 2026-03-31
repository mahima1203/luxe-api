from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from core.security import get_current_user
from services import review_service

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.post("/", response_model=schemas.ReviewResponse)
def create_review(
    data: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Submit a review for a product (Verified Purchase required)."""
    return review_service.create_review(user.id, data, db)

@router.get("/product/{product_id}", response_model=List[schemas.ReviewResponse])
def list_product_reviews(product_id: int, db: Session = Depends(get_db)):
    """Fetch all reviews for a specific product."""
    return review_service.get_product_reviews(product_id, db)

@router.get("/can-review/{product_id}", response_model=schemas.ReviewEligibilityResponse)
def check_eligibility(
    product_id: int, 
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Helper for frontend to check if user can review this product."""
    can_review, message = review_service.check_review_eligibility(user.id, product_id, db)
    return {"can_review": can_review, "message": message}
