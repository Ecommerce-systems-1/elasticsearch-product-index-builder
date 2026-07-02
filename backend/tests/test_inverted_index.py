import pytest
from app.core.inverted_index import InvertedIndex
from app.models.schemas import Product

def make_products():
    return [
        Product(id="p1", name="Cozy Warm Sweater", description="A cozy sweater for winter",
                category="tops", color="blue", price=49.99, tags=["cozy","warm"],
                brand="TestBrand", in_stock=True, created_at="2026-01-01T00:00:00Z"),
        Product(id="p2", name="Blue Sneakers", description="Light running shoes",
                category="shoes", color="blue", price=89.99, tags=["sporty","light"],
                brand="TestBrand", in_stock=True, created_at="2026-01-01T00:00:00Z"),
        Product(id="p3", name="Classic Jacket", description="Warm classic outerwear",
                category="outerwear", color="black", price=149.99, tags=["classic","warm"],
                brand="TestBrand", in_stock=True, created_at="2026-01-01T00:00:00Z"),
    ]

@pytest.fixture
def idx():
    index = InvertedIndex()
    index.rebuild(make_products())
    return index

def test_total_docs_correct(idx):
    assert idx.total_docs == 3

def test_token_in_postings(idx):
    assert "cozy" in idx.postings
    assert "sweater" in idx.postings

def test_posting_contains_correct_product(idx):
    postings = idx.postings["cozy"]
    product_ids = [p.product_id for p in postings]
    assert "p1" in product_ids

def test_doc_freq_correct(idx):
    assert idx.doc_freq["warm"] == 2   # appears in p1 name/desc and p3 desc
    assert idx.doc_freq["cozy"] == 1

def test_search_returns_matching_products(idx):
    hits = idx.search("cozy sweater")
    ids = [h.product_id for h in hits]
    assert "p1" in ids

def test_search_ranks_better_match_higher(idx):
    hits = idx.search("cozy")
    assert hits[0].product_id == "p1"

def test_search_empty_query_returns_all(idx):
    hits = idx.search("")
    assert len(hits) == 3

def test_rebuild_replaces_old_index(idx):
    new_products = [make_products()[0]]
    idx.rebuild(new_products)
    assert idx.total_docs == 1
    assert "sneakers" not in idx.postings