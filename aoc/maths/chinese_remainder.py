import itertools
from functools import reduce
from math import gcd
from typing import Sequence


def solve_chinese_remainder_theorem(elements: Sequence[tuple[int, int]]) -> int:
    """
    Solves chinese remainder theory
    :param elements: list of tuples with the first element being the required number
    and the second element being the modulo. Modulos need to be pairwise coprime.
    :return: solved x that equals the required number for each modulo
    """
    if not check_pairwise_coprime([element[1] for element in elements]):
        raise ValueError('Numbers need to be pairwise coprime')
    N = reduce(int.__mul__, [element[1] for element in elements])
    result = 0
    for number, modulo in elements:
        n = int(N / modulo)
        for i in itertools.count(1):
            if n * i % modulo == number:
                result += n * i
                break
    return result % N


def check_pairwise_coprime(elements: Sequence[int]) -> bool:
    for i in range(len(elements) - 1):
        for j in range(i + 1, len(elements)):
            if gcd(elements[i], elements[j]) != 1:
                return False
    return True
