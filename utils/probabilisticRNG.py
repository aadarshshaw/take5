from math import random

import Constants

def probabilisticRNG( rangeOfNumbers: list, probabilityList: list ) -> int:
    assert(len(rangeOfNumbers) == len(probabilityList))

    return random.choices(rangeOfNumbers, weights=probabilityList, k=Constants.TOTAL_CARDS)

    