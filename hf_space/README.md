---
title: Product Index Builder
emoji: 🔎
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Product Index Builder

A from-scratch inverted index over 500 products: BM25-style scoring, field boosts, filters, facets, and highlighting.

The landing page is an interactive API console — click any endpoint to call the live API.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Ready + doc count |
| GET | `/search?q=` | Ranked search with filters + pagination |
| GET | `/facets?q=` | Category/color/price facets |
| GET | `/products/{id}` | Product detail |
| POST | `/index/rebuild` | Rebuild the index |

## Stack

Python 3.11 · FastAPI · SQLite · Pydantic v2 · Next.js 14 (static export) · Tailwind CSS · Docker
