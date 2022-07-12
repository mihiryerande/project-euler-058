# Problem 58:
#     Spiral Primes
#
# Description:
#     Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.
#
#         [37] 36  35  34  33  32 [31]
#          38 [17] 16  15  14 [13] 30
#          39  18  [5]  4  [3] 12  29
#          40  19   6   1   2  11  28
#          41  20  [7]  8   9  10  27
#          42  21  22  23  24  25  26
#         [43] 44  45  46  47  48  49
#
#     It is interesting to note that the odd squares lie along the bottom right diagonal,
#       but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime;
#       that is, a ratio of 8/13 ≈ 62%.
#
#     If one complete new layer is wrapped around the spiral above,
#       a square spiral with side length 9 will be formed.
#     If this process is continued, what is the side length of the square spiral
#       for which the ratio of primes along both diagonals first falls below 10%?

from math import floor, sqrt


def is_prime(x: int) -> bool:
    """
    Returns True iff `x` is prime.

    Args:
        x (int): Integer greater than 1

    Returns:
        (bool) True iff `x` is prime

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(x) == int and x > 1
    mid = floor(sqrt(x)) + 1
    for d in range(2, mid):
        if x % d == 0:
            return False
    return True


def main(pct: int) -> int:
    """
    Returns the side length of the square number spiral
      for which the proportion of prime numbers along both diagonals
      first falls below `pct`%.

    Args:
        pct (int): Percentage in range [1, 100]

    Returns:
        (int): First spiral side length

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(pct) == int and 0 < pct <= 100
    pct /= 100

    # Spiral of length 1 works trivially at 0%, and so is irrelevant, so ignore it
    # Initiate with spiral of length 3, for code convenience later
    s = 3
    primes = 3  # {3, 5, 7}
    total = 5   # 1 (center) + 4 (corners)
    if primes / total < pct:
        return s

    # Iterate up through spiral sizes, keeping track of primes on corners of spiral layer
    while True:
        s += 2
        d = s - 1

        # Idea:
        #     Optimize by skipping prime-check for some corners

        # Case 1:
        #     Bottom-right corner
        #         val_br = (s**2)
        #     Can't be prime, so ignore all
        c = s ** 2  # Bottom-right corner of current spiral layer

        # Case 2:
        #     Bottom-left corner
        #         val_bl = s**2 - s + 1
        #                = s*(s-1) + 1
        #
        #     When s % 3 == 2, we see the value is divisible 3, as follows:
        #         val_bl (mod 3) = [s*(s-1) + 1] (mod 3)
        #                        = [ [s](mod 3) * [s-1](mod 3) + [1](mod 3) ](mod 3)
        #                        = [ 2 * 1 + 1 ](mod 3)
        #                        = [ 3 ](mod 3)
        #                        = 0 (mod 3)
        #
        #     So skip prime-check of bottom-left corner in this case.
        primes += (s % 3 != 2 and is_prime(c-d))

        # Case 3:
        #     Top-left corner
        #         val_tl = s**2 - 2*s + 2
        #                = s*(s-2) + 2
        #
        #     No specific pattern found here, so always prime-check top-left corner.
        primes += is_prime(c-2*d)

        # Case 4:
        #     Top-right corner
        #         val_tr = s**2 - 3*s + 3
        #                = s*(s-2) + 2
        #
        #     When s % 3 == 0, corner value will clearly be divisible by 3.
        #     So skip prime-check of top-right corner in this case.
        #
        #     Note that s = 3 -> val_tr = 3, so only skip for s > 3
        #     This is why the spiral was initiated with s = 3 above.
        primes += (s % 3 != 0 and is_prime(c-3*d))

        total += 4
        if primes / total < pct:
            return s


if __name__ == '__main__':
    diagonal_percentage = int(input('Enter a percentage: '))
    spiral_side_length = main(diagonal_percentage)
    print('Spiral side length when prime percentage along diagonals first falls below {}%:'.format(diagonal_percentage))
    print('  {}'.format(spiral_side_length))
