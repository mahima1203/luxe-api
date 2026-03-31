import sqlite3
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def sync_data():
    # 1. Connect to local SQLite database
    print("Reading products from local luxe.db...")
    try:
        local_conn = sqlite3.connect('luxe.db')
        cur = local_conn.cursor()
        cur.execute('SELECT brand, name, price, originalPrice, discount, image, category, subcategory, badge FROM products')
        rows = cur.fetchall()
        local_conn.close()
    except Exception as e:
        print(f"Error reading local database: {e}")
        return

    if not rows:
        print("No products found in local database.")
        return

    print(f"Found {len(rows)} local products.")

    # 2. Connect to Production database (Render/Neon)
    db = SessionLocal()
    try:
        # Create table if not exists in production
        models.Base.metadata.create_all(bind=engine)
        
        # Clear old data to prevent duplicates (Sync approach)
        print("Cleaning up old products in production...")
        db.query(models.Product).delete()
        db.commit()

        print("Syncing data to production...")
        for row in rows:
            product = models.Product(
                brand=row[0],
                name=row[1],
                price=row[2],
                originalPrice=row[3],
                discount=row[4],
                image=row[5],
                category=row[6],
                subcategory=row[7],
                badge=row[8]
            )
            db.add(product)
        
        db.commit()
        print(f"✅ Success! {len(rows)} products synced to production!")
    except Exception as e:
        print(f"Error syncing to production: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sync_data()
