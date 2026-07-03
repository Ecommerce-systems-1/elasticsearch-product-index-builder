import re
from fastapi import APIRouter, HTTPException, Query, Request
from app.models.schemas import Product

router = APIRouter(tags=["search"])


def _highlight(text: str, terms: list[str]) -> str:
    out = text
    for t in terms:
        out = re.sub(rf"(?i)\b({re.escape(t)})\b", r"<em>\1</em>", out)
    return out


@router.get("/search")
def search(
    request: Request,
    q: str = "",
    category: str | None = None,
    color: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    index = request.app.state.index
    terms = index._tok.tokenise(q)
    results = []
    for h in index.search(q):
        p: Product = index.products[h.product_id]
        if category and p.category != category:
            continue
        if color and p.color != color:
            continue
        if min_price is not None and p.price < min_price:
            continue
        if max_price is not None and p.price > max_price:
            continue
        results.append({
            "product_id": p.id,
            "name": p.name,
            "category": p.category,
            "color": p.color,
            "price": p.price,
            "brand": p.brand,
            "score": round(h.score, 4),
            "matched_fields": h.matched_fields,
            "highlight": _highlight(p.name, terms),
        })
    total = len(results)
    start = (page - 1) * size
    return {"total": total, "page": page, "size": size, "hits": results[start:start + size]}


@router.get("/products/{product_id}")
def product_detail(request: Request, product_id: str):
    p = request.app.state.index.products.get(product_id)
    if not p:
        raise HTTPException(404, "Product not found")
    return p
