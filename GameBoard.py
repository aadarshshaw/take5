from exceptions.SmallestCardOnRightException import SmallestCardOnRightException
from utils.Constants import Constants
from Card import Card
from collections import deque
import math


class Board:

    def __init__(self):
        self.board = [deque() for _ in range(Constants.ROWS)]

    def getBoard(self):
        return self.board

    def setInitialPositons(self, cards: list[Card]):
        assert len(cards) == Constants.ROWS

        for i in range(Constants.ROWS):
            self.board[i].append(cards[i])

    def clearRow(self, row: int) -> list[Card]:
        cardsToReturn = []
        while len(self.board[row]) > 0:
            cardsToReturn.append(self.board[row].popleft())
        return cardsToReturn

    def addCardtoBoard(self, card: Card) -> list[int]:
        rowToAdd = -1
        closestDiff = math.inf
        cardsToReturn = []
        for i in range(Constants.ROWS):
            if self.board[i][-1].getValue() < card.getValue():
                diff = card.getValue() - self.board[i][-1].getValue()
                if diff < closestDiff:
                    closestDiff = diff
                    rowToAdd = i
        if rowToAdd == -1:
            raise SmallestCardOnRightException("Card needs to be added to the front")

        if len(self.board[rowToAdd]) == Constants.COLUMNS:
            print(
                f"{Constants.COLUMNS + 1}th card to be placed, getting rid of the row"
            )
            cardsToReturn = self.clearRow(rowToAdd)
            self.board[rowToAdd].append(card)
        else:
            self.board[rowToAdd].append(card)

        return cardsToReturn

    def addCardToBoardFront(self, card: Card, row: int) -> list[Card]:
        assert row >= 0
        assert row < Constants.ROWS

        cardsToReturn = self.clearRow(row)
        self.board[row].appendleft(card)

        return cardsToReturn
