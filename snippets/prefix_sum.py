# =====================================================
# 累積和 / 2次元累積和 / いもす法 の型
# =====================================================
# 全て共通の思想: 「区間の和 = 引き算」「区間の更新 = 端点だけ記録」
#
# 事故ポイントは1つだけ:
#   ★累積和配列は長さ N+1 にして、prefix[i+1] に a[0..i] の和を置く★
#   こうすると 区間[l, r) の和 = prefix[r] - prefix[l] が
#   l=0 でも崩れない。この型で固定する。
# =====================================================

from itertools import accumulate


# -----------------------------------------------------
# 1次元累積和
# -----------------------------------------------------
def prefix_sum_1d(a):
    n = len(a)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]
    return prefix
    # ワンライナー版 (accumulateは覚えると速い):
    # prefix = [0] + list(accumulate(a))


# 区間 [l, r) の和 (半開区間で統一する)
def range_sum(prefix, l, r):
    return prefix[r] - prefix[l]


# -----------------------------------------------------
# 2次元累積和
#   prefix[i][j] = 「左上(0,0)〜(i-1, j-1)の長方形」の総和
#   長方形和は「大きい所から縦横を引いて、二重に引いた角を足し戻す」
#   (包除原理の絵を1回自分で描くと忘れない)
# -----------------------------------------------------
def prefix_sum_2d(grid):
    H, W = len(grid), len(grid[0])
    prefix = [[0] * (W + 1) for _ in range(H + 1)]
    for i in range(H):
        for j in range(W):
            prefix[i + 1][j + 1] = (
                grid[i][j]
                + prefix[i][j + 1]     # 上の長方形
                + prefix[i + 1][j]     # 左の長方形
                - prefix[i][j]         # 重なり(左上)を引き戻す
            )
    return prefix


# 長方形 [y1, y2) × [x1, x2) の和
def rect_sum(prefix, y1, x1, y2, x2):
    return (
        prefix[y2][x2]
        - prefix[y1][x2]
        - prefix[y2][x1]
        + prefix[y1][x1]
    )


# -----------------------------------------------------
# いもす法 (差分配列): 「区間への一様加算が大量」→「最後に累積」
#   [l, r) に x を足す = diff[l] += x, diff[r] -= x と記録し、
#   全クエリ後に累積和を取ると各点の値になる。
#   クエリ O(1) × Q回 + 復元 O(N)
# -----------------------------------------------------
def imos_1d(n, queries):
    """queries = [(l, r, x), ...] : [l, r) に x を加算"""
    diff = [0] * (n + 1)
    for l, r, x in queries:
        diff[l] += x       # ここから効果が始まる
        diff[r] -= x       # ここで効果が終わる
    # 累積して実際の値に戻す
    res = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        res[i] = cur
    return res


# 2次元いもす: 長方形 [y1,y2)×[x1,x2) に x を足すなら
#   diff[y1][x1] += x; diff[y1][x2] -= x
#   diff[y2][x1] -= x; diff[y2][x2] += x
# → 横方向に累積 → 縦方向に累積 の2段で復元


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    a = [3, 1, 4, 1, 5]
    p = prefix_sum_1d(a)
    print(range_sum(p, 1, 4))   # 1+4+1 = 6

    g = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    p2 = prefix_sum_2d(g)
    print(rect_sum(p2, 0, 0, 2, 2))   # 1+2+4+5 = 12

    print(imos_1d(5, [(0, 3, 1), (2, 5, 10)]))   # [1, 1, 11, 10, 10]
