# =====================================================
# BFS (幅優先探索) : グリッド版 & グラフ版
# =====================================================
# ★追加ファイル: これはABCのC〜D問題で最頻出の道具なので、
#   最終的には見ないで書けるようになりたい筆頭。
#
# 計算量: O(V + E)  (グリッドなら O(H*W))
#
# できること: 辺の重みが全て1のときの最短距離
#   (重みが0/1 → bfs01.py, 一般の非負 → dijkstra.py)
#
# 実装のツボ:
#   - dist配列を「未訪問フラグ」兼「距離」として使う (-1 = 未訪問)
#   - キューは collections.deque (listのpop(0)はO(N)なので厳禁!)
#   - グリッドでは方向ベクトル (dy, dx) を配列にして回す
#   - 訪問チェックは「キューに入れる時」に行う
#     (取り出す時に行うと同じ頂点が複数回キューに入り遅くなる)
# =====================================================

from collections import deque


def bfs_grid(grid, sy, sx, wall="#"):
    """
    grid : 文字列のリスト。wall のマスは通れない
    (sy, sx) : スタート座標
    戻り値: dist[y][x] = 最短手数 (到達不能は -1)
    """
    H, W = len(grid), len(grid[0])
    dist = [[-1] * W for _ in range(H)]
    dist[sy][sx] = 0
    dq = deque([(sy, sx)])

    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            # 場外チェック → 壁チェック → 訪問済みチェック の順が定石
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            if grid[ny][nx] == wall:
                continue
            if dist[ny][nx] != -1:
                continue
            dist[ny][nx] = dist[y][x] + 1
            dq.append((ny, nx))
    return dist


def bfs_graph(n, graph, start):
    """
    グラフ版。graph[u] = [v, ...] (隣接リスト, 重みなし)
    戻り値: dist[v] = 最短手数 (到達不能は -1)
    """
    dist = [-1] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist


# =====================================================
# 多始点BFS: 「複数のスタート地点から一番近い距離」
#   最初に全ての始点を距離0でキューに入れるだけ。
#   例:「各マスについて、最寄りの'F'までの距離」系で頻出
# =====================================================
def multi_source_bfs_grid(grid, starts, wall="#"):
    H, W = len(grid), len(grid[0])
    dist = [[-1] * W for _ in range(H)]
    dq = deque()
    for sy, sx in starts:          # ★始点を全部先に入れる
        dist[sy][sx] = 0
        dq.append((sy, sx))
    while dq:
        y, x = dq.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] != wall and dist[ny][nx] == -1:
                dist[ny][nx] = dist[y][x] + 1
                dq.append((ny, nx))
    return dist


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    grid = [
        "S..#",
        ".#.#",
        "...G",
    ]
    # S, G の位置を探す型もよく書くので覚えておく
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "S":
                sy, sx = y, x
            if grid[y][x] == "G":
                gy, gx = y, x
    d = bfs_grid(grid, sy, sx)
    print(d[gy][gx])   # 5
