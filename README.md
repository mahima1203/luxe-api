# Luxe Fashion - Backend API

A high-performance, modular e-commerce backend built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This API powers the Luxe Fashion storefront, managing authentication, product catalogs, shopping bags, and secure checkouts.

## 🚀 Teck Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: JWT (JSON Web Tokens)
- **Payments**: Razorpay Integration (via `razorpay` python SDK)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)

## 🏗️ Architecture
The project follows a **Controller-Service** architecture for better modularity and testability:

- `api/routers/`: Request handling and routing (Controllers).
- `services/`: Core business logic and database interactions.
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic data validation schemas.
- `core/`: Security configurations and core constants.

## 🛠️ Getting Started

### 1. Installation
Ensure you have Python 3.9+ installed.

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./luxe.db
JWT_SECRET=your_super_secret_key
RAZORPAY_KEY_ID=your_razorpay_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### 3. Database Setup & Seeding
Initialize the database and populate it with premium luxury items.

```bash
# Initialize tables and seed local data
python seed.py

# (Optional) Seed with production-ready fashion items
python seed_production.py
```

### 4. Running the Server
```bash
# Start in development mode
fastapi dev main.py
```
The API will be available at [http://localhost:8000](http://localhost:8000).

## 📒 API Documentation
Luxe Fashion provides interactive API docs out of the box:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔑 Key Features
- **User Management**: Secure signup, login (JWT), and profile management.
- **Product Catalog**: Categorized items (Men/Women) with real-time stock management.
- **Shopping Bag**: Persistence across devices with support for "Selective Checkout".
- **Wishlist**: Save-for-later functionality tied to user accounts.
- **Orders & Payments**: Secure order placement with Razorpay signature verification.
- **Admin Utilities**: Data syncing scripts for production deployment.

---
Built with ❤️ by the Luxe Team
