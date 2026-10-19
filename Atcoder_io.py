"""
AtCoder 入力形式カタログ  ---  sys.stdin.buffer.read().split() 統一方式

================================================================
基本原則
================================================================
    data = sys.stdin.buffer.read().split()

これで入力全体が「空白文字で区切られたトークンのフラットな列」になる。
改行と空白の区別は消える。したがって考えるべきことは1つだけ：

        欲しい値は data の何番目か

「1行に何個あるか」「何行あるか」を数えて input() の呼び方を
変える作業が完全に消える。同じ N 個の整数列でも、1行に並んでいても
N 行に縦に並んでいても、下のコードは1文字も変わらない。

トークンは bytes（b'123'）。int() は bytes をそのまま受け付けるので
数値は decode 不要。文字列として使うときだけ .decode() する。

================================================================
2つのモード
================================================================
[A] 静的スライス方式  ... 構造が入力を読む前から決まっている場合（95%）
                          添字を直接書く。最速。

[B] イテレータ方式    ... トークン数が入力内容に依存する場合
                          （複数テストケース / 種類で長さが変わるクエリ）
                          it = iter(data) を作り islice で消費する。

    from itertools import islice
    it = iter(data)
    N = int(next(it))
    A = list(map(int, islice(it, N)))      # 一括変換のまま速い

    islice は「まとめて n 個消費」を C レベルで行うのでスライスと同速。
    [int(next(it)) for _ in range(n)] は 1.4 倍ほど遅いので使わないこと。
"""

import sys
from itertools import islice


# ============================================================
# [A] 静的スライス方式
# ============================================================

def p01_int1(data):
    """  N  """
    N = int(data[0])
    return N


def p02_int2(data):
    """  N M  （同じ行でも別々の行でも同一コード）"""
    N, M = map(int, data[:2])
    return N, M


def p03_str1(data):
    """  S  """
    S = data[0].decode()
    return S


def p04_int_and_str(data):
    """
    N
    S
    """
    N = int(data[0])
    S = data[1].decode()
    return N, S


def p05_array(data):
    """
    N
    A_1 A_2 ... A_N        ← 1行に並んでいても
                              N 行に縦に並んでいても同じコード
    """
    N = int(data[0])
    A = list(map(int, data[1:1 + N]))
    return N, A


def p06_two_arrays(data):
    """
    N
    A_1 ... A_N
    B_1 ... B_N
    """
    N = int(data[0])
    A = list(map(int, data[1:1 + N]))
    B = list(map(int, data[1 + N:1 + 2 * N]))
    return N, A, B


def p07_pairs_columns(data):
    """
    N
    a_1 b_1
    a_2 b_2
    ...
    a_N b_N

    列ごとに分けたいとき。ストライドスライスが最速。
    """
    N = int(data[0])
    body = data[1:1 + 2 * N]
    A = list(map(int, body[0::2]))
    B = list(map(int, body[1::2]))
    return N, A, B


def p08_pairs_zipped(data):
    """
    同じ形式を (a, b) のペア列として受けたいとき。
    zip(*[iter(x)]*2) は「2個ずつまとめる」定型句。
    """
    N = int(data[0])
    body = map(int, data[1:1 + 2 * N])
    P = list(zip(*[body] * 2))
    return N, P


def p09_graph_edges(data):
    """
    N M
    u_1 v_1
    ...
    u_M v_M

    隣接リストは受け取りと同時に構築してしまう。
    1-indexed のまま N+1 個の箱を用意するのが定石（変換ミスが減る）。
    """
    N, M = map(int, data[:2])
    body = data[2:2 + 2 * M]
    G = [[] for _ in range(N + 1)]
    for i in range(M):
        u = int(body[2 * i])
        v = int(body[2 * i + 1])
        G[u].append(v)
        G[v].append(u)
    return N, M, G


def p10_weighted_edges(data):
    """
    N M
    u_1 v_1 w_1
    ...
    u_M v_M w_M
    """
    N, M = map(int, data[:2])
    body = data[2:2 + 3 * M]
    G = [[] for _ in range(N + 1)]
    for i in range(M):
        u = int(body[3 * i])
        v = int(body[3 * i + 1])
        w = int(body[3 * i + 2])
        G[u].append((v, w))
        G[v].append((u, w))
    return N, M, G


