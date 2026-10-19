"""
区間マージ + 二分探索による高速メンバーシップ判定ライブラリ

用途:
    key ごとに複数の半開区間 [s, e) が紐づくデータ(例: ある y 座標に対する
    x の到達可能範囲の集合)を事前に整理しておき、
    「あるキーについて、値 v がいずれかの区間に含まれるか」を
    O(log M) で判定したいときに使う。

    典型例: AtCoder ABC385 D (経路が通ったマスの判定) のような、
    座標 x/y ごとに区間の和集合を持ち、点がその中に入っているか
    大量にクエリする問題。

計算量:
    - build_index: 全区間数を M として O(M log M)
    - contains: 1クエリあたり O(log M)

使い方:
    from interval_index import build_index, contains

    D = defaultdict(list)
    D[key].append((s, e))  # 半開区間 [s, e) を追加していく

    idx = build_index(D)
    contains(idx, key, v)  # v がキー key の区間のいずれかに入っているか
"""

import bisect
from collections import defaultdict


def build_index(D):
    """
    key -> [(s, e), ...] という半開区間の辞書を受け取り、
    key ごとに区間をソート・マージして二分探索できる形にする。

    区間 (s, e) は [s, e) の半開区間として扱う(s <= e が前提)。

    戻り値:
        idx: key -> (starts, merged)
            starts: マージ後の各区間の開始点をソートしたリスト
            merged: マージ後の [s, e) のリスト(開始点順)
    """
    idx = {}
    for key, intervals in D.items():
        intervals.sort()
        merged = []
        for s, e in intervals:
            if merged and s <= merged[-1][1]:
                # 直前区間と重なる/隣接する -> 終端を拡張してマージ
                # max を取るのは、後続区間が直前区間に完全に
                # 内包される(入れ子になる)ケースで終端を
                # 縮めてしまわないようにするため
                merged[-1][1] = max(merged[-1][1], e)
            else:
                # 独立した新しい区間として追加
                merged.append([s, e])
        starts = [s for s, e in merged]
        idx[key] = (starts, merged)
    return idx


def contains(idx, key, v):
    """
    build_index() で作った idx に対して、
    key に属する区間のいずれかに v が含まれるか判定する。
    """
    if key not in idx:
        return False
    starts, merged = idx[key]
    i = bisect.bisect_right(starts, v) - 1
    if i < 0:
        return False
    s, e = merged[i]
    return s <= v < e


if __name__ == "__main__":
    # 簡単な動作確認
    D = defaultdict(list)
    D[3].append((1, 5))
    D[3].append((4, 8))
    D[3].append((10, 12))

    idx = build_index(D)
    assert idx[3][1] == [[1, 8], [10, 12]]

    assert contains(idx, 3, 0) is False
    assert contains(idx, 3, 1) is True
    assert contains(idx, 3, 7) is True
    assert contains(idx, 3, 8) is False  # 半開区間なので終端は含まない
    assert contains(idx, 3, 10) is True
    assert contains(idx, 3, 12) is False
    assert contains(idx, 4, 0) is False  # 存在しないキー

    print("OK")