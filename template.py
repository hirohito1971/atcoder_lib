# =====================================================
# template.py : コンテスト開始時にコピーする雛形
# =====================================================
# 使い方:
#   1. このファイルを問題ごとにコピー (a.py, b.py, ...)
#   2. main() の中に解答を書く
#   3. 必要なライブラリを atcoder_lib/ からコピペして
#      main() の上に貼る
#
# ポイント:
#   - input = sys.stdin.readline で入力が高速化される
#     (通常の input() はPyPyでもPythonでも遅い)
#   - readline は末尾に改行 '\n' が付くので、
#     文字列として使うときは .rstrip() を忘れない!
#     (整数変換 int() は改行があっても動くので不要)
#   - 再帰DFSを書くなら setrecursionlimit を上げる
#     ただしPythonの再帰は遅い+深さ10^5級はスタック溢れの
#     危険があるので、基本は「スタックを使った非再帰」推奨
# =====================================================

import sys
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)


def main():
    # ---- 入力の型 (よく使うものをコメントで常備) ----
    # N = int(input())
    # N, M = map(int, input().split())
    # A = list(map(int, input().split()))
    # S = input().rstrip()          # 文字列は rstrip 必須!
    # グリッド: G = [input().rstrip() for _ in range(H)]
    pass


if __name__ == "__main__":
    main()
