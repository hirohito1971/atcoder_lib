# =====================================================
# セグメント木 (Point Update / Range Query)
# =====================================================
# できること:
#   - update(i, x) : i番目の値をxに変更           O(log N)
#   - query(l, r)  : 区間[l, r)の演算結果を取得    O(log N)
#   演算は「モノイド」なら何でもOK (min, max, sum, gcd, xor...)
#
# モノイドとは:
#   - 結合法則が成り立つ: op(op(a,b),c) == op(a,op(b,c))
#   - 単位元 e がある:     op(a, e) == op(e, a) == a
#   ※可換性は不要! (行列積のような非可換演算も乗る。
#     このコードのqueryが res_left / res_right を分けて
#     いるのは非可換対応のため)
#   ※逆元も不要! (BITとの違い。minは「引き算で戻せない」が
#     セグ木なら扱える。mod上の積も0の逆元がないので
#     累積積の割り算では対応できず、セグ木の出番になる)
#
# --- 具体的な演算とモノイドの対応表 ---
# | クエリ         | op              | 単位元 e      | Pythonでの書き方                          |
# |---------------|-----------------|--------------|------------------------------------------|
# | 範囲合計 RSQ   | 加算 (+)        | 0            | op=lambda a,b: a+b,  e=0                 |
# | 範囲最小 RMQ   | min(a,b)        | INF          | op=min,              e=float('inf')      |
# | 範囲最大 RMQ   | max(a,b)        | -INF         | op=max,              e=-float('inf')     |
# | 範囲積         | 乗算 (×)        | 1            | op=lambda a,b: a*b%MOD, e=1              |
# | 範囲GCD        | gcd(a,b)        | 0            | op=math.gcd,         e=0                 |
# | 範囲AND        | a & b           | 全ビット1     | op=lambda a,b: a&b,  e=(1<<60)-1 など    |
# | 範囲OR         | a | b           | 0            | op=lambda a,b: a|b,  e=0                 |
# | 範囲XOR        | a ^ b           | 0            | op=lambda a,b: a^b,  e=0                 |
# | 範囲行列積     | 行列の積        | 単位行列 I    | 非可換。res_left/rightの分離が効く例      |
#
# 単位元の覚え方:「その演算をしても相手が変わらない値」
#   min→INF (何とminしても相手が勝つ)
#   AND→全ビット1 (何とANDしても相手のまま)
#   gcd→0 (gcd(x, 0) = x と定義される)
#
# 典型的な使いどころ:
#   - 「値が更新されながら、区間min/max/sumを何度も聞かれる」
#   - 転倒数 (BITでも可)
#   - 「自分より左にある、自分より大きい値の個数」系
#
# 実装のツボ:
#   - 完全二分木を配列で表現する。サイズを2べきに切り上げる
#   - 節点 i の子は 2i, 2i+1 / 親は i//2 (1-indexed)
#   - 葉は data[size + i] に置く
#   - queryは「l, rを葉から根に向かって登らせながら、
#     はみ出た部分だけ演算に取り込む」非再帰スタイル
# =====================================================


class SegmentTree:
    def __init__(self, n, op, e):
        """
        n  : 要素数
        op : 二項演算 (例: min, lambda a,b: a+b)
        e  : 単位元   (例: minならfloat('inf'), sumなら0)
        """
        self.n = n
        self.op = op
        self.e = e
        self.size = 1
        while self.size < n:
            self.size *= 2
        # 木全体を単位元で初期化 (長さ 2*size, index 1 が根)
        self.data = [e] * (2 * self.size)

    def build(self, arr):
        """配列 arr で一括初期化 O(N) (update N回より速い)"""
        for i, x in enumerate(arr):
            self.data[self.size + i] = x
        # 葉の1つ上の段から根に向かって計算していく
        for i in range(self.size - 1, 0, -1):
            self.data[i] = self.op(self.data[2 * i], self.data[2 * i + 1])

    def update(self, i, x):
        """i番目 (0-indexed) の値を x に変更"""
        i += self.size          # 葉の位置へ
        self.data[i] = x
        i //= 2
        while i:                # 根まで親を更新し続ける
            self.data[i] = self.op(self.data[2 * i], self.data[2 * i + 1])
            i //= 2

    def query(self, l, r):
        """区間 [l, r) の演算結果 (半開区間! rは含まない)"""
        res_left = self.e       # 左端から取り込んだ分
        res_right = self.e      # 右端から取り込んだ分
        l += self.size
        r += self.size
        while l < r:
            # lが右の子(奇数)なら、その節点は区間に完全に含まれるので取り込む
            if l & 1:
                res_left = self.op(res_left, self.data[l])
                l += 1
            # rが右の子(奇数)なら、r-1(左隣)が区間に完全に含まれる
            if r & 1:
                r -= 1
                res_right = self.op(self.data[r], res_right)
            l //= 2
            r //= 2
        # 非可換な演算 (例: 文字列連結) にも対応できるよう左右を分けている
        return self.op(res_left, res_right)

    def get(self, i):
        """i番目の値を単独取得"""
        return self.data[self.size + i]


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    INF = float("inf")
    a = [3, 1, 4, 1, 5, 9, 2, 6]

    # 区間min
    st = SegmentTree(len(a), min, INF)
    st.build(a)
    print(st.query(2, 6))   # a[2:6]=[4,1,5,9] の min → 1
    st.update(3, 100)       # a[3] = 100
    print(st.query(2, 6))   # [4,100,5,9] の min → 4

    # 区間sumにしたければ:
    # st = SegmentTree(len(a), lambda x, y: x + y, 0)
