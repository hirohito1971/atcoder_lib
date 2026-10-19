# =====================================================
# 素数まわり (エラトステネスの篩, 高速素因数分解)
# =====================================================
# 使い分けの目安:
#   - 1個の数 n (〜10^12程度) を素因数分解 → trial_division (√n試し割り)
#   - 大量の数 (それぞれ〜10^6程度) を素因数分解
#       → SPF(最小素因数)テーブルを前計算 ★これが強い
#   - 「n以下の素数を列挙」 → sieve
#
# 計算量:
#   sieve / SPF構築 : O(N log log N)
#   SPFでの1個の分解: O(log n)
#   試し割り        : O(√n)
# =====================================================


def sieve(n):
    """
    エラトステネスの篩。
    戻り値: (is_prime, primes)
      is_prime[i] = iが素数か (bool のリスト)
      primes      = n以下の素数のリスト
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # iの倍数を消す。i*iから始めてよい
            # (それ未満のi*k は kの素因数で既に消されている)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    primes = [i for i in range(n + 1) if is_prime[i]]
    return is_prime, primes


def smallest_prime_factors(n):
    """
    SPFテーブル: spf[x] = xの最小の素因数
    これがあると素因数分解が O(log x) でできる
    """
    spf = list(range(n + 1))       # 初期値は自分自身
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:            # iが素数のとき
            for j in range(i * i, n + 1, i):
                if spf[j] == j:    # まだ小さい素因数が付いてなければ
                    spf[j] = i
    return spf


def factorize_by_spf(x, spf):
    """SPFテーブルを使って素因数分解。戻り値: {素因数: 指数}"""
    res = {}
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        res[p] = cnt
    return res


def trial_division(n):
    """
    √n までの試し割りによる素因数分解 (前計算不要, 1個ならこれで十分)
    戻り値: {素因数: 指数}
    n <= 10^12 程度まで実用的
    """
    res = {}
    x = n
    p = 2
    while p * p <= x:
        while x % p == 0:
            res[p] = res.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:              # 最後に残ったxは素数 (√nより大きい素因数は高々1個)
        res[x] = res.get(x, 0) + 1
    return res


def divisors(n):
    """
    nの約数を全列挙 O(√n)。
    i が約数なら n//i も約数、というペアで集めるのがコツ
    """
    small, large = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i != n // i:        # 平方数のとき二重登録しない
                large.append(n // i)
        i += 1
    return small + large[::-1]     # 昇順に結合


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    is_p, primes = sieve(30)
    print(primes)                    # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    spf = smallest_prime_factors(100)
    print(factorize_by_spf(84, spf))  # {2: 2, 3: 1, 7: 1}

    print(trial_division(600851475143))  # {71:1, 839:1, 1471:1, 6857:1}
    print(divisors(36))               # [1, 2, 3, 4, 6, 9, 12, 18, 36]
