# =====================================================
# 遅延伝播セグメント木 (Range Update / Range Query)
# =====================================================
# できること:
#   - apply(l, r, f) : 区間[l, r)全体に作用fを適用   O(log N)
#   - query(l, r)    : 区間[l, r)の演算結果を取得     O(log N)
#   例: 「区間に一様にxを足す」+「区間和を聞く」
#
# 必要な部品 (ACL: AtCoder Library と同じ設計):
#   op(a, b)       : 値同士のマージ (普通のセグ木と同じ)
#   e              : opの単位元
#   mapping(f, a)  : 作用fを値aに適用した結果
#   composition(f, g): 作用の合成。「先にg、後にf」を1つの作用に
#   id_            : 「何もしない」作用 (mappingの単位元)
#
# --- 頻出の組み合わせレシピ表 ---
# (値, 作用) の2つのモノイドをセットで覚える。★=下に完成品あり
#
# | # | 更新 × 取得        | 値の持ち方   | mapping(f, a)         | composition(f, g) | id_   |
# |---|-------------------|-------------|-----------------------|-------------------|-------|
# | 1 | 区間加算 × 区間和 ★| (和, 幅)    | (a.和 + f*a.幅, a.幅) | f + g             | 0     |
# | 2 | 区間加算 × 区間min★| min値       | a + f                 | f + g             | 0     |
# | 3 | 区間加算 × 区間max | max値       | a + f                 | f + g             | 0     |
# | 4 | 区間代入 × 区間min★| min値       | f (代入=上書き)        | f (後勝ち!)       | None  |
# | 5 | 区間代入 × 区間和 ★| (和, 幅)    | (f * a.幅, a.幅)      | f (後勝ち!)       | None  |
# | 6 | 区間アフィン × 区間和★| (和, 幅)  | f=(b,c)として          | 合成 (下記)       | (1,0) |
# |   |  (a→b*a+c)        |             | (b*a.和 + c*a.幅, 幅) |                   |       |
#
# 表の読み方・ツボ:
#
# ◆「幅」が要るのはどんな時か (#1, #5, #6):
#   取得が「和」のとき、区間全体への作用は幅の分だけ効く。
#   「+f を幅w の区間にかけると和は f*w 増える」→ 幅の情報が
#   値側に必要。だから葉を (値, 1) のペアにして持つ。
#   min/max なら区間の代表1個に効くだけなので幅は不要 (#2〜4)。
#
# ◆ composition の向きに注意:
#   composition(f, g) = 「先に g、後に f」。
#   加算なら順序は関係ない (f+g) が、
#   代入は ★後からの f が勝つ★ ので composition = f。
#   アフィン f=(b2,c2), g=(b1,c1) の合成は
#     x → b2*(b1*x + c1) + c2 = (b2*b1)*x + (b2*c1 + c2)
#   → composition = (b2*b1, b2*c1 + c2)  ※順序を入れ替えると別物!
#   「非可換かも」と常に疑うこと。迷ったら紙で1回展開する。
#
# ◆ 代入の id_ に None を使うテク (#4, #5):
#   代入作用に「何もしない」に当たる値がないので、
#   番兵として None を使い、mapping/composition の先頭で
#   if f is None: return a (または g) と逃がすのが定石。
#   ※このクラスの _push_down は `is not` で判定しているので
#     id_=None がそのまま安全に使える (下の実装メモ参照)。
#
# ◆ 設計チェックリスト (新しい組を自作する時に自問する):
#   1. op は結合法則を満たすか? e はあるか? (普通のセグ木と同じ)
#   2. mapping(f, op(a,b)) == op(mapping(f,a), mapping(f,b)) か?
#      = 「まとめて作用」と「別々に作用してマージ」が一致するか。
#      ★これが遅延セグ木に乗る条件の本体。
#      (区間和×区間加算で幅が必要になるのは、素朴に書くと
#       ここが崩れるから。幅を持たせて成立させている)
#   3. composition は結合法則を満たすか? id_ はあるか?
#
# 「遅延」の気持ち:
#   区間更新をその場で葉まで反映すると O(N) かかる。
#   そこで「この節点以下には作用fが保留中」というメモ(lazy)を
#   節点に貼っておき、その節点より深く潜る必要が生じた時に
#   初めて子へ伝播する (push_down)。これで O(log N) になる。
#
# ★これは最難関クラスの道具。まずは完成品 (#1, #2) を
#   使うところから。#4〜#6 が必要な問題に出会ったら、
#   この表と完成品を見比べながら仕組みを理解していく。
# =====================================================


