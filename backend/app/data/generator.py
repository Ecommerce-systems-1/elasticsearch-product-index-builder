import random
from app.models.schemas import Product
from datetime import datetime, timezone

CATEGORIES = ["tops","bottoms","shoes","accessories","outerwear","home"]
COLORS = ["red","blue","green","black","white","grey","brown","navy"]
BRANDS = ["Verano","NordStyle","LuxCore","UrbanThread","CozyMade",
          "PeakWear","SolStudio","ArcLine","DriftCo","PureFit"]
ADJECTIVES = ["cozy","sleek","classic","modern","durable","vibrant",
              "lightweight","premium","casual","elegant","bold","soft"]
NOUNS = {
    "tops":["sweater","t-shirt","blouse","hoodie","cardigan","tank","shirt"],
    "bottoms":["jeans","chinos","shorts","leggings","skirt","trousers"],
    "shoes":["sneakers","boots","sandals","loafers","heels","mules"],
    "accessories":["scarf","belt","hat","bag","wallet","sunglasses"],
    "outerwear":["jacket","coat","parka","blazer","windbreaker"],
    "home":["pillow","blanket","lamp","rug","candle","throw"],
}
TAG_POOL = ["cozy","warm","casual","sporty","formal","vintage","minimal",
            "sustainable","handmade","limited","sale","new","trending",
            "comfortable","durable","lightweight","breathable","waterproof"]

class ProductGenerator:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def generate(self, count: int = 500) -> list[Product]:
        products = []
        for i in range(1, count + 1):
            cat = self.rng.choice(CATEGORIES)
            adj = self.rng.choice(ADJECTIVES)
            noun = self.rng.choice(NOUNS[cat])
            color = self.rng.choice(COLORS)
            brand = self.rng.choice(BRANDS)
            price = round(self.rng.uniform(9.99, 499.99), 2)
            tags = self.rng.sample(TAG_POOL, self.rng.randint(3, 6))
            desc = (
                f"This {adj} {noun} from {brand} is perfect for any occasion. "
                f"Available in {color}, it combines style with comfort. "
                f"Crafted with care for the modern consumer."
            )
            products.append(Product(
                id=f"prod_{i:03d}",
                name=f"{adj.title()} {color.title()} {noun.title()}",
                description=desc,
                category=cat,
                color=color,
                price=price,
                tags=tags,
                brand=brand,
                in_stock=self.rng.random() > 0.1,
                created_at=datetime.now(timezone.utc).isoformat(),
            ))
        return products