def p11_grid_char(data):
    """
    H W
    S_1
    ...
    S_H

    各行は空白を含まないので 1 トークン。そのまま並んでいる。
    """
    H, W = map(int, data[:2])
    S = [row.decode() for row in data[2:2 + H]]
    return H, W, S


def p12_grid_char_bytes(data):
    """
    同じグリッドを bytes のまま持つ版（decode を省く高速化）。

    bytes への添字アクセスは int を返すので、比較は文字ではなく
    バイト値で行う：  S[i][j] == 35   （35 = ord('#'), 46 = ord('.')）
    可読性は落ちるので、H*W が 10^6 級のときだけ使う。
    """
    H, W = map(int, data[:2])
    S = data[2:2 + H]
    WALL = ord('#')
    walls = sum(1 for i in range(H) for j in range(W) if S[i][j] == WALL)
    return H, W, walls


def p13_grid_int(data):
    """
    H W
    A_11 A_12 ... A_1W
    ...
    A_H1 A_H2 ... A_HW
    """
    H, W = map(int, data[:2])
    body = data[2:2 + H * W]
    G = [list(map(int, body[i * W:(i + 1) * W])) for i in range(H)]
    return H, W, G


def p14_array_and_queries(data):
    """
    N Q
    A_1 ... A_N
    l_1 r_1
    ...
    l_Q r_Q
    """
    N, Q = map(int, data[:2])
    A = list(map(int, data[2:2 + N]))
    body = data[2 + N:2 + N + 2 * Q]
    L = list(map(int, body[0::2]))
    R = list(map(int, body[1::2]))
    return N, Q, A, L, R


def p15_str_int_pairs(data):
    """
    N
    S_1 A_1
    ...
    S_N A_N

    文字列と数値が混在する行。列ごとに取り出して型を分ける。
    """
    N = int(data[0])
    body = data[1:1 + 2 * N]
    S = [s.decode() for s in body[0::2]]
    A = list(map(int, body[1::2]))
    return N, S, A


def p16_floats(data):
    """
    X Y

    小数。ただし AtCoder では誤差を避けるため、
    「10^k 倍して整数で扱う」「有理数のまま比較する」で
    済ませられないか先に検討すること。
    """
    X, Y = map(float, data[:2])
    return X, Y


# ============================================================
# [B] イテレータ方式（トークン数が入力内容に依存する場合）
# ============================================================

def p17_multi_testcase(data):
    """
    T
    N_1
    A_1 ... A_N1
    N_2
    A_1 ... A_N2
    ...

    各ケースの長さが違うので静的な添字が書けない。
    """
    it = iter(data)
    T = int(next(it))
    cases = []
    for _ in range(T):
        N = int(next(it))
        A = list(map(int, islice(it, N)))
        cases.append((N, A))
    return T, cases


def p18_variable_queries(data):
    """
    Q
    1 x      ← 追加クエリ（トークン2個）
    2        ← 取り出しクエリ（トークン1個）
    3 l r    ← 区間クエリ（トークン3個）
    ...

    クエリ種別によってトークン数が変わる典型。
    イテレータ方式でないと書けない（これが [B] の存在理由）。
    """
    it = iter(data)
    Q = int(next(it))
    ops = []
    for _ in range(Q):
        t = int(next(it))
        if t == 1:
            ops.append((1, int(next(it))))
        elif t == 2:
            ops.append((2,))
        else:
            ops.append((3, int(next(it)), int(next(it))))
    return Q, ops


# ============================================================
# 出力側テンプレート
# ============================================================

def out_lines(values):
    """1行1個で大量出力。print を回すより速い。"""
    return "\n".join(map(str, values)) + "\n"


def out_yesno(flags):
    """Yes / No を大量出力。"""
    return "\n".join("Yes" if f else "No" for f in flags) + "\n"


def out_grid(G):
    """2次元配列を空白区切りで出力。"""
    return "\n".join(" ".join(map(str, row)) for row in G) + "\n"


