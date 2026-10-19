import random

class RollingHash:
    MOD = (1 << 61) - 1

    def __init__(self, s, base=None):
        self.base = base or random.randrange(129, self.MOD - 1)
        M, b = self.MOD, self.base
        n = len(s)
        self.h = h = [0] * (n + 1)
        self.p = p = [1] * (n + 1)
        for i, c in enumerate(s):
            v = c if isinstance(c, int) else ord(c)
            h[i + 1] = (h[i] * b + v) % M
            p[i + 1] = p[i] * b % M

    def get(self, l, r):
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.MOD

    def concat(self, hl, hr, r_len):
        return (hl * self.p[r_len] + hr) % self.MOD