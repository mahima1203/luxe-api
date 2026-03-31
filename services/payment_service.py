import os
import razorpay
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")

# Initialize Razorpay Client if keys are present (silently ignore if missing for mock mode)
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and "replace_me" not in RAZORPAY_KEY_ID:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_razorpay_order(user_id: int, order_id: int, db: Session) -> dict:
    """
    Creates a Razorpay order for an existing internal Order.
    Raises 404 if order doesn't exist or isn't owned by the user.
    """
    # 1. Fetch our internal order
    order = db.query(models.Order).filter(
        models.Order.id == order_id, 
        models.Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.status != "pending":
        raise HTTPException(status_code=400, detail=f"Cannot pay for order in {order.status} state")

    if not razorpay_client:
        # Fallback for dev: Just mock the response if no keys provided
        mock_id = f"order_mock_{order.id}"
        order.razorpay_order_id = mock_id
        db.commit()
        return {
            "id": mock_id,
            "amount": int(order.total * 100),
            "currency": "INR",
            "receipt": str(order.id)
        }

    # 2. Create Razorpay order request
    # Razorpay expects amount in paise (1 INR = 100 paise)
    options = {
        "amount": int(order.total * 100), 
        "currency": "INR",
        "receipt": f"receipt_order_{order.id}",
        "payment_capture": 1 # Auto capture
    }

    try:
        rzp_order = razorpay_client.order.create(data=options)
        
        # 3. Save the razorpay_order_id back to our DB
        order.razorpay_order_id = rzp_order["id"]
        db.commit()
        
        return rzp_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Razorpay error: {str(e)}")

def verify_payment_signature(user_id: int, order_id: int, rzp_order_id: str, rzp_payment_id: str, rzp_signature: str, db: Session) -> models.Order:
    """
    Verifies the signature returned by Razorpay Checkout to ensure payment is legit.
    If valid, marks our internal Order as 'paid'.
    """
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.razorpay_order_id != rzp_order_id:
        raise HTTPException(status_code=400, detail="Order ID mismatch")

    if not razorpay_client:
        # Fallback for dev
        order.status = "paid"
        order.razorpay_payment_id = rzp_payment_id
        
        # CLEAR CART for successful order items
        order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
        for item in order_items:
            db.query(models.CartItem).filter(
                models.CartItem.user_id == user_id,
                models.CartItem.product_id == item.product_id
            ).delete()

        db.commit()
        db.refresh(order)
        return order

    # Verify signature
    params_dict = {
        'razorpay_order_id': rzp_order_id,
        'razorpay_payment_id': rzp_payment_id,
        'razorpay_signature': rzp_signature
    }
    
    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Signature is valid. Mark as paid
        order.status = "paid"
        order.razorpay_payment_id = rzp_payment_id
        
        # CLEAR CART for successful order items
        order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
        for item in order_items:
            db.query(models.CartItem).filter(
                models.CartItem.user_id == user_id,
                models.CartItem.product_id == item.product_id
            ).delete()

        db.commit()
        db.refresh(order)
        return order
        
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification error: {str(e)}")
