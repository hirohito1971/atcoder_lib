# =====================================================
# ワーシャルフロイド法 (全点対最短路)
# =====================================================
# 計算量: O(V^3)  → 頂点数 N <= 400 程度が目安
#
# 典型的な使いどころ:
#   - 「全ての頂点ペアの最短距離」が必要なとき
#   - 「辺を1本追加したら最短距離はどう変わる?」系
#     (先に全点対を求めておくと差分計算が楽)
#   - 到達可能性判定 (重みを0/1にして「推移閉包」)
#
# 実装のツボ:
#   - 3重ループの順番は ★k(経由点)が一番外側★
#     ここを間違えると正しく更新されない。
#     「経由してよい頂点を k=0,1,2,... と1つずつ解禁していく」
#     というDPだと理解すると順番を忘れない。
#   - dist[i][i] = 0 の初期化を忘れない
#   - 多重辺があり得る入力では min を取りながら読み込む
# =====================================================


def warshall_floyd(n, dist):
    """
    n    : 頂点数
    dist : n×n の距離行列 (直接辺がなければ INF, dist[i][i]=0)
           ★破壊的に更新する
    戻り値: 全点対最短距離の行列
    """
    for k in range(n):          # 経由してよい頂点を1つずつ増やす
        dk = dist[k]            # 行を変数に出すとPythonでは少し速い
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == float("inf"):
                continue        # i→k が無理なら k 経由はあり得ない
            for j in range(n):
                # i→k→j が現状の i→j より短ければ更新
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd
    return dist


def has_negative_cycle(dist):
    """WF実行後、dist[i][i] < 0 の頂点があれば負閉路あり"""
    return any(dist[i][i] < 0 for i in range(len(dist)))


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    INF = float("inf")
    n = 4
    # 距離行列の初期化の型
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    edges = [(0, 1, 5), (1, 2, 3), (0, 2, 10), (2, 3, 1)]
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)   # 多重辺対策のmin
        dist[v][u] = min(dist[v][u], w)   # 無向グラフの場合

    warshall_floyd(n, dist)
    print(dist[0][3])   # 0→1→2→3 = 9
