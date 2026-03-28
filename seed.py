from database import SessionLocal, engine
import models

# Reusing the structure from Next.js mock data
brands = ['ZARA', 'H&M', 'GUCCI', 'NIKE', 'MANGO', 'RALPH LAUREN', 'PRADA', 'ADIDAS', "LEVI'S", 'PUMA']
subcategoriesMen = ['Shirts', 'T-shirts', 'Jeans', 'Trousers', 'Jackets']
subcategoriesWomen = ['Dresses', 'Tops', 'Tunics', 'Skirts', 'Jeans', 'Jackets']

cloudinaryImages = [
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078840/jeans_1_-_Copy_lojxgp.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078837/jeans_1_lzc6kz.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078834/jeans_2_kmcza1.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078831/jeans_3_h4szui.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078728/kurti_1_qbx896.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078724/kurti_2_sz3a1j.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078721/kurti_3_wcpta5.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078709/midi_1_lfnxpz.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078706/midi_2_ga1xrq.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078617/midi_3_raeyno.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078513/trouser_1_rgy08x.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078509/trouser_2_xkdfsi.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773078507/trouser_3_mf1vi8.avif"
]
cloudinaryImagesMen = [
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164248/thsirt_2_uyztdy.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164254/trouser_2_uoxnls.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164249/trouser_3_lhwar2.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164247/trouser_1_hin5uo.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164249/trouser_4_dvxqre.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164250/tshirt_4_baz2ho.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164246/thsirt_3_mlxobh.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164242/jeans_5_zgnlj9.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164250/tshirt_1_olze1s.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164244/shirt_5_hmlgoj.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164246/thsirt_5_plsvhi.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164241/shirt_2_cuazmy.avif",
    "https://res.cloudinary.com/djha7wiuw/image/upload/v1773164243/shirt_3_unbhnm.avif"
]

import random

def get_subcategory_from_url(url: str, default_subcategories: list) -> str:
    filename = url.split('/')[-1].lower()
    
    if 'jean' in filename:
        return 'Jeans'
    elif 'trouser' in filename:
        return 'Trousers'
    elif 'kurti' in filename or 'tunic' in filename:
        return 'Tunics'
    elif 'midi' in filename or 'dress' in filename:
        return 'Dresses'
    elif 'skirt' in filename:
        return 'Skirts'
    elif 'top' in filename:
        return 'Tops'
    elif 'thsirt' in filename or 'tshirt' in filename:  # Handling typo in URL
        return 'T-shirts'
    elif 'shirt' in filename:
        return 'Shirts'
    elif 'jacket' in filename:
        return 'Jackets'
    else:
        return random.choice(default_subcategories)

def generate_products(category: str, count: int) -> list:
    products = []
    subcategories = subcategoriesMen if category == 'men' else subcategoriesWomen
    for i in range(1, count + 1):
        brand = random.choice(brands)
        
        image = ""
        if category == 'women':
            image = cloudinaryImages[i % len(cloudinaryImages)]
        else:
            image = cloudinaryImagesMen[i % len(cloudinaryImagesMen)]
            
        subcategory = get_subcategory_from_url(image, subcategories)
        
        price = random.randint(1500, 15000)
        discount = random.randint(10, 60)
        original_price = float(price / (1 - discount / 100))
        
        badges = ['New', 'Bestseller', 'Trending', None, None, None]
        badge = random.choice(badges)
        
        products.append(models.Product(
            id=1000 + i if category == 'men' else 2000 + i,
            brand=brand,
            name=f"{brand} {subcategory} {i}",
            price=price,
            originalPrice=original_price,
            discount=discount,
            image=image,
            badge=badge,
            category=category,
            subcategory=subcategory
        ))
    return products

def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(models.Product).first():
        db.query(models.Product).delete()
        db.commit()

    men_products = generate_products('men', 25)
    women_products = generate_products('women', 25)
    
    db.add_all(men_products + women_products)
    db.commit()
    db.close()
    print("Seeded database with products")

if __name__ == "__main__":
    seed()