# ============================================================
# 注意点
# ============================================================
"""
1. split() は空白文字すべてで区切る
   タブ・改行・連続空白をまとめて処理してくれる一方、
   「空白を含む文字列」が値として来る形式では使えない。
   AtCoder ではほぼ発生しないが、来たら .split(b"\\n") で行分割する。

2. 空行は消える
   split() は空トークンを生成しないので、
   「空行が意味を持つ」形式には使えない。（AtCoder では出ない）

3. int() は bytes をそのまま受ける
   int(b'123') == 123。数値に decode は不要で、書くだけ遅くなる。

4. bytes への添字は int を返す
   b'abc'[0] は 97 であって b'a' ではない。
   グリッドを bytes のまま持つときはここで必ず一度つまずく。

5. 出力に print を混ぜない
   print と sys.stdout.write はバッファが別なので、
   混在させると出力順が保証されない。どちらかに統一する。

6. 1-indexed / 0-indexed
   受け取り時に -1 して 0-indexed に統一するか、
   N+1 個の箱を用意して 1-indexed のまま扱うか、
   問題ごとにブレさせずどちらかに固定しておくとバグが減る。
"""


# ============================================================
# 自己テスト
# ============================================================

def _run(fn, text):
    return fn(text.encode().split())


def _selftest():
    assert _run(p01_int1, "42") == 42
    assert _run(p02_int2, "3 5") == (3, 5)
    assert _run(p02_int2, "3\n5") == (3, 5)          # 行が違っても同一
    assert _run(p03_str1, "abcde") == "abcde"
    assert _run(p04_int_and_str, "3\nabc") == (3, "abc")

    assert _run(p05_array, "4\n1 2 3 4") == (4, [1, 2, 3, 4])
    assert _run(p05_array, "4\n1\n2\n3\n4") == (4, [1, 2, 3, 4])   # 縦でも同一

    assert _run(p06_two_arrays, "3\n1 2 3\n4 5 6") == (3, [1, 2, 3], [4, 5, 6])

    assert _run(p07_pairs_columns, "3\n1 2\n3 4\n5 6") == (3, [1, 3, 5], [2, 4, 6])
    assert _run(p08_pairs_zipped, "3\n1 2\n3 4\n5 6") == (3, [(1, 2), (3, 4), (5, 6)])

    N, M, G = _run(p09_graph_edges, "4 3\n1 2\n2 3\n1 4")
    assert (N, M) == (4, 3) and G[1] == [2, 4] and G[2] == [1, 3]

    N, M, G = _run(p10_weighted_edges, "3 2\n1 2 10\n2 3 20")
    assert G[2] == [(1, 10), (3, 20)]

    assert _run(p11_grid_char, "2 3\n#.#\n..#") == (2, 3, ["#.#", "..#"])
    assert _run(p12_grid_char_bytes, "2 3\n#.#\n..#") == (2, 3, 3)

    assert _run(p13_grid_int, "2 3\n1 2 3\n4 5 6") == (2, 3, [[1, 2, 3], [4, 5, 6]])

    assert _run(p14_array_and_queries, "3 2\n7 8 9\n1 2\n2 3") == \
        (3, 2, [7, 8, 9], [1, 2], [2, 3])

    assert _run(p15_str_int_pairs, "2\nfoo 10\nbar 20") == (2, ["foo", "bar"], [10, 20])
    assert _run(p16_floats, "1.5 2.25") == (1.5, 2.25)

    T, cases = _run(p17_multi_testcase, "2\n3\n1 2 3\n2\n9 8")
    assert T == 2 and cases == [(3, [1, 2, 3]), (2, [9, 8])]

    Q, ops = _run(p18_variable_queries, "4\n1 5\n2\n3 1 4\n1 7")
    assert Q == 4 and ops == [(1, 5), (2,), (3, 1, 4), (1, 7)]

    assert out_lines([1, 2, 3]) == "1\n2\n3\n"
    assert out_yesno([True, False]) == "Yes\nNo\n"
    assert out_grid([[1, 2], [3, 4]]) == "1 2\n3 4\n"

    print("all patterns OK")


if __name__ == "__main__":
    _selftest()