import re
from typing import ClassVar

STOPWORDS: set[str] = {
    "a","an","the","and","or","but","in","on","at","to","for",
    "of","with","by","from","is","it","its","be","as","are","was",
    "were","been","this","that","these","those","has","have","had",
}

class Tokeniser:
    MAX_TOKENS: ClassVar[int] = 50

    def tokenise(self, text: str) -> list[str]:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
        return tokens[: self.MAX_TOKENS]