from dataclasses import dataclass, field
from app.core.tokeniser import Tokeniser
from app.core.scorer import Scorer
from app.models.schemas import Product, SearchHit

@dataclass
class Posting:
    product_id: str
    field: str
    term_freq: int
    field_length: int

@dataclass
class HitResult:
    product_id: str
    score: float
    matched_fields: list[str]

class InvertedIndex:
    FIELD_BOOSTS = {"name": 3.0, "tags": 2.0, "description": 1.0}

    def __init__(self):
        self.postings: dict[str, list[Posting]] = {}
        self.products: dict[str, Product] = {}
        self.doc_freq: dict[str, int] = {}
        self.total_docs: int = 0
        self._tok = Tokeniser()
        self._scorer = Scorer()
        self._avg_field_lengths: dict[str, float] = {}

    def rebuild(self, products: list[Product]) -> None:
        postings: dict[str, list[Posting]] = {}
        products_dict: dict[str, Product] = {}
        doc_freq: dict[str, int] = {}
        field_lengths_sum: dict[str, int] = {"name": 0, "tags": 0, "description": 0}

        for prod in products:
            products_dict[prod.id] = prod
            fields = {
                "name": prod.name,
                "tags": " ".join(prod.tags),
                "description": prod.description,
            }
            seen_terms: set[str] = set()
            for fname, ftext in fields.items():
                tokens = self._tok.tokenise(ftext)
                field_lengths_sum[fname] += len(tokens)
                freq: dict[str, int] = {}
                for t in tokens:
                    freq[t] = freq.get(t, 0) + 1
                for term, tf in freq.items():
                    p = Posting(prod.id, fname, tf, len(tokens))
                    postings.setdefault(term, []).append(p)
                    if term not in seen_terms:
                        doc_freq[term] = doc_freq.get(term, 0) + 1
                        seen_terms.add(term)

        avg_fl = {f: (s / len(products) if products else 1)
                  for f, s in field_lengths_sum.items()}
        # atomic swap
        self.postings = postings
        self.products = products_dict
        self.doc_freq = doc_freq
        self.total_docs = len(products)
        self._avg_field_lengths = avg_fl

    def search(self, query: str) -> list[HitResult]:
        if not query.strip():
            return [HitResult(pid, 0.0, []) for pid in self.products]
        terms = self._tok.tokenise(query)
        scores: dict[str, float] = {}
        matched: dict[str, set[str]] = {}
        for term in terms:
            df = self.doc_freq.get(term, 0)
            idf = self._scorer.idf(self.total_docs, df)
            for posting in self.postings.get(term, []):
                boost = self.FIELD_BOOSTS[posting.field]
                avg_fl = self._avg_field_lengths.get(posting.field, 1)
                tf_n = self._scorer.tf_norm(posting.term_freq, posting.field_length, avg_fl)
                scores[posting.product_id] = scores.get(posting.product_id, 0.0) + idf * boost * tf_n
                matched.setdefault(posting.product_id, set()).add(posting.field)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [HitResult(pid, score, list(matched[pid])) for pid, score in ranked]