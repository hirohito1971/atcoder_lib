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
#
# ★注意: dist は「短くなったら書き換える」。積んだ時点で確定させない!
#   普通のBFSと違い、先に重み1で見つけた頂点に、後から重み0で
#   もっと短く辿り着くことがある。(ABC481-D で WA)
#   反例: 1→2, 1→3, 2→3 で S=1, T=3 (2が1の最小の行き先、3が2の最小の行き先)
#         正解 0。積んだときに確定させると 1 になる。
# =====================================================

from collections import deque

INF = 10**18


def bfs01(n, graph, start):
    """
    n     : 頂点数
    graph : 隣接リスト。graph[u] = [(v, w), ...]  w は 0 or 1
    start : 始点
    戻り値: dist[v] = 最短距離 (到達不能は INF)
    """
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
                    dq.appendleft(v)  # コスト0 → 先頭へ (優先)
                else:
                    dq.append(v)  # コスト1 → 末尾へ
    return dist


# =====================================================
# グリッド版の例: '#'を壊すのに1コスト、'.'は0コストで移動
# (よくある「壁破壊最小回数」の型)
# =====================================================
def bfs01_grid(grid, sy, sx):
    H, W = len(grid), len(grid[0])

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