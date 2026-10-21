# =====================================================
# 状態BFS (暗黙グラフのBFS)
# =====================================================
# 頂点が「盤面」「文字列」「タプル」などで、事前に番号を振れないときの BFS。
# 距離は配列ではなく dict で持つ (dict にない = 未訪問)。
#
# 使いどころ:
#   - 制約が小さい (N <= 10〜15 程度) パズル・並べ替え系
#   - 「最小の操作回数」を聞かれ、1回の操作のコストが全部同じ
#   - 状態の総数を数えて、10^6 程度までに収まると確認できたとき
#
# 手順:
#   1. 状態の持ち方を決める (str / tuple など hashable なもの)
#   2. 状態の総数を見積もる (操作で変わらない量があれば絞れる)
#   3. 隣の状態を作る関数 neighbors(s) を書く
#   4. bfs_state(start, neighbors) で距離の dict を得る
#
# ★注意: dist は defaultdict(int) にしない!
#   到達不能な状態を dist[goal] で読むと 0 が勝手に作られ、
#   「未訪問」と「距離0」の区別がつかなくなる。
#   ふつうの dict なら書き間違えたとき KeyError で気づける。
#
# ★注意: list は dict のキーにできない。状態は str か tuple にする。
#
# 使用例: ABC361-D (Go Stone Puzzle)
#   状態 = 長さ N+2 の文字列 (空きは '.')
#   状態数 <= (N+1) * C(N, 黒の個数)  ← 色の個数は操作で変わらない
# =====================================================

from collections import deque


def bfs_state(start, neighbors, goal=None):
    """start から到達できる全状態への最短距離を dict で返す。
    goal を指定すると、到達した時点で打ち切る (dist には goal までが入る)。
    neighbors(s) は s から1手で行ける状態を yield / return する関数。"""
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        if s == goal:
            break
        d = dist[s] + 1
        for t in neighbors(s):
            if t not in dist:
                dist[t] = d
                q.append(t)
    return dist


# -----------------------------------------------------
# 使用例: ABC361-D (Go Stone Puzzle)
# -----------------------------------------------------
def abc361d_example():
    N = int(input())
    S = input().strip() + ".."
    T = input().strip() + ".."

    def neighbors(s):
        k = s.index('.')                  # 空き2マスの左端
        for x in range(N + 1):
            if '.' in s[x:x + 2]:         # x, x+1 が両方とも石のときだけ
                continue
            t = list(s)
            t[k:k + 2] = s[x:x + 2]       # 石2つを空きへ (順番はそのまま)
            t[x:x + 2] = '..'             # 元の場所が空きになる
            yield ''.join(t)

    dist = bfs_state(S, neighbors, goal=T)
    print(dist.get(T, -1))                # 到達不能なら -1


if __name__ == "__main__":
    abc361d_example()