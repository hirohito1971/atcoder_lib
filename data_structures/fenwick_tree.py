# =====================================================
# Fenwick Tree / BIT (Binary Indexed Tree)
# =====================================================
# できること:
#   - add(i, x) : i番目に x を加算            O(log N)
#   - sum(l, r) : 区間[l, r)の和              O(log N)
#   つまり「更新できる累積和」。
#
# セグ木との使い分け:
#   - 和(加算)しかしないなら BIT が短く・速く・バグりにくい
#   - min/max等が欲しいならセグ木
#
# 典型的な使いどころ:
#   - 転倒数 (バブルソートの交換回数)  ★超頻出
#   - 「今までに出た値のうち x 以下は何個?」系のカウント
#     (座標圧縮 snippets/coordinate_compression.py と併用が多い)
#
# 実装のツボ:
#   - 内部は 1-indexed。i & (-i) が「iの最下位ビット」で、
#     これを足し引きして木を登り降りするのが全て
#   - _prefix(i) = [0, i) の和 を部品にして、
#     sum(l, r) = _prefix(r) - _prefix(l) と組み立てる
#     (累積和の「引き算で区間を出す」思想と同じ)
# =====================================================


class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)   # 1-indexed なので n+1 個

    def add(self, i, x):
        """0-indexed の位置 i に x を加算"""
        i += 1                       # 内部は1-indexed
        while i <= self.n:
            self.tree[i] += x
            i += i & (-i)            # 最下位ビットを足して親分へ

    def _prefix(self, i):
        """[0, i) の和 (iは0-indexedの個数)"""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)            # 最下位ビットを引いて下る
        return s

    def sum(self, l, r):
        """区間 [l, r) の和 (0-indexed, 半開区間)"""
        return self._prefix(r) - self._prefix(l)


# =====================================================
# 頻出応用: 転倒数 (i < j かつ a[i] > a[j] のペア数)
#   左から順に見て「自分より大きい値が既に何個出たか」を
#   BITで数える。値の範囲が大きい場合は先に座標圧縮する。
# =====================================================
def inversion_count(a):
    # 座標圧縮 (値を 0..len(set)-1 に潰す)
    comp = {v: i for i, v in enumerate(sorted(set(a)))}
    n = len(comp)
    bit = BIT(n)
    inv = 0
    for x in a:
        c = comp[x]
        # 既に出現した中で「自分より大きい値」の個数
        inv += bit.sum(c + 1, n)
        bit.add(c, 1)   # 自分の出現を記録
    return inv


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    bit = BIT(8)
    for i, v in enumerate([3, 1, 4, 1, 5, 9, 2, 6]):
        bit.add(i, v)
    print(bit.sum(2, 6))              # 4+1+5+9 = 19
    bit.add(3, 100)                    # a[3] += 100
    print(bit.sum(2, 6))              # 119

    print(inversion_count([3, 1, 4, 1, 5]))  # 転倒数 3
