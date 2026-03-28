from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from services import address_service


def create_order(user_id: int, data: schemas.OrderCreate, db: Session) -> models.Order:
    """Create an order from cart items. Snapshots the address for history."""
    # Get address snapshot (raises 404 if not owned by user)
    snapshot = address_service.get_address_as_snapshot(user_id, data.address_id, db)

    if not data.items:
        raise HTTPException(status_code=400, detail="Cannot create an order with no items.")

    # Calculate total
    total = sum(item.price * item.quantity for item in data.items)

    order = models.Order(
        user_id=user_id,
        address_snapshot=snapshot,
        total=total,
        status="pending",
    )
    db.add(order)
    db.flush()  # Get order.id without committing

    # Add items
    for item_data in data.items:
        item = models.OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            product_name=item_data.product_name,
            product_brand=item_data.product_brand,
            product_image=item_data.product_image,
            price=item_data.price,
            quantity=item_data.quantity,
        )
        db.add(item)

    db.commit()
    db.refresh(order)
    return order


def get_user_orders(user_id: int, db: Session) -> list[models.Order]:
    """Return all orders for a user, newest first."""
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .all()
    )


def get_order_by_id(user_id: int, order_id: int, db: Session) -> models.Order:
    """Get a single order by ID ensuring it belongs to the requesting user."""
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order


def get_order_items(order_id: int, db: Session) -> list[models.OrderItem]:
    """Return all items for a given order."""
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()


def mark_order_paid(order_id: int, razorpay_payment_id: str, db: Session) -> models.Order:
    """Mark order as paid after successful Razorpay verification."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    order.status = "paid"
    order.razorpay_payment_id = razorpay_payment_id
    db.commit()
    db.refresh(order)
    return order
