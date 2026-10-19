# =====================================================
# トポロジカルソート (Kahnのアルゴリズム / BFS版)
# =====================================================
# 計算量: O(V + E)
#
# できること: DAG (閉路のない有向グラフ) の頂点を
#   「全ての辺が前→後ろを向く」ように並べる
#
# 典型的な使いどころ:
#   - 依存関係の解決 (「AをやってからB」系)
#   - ★DAG上のDP: トポロジカル順に配れば正しい順序で更新できる
#     (最長経路、経路数のカウントなど。青を目指すなら頻出)
#   - 閉路検出: ソート結果の長さ < V なら閉路がある
#
# 実装のツボ:
#   - 各頂点の「入次数 (入ってくる辺の数)」を数えておき、
#     入次数0の頂点からキューに入れて処理する
#   - 頂点を処理したら、そこから出る辺の先の入次数を減らし、
#     0になったらキューに追加
#   - 辞書順最小が欲しいときは deque を heapq に替えるだけ
# =====================================================

from collections import deque


def topological_sort(n, graph):
    """
    n     : 頂点数
    graph : 隣接リスト。graph[u] = [v, ...] (有向辺 u→v)
    戻り値: トポロジカル順の頂点リスト。
            長さが n 未満なら閉路が存在する。
    """
    indeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            indeg[v] += 1

    # 入次数0 = 「誰にも依存されていない=最初にやれる」頂点
    dq = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1          # uが片付いたので依存を1つ減らす
            if indeg[v] == 0:
                dq.append(v)
    return order


# =====================================================
# 応用の型: DAG上のDP (最長経路)
#   トポロジカル順に「配るDP」をするだけ。
#   dp[v] = vに到達する経路の最大辺数
# =====================================================
def longest_path_on_dag(n, graph):
    order = topological_sort(n, graph)
    assert len(order) == n, "閉路があります"
    dp = [0] * n
    for u in order:                 # ★この順で回すのがポイント
        for v in graph[u]:
            dp[v] = max(dp[v], dp[u] + 1)
    return max(dp)


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    n = 5
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    order = topological_sort(n, graph)
    print(order)                        # 例: [0, 1, 2, 3, 4]
    print(len(order) == n)              # True → 閉路なし
    print(longest_path_on_dag(n, graph))  # 3 (0→1→3→4 など)
