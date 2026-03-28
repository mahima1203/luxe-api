from pydantic import BaseModel
from typing import Optional, List
import datetime

# ─── Products ──────────────────────────────────────────────────────────────────

class ProductBase(BaseModel):
    brand: str
    name: str
    price: float
    originalPrice: float
    discount: int
    image: str
    badge: Optional[str] = None
    category: str
    subcategory: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[Product]
    hasMore: bool
    total: int

# ─── Auth ──────────────────────────────────────────────────────────────────────

class SendOTPRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ─── Users ─────────────────────────────────────────────────────────────────────

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None

class UserProfile(BaseModel):
    id: int
    email: str
    role: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    is_deleted: bool

    class Config:
        from_attributes = True

# ─── Addresses ─────────────────────────────────────────────────────────────────

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    type: Optional[str] = "Home"

class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    type: Optional[str] = None
    is_default: Optional[bool] = None

class AddressResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    type: str
    is_default: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# ─── Orders ────────────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    product_brand: str
    product_image: str
    price: float
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_brand: str
    product_image: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    address_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_snapshot: str  # JSON string
    total: float
    status: str
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    created_at: datetime.datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

# ─── Cart & Wishlist ──────────────────────────────────────────────────────────

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    created_at: datetime.datetime
    product: Product

    class Config:
        from_attributes = True

class WishlistItemCreate(BaseModel):
    product_id: int

class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    created_at: datetime.datetime
    product: Product

    class Config:
        from_attributes = True

# ─── Payments ──────────────────────────────────────────────────────────────────

class RazorpayOrderCreate(BaseModel):
    order_id: int  # Internal DB Order ID

class RazorpayVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    order_id: int  # Internal DB Order ID



