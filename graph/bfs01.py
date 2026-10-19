# =====================================================
# 0-1 BFS (辺の重みが 0 か 1 だけのグラフの最短路)
# =====================================================
# 計算量: O(V + E)  ← ダイクストラの log が消える
#
# 使える条件: 辺の重みが 0 または 1 のみ
#
# 典型的な使いどころ:
#   - 「壁を壊す回数を最小化」系 (移動コスト0, 壊すコスト1)
#   - 「方向転換の回数を最小化」系
#   - グリッド問題で頻出 ★
#
# 仕組み (ここが面白いところ):
#   deque (両端キュー) を使い、
#     重み0の辺 → appendleft (キューの先頭に入れる)
#     重み1の辺 → append     (キューの末尾に入れる)
#   すると deque の中は常に「距離の昇順」が保たれるので、
#   ヒープなしでダイクストラと同じ正しさが得られる。
# =====================================================

from collections import deque


def bfs01(n, graph, start):
    """
    n     : 頂点数
    graph : 隣接リスト。graph[u] = [(v, w), ...]  w は 0 or 1
    start : 始点
    戻り値: dist[v] = 最短距離 (到達不能は INF)
    """
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])

    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)   # コスト0 → 先頭へ (優先)
                else:
                    dq.append(v)       # コスト1 → 末尾へ
    return dist


# =====================================================
# グリッド版の例: '#'を壊すのに1コスト、'.'は0コストで移動
# (よくある「壁破壊最小回数」の型)
# =====================================================
def bfs01_grid(grid, sy, sx):
    H, W = len(grid), len(grid[0])
    INF = float("inf")
    dist = [[INF] * W for _ in range(H)]
    dist[sy][sx] = 0
    dq = deque([(sy, sx)])

    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            w = 1 if grid[ny][nx] == "#" else 0
            nd = dist[y][x] + w
            if nd < dist[ny][nx]:
                dist[ny][nx] = nd
                if w == 0:
                    dq.appendleft((ny, nx))
                else:
                    dq.append((ny, nx))
    return dist


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    grid = [
        ".#.",
        ".#.",
        "...",
    ]
    d = bfs01_grid(grid, 0, 0)
    print(d[0][2])   # 右上へ: 壁を迂回できるので 0
    grid2 = [
        ".#.",
        "###",
        ".#.",
    ]
    d2 = bfs01_grid(grid2, 0, 0)
    print(d2[2][2])  # 壁を最低2枚壊す必要 → 2
