import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas


def get_user_addresses(user_id: int, db: Session) -> list[models.Address]:
    """Return all addresses for a user, default first."""
    return (
        db.query(models.Address)
        .filter(models.Address.user_id == user_id)
        .order_by(models.Address.is_default.desc(), models.Address.created_at.asc())
        .all()
    )


def create_address(user_id: int, data: schemas.AddressCreate, db: Session) -> models.Address:
    """Create a new address. If it's the user's first address, make it default."""
    existing = db.query(models.Address).filter(models.Address.user_id == user_id).count()
    is_default = existing == 0  # First address is always default

    address = models.Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        line1=data.line1,
        line2=data.line2,
        city=data.city,
        state=data.state,
        pincode=data.pincode,
        type=data.type or "Home",
        is_default=is_default,
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(user_id: int, address_id: int, data: schemas.AddressUpdate, db: Session) -> models.Address:
    """Update an existing address. If setting as default, unset all others first."""
    address = _get_owned_address_or_404(user_id, address_id, db)

    if data.is_default is True:
        _clear_default(user_id, db)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    return address


def delete_address(user_id: int, address_id: int, db: Session) -> None:
    """Delete an address. If it was default, promote the next oldest one."""
    address = _get_owned_address_or_404(user_id, address_id, db)
    was_default = address.is_default
    db.delete(address)
    db.commit()

    if was_default:
        # Promote the next address to default if any remain
        next_address = (
            db.query(models.Address)
            .filter(models.Address.user_id == user_id)
            .order_by(models.Address.created_at.asc())
            .first()
        )
        if next_address:
            next_address.is_default = True
            db.commit()


def set_default_address(user_id: int, address_id: int, db: Session) -> models.Address:
    """Set an address as the default, un-setting any previous default."""
    address = _get_owned_address_or_404(user_id, address_id, db)
    _clear_default(user_id, db)
    address.is_default = True
    db.commit()
    db.refresh(address)
    return address


def get_address_as_snapshot(user_id: int, address_id: int, db: Session) -> str:
    """Return a JSON string snapshot of the address for embedding in an order."""
    address = _get_owned_address_or_404(user_id, address_id, db)
    snapshot = {
        "full_name": address.full_name,
        "phone": address.phone,
        "line1": address.line1,
        "line2": address.line2,
        "city": address.city,
        "state": address.state,
        "pincode": address.pincode,
        "type": address.type,
    }
    return json.dumps(snapshot)


# ─── Private helpers ───────────────────────────────────────────────────────────

def _get_owned_address_or_404(user_id: int, address_id: int, db: Session) -> models.Address:
    address = db.query(models.Address).filter(
        models.Address.id == address_id,
        models.Address.user_id == user_id
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found.")
    return address


def _clear_default(user_id: int, db: Session) -> None:
    db.query(models.Address).filter(
        models.Address.user_id == user_id,
        models.Address.is_default == True  # noqa: E712
    ).update({"is_default": False})
    db.commit()
