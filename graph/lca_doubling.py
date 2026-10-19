# =====================================================
# LCA (最小共通祖先) + ダブリング  ★青向け追加ファイル
# =====================================================
# できること:
#   - lca(u, v)      : 木の上で u と v の共通祖先のうち最も深いもの
#   - dist(u, v)     : 木の上での u-v 間の距離 (辺数)
#   - la(u, k)       : uのk個上の祖先 (Level Ancestor)
# 前処理 O(N log N), クエリ O(log N)
#
# 典型的な使いどころ:
#   - 「木上の2点間パス」に関する質問全般
#     (パスの長さ、パス上に頂点xはあるか、など)
#   - ダブリング自体が汎用テク:
#     「1回の遷移先が決まっている状態をK回進めたらどこ?」
#     (K <= 10^18 でもOK) ← ABC-D/Eで頻出の考え方 ★
#
# ダブリングの気持ち:
#   parent[k][v] = 「vの 2^k 個上の祖先」を前計算しておく。
#   parent[k][v] = parent[k-1][ parent[k-1][v] ]
#   (2^k上 = 2^(k-1)上のさらに2^(k-1)上)
#   すると「7個上」= 4上→2上→1上 のように
#   Kを2進数に分解してO(log K)で飛べる。
# =====================================================


class LCA:
    def __init__(self, n, graph, root=0):
        """
        n     : 頂点数
        graph : 木の隣接リスト (無向) graph[u] = [v, ...]
        root  : 根
        """
        self.n = n
        self.LOG = max(1, (n - 1).bit_length())
        self.depth = [0] * n
        # parent[k][v] = vの2^k個上の祖先 (いなければ -1)
        self.parent = [[-1] * n for _ in range(self.LOG)]

        # --- BFSで depth と parent[0] を作る (非再帰) ---
        from collections import deque
        visited = [False] * n
        visited[root] = True
        dq = deque([root])
        while dq:
            u = dq.popleft()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    self.depth[v] = self.depth[u] + 1
                    self.parent[0][v] = u
                    dq.append(v)

        # --- ダブリングテーブル構築 ---
        for k in range(self.LOG - 1):
            for v in range(n):
                p = self.parent[k][v]
                # 2^(k+1)上 = (2^k上) の (2^k上)
                self.parent[k + 1][v] = -1 if p == -1 else self.parent[k][p]

    def la(self, u, k):
        """uのk個上の祖先。いなければ -1"""
        for i in range(self.LOG):
            if k >> i & 1:            # kの2進数のiビット目が立っていたら
                u = self.parent[i][u]  # 2^i 上に飛ぶ
                if u == -1:
                    return -1
        return u

    def lca(self, u, v):
        # 1) 深い方を浅い方の高さまで引き上げる
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.la(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        # 2) 「祖先が一致しないギリギリまで」大きいジャンプから飛ぶ
        for k in range(self.LOG - 1, -1, -1):
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        # 3) 最後に1個上がLCA
        return self.parent[0][u]

    def dist(self, u, v):
        """木上の距離 (辺数)。深さの和から共通部分を2回引く"""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    #        0
    #       / \
    #      1   2
    #     / \    \
    #    3   4    5
    n = 6
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    lca = LCA(n, graph, root=0)
    print(lca.lca(3, 4))   # 1
    print(lca.lca(3, 5))   # 0
    print(lca.dist(3, 5))  # 4
    print(lca.la(3, 2))    # 3の2個上 → 0
