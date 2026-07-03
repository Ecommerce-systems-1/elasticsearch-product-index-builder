from fastapi import APIRouter, Request

router = APIRouter(tags=["facets"])

PRICE_RANGES = [(0, 50), (50, 100), (100, 200), (200, 500)]


@router.get("/facets")
def facets(request: Request, q: str = ""):
    index = request.app.state.index
    category: dict[str, int] = {}
    color: dict[str, int] = {}
    range_counts = [0] * len(PRICE_RANGES)
    for h in index.search(q):
        p = index.products[h.product_id]
        category[p.category] = category.get(p.category, 0) + 1
        color[p.color] = color.get(p.color, 0) + 1
        for i, (lo, hi) in enumerate(PRICE_RANGES):
            if lo <= p.price < hi:
                range_counts[i] += 1
                break
    return {
        "category": category,
        "color": color,
        "price_ranges": [
            {"range": f"{lo}-{hi}", "count": c}
            for (lo, hi), c in zip(PRICE_RANGES, range_counts)
        ],
    }
