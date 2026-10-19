from bisect import bisect_left, bisect_right


class SortedPrefixQuery:
    """
    ソート済み配列に対する片側集計クエリ

    「距離の総和」「ある値との差の総和」系の問題で頻出のパターン:
      - 配列をソートして累積和を前計算
      - 各クエリ値 a に対して、a未満/a以下の要素の「個数」と「総和」を
        bisect + 累積和で O(log N) で取得する

    典型用途: sum(|a - b_i| for b_i in B) をAごとに高速計算する等
    """

    def __init__(self, arr):
        # arr: 集計対象の配列（内部でソートするので破壊しない）
        self.sorted_arr = sorted(arr)
        self.n = len(self.sorted_arr)
        # 累積和 S[i] = sorted_arr[0] + ... + sorted_arr[i-1]
        self.prefix_sum = [0] * (self.n + 1)
        for i, v in enumerate(self.sorted_arr):
            self.prefix_sum[i + 1] = self.prefix_sum[i] + v

    def count_and_sum_less(self, x):
        """
        x より真に小さい要素の (個数, 総和) を返す
        境界値 x 自身は含めない → bisect_left を使う
        """
        idx = bisect_left(self.sorted_arr, x)
        return idx, self.prefix_sum[idx]

    def count_and_sum_less_equal(self, x):
        """
        x 以下の要素の (個数, 総和) を返す
        境界値 x 自身を含める → bisect_right を使う
        """
        idx = bisect_right(self.sorted_arr, x)
        return idx, self.prefix_sum[idx]

    def count_and_sum_greater(self, x):
        """
        x より真に大きい要素の (個数, 総和) を返す
        = 全体 - (x以下の集計)
        """
        cnt_le, sum_le = self.count_and_sum_less_equal(x)
        return self.n - cnt_le, self.prefix_sum[-1] - sum_le

    def count_and_sum_greater_equal(self, x):
        """
        x 以上の要素の (個数, 総和) を返す
        = 全体 - (xより真に小さい集計)
        """
        cnt_lt, sum_lt = self.count_and_sum_less(x)
        return self.n - cnt_lt, self.prefix_sum[-1] - sum_lt

    def sum_of_abs_diff(self, x):
        """
        sum(|x - b| for b in B) を O(log N) で計算する
        （ABC437-D の中核ロジックをそのまま関数化したもの）
        x と等しい要素の寄与は 0 になるので、
        less/less_equal のどちらの境界を使っても結果は同じ
        """
        cnt_small, sum_small = self.count_and_sum_less(x)
        total_cnt = self.n
        total_sum = self.prefix_sum[-1]
        cnt_large = total_cnt - cnt_small
        sum_large = total_sum - sum_small
        return x * cnt_small - sum_small + sum_large - x * cnt_large