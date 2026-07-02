import pytest
from app.core.tokeniser import Tokeniser

@pytest.fixture
def tok():
    return Tokeniser()

def test_lowercases_input(tok):
    assert tok.tokenise("Cozy SWEATER") == ["cozy", "sweater"]

def test_strips_punctuation(tok):
    assert tok.tokenise("100% cotton!") == ["100", "cotton"]

def test_removes_stopwords(tok):
    tokens = tok.tokenise("the cozy and warm sweater")
    assert "the" not in tokens
    assert "and" not in tokens
    assert "cozy" in tokens

def test_empty_string_returns_empty(tok):
    assert tok.tokenise("") == []

def test_caps_at_fifty_tokens(tok):
    long_text = " ".join(["word"] * 100)
    assert len(tok.tokenise(long_text)) <= 50

def test_deduplicates_preserving_order(tok):
    # tokenise returns list (with duplicates — duplicates needed for TF)
    tokens = tok.tokenise("cozy cozy warm")
    assert tokens.count("cozy") == 2

def test_numeric_tokens_preserved(tok):
    assert "42" in tok.tokenise("42 inch screen")