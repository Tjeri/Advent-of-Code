def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    div, mod = divmod(b, a)
    g, x, y = extended_gcd(mod, a)
    return g, y - div * x, x


def mod_inverse(a: int, b: int) -> int:
    g, x, _ = extended_gcd(a, b)
    if g != 1:
        raise ValueError(f'No gcd possible for {a}, {b}.')
    return x % b