class LazySegmentTree:
    def __init__(self, n, op, e, mapping, composition, id_):
        self.n = n
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id_
        self.log = (n - 1).bit_length() if n > 1 else 0
        self.size = 1 << self.log
        self.data = [e] * (2 * self.size)
        self.lazy = [id_] * self.size   # 内部節点にだけ保留作用を持つ

    def build(self, arr):
        for i, x in enumerate(arr):
            self.data[self.size + i] = x
        for i in range(self.size - 1, 0, -1):
            self._pull(i)

    def _pull(self, k):
        """子2つから節点kの値を再計算"""
        self.data[k] = self.op(self.data[2 * k], self.data[2 * k + 1])

    def _apply_node(self, k, f):
        """節点kに作用fを当てる。内部節点ならlazyにも合成して保留"""
        self.data[k] = self.mapping(f, self.data[k])
        if k < self.size:  # 内部節点なら子への伝播を保留
            self.lazy[k] = self.composition(f, self.lazy[k])

    def _push_down(self, k):
        """節点kの保留作用を子2つへ渡してリセット"""
        # 実装メモ: `!=` ではなく `is not` で判定している。
        #   - id_=None (代入系の番兵) のとき意図が明確
        #   - _push_down後は必ず lazy[k] = self.id (同一オブジェクト)
        #     を代入するので、`is not` で「保留なし」を正しく検出できる
        #   - composition の結果がたまたま id_ と同値 (例: アフィンで
        #     (1,0) に戻る) の場合は余分に伝播するが、正しさは変わらない
        if self.lazy[k] is not self.id:
            self._apply_node(2 * k, self.lazy[k])
            self._apply_node(2 * k + 1, self.lazy[k])
            self.lazy[k] = self.id

    def apply(self, l, r, f):
        """区間 [l, r) に作用fを適用"""
        if l >= r:
            return
        l += self.size
        r += self.size
        # 1) 上から降りながら、通り道の保留作用を先に子へ流す
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push_down(l >> i)
            if ((r >> i) << i) != r:
                self._push_down((r - 1) >> i)
        # 2) 普通のセグ木queryと同じ要領で、区間を覆う節点にfを当てる
        ll, rr = l, r
        while ll < rr:
            if ll & 1:
                self._apply_node(ll, f)
                ll += 1
            if rr & 1:
                rr -= 1
                self._apply_node(rr, f)
            ll //= 2
            rr //= 2
        # 3) 下から登りながら、通り道の節点の値を再計算
        for i in range(1, self.log + 1):
            if ((l >> i) << i) != l:
                self._pull(l >> i)
            if ((r >> i) << i) != r:
                self._pull((r - 1) >> i)

    def query(self, l, r):
        """区間 [l, r) の演算結果"""
        if l >= r:
            return self.e
        l += self.size
        r += self.size
        # queryでも通り道の保留作用を先に流す必要がある
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push_down(l >> i)
            if ((r >> i) << i) != r:
                self._push_down((r - 1) >> i)
        res_l, res_r = self.e, self.e
        while l < r:
            if l & 1:
                res_l = self.op(res_l, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                res_r = self.op(self.data[r], res_r)
            l //= 2
            r //= 2
        return self.op(res_l, res_r)


# =====================================================
# 完成品 #1: 区間加算 + 区間和
#   値は (合計, 区間幅) のペアで持つのがコツ。
#   「区間にxを足す」と和は x * 幅 だけ増えるため、
#   幅の情報が値側に必要になる。
# =====================================================
def make_range_add_range_sum(n, init=None):
    op = lambda a, b: (a[0] + b[0], a[1] + b[1])   # (和, 幅) 同士の合併
    e = (0, 0)
    mapping = lambda f, a: (a[0] + f * a[1], a[1])  # 和 += f*幅
    composition = lambda f, g: f + g                # 加算作用の合成は足し算
    id_ = 0
    st = LazySegmentTree(n, op, e, mapping, composition, id_)
    arr = init if init is not None else [0] * n
    st.build([(x, 1) for x in arr])                 # 葉は幅1
    return st


# =====================================================
# 完成品 #2: 区間加算 + 区間min
#   (#3 の区間max は min→max, INF→-INF に変えるだけ)
# =====================================================
def make_range_add_range_min(n, init=None):
    INF = float("inf")
    op = min
    e = INF
    mapping = lambda f, a: a + f
    composition = lambda f, g: f + g
    id_ = 0
    st = LazySegmentTree(n, op, e, mapping, composition, id_)
    arr = init if init is not None else [0] * n
    st.build(arr)
    return st


# =====================================================
# 完成品 #4: 区間代入 + 区間min
#   代入作用の id_ は None 番兵。
#   mapping / composition の先頭で None を逃がすのが型。
# =====================================================
def make_range_assign_range_min(n, init=None):
    INF = float("inf")
    op = min
    e = INF
    # f=None は「何もしない」: 値aをそのまま返す
    mapping = lambda f, a: a if f is None else f
    # 代入は後勝ち: 後から来た f が None でなければ f、None なら g が残る
    composition = lambda f, g: g if f is None else f
    id_ = None
    st = LazySegmentTree(n, op, e, mapping, composition, id_)
    arr = init if init is not None else [0] * n
    st.build(arr)
    return st


# =====================================================
# 完成品 #5: 区間代入 + 区間和
#   #1 と同じく (和, 幅) で持ち、「代入すると和 = f * 幅」
# =====================================================
def make_range_assign_range_sum(n, init=None):
    op = lambda a, b: (a[0] + b[0], a[1] + b[1])
    e = (0, 0)
    mapping = lambda f, a: a if f is None else (f * a[1], a[1])
    composition = lambda f, g: g if f is None else f
    id_ = None
    st = LazySegmentTree(n, op, e, mapping, composition, id_)
    arr = init if init is not None else [0] * n
    st.build([(x, 1) for x in arr])
    return st


# =====================================================
# 完成品 #6: 区間アフィン変換 (a → b*a + c) + 区間和
#   加算 (b=1) も代入 (b=0) も特殊ケースとして含む最強の組。
#   ACL Practice Contest K がこの形 (mod付き)。
#   composition は非可換なので順序に注意 (ヘッダの展開式を参照)。
# =====================================================
def make_range_affine_range_sum(n, init=None, mod=None):
    if mod is None:
        op = lambda a, b: (a[0] + b[0], a[1] + b[1])
        mapping = lambda f, a: (f[0] * a[0] + f[1] * a[1], a[1])
        composition = lambda f, g: (f[0] * g[0], f[0] * g[1] + f[1])
    else:
        op = lambda a, b: ((a[0] + b[0]) % mod, a[1] + b[1])
        mapping = lambda f, a: ((f[0] * a[0] + f[1] * a[1]) % mod, a[1])
        composition = lambda f, g: (f[0] * g[0] % mod, (f[0] * g[1] + f[1]) % mod)
    e = (0, 0)
    id_ = (1, 0)     # b=1, c=0 は「何もしない」
    st = LazySegmentTree(n, op, e, mapping, composition, id_)
    arr = init if init is not None else [0] * n
    st.build([(x, 1) for x in arr])
    return st


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    # #1 区間加算 + 区間和
    st = make_range_add_range_sum(5, [1, 2, 3, 4, 5])
    print(st.query(0, 5)[0])   # 15
    st.apply(1, 4, 10)          # a[1..3] に +10
    print(st.query(0, 5)[0])   # 45
    print(st.query(2, 3)[0])   # a[2] = 13

    # #2 区間加算 + 区間min
    st2 = make_range_add_range_min(5, [3, 1, 4, 1, 5])
    print(st2.query(0, 5))     # 1
    st2.apply(0, 4, 10)         # a[0..3] に +10
    print(st2.query(0, 5))     # 5 (a[4]だけ加算されず最小)

    # #4 区間代入 + 区間min
    st4 = make_range_assign_range_min(5, [3, 1, 4, 1, 5])
    st4.apply(0, 3, 7)          # a[0..2] = 7
    print(st4.query(0, 3))     # 7
    print(st4.query(0, 5))     # 1 (a[3]が残っている)
    st4.apply(1, 5, 0)          # 代入の上書き (後勝ちの確認)
    print(st4.query(0, 5))     # 0

    # #5 区間代入 + 区間和
    st5 = make_range_assign_range_sum(5, [1, 2, 3, 4, 5])
    st5.apply(1, 4, 10)         # a[1..3] = 10
    print(st5.query(0, 5)[0])  # 1 + 10*3 + 5 = 36

    # #6 区間アフィン + 区間和 (a → 2a+1 を区間にかける)
    st6 = make_range_affine_range_sum(5, [1, 2, 3, 4, 5])
    st6.apply(0, 3, (2, 1))     # a[0..2] → 2a+1 = [3, 5, 7]
    print(st6.query(0, 5)[0])  # 3+5+7+4+5 = 24
    st6.apply(0, 5, (0, 9))     # b=0 は代入と同じ: 全部9
    print(st6.query(0, 5)[0])  # 45
