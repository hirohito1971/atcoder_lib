# =====================================================
# 座標圧縮  ★追加ファイル
# =====================================================
# 値の範囲が大きい (〜10^18) が、登場する値の「種類数」は
# 少ない (〜10^5) とき、値を 0, 1, 2, ... の連番に潰す。
#
# 使いどころ:
#   - BIT/セグ木に値を乗せたいが、値域が大きすぎて配列が作れない
#     (転倒数、「x以下の個数」クエリなど) ★BITとセットで頻出
#   - 大きい座標のグリッド・区間を扱う問題
#
# 型は2行で書ける:
#   sorted(set(...)) で「重複を消してソート」
#   {v: i for ...}   で「値→連番」の辞書を作る
# =====================================================

from bisect import bisect_left


def compress(a):
    """
    戻り値: (compressed, sorted_vals)
      compressed  : aの各要素を連番に置き換えたリスト
      sorted_vals : 連番→元の値 の対応 (復元用)
    """
    sorted_vals = sorted(set(a))
    rank = {v: i for i, v in enumerate(sorted_vals)}
    compressed = [rank[x] for x in a]
    return compressed, sorted_vals


# 辞書を作らず bisect で引く版 (クエリの値がaに含まれるとは限らない時に便利)
def compress_bisect(a):
    sorted_vals = sorted(set(a))
    compressed = [bisect_left(sorted_vals, x) for x in a]
    return compressed, sorted_vals


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    a = [100, 10**9, 5, 100, 7]
    comp, vals = compress(a)
    print(comp)    # [2, 3, 0, 2, 1]
    print(vals)    # [5, 7, 100, 1000000000]
    # 復元: vals[comp[i]] == a[i]
    print([vals[c] for c in comp])   # 元に戻る

    # 型として覚える最小形はこの2行:
    # rank = {v: i for i, v in enumerate(sorted(set(a)))}
    # b = [rank[x] for x in a]
