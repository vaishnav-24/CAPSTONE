"""Seed sample products. Run: python -m scripts.seed_products"""
from app import create_app
from app.extensions import db
from app.models import Product

SAMPLES = [
    ("Wireless Headphones", "Comfortable over-ear headphones with 30h battery.", 79.99, 25, "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?w=600"),
    ("Smart Watch", "Track fitness, heart rate, and notifications on the go.", 149.00, 18, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"),
    ("Bluetooth Speaker", "Portable speaker with rich bass and water resistance.", 49.50, 40, "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600"),
    ("Mechanical Keyboard", "Tactile switches, RGB backlight, durable build.", 99.99, 15, "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600"),
    ("4K Webcam", "Crystal-clear video for meetings and streaming.", 89.00, 22, "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=600"),
    ("Ergonomic Mouse", "Reduce wrist strain with this contoured design.", 39.99, 35, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600"),
]


def main() -> None:
    app = create_app()
    with app.app_context():
        if Product.query.count() > 0:
            print("Products already exist. Skipping.")
            return
        for name, desc, price, stock, img in SAMPLES:
            db.session.add(Product(name=name, description=desc, price=price, stock_quantity=stock, image_url=img))
        db.session.commit()
        print(f"Seeded {len(SAMPLES)} products.")


if __name__ == "__main__":
    main()
