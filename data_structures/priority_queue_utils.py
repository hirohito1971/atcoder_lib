# =====================================================
# 優先度付きキュー (heapq) の使い方まとめ + 便利ラッパー
# =====================================================
# heapq は「最小値を O(log N) で取り出せる」データ構造。
#
# 基本操作 (これは体で覚える):
#   import heapq
#   h = []
#   heapq.heappush(h, x)   # 追加        O(log N)
#   x = heapq.heappop(h)   # 最小を取出   O(log N)
#   h[0]                   # 最小を見るだけ O(1)
#   heapq.heapify(lst)     # リストを一括ヒープ化 O(N)
#
# よくあるテク:
#   - 最大値が欲しい → 符号反転して入れる: heappush(h, -x)
#   - タプルを入れると第1要素→第2要素の順で比較される
#     Dijkstraの (距離, 頂点) はこれを利用している
# =====================================================

import heapq
from collections import defaultdict


class RemovableHeap:
    """
    削除可能な最小ヒープ (遅延削除方式)

    heapq には「任意の要素の削除」がない。そこで:
      - remove(x) では削除ヒープ側に x を積むだけ
      - top/pop の直前に、両ヒープの先頭が一致していたら
        「削除予約済みの要素が先頭に来た」ので双方から捨てる
    これで実質的な削除を O(log N) で実現する。

    使いどころ:
      - 「集合に追加/削除しながら最小値(最大値)を何度も聞かれる」
      - スライディングウィンドウの min/max (dequeでも可だが汎用性はこちら)
    """

    def __init__(self):
        self.heap = []      # 本体
        self.removed = []   # 削除予約
        self.counter = defaultdict(int)  # 各値の実質個数 (安全確認用)
        self.size = 0

    def push(self, x):
        heapq.heappush(self.heap, x)
        self.counter[x] += 1
        self.size += 1

    def remove(self, x):
        """xを1個削除 (xが入っている前提で呼ぶこと)"""
        assert self.counter[x] > 0, f"{x} is not in heap"
        heapq.heappush(self.removed, x)
        self.counter[x] -= 1
        self.size -= 1

    def _clean(self):
        # 先頭が削除予約と一致している間、双方から取り除く
        while self.removed and self.heap[0] == self.removed[0]:
            heapq.heappop(self.heap)
            heapq.heappop(self.removed)

    def top(self):
        """最小値を見る (削除はしない)"""
        self._clean()
        return self.heap[0]

    def pop(self):
        """最小値を取り出す"""
        self._clean()
        x = heapq.heappop(self.heap)
        self.counter[x] -= 1
        self.size -= 1
        return x

    def __len__(self):
        return self.size


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    h = RemovableHeap()
    for v in [5, 1, 3]:
        h.push(v)
    print(h.top())    # 1
    h.remove(1)       # 最小の1を削除
    print(h.top())    # 3
    h.remove(5)       # 途中の値も削除できる
    print(h.pop())    # 3
    print(len(h))     # 0

    # --- 最大ヒープの型 (符号反転) ---
    mx = []
    for v in [5, 1, 3]:
        heapq.heappush(mx, -v)
    print(-mx[0])     # 最大値 5
