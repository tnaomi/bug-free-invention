"""
  # Manual Batch Processing

  - Make sure to run this file with command-line argument:
    - `python batch.py 30 X Y X Y X Y X Y` where
    **30** is a variable discount rate,
    **X** is the original price,
    **Y** is the original discounted price.
"""

import math
import sys

global args

args = sys.argv[1:]

def process_args() -> list[float]:
    try:
        result = list(map(float, args))
    except Exception as X:
        raise Exception("An error occurred while attempting to process the args", X)
    if 0 < result[0] > 100:
        raise Exception("Come on! A discount can be within 0 and 100%")
    if len(result[1:]) % 2 != 0:
        raise Exception("Prices should be paired: original and discounted")
    return result


def compare_prices() -> dict[str, str]:
    input_args = process_args()
    discount = input_args[0] / 100
    prices = input_args[1:]

    original_prices = [prices[i] for i in range(0, len(prices), 2)]
    original_discounts = [prices[i + 1] for i in range(0, len(prices), 2)]
    discounted_prices = list(
        map(lambda x: math.fma(discount, -1 * x, x), original_prices)
    )

    result = dict(
        map(
            lambda x, y, z: (f"{x} and {y}", f"Match: {math.isclose(y, z)}"),
            original_prices,
            original_discounts,
            discounted_prices,
        )
    )

    print(result)
    return result
