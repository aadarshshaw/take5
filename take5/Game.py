import random
from concurrent.futures import ThreadPoolExecutor
from typing import List
from Card import Card
from Player import Player
from GameBoard import Board
from exceptions.SmallestCardOnRightException import SmallestCardOnRightException
from renderers.BoardRenderer import BoardRenderer
from utils.Constants import Constants
from utils.getBulls import getBulls


class Game:

    def __init__(self, players: List[Player]):
        self.gameStarted = False
        self.entryStopped = False
        self.players: List[Player] = players
        self.deck = [Card(i, getBulls(i)) for i in range(1, Constants.TOTAL_CARDS + 1)]
        self.shuffledDeck = random.sample(self.deck, k=Constants.TOTAL_CARDS)
        self.discardPile: List[Card] = []
        self.gameBoard = Board()
        self.renderer = BoardRenderer()

    def getPlayers(self):
        return self.players

    def getCardsFromShuffledDeck(self, numCards: int) -> List[Card]:
        if len(self.shuffledDeck) < numCards:
            self.broadcast("Shuffling from discard pile\n")
            random.shuffle(self.discardPile)
            self.shuffledDeck = self.discardPile + self.shuffledDeck
            self.discardPile = []

        cards = self.shuffledDeck[:numCards]
        self.shuffledDeck = self.shuffledDeck[numCards:]
        return cards

    def distributeCards(self):
        for player in self.players:
            player_cards = self.getCardsFromShuffledDeck(Constants.CARDS_PER_HAND)
            player.addCards(player_cards)

    def broadcast(self, message: str):
        for player in self.players:
            player.sendMessage(message)
    
    def broadcastUpdate(self):
        """Send updated board to all players."""
        for player in self.players:
            output = "\n".join([
                self.renderer.clearScreen(),
                self.renderer.renderHeader(),
                self.renderer.renderGameBoard(self.gameBoard.getBoard(), self.players),
                self.renderer.renderFooter()
            ])
            player.sendMessage(output)

    def log(self, message: str):
        self.renderer.addLog(message)
        self.broadcastUpdate()

    def startGame(self):
        if len(self.players) < Constants.MIN_PLAYERS:
            self.broadcast("Not enough players to start the game\n")
            return
        if len(self.players) > Constants.MAX_PLAYERS_PER_ROOM:
            self.broadcast("Too many players to start the game\n")
            return

        initialCards = self.getCardsFromShuffledDeck(Constants.ROWS)
        self.gameBoard.setInitialPositons(initialCards)
        self.distributeCards()
        self.gameStarted = True
        self.runGame()

    def endGame(self) -> bool:
        maxPenaltyPoints = max(player.getPenaltyPoints() for player in self.players)
        if maxPenaltyPoints >= Constants.MAX_PENALTY_POINTS:
            self.broadcast("Game Ended\n")
            self.players.sort(key=lambda x: x.getPenaltyPoints())
            for player in self.players:
                self.broadcast(f"{player.getName()} has {player.getPenaltyPoints()} penalty points\n")
            self.broadcast(f"{self.players[0].getName()} won the game!\n")
            return True
        return False

    def runGame(self):
        rounds = 0
        while True:
            rounds += 1
            self.broadcastUpdate()

            executor = ThreadPoolExecutor(max_workers=len(self.players))
            results = executor.map(lambda player: player.playCard(self.gameBoard.getBoard(), self.players, self.renderer), self.players)
            cardsReceived = sorted(list(results), key=lambda x: x["card"].getValue())

            for entry in cardsReceived:
                card: Card = entry["card"]
                player: Player = entry["player"]
                self.log(f"{player.getName()} played {card}")
                cardsReturned = []
                try:
                    cardsReturned = self.gameBoard.addCardtoBoard(card)
                except SmallestCardOnRightException:
                    self.log(f"{player.getName()} must place {card} at the front")
                    rowIndex = player.getRowToAdd(card, self.gameBoard.getBoard(), self.players, self.renderer)
                    cardsReturned = self.gameBoard.addCardToBoardFront(card, rowIndex)

                for c in cardsReturned:
                    self.log(f"{c.getBulls()} bulls from {c} added to {player.getName()}")
                    player.addPenaltyPoints(c.getBulls())
                    self.discardPile.append(c)

            executor.shutdown(wait=True)

            if rounds % Constants.CARDS_PER_HAND == 0:
                self.distributeCards()

            if self.endGame():
                break