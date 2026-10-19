from math import isqrt

def count_squares(L, R):
    """区間 [L, R] に含まれる正の平方数 k² (k ≥ 1) の個数。
    isqrt(n) = n 以下の正の平方数の個数、を引き算で使う。O(1)。"""
    L = max(L, 1)
    if R < L:
        return 0
    return isqrt(R) - isqrt(L - 1)