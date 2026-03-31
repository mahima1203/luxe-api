import sys
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 1. Clear existing products (Optional - set to True if you want a fresh start)
CLEAR_EXISTING = True

def seed_data():
    db = SessionLocal()
    try:
        # Create tables if they don't exist
        models.Base.metadata.create_all(bind=engine)
        
        if CLEAR_EXISTING:
            print("Cleaning up old products...")
            db.query(models.Product).delete()
            db.commit()

        print("Seeding Luxury Fashion Products...")
        
        # --- WOMEN'S CATEGORY (25 Items) ---
        women_brands = ["ZARA", "H&M", "GUCCI", "PRADA", "MANGO", "CHANEL"]
        women_images = [
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078709/midi_1_lfnxpz.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078706/midi_2_ga1xrq.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078728/kurti_1_qbx896.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078724/kurti_2_sz3a1j.avif"
        ]
        
        women_products = []
        for i in range(1, 26):
            brand = women_brands[i % len(women_brands)]
            img = women_images[i % len(women_images)]
            women_products.append(models.Product(
                brand=brand,
                name=f"Premium Choice {i} - Women's Special",
                price=1999 + (i * 100),
                originalPrice=3999 + (i * 100),
                discount=50,
                image=img,
                category="women",
                subcategory="topwear",
                badge="Bestseller" if i % 5 == 0 else None
            ))

        # --- MEN'S CATEGORY (25 Items) ---
        men_brands = ["NIKE", "ADIDAS", "RALPH LAUREN", "PUMA", "LEVIS"]
        men_images = [
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164248/thsirt_2_uyztdy.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164244/shirt_5_hmlgoj.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164242/jeans_5_zgnlj9.avif",
            "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164254/trouser_2_uoxnls.avif"
        ]

        men_products = []
        for i in range(1, 26):
            brand = men_brands[i % len(men_brands)]
            img = men_images[i % len(men_images)]
            men_products.append(models.Product(
                brand=brand,
                name=f"Classic Fit {i} - Men's Collection",
                price=1499 + (i * 150),
                originalPrice=2999 + (i * 150),
                discount=50,
                image=img,
                category="men",
                subcategory="casual",
                badge="New Arrival" if i % 4 == 0 else None
            ))

        db.add_all(women_products)
        db.add_all(men_products)
        db.commit()
        print(f"Successfully seeded {len(women_products) + len(men_products)} products!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
