# atcoder_lib — AtCoder青を目指すための道具箱

運用方針: **コピペ運用**。必要なクラス/関数を提出コードに貼り付けて使う。
`snippets/` だけは性格が違い、「コンテスト前に見返して、見ないで書けるか確認する」ための備忘録。

> 百科事典として使う: 今すべて理解できていなくてよい。
> 問題で必要になったページを開き、コメントを読み、写経し、自分のものにしていく。

---

## 学習優先度マップ (D埋め→青を見据えた順)

| 優先度 | ファイル | 目安 |
|---|---|---|
| ★★★ 最優先 (見ないで書けるを目指す) | bfs_grid, binary_search, prefix_sum, union_find, dp_patterns | 緑〜水色のD問題の主戦場 |
| ★★ 次点 (コピペで使いつつ中身を理解) | dijkstra, fenwick_tree, coordinate_compression, mod_arithmetic, sieve, run_length | Dの後半〜E前半 |
| ★ 出てきたら開く | segment_tree, bfs01, topological_sort, warshall_floyd, bit_dp, priority_queue_utils, gcd_lcm_ext | E問題の武器 |
| 将来の楽しみ | lazy_segment_tree, lca_doubling | 水色後半〜青のE/F |

---

## 一覧と計算量

### data_structures/
| ファイル | 内容 | 計算量 | verify済み問題 |
|---|---|---|---|
| union_find.py | Union-Find (経路圧縮+size) | ならしO(α(N)) | (記入欄) |
| segment_tree.py | セグ木 点更新/区間クエリ | 構築O(N), クエリO(logN) | |
| lazy_segment_tree.py | 遅延セグ木 (レシピ表+完成品5種: 加算×和/min, 代入×min/和, アフィン×和) | クエリO(logN) | |
| fenwick_tree.py | BIT + 転倒数 | クエリO(logN) | |
| priority_queue_utils.py | heapq基本 + 削除可能ヒープ | O(logN) | |

### graph/
| ファイル | 内容 | 計算量 | verify済み問題 |
|---|---|---|---|
| bfs_grid.py | BFS (グリッド/グラフ/多始点) | O(V+E) | |
| bfs01.py | 0-1 BFS | O(V+E) | |
| dijkstra.py | ダイクストラ (+経路復元) | O((V+E)logV) | |
| warshall_floyd.py | 全点対最短路 | O(V^3), N≦400目安 | |
| topological_sort.py | トポソ + DAG上DP | O(V+E) | |
| lca_doubling.py | LCA・ダブリング | 前計算O(NlogN), クエリO(logN) | |

### math_utils/
| ファイル | 内容 | 計算量 | verify済み問題 |
|---|---|---|---|
| mod_arithmetic.py | 逆元・nCr前計算・nPr・nHr | 前計算O(N), クエリO(1) | |
| sieve.py | 篩・SPF高速素因数分解・約数列挙 | O(N loglogN) | |
| gcd_lcm_ext.py | 拡張ユークリッド・一般逆元・CRT | O(log min(a,b)) | |
| count_squares.py | 区間 [L, R] の平方数の個数 (isqrt) | O(1) | |

### snippets/ (見返して手で書く練習用)
| ファイル | 内容 |
|---|---|
| binary_search.py | bisectチートシート・めぐる式・実数二分探索 |
| prefix_sum.py | 1D/2D累積和・いもす法 |
| input_fast.py | 高速入出力・非再帰DFSの型 |
| dp_patterns.py | ナップサック2種・LIS・部分和 |
| bit_dp.py | bitDP (TSP・マッチング数え上げ) |
| coordinate_compression.py | 座標圧縮 (BITとセットで使う) |
| run_length.py | ランレングス圧縮・文字列イディオム |
| sorted_prefix_query.py | ソート＋累積和＋bisect で「各値との差の絶対値の総和」などを O(log N) |
| enumerate_dfs.py | 辞書順列挙 DFS (副作用だけの再帰の型) |
| stdlib_recipes.py | Python 標準ライブラリのレシピ集 (accumulate, bisect, heapq など) |

### strings/
| ファイル | 内容 | 計算量 | verify済み問題 |
|---|---|---|---|
| rolling_hash.py | ローリングハッシュ (mod 2^61-1, 連結対応) | 構築O(N), クエリO(1) | |

### ルート直下
| ファイル | 内容 |
|---|---|
| template.py | コンテスト開始時にコピーする雛形 |
| Atcoder_io.py | 入力形式カタログ (stdin.buffer.read().split() 統一方式) |
| frontier_propagation.py | フロンティア伝播 (直前に変化したマスの隣接だけを調べる) |
| interval_index.py | 区間マージ＋二分探索による高速メンバーシップ判定 |

---

## 運用ルール (自分との約束)

1. **verify欄を埋める**: ライブラリを実戦投入してACしたら、上の表に問題番号を書く。
   「このセグ木は本当に正しいか?」と不安になったとき、動作確認済みの実例に戻れる。
2. **snippetsはコピペ禁止**: 見返すのはOK。書くのは自分の手で。
   binary_search / prefix_sum / bfs_grid / dp_patterns は「指が覚えた」状態がゴール。
3. **コメントは育てる**: 実戦で「ここで詰まった」「この引数を間違えた」と気づいたら、
   その場でこのライブラリのコメントに追記する。百科事典に自分の書き込みを増やしていく。
4. **各ファイルは単体実行できる**: `python union_find.py` のように動かすと使用例が走る。
   写経後の動作確認にどうぞ。

## 使い方 (コンテスト当日)

1. `template.py` をコピーして問題ファイルを作る
2. 解法を考え、必要な道具が確定したら該当ファイルからクラス/関数をコピペ
3. 使用例 (`if __name__ == "__main__"` 以下) はコピペしない

---

## ライセンス

[MIT License](LICENSE)
