from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.inverted_index import InvertedIndex
from app.data.generator import ProductGenerator
from app.routers import index_router, search_router, facet_router
import pathlib

index = InvertedIndex()

@asynccontextmanager
async def lifespan(app: FastAPI):
    products = ProductGenerator(seed=42).generate(500)
    index.rebuild(products)
    app.state.index = index
    yield

app = FastAPI(title="Product Index Builder", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(index_router.router)
app.include_router(search_router.router)
app.include_router(facet_router.router)

static_dir = pathlib.Path("/app/frontend/out")
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")