# =====================================================
# GCD / LCM / 拡張ユークリッド / CRT (中国剰余定理)
# =====================================================
# まず組み込みを覚える (自作不要なもの):
#   math.gcd(a, b, ...)   最大公約数 (Python3.9+は3個以上OK)
#   math.lcm(a, b, ...)   最小公倍数 (Python3.9+)
#
# 自作が必要になるのはここから:
#   - 拡張ユークリッド: ax + by = gcd(a,b) の整数解 (x, y)
#   - 「MODが素数でない」ときの逆元 (フェルマー小定理が使えない)
#   - 中国剰余定理 (CRT): 連立合同式を解く
# =====================================================

from math import gcd


def ext_gcd(a, b):
    """
    拡張ユークリッドの互除法
    ax + by = gcd(a, b) を満たす (g, x, y) を返す

    仕組み: gcd(a,b) = gcd(b, a%b) の再帰をほどきながら
    係数を逆算していく。非再帰で書いている。
    """
    # (x1, y1) は a の係数列、(x2, y2) は b の係数列
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0     # a = gcd, x0*a_orig + y0*b_orig = gcd


def mod_inverse_general(a, m):
    """
    a の mod m での逆元 (mが素数でなくてもOK)
    gcd(a, m) == 1 が条件。存在しなければ None
    """
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        return None      # 互いに素でないと逆元は存在しない
    return x % m


def crt(r1, m1, r2, m2):
    """
    中国剰余定理:
      x ≡ r1 (mod m1)
      x ≡ r2 (mod m2)
    を満たす最小の非負整数 x と 周期 lcm(m1, m2) を返す。
    解なしのときは (None, None)。
    m1, m2 は互いに素でなくてもよい一般版。

    使いどころ: 「a日周期の現象とb日周期の現象が同時に起きる日」系
    """
    g, p, _ = ext_gcd(m1, m2)
    if (r2 - r1) % g != 0:
        return None, None            # 解なし
    lcm = m1 // g * m2
    # x = r1 + m1 * t の形で t を決める
    t = ((r2 - r1) // g * p) % (m2 // g)
    x = (r1 + m1 * t) % lcm
    return x, lcm


# ---------------- 使用例 ----------------
if __name__ == "__main__":
    g, x, y = ext_gcd(111, 30)
    print(g, x, y, 111 * x + 30 * y)   # 3 3 -11 3

    # mod 10 (素数でない) での 3 の逆元
    print(mod_inverse_general(3, 10))   # 7 (3*7=21≡1 mod 10)

    # x ≡ 2 (mod 3), x ≡ 3 (mod 5) → x = 8 (mod 15)
    print(crt(2, 3, 3, 5))              # (8, 15)
