from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from core.security import get_current_user
from services import address_service

router = APIRouter(prefix="/api/addresses", tags=["addresses"])


@router.get("/", response_model=List[schemas.AddressResponse])
def list_addresses(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Get all addresses for the authenticated user."""
    return address_service.get_user_addresses(user.id, db)


@router.post("/", response_model=schemas.AddressResponse, status_code=201)
def create_address(
    data: schemas.AddressCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Create a new address for the authenticated user."""
    return address_service.create_address(user.id, data, db)


@router.put("/{address_id}", response_model=schemas.AddressResponse)
def update_address(
    address_id: int,
    data: schemas.AddressUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Update an existing address."""
    return address_service.update_address(user.id, address_id, data, db)


@router.delete("/{address_id}", status_code=204)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Delete an address. If it was the default, the next one is promoted."""
    address_service.delete_address(user.id, address_id, db)


@router.patch("/{address_id}/set-default", response_model=schemas.AddressResponse)
def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    """Set an address as the user's default delivery address."""
    return address_service.set_default_address(user.id, address_id, db)
