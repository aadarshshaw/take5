def getBulls(cardNumber: int) -> int:
    if cardNumber == 55:
        return 7
    elif cardNumber % 11 == 0:
        return 5
    elif cardNumber % 10 == 0:
        return 3
    elif cardNumber % 5 == 0:
        return 2
    else:
        return 1