import pytest
from app.data.generator import ProductGenerator

@pytest.fixture
def gen():
    return ProductGenerator(seed=42)

def test_generates_correct_count(gen):
    products = gen.generate(500)
    assert len(products) == 500

def test_ids_are_unique(gen):
    products = gen.generate(500)
    ids = [p.id for p in products]
    assert len(ids) == len(set(ids))

def test_deterministic_with_same_seed():
    g1 = ProductGenerator(seed=42)
    g2 = ProductGenerator(seed=42)
    p1 = g1.generate(10)
    p2 = g2.generate(10)
    assert [p.name for p in p1] == [p.name for p in p2]

def test_different_seed_different_output():
    p1 = ProductGenerator(seed=1).generate(10)
    p2 = ProductGenerator(seed=2).generate(10)
    assert [p.name for p in p1] != [p.name for p in p2]

def test_price_in_valid_range(gen):
    products = gen.generate(100)
    for p in products:
        assert 9.99 <= p.price <= 499.99

def test_categories_are_valid(gen):
    valid = {"tops","bottoms","shoes","accessories","outerwear","home"}
    products = gen.generate(100)
    for p in products:
        assert p.category in valid

def test_tags_list_has_3_to_6_items(gen):
    products = gen.generate(100)
    for p in products:
        assert 3 <= len(p.tags) <= 6

def test_all_categories_represented(gen):
    products = gen.generate(500)
    cats = {p.category for p in products}
    assert cats == {"tops","bottoms","shoes","accessories","outerwear","home"}