# =====================================================
# ダイクストラ法 (単一始点最短路, 辺の重みが非負)
# =====================================================
# 計算量: O((V + E) log V)
#
# 使える条件: ★辺の重みが全て 0 以上★ (負の辺があるとダメ
#   → 負辺ありならベルマンフォード)
#
# 典型的な使いどころ:
#   - 重み付きグラフの最短距離 (そのまま)
#   - 「状態」を頂点とみなす拡張ダイクストラ ★青を目指すなら重要
#     例: (頂点, 切符の残り枚数) をひとつの状態にする、など
#
# 実装のツボ:
#   - ヒープには (暫定距離, 頂点) のタプルを入れる
#     → タプルは第1要素から比較されるので距離が小さい順に出てくる
#   - 取り出した時に dist[v] < d なら「古い情報」なのでスキップ
#     (同じ頂点が複数回ヒープに入るのは正常。visitedフラグ管理より
#      この「スキップ方式」の方がバグりにくい)
# =====================================================

import heapq


def dijkstra(n, graph, start):
    """
    n     : 頂点数
    graph : 隣接リスト。graph[u] = [(v, w), ...]  (u→v, 重みw)
    start : 始点
    戻り値: dist[v] = startからvへの最短距離 (到達不能は INF)
    """
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    heap = [(0, start)]   # (距離, 頂点)

    while heap:
        d, u = heapq.heappop(heap)
        # 既により短い距離で確定済みなら、この情報は古いので捨てる
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def dijkstra_with_path(n, graph, start, goal):
    """経路復元つき版。(最短距離, 経路リスト) を返す"""
    INF = float("inf")
    dist = [INF] * n
    prev = [-1] * n       # 最短路で「どこから来たか」を記録
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u          # ★ここで来た道を覚える
                heapq.heappush(heap, (nd, v))

    if dist[goal] == INF:
        return INF, []
    # goal から prev を辿って逆順に経路を作る
    path = []
    cur = goal
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    return dist[goal], path[::-1]


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    # 頂点0..4, 有向グラフ
    n = 5
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        # 無向グラフなら逆向きも: graph[v].append((u, w))

    print(dijkstra(n, graph, 0))          # [0, 3, 1, 4, 7]
    print(dijkstra_with_path(n, graph, 0, 4))  # (7, [0, 2, 1, 3, 4])
