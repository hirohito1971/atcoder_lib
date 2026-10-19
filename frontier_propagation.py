"""
frontier_propagation.py

局所伝播(フロンティア伝播)パターン
----------------------------------
セルオートマトン的な「毎ステップ、条件を満たすマスが変化する」系の問題で、
全盤面を毎回スキャンすると O(steps * H * W) になり TLE する場合に使うテクニック。

キーとなる性質:
  - ステップ i で新たに変化する集合 T_i の各マスは、
    必ず T_{i-1}(直前に変化した集合)のどれかに隣接している。
  - よって次の候補は「盤面全体」ではなく「直前に変化したマスの隣接だけ」で十分。
  - T_1, T_2, ... は互いに素なので、全ステップの候補チェック回数の合計は O(H*W) に収まる。

注意(重要な誤解ポイント):
  - 「BFS距離(最短距離)のレイヤー順に確定していく」という考え方は、
    このテンプレの一般形には *通用しない* 場合がある(Ulam-Warburton系など)。
    ブロックされた影響で、遠い距離のマスから遅れて活性化されることがあるため。
  - 正しく成り立つのは「変化は直前の変化の隣接からしか起きない」という
    局所性(隣接性)のみ。距離の単調性は仮定してはいけない。

典型例: AtCoder ABC425 D (Ulam-Warburton Automaton)
  各白マスは、隣接する黒マスがちょうど1つのときだけ黒に変わる。
  これを全盤面スキャンで毎ステップ判定すると O(HW) ステップ * O(HW) スキャン = TLE。
  フロンティア伝播で「前回黒くなったマスの隣接だけ」を候補にすることで解決する。

適用条件の目安:
  - 各セルの状態変化が、近傍セルの状態のみに依存して決まる(局所的な規則)
  - 変化したセルは基本的に「もう二度と変化しない」(不可逆、単調)
  - 変化が起きる場所は必ず「直前に変化した場所」の近傍に限られる
"""

from typing import List, Tuple, Callable


def frontier_propagate(
    H: int,
    W: int,
    is_active: Callable[[int, int], bool],
    activate: Callable[[int, int], None],
    check_condition: Callable[[int, int], bool],
    initial_active: List[Tuple[int, int]],
    dh: Tuple[int, ...] = (-1, 0, 1, 0),
    dw: Tuple[int, ...] = (0, -1, 0, 1),
) -> None:
    """
    局所伝播の汎用フレームワーク。

    Parameters
    ----------
    H, W : グリッドサイズ
    is_active(h, w) -> bool
        マス(h, w)が既に「確定済み(黒)」かどうかを返す関数
    activate(h, w) -> None
        マス(h, w)を確定済み(黒)にする副作用を行う関数(盤面の更新)
    check_condition(h, w) -> bool
        マス(h, w)がまだ非確定のとき、「今このマスを確定させてよいか」を判定する関数
        (例: 隣接する確定済みマスの数がちょうど1)
    initial_active : 最初から確定済みのマスのリスト(= 最初のフロンティア)
    dh, dw : 隣接方向(デフォルトは上下左右)

    使い方の例 (ABC425 D):
        S = [list(input()) for _ in range(H)]
        def is_active(h, w): return S[h][w] == '#'
        def activate(h, w): S[h][w] = '#'
        def count_black_neighbors(h, w):
            c = 0
            for d in range(4):
                nh, nw = h + dh[d], w + dw[d]
                if 0 <= nh < H and 0 <= nw < W and S[nh][nw] == '#':
                    c += 1
            return c
        def check_condition(h, w): return count_black_neighbors(h, w) == 1

        initial = [(h, w) for h in range(H) for w in range(W) if S[h][w] == '#']
        frontier_propagate(H, W, is_active, activate, check_condition, initial)
    """
    U = set(initial_active)

    while U:
        V = set()
        for h, w in U:
            for d in range(len(dh)):
                nh, nw = h + dh[d], w + dw[d]
                if nh < 0 or nw < 0 or nh >= H or nw >= W:
                    continue
                if is_active(nh, nw):
                    continue
                if check_condition(nh, nw):
                    V.add((nh, nw))
        for nh, nw in V:
            activate(nh, nw)
        U = V


# ---------------------------------------------------------------------------
# 実戦形(ABC425 D そのもの、コピペしてすぐ使える形)
# ---------------------------------------------------------------------------
def ulam_warburton_count(H: int, W: int, S: List[List[str]]) -> int:
    """
    S: H x W のグリッド。'#' が黒、'.' が白。
    毎ステップ、隣接する黒マスがちょうど1つの白マスが黒に変わる(同時更新)。
    これを変化がなくなるまで繰り返した後の、黒マスの総数を返す。

    実装ノート: 直前に黒くなったマスの隣接だけを候補にすることで O(H*W) を達成。
    """
    dh = (-1, 0, 1, 0)
    dw = (0, -1, 0, 1)

    U = set()
    for h in range(H):
        for w in range(W):
            if S[h][w] == "#":
                U.add((h, w))

    while U:
        V = set()
        for h, w in U:
            for d in range(4):
                nh, nw = h + dh[d], w + dw[d]
                if nh < 0 or nw < 0 or nh >= H or nw >= W:
                    continue
                if S[nh][nw] == "#":
                    continue
                cnt = 0
                for dd in range(4):
                    nnh, nnw = nh + dh[dd], nw + dw[dd]
                    if nnh < 0 or nnw < 0 or nnh >= H or nnw >= W:
                        continue
                    if S[nnh][nnw] == "#":
                        cnt += 1
                if cnt == 1:
                    V.add((nh, nw))
        for nh, nw in V:
            S[nh][nw] = "#"
        U = V

    return sum(row.count("#") for row in S)