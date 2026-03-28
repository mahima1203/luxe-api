from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
import models, schemas
from database import get_db
from core.security import get_current_user
from services import order_service

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", status_code=201)
def create_order(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """
    Create a new order from cart items.
    Returns the created order with its ID (used to initiate Razorpay payment).
    """
    order = order_service.create_order(user.id, data, db)
    items = order_service.get_order_items(order.id, db)
    return _build_order_response(order, items)


@router.get("/", )
def list_orders(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Get all orders for the authenticated user, newest first."""
    orders = order_service.get_user_orders(user.id, db)
    result = []
    for order in orders:
        items = order_service.get_order_items(order.id, db)
        result.append(_build_order_response(order, items))
    return result


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Get a single order by ID."""
    order = order_service.get_order_by_id(user.id, order_id, db)
    items = order_service.get_order_items(order.id, db)
    return _build_order_response(order, items)


# ─── Helper ────────────────────────────────────────────────────────────────────

def _build_order_response(order: models.Order, items: list[models.OrderItem]) -> dict:
    """Serialize an order + its items into a dict, parsing the address snapshot."""
    return {
        "id": order.id,
        "user_id": order.user_id,
        "address": json.loads(order.address_snapshot),
        "total": order.total,
        "status": order.status,
        "razorpay_order_id": order.razorpay_order_id,
        "razorpay_payment_id": order.razorpay_payment_id,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "product_brand": item.product_brand,
                "product_image": item.product_image,
                "price": item.price,
                "quantity": item.quantity,
            }
            for item in items
        ],
    }
