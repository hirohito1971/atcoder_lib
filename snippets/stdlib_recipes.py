"""
snippets/stdlib_recipes.py
AtCoder で使う Python 標準ライブラリのレシピ集（コピペ用＋動作確認テスト付き）

使い方:
  - 各関数はそのままコピペして使える最小形
  - `python stdlib_recipes.py` でテストが走る（全部通れば "all ok"）

教訓（ABC479-D）:
  前計算配列は「経路」ではなく「集約値」で定義する。
  例: × LR = 左→右の経路   ○ minR[i] = min(R[0..i])
  経路の組み立て（L[s] + minR[s] など）はクエリ側の式で行う。
  書く前に定義を1行コメントにし、作る側・使う側の両方を照合する。
"""

import math
import operator
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, cmp_to_key
from heapq import heappop, heappush, nsmallest
from itertools import (accumulate, chain, combinations,
                       combinations_with_replacement, groupby, pairwise,
                       permutations, product)


# ============================================================
# 1. 累積系（itertools.accumulate）
# ============================================================

def prefix_sum(A):
    """S[i] = sum(A[0..i-1])。区間 [l, r) の和は S[r] - S[l]"""
    return list(accumulate(A, initial=0))


def prefix_min(A):
    """P[i] = min(A[0..i])"""
    return list(accumulate(A, min))


def suffix_min(A):
    """S[i] = min(A[i..N-1])"""
    return list(accumulate(reversed(A), min))[::-1]


def prefix_max(A):
    """P[i] = max(A[0..i])"""
    return list(accumulate(A, max))


def suffix_max(A):
    """S[i] = max(A[i..N-1])"""
    return list(accumulate(reversed(A), max))[::-1]


def prefix_xor(A):
    """X[i] = A[0]^...^A[i-1]。区間 [l, r) の xor は X[r] ^ X[l]"""
    return list(accumulate(A, operator.xor, initial=0))


# ============================================================
# 2. 列の加工（itertools）
# ============================================================

def run_length(S):
    """ランレングス圧縮: "aaabcc" -> [('a',3), ('b',1), ('c',2)]"""
    return [(k, len(list(g))) for k, g in groupby(S)]


def diffs(A):
    """隣接差: [1,4,6] -> [3,2]"""
    return [b - a for a, b in pairwise(A)]


def flatten(G):
    """2次元 -> 1次元"""
    return list(chain.from_iterable(G))


def all_bits(N):
    """bit全探索の代わり: 長さNの0/1タプルを全列挙"""
    return product(range(2), repeat=N)

# permutations(A)                     順列
# combinations(A, k)                  組合せ
# combinations_with_replacement(A, k) 重複組合せ
# itertools.batched(A, k)             k個ずつ区切る（3.12以降）


# ============================================================
# 3. 二分探索（bisect）  ※ A はソート済み
# ============================================================

def count_less(A, x):
    """x 未満の個数"""
    return bisect_left(A, x)


def count_le(A, x):
    """x 以下の個数"""
    return bisect_right(A, x)


def count_range(A, lo, hi):
    """lo <= a < hi の個数"""
    return bisect_left(A, hi) - bisect_left(A, lo)

# キー付き（3.10以降）: bisect_left(A, x, key=lambda a: a[0])


# ============================================================
# 4. ヒープ・キュー・辞書（heapq / collections）
# ============================================================

def k_smallest(A, k):
    return nsmallest(k, A)


def max_heap_demo(A):
    """最大ヒープは符号反転で"""
    h = []
    for a in A:
        heappush(h, -a)
    return [-heappop(h) for _ in range(len(h))]


def bfs(G, s):
    """隣接リスト G の非重み付き最短距離"""
    dist = [-1] * len(G)
    dist[s] = 0
    q = deque([s])
    while q:
        v = q.popleft()
        for u in G[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def group_by_key(pairs):
    """[(k, v), ...] -> {k: [v, ...]}"""
    d = defaultdict(list)
    for k, v in pairs:
        d[k].append(v)
    return d

# Counter(A).most_common(k)  出現回数の上位k個


# ============================================================
# 5. 数学（math / 組み込み）
# ============================================================

def is_square(n):
    """int(n**0.5) は誤差が出るので isqrt を使う"""
    r = math.isqrt(n)
    return r * r == n


def modinv(x, m):
    """m と互いに素な x の逆元（3.8以降）"""
    return pow(x, -1, m)

# math.gcd(*A), math.lcm(*A)   複数引数OK（3.9以降）
# math.comb(n, k), math.perm(n, k)
# divmod(a, b)                 (商, 余り)
# x.bit_count()                popcount（3.10以降）
# int(s, 2), bin(x)[2:]        2進変換


# ============================================================
# 6. ソート・グリッド・メモ化
# ============================================================

def sort_fractions(F):
    """(分子, 分母>0) を値の昇順に。浮動小数を使わず比較"""
    def cmp(p, q):
        return p[0] * q[1] - q[0] * p[1]
    return sorted(F, key=cmp_to_key(cmp))


def transpose(G):
    return [list(r) for r in zip(*G)]


def rotate_cw(G):
    """時計回りに90度回転"""
    return [list(r) for r in zip(*G[::-1])]

# @cache を付けた再帰関数でメモ化。
# 深い再帰は sys.setrecursionlimit が必要。PyPy では遅くなりやすいのでループ化を優先。


# ============================================================
# 外部ライブラリ（AtCoder 環境）
#   from sortedcontainers import SortedList   順序付き多重集合
#   numpy                                     大きい配列の一括演算
#   ac-library-python                         既存の atcoder_lib と重複に注意
# ============================================================


# ============================================================
# テスト
# ============================================================
if __name__ == "__main__":
    A = [3, 1, 4, 1, 5, 9, 2, 6]

    assert prefix_sum([1, 2, 3]) == [0, 1, 3, 6]
    S = prefix_sum(A)
    assert S[5] - S[2] == sum(A[2:5])
    assert prefix_min(A) == [3, 1, 1, 1, 1, 1, 1, 1]
    assert suffix_min(A) == [1, 1, 1, 1, 2, 2, 2, 6]
    assert prefix_max(A) == [3, 3, 4, 4, 5, 9, 9, 9]
    assert suffix_max(A) == [9, 9, 9, 9, 9, 9, 6, 6]
    X = prefix_xor(A)
    assert X[4] ^ X[1] == 1 ^ 4 ^ 1

    assert run_length("aaabcc") == [("a", 3), ("b", 1), ("c", 2)]
    assert diffs([1, 4, 6]) == [3, 2]
    assert flatten([[1, 2], [3]]) == [1, 2, 3]
    assert len(list(all_bits(3))) == 8

    B = sorted(A)
    assert count_less(B, 4) == 4
    assert count_le(B, 4) == 5
    assert count_range(B, 2, 6) == 4

    assert k_smallest(A, 3) == [1, 1, 2]
    assert max_heap_demo(A) == sorted(A, reverse=True)
    G = [[1, 2], [3], [3], []]
    assert bfs(G, 0) == [0, 1, 1, 2]
    assert group_by_key([(1, "a"), (2, "b"), (1, "c")]) == {1: ["a", "c"], 2: ["b"]}

    assert is_square(10**18) and not is_square(10**18 - 1)
    assert modinv(3, 998244353) * 3 % 998244353 == 1

    assert sort_fractions([(1, 2), (1, 3), (2, 3)]) == [(1, 3), (1, 2), (2, 3)]
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert rotate_cw([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]

    print("all ok")
