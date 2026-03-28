from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, models
from database import get_db
from core.security import get_current_user
from services import payment_service

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post("/create-order")
def create_payment_order(
    data: schemas.RazorpayOrderCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """
    Called when the user clicks 'Pay Now'.
    Takes the internal DB Order ID, creates a Razorpay Order for it, and returns the Razorpay Order dict.
    """
    rzp_order = payment_service.create_razorpay_order(user.id, data.order_id, db)
    return rzp_order


@router.post("/verify")
def verify_payment(
    data: schemas.RazorpayVerify,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """
    Called by the frontend after Razorpay Checkout succeeds.
    Verifies the signature and marks the internal DB Order as 'paid'.
    """
    order = payment_service.verify_payment_signature(
        user_id=user.id,
        order_id=data.order_id,
        rzp_order_id=data.razorpay_order_id,
        rzp_payment_id=data.razorpay_payment_id,
        rzp_signature=data.razorpay_signature,
        db=db
    )
    return {"status": "success", "message": "Payment verified securely.", "order_status": order.status}
