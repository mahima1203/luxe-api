"""
migrate_db.py – run this whenever the schema changes.

Strategy:
  1. Use SQLAlchemy `create_all` to create any NEW tables that don't yet exist.
     (Safe: it never drops or modifies tables that already exist.)
  2. Run raw ALTER TABLE for adding columns to existing tables
     (SQLAlchemy create_all can't add columns to existing tables).
"""
import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import engine, Base
import models  # noqa: F401 – importing registers all models with Base.metadata

def migrate():
    # Step 1: Create all new tables (addresses, orders, order_items) safely
    print("Creating new tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Tables synced.")

    # Step 2: Legacy column additions for the `users` table
    db_path = 'c:/Users/Amit/OneDrive/Desktop/luxee/backend/luxe.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    user_columns = [
        ("full_name", "VARCHAR"),
        ("phone_number", "VARCHAR"),
        ("gender", "VARCHAR"),
        ("is_deleted", "BOOLEAN DEFAULT 0"),
    ]

    for col_name, col_type in user_columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added users.{col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"users.{col_name} already exists – skipping.")
            else:
                print(f"Error adding users.{col_name}: {e}")

    try:
        cursor.execute("ALTER TABLE cart_items ADD COLUMN size VARCHAR")
        print("Added cart_items.size")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("cart_items.size already exists - skipping.")
        else:
            print(f"Error adding cart_items.size: {e}")
            
    try:
        cursor.execute("ALTER TABLE order_items ADD COLUMN size VARCHAR")
        print("Added order_items.size")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("order_items.size already exists - skipping.")
        else:
            print(f"Error adding order_items.size: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
