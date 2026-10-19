# =====================================================
# Union-Find (素集合データ構造 / DSU)
# =====================================================
# できること:
#   - unite(x, y): xの属するグループとyの属するグループを合併
#   - same(x, y) : xとyが同じグループか判定
#   - size(x)    : xの属するグループの要素数
# 計算量: ほぼ O(1) (正確にはならし O(α(N)), αはアッカーマン逆関数)
#
# 典型的な使いどころ:
#   - 「辺を追加していって連結かどうか」系 (クラスカル法もこれ)
#   - 「同じグループに属するか」のクエリ
#   - グラフの連結成分の個数・サイズ
#
# 実装のツボ (手で書けるようになりたいポイント):
#   - parent配列1本で「親」と「サイズ」を兼用するテク:
#     負の値なら「自分が根で、絶対値がグループサイズ」
#     正の値なら「親の頂点番号」
#   - find で経路圧縮 (根まで辿ったら、道中の頂点を根に直結)
#   - unite はサイズが大きい方に小さい方をぶら下げる (union by size)
# =====================================================


class UnionFind:
    def __init__(self, n):
        # 全要素が「自分が根・サイズ1」の状態で開始
        # -1 = 「根であり、サイズは1」
        self.parent = [-1] * n

    def find(self, x):
        """xの根を返す (経路圧縮つき・非再帰)"""
        # まず根まで辿る
        root = x
        while self.parent[root] >= 0:
            root = self.parent[root]
        # 経路圧縮: 道中の頂点を全部、根に直接つなぎ直す
        # → 次回以降の find がほぼ O(1) になる
        while x != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def unite(self, x, y):
        """xとyのグループを合併。すでに同じなら False を返す"""
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        # union by size: サイズの大きい方(xとする)に小さい方をぶら下げる
        # parent が負の値でサイズを持っているので「小さい方が大きい」に注意
        # (parent[x] = -5 はサイズ5)
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.parent[x] += self.parent[y]  # サイズを合算
        self.parent[y] = x                # yの根をxにする
        return True

    def same(self, x, y):
        """xとyが同じグループなら True"""
        return self.find(x) == self.find(y)

    def size(self, x):
        """xの属するグループの要素数"""
        return -self.parent[self.find(x)]

    def groups(self):
        """全グループを {根: [メンバー...]} で返す (デバッグや集計に便利)"""
        from collections import defaultdict
        d = defaultdict(list)
        for i in range(len(self.parent)):
            d[self.find(i)].append(i)
        return d


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    uf = UnionFind(5)          # 頂点 0..4
    uf.unite(0, 1)
    uf.unite(1, 2)
    print(uf.same(0, 2))       # True
    print(uf.same(0, 3))       # False
    print(uf.size(0))          # 3
    print(uf.groups())         # {0: [0, 1, 2], 3: [3], 4: [4]} など
