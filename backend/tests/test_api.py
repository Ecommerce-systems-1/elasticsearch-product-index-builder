import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        c.post("/index/rebuild")
        yield c

def test_health_returns_ready(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["ready"] is True
    assert data["doc_count"] == 500

def test_rebuild_returns_200(client):
    r = client.post("/index/rebuild")
    assert r.status_code == 200
    assert r.json()["indexed"] == 500

def test_search_basic_returns_hits(client):
    r = client.get("/search?q=cozy")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0
    assert len(data["hits"]) <= 20

def test_search_hit_schema(client):
    r = client.get("/search?q=sweater")
    hit = r.json()["hits"][0]
    assert "product_id" in hit
    assert "name" in hit
    assert "score" in hit
    assert "matched_fields" in hit
    assert "highlight" in hit

def test_search_category_filter(client):
    r = client.get("/search?q=warm&category=tops")
    hits = r.json()["hits"]
    for h in hits:
        assert h["category"] == "tops"

def test_search_price_filter(client):
    r = client.get("/search?q=jacket&min_price=100&max_price=200")
    hits = r.json()["hits"]
    for h in hits:
        assert 100 <= h["price"] <= 200

def test_search_pagination(client):
    r1 = client.get("/search?q=sweater&page=1&size=5")
    r2 = client.get("/search?q=sweater&page=2&size=5")
    ids1 = [h["product_id"] for h in r1.json()["hits"]]
    ids2 = [h["product_id"] for h in r2.json()["hits"]]
    assert set(ids1).isdisjoint(set(ids2))

def test_facets_returns_categories(client):
    r = client.get("/facets?q=cozy")
    assert r.status_code == 200
    data = r.json()
    assert "category" in data
    assert "color" in data
    assert "price_ranges" in data
    assert sum(data["category"].values()) > 0

def test_facets_price_ranges_all_positive(client):
    r = client.get("/facets?q=warm")
    ranges = r.json()["price_ranges"]
    for pr in ranges:
        assert pr["count"] >= 0

def test_product_detail(client):
    r = client.get("/products/prod_001")
    assert r.status_code == 200
    assert r.json()["id"] == "prod_001"

def test_product_not_found(client):
    r = client.get("/products/nonexistent")
    assert r.status_code == 404