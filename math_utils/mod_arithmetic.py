# =====================================================
# mod演算まわり (modpow, 逆元, 二項係数 nCr)
# =====================================================
# AtCoderの「998244353で割った余りを求めよ」系は全部これ。
#
# 大原則:
#   - 足し算・引き算・掛け算は「都度 % MOD」すればよい
#   - ★割り算だけは特別★ : a / b は a * (bの逆元) で計算する
#     bの逆元 = pow(b, MOD-2, MOD)  (フェルマーの小定理, MODが素数のとき)
#
# 覚えるべき組み込み:
#   pow(a, b, MOD)  ← Python標準で高速べき乗(繰り返し二乗法)ができる。
#                      自作modpow不要! これは大きい。
#
# よく使うMOD:
#   998244353 (最近の主流), 10**9 + 7 (古い問題)
# =====================================================

MOD = 998244353


def mod_inverse(a, mod=MOD):
    """aの逆元 (modは素数であること)"""
    # フェルマーの小定理: a^(p-1) ≡ 1 (mod p) より a^(p-2) が逆元
    return pow(a, mod - 2, mod)


class ModComb:
    """
    二項係数 nCr % MOD を大量に計算するための前計算クラス
      前計算 O(N), クエリ O(1)

    仕組み:
      nCr = n! / (r! (n-r)!)
      階乗 fact[] と 階乗の逆元 inv_fact[] を前計算しておけば
      掛け算3回で求まる。
      inv_fact は「一番大きいNの逆元を1回だけpowで求め、
      inv_fact[i-1] = inv_fact[i] * i で降りてくる」のがO(N)のコツ。
    """

    def __init__(self, n_max, mod=MOD):
        self.mod = mod
        self.fact = [1] * (n_max + 1)
        for i in range(1, n_max + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact = [1] * (n_max + 1)
        # powは1回だけ (ここがO(N)にする工夫)
        self.inv_fact[n_max] = pow(self.fact[n_max], mod - 2, mod)
        for i in range(n_max, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % mod

    def comb(self, n, r):
        """nCr % MOD (範囲外は0)"""
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def perm(self, n, r):
        """nPr % MOD (順列)"""
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[n - r] % self.mod

    def homo(self, n, r):
        """重複組合せ nHr = (n+r-1)Cr : n種類からr個を重複を許して選ぶ"""
        if n == 0:
            return 1 if r == 0 else 0
        return self.comb(n + r - 1, r)


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    # 割り算の例: 10 / 4 (mod 998244353)
    x = 10 * mod_inverse(4) % MOD
    print(x * 4 % MOD)      # 10 に戻る

    mc = ModComb(10 ** 6)   # N最大値まで前計算 (10^6でも一瞬)
    print(mc.comb(5, 2))    # 10
    print(mc.perm(5, 2))    # 20
    print(mc.homo(3, 2))    # 6 (3種から2個重複可: 6通り)

    # べき乗はpow一択
    print(pow(2, 10 ** 18, MOD))   # 2^(10^18) % MOD が一瞬で出る
