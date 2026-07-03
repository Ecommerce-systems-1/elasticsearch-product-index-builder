import math


class Scorer:
    def idf(self, N: int, df: int, eps: float = 0.5) -> float:
        return math.log(1 + (N - df + eps) / (df + eps))

    def tf_norm(self, tf: int, field_len: int, avg_fl: float,
                k1: float = 1.2, b: float = 0.75) -> float:
        return tf / (tf + k1 * (1 - b + b * field_len / max(avg_fl, 1)))
