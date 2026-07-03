from fastapi import APIRouter, Request
from app.data.generator import ProductGenerator

router = APIRouter(tags=["index"])


@router.post("/index/rebuild")
def rebuild(request: Request):
    index = request.app.state.index
    products = ProductGenerator(seed=42).generate(500)
    index.rebuild(products)
    return {"indexed": index.total_docs}


@router.get("/health")
def health(request: Request):
    index = request.app.state.index
    return {"status": "ok", "ready": index.total_docs > 0, "doc_count": index.total_docs}
