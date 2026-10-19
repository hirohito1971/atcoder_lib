# =====================================================
# 高速入力の型
# =====================================================
# Pythonで TLE(時間切れ) するとき、アルゴリズムが正しくても
# 入出力が遅くて落ちることがある。特に N >= 10^5 行の入力。
#
# レベル1 (まずこれを常用): readline に差し替え
# レベル2 (行数が多い時)   : 全部一括読み
# 出力も同様に、大量printは '\n'.join でまとめる
# =====================================================

import sys


# -----------------------------------------------------
# レベル1: input を readline に差し替える (template.py 標準装備)
# -----------------------------------------------------
# input = sys.stdin.readline
#
# ★注意: readline は末尾の改行 '\n' を含む!
#   S = input()          → "abc\n" になってしまう
#   S = input().rstrip() → "abc"   ← 文字列はこれ必須
#   int(input()) や map(int, input().split()) は改行があっても
#   正しく動くので rstrip 不要


# -----------------------------------------------------
# レベル2: 全部一括で読んでしまう (最速・クエリ多数向け)
#   read().split() で空白・改行を区別せず全トークンを取り、
#   イテレータで前から順に消費する型
# -----------------------------------------------------
def fast_read_example():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    q = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    # 文字列が混ざるときは .decode() する:
    # s = next(it).decode()

    queries = []
    for _ in range(q):
        l = int(next(it))
        r = int(next(it))
        queries.append((l, r))
    return n, a, queries


# -----------------------------------------------------
# 出力の高速化: printを10^5回呼ぶと遅い。リストに溜めて一括出力
# -----------------------------------------------------
def fast_output_example(answers):
    print('\n'.join(map(str, answers)))
    # もしくは sys.stdout.write('\n'.join(map(str, answers)) + '\n')



# -----------------------------------------------------
# T ケース型: テストケースが複数ある問題の完成形
#   入力は readline、答えはリストに溜めて最後に1回だけ出力する。
#   T が 10^5 を超えるときは、この形を必ず使うこと。
#
# 実測 (ABC428-D, T = 3×10^5, PyPy):
#   input() + 毎回print         : 1110 ms
#   readline + 毎回print        :  769 ms  (入力で約340 ms減)
#   readline + 出力を一括       :  520 ms  (出力で約250 ms減)
# -----------------------------------------------------
def multi_testcase_template():
    input = sys.stdin.readline        # レベル1の差し替え

    T = int(input())
    ans = []                          # 答えはここに溜める (毎回printしない)

    for _ in range(T):
        N, M = map(int, input().split())
        # S = input().rstrip()        # ★文字列を読むときは rstrip 必須
        # ... 本体 ...
        ans.append(0)                 # このケースの答えを追加

    print('\n'.join(map(str, ans)))   # 最後に1回だけ出力

if __name__ == "__main__":
    print("このファイルは読み物です。型を templates にコピペして使ってください。")
