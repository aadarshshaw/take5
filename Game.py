import socket
import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
from Card import Card
from Player import Player
from GameBoard import Board
from exceptions.SmallestCardOnRightException import SmallestCardOnRightException
from utils.Constants import Constants


class Game:

    def __init__(self):
        self.gameStarted = False
        self.entryStopped = False
        self.players: List[Player] = []
        self.deck = [Card(i, random.choice([x for x in range(1, 3)])) for i in range(1, Constants.TOTAL_CARDS + 1)]
        self.shuffledDeck = random.sample(self.deck, k=Constants.TOTAL_CARDS)
        self.discardPile: List[Card] = []
        self.gameBoard = Board()

    def addPlayer(self, player: Player):
        if len(self.players) >= Constants.MAX_PLAYERS or self.entryStopped:
            return
        self.players.append(player)

    def removePlayer(self, player: Player):
        self.players.remove(player)

    def stopEntry(self):
        self.entryStopped = True

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
            player.send_message(message)

    def waitForPlayers(self, host: str = '0.0.0.0', port: int = 12345):
        print(f"[SERVER] Waiting for players on {host}:{port}...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(Constants.MAX_PLAYERS)

        while len(self.players) < Constants.MAX_PLAYERS:
            conn, addr = server.accept()
            print(f"[CONNECTED] {addr} connected.")
            conn.sendall(b"Enter your name: ")
            name = conn.recv(1024).decode().strip()
            new_player = Player(name, conn)
            self.addPlayer(new_player)
            new_player.send_message(f"Welcome, {name}! Waiting for other players...\n")
            self.broadcast(f"{name} has joined the game!\n")

            if len(self.players) >= Constants.MIN_PLAYERS:
                self.broadcast("Minimum players reached. Starting soon...\n")
                for i in range(3):
                    self.broadcast(f"Starting in {3 - i} seconds...")
                    time.sleep(1)
                    self.broadcast("\n")        
                break            

        self.stopEntry()
        server.close()

    def startGame(self):
        if self.gameStarted:
            self.broadcast("Game already started\n")
            return
        if len(self.players) < Constants.MIN_PLAYERS:
            self.broadcast("Not enough players to start the game\n")
            return
        if len(self.players) > Constants.MAX_PLAYERS:
            self.broadcast("Too many players to start the game\n")
            return

        initialCards = self.getCardsFromShuffledDeck(Constants.ROWS)
        self.gameBoard.setInitialPositons(initialCards)
        self.distributeCards()
        self.gameStarted = True

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

            # Render and send board to all clients
            board_str = self.gameBoard.printBoard()
            self.broadcast("\nCurrent Board:\n")
            self.broadcast(board_str + "\n")

            executor = ThreadPoolExecutor(max_workers=len(self.players))
            results = executor.map(lambda player: player.playCard(), self.players)
            cardsReceived = list(results)
            cardsReceived.sort(key=lambda x: x["card"].getValue()) # Smallest card gets placed first

            for cardReceived in cardsReceived:
                player = cardReceived["player"]
                card = cardReceived["card"]
                self.broadcast(f"{player.getName()} played {card}\n")

                try:
                    cardsReturned = self.gameBoard.addCardtoBoard(card)
                except SmallestCardOnRightException:
                    self.broadcast(f"{player.getName()} needs to play {card} on the front\n")
                    rowSelected = player.getRowToAdd(card)
                    cardsReturned = self.gameBoard.addCardToBoardFront(card, rowSelected)

                for returnedCard in cardsReturned:
                    bulls = returnedCard.getBulls()
                    self.broadcast(f"Adding {bulls} bulls to {player.getName()}'s penalty points\n")
                    player.addPenaltyPoints(bulls)
                    self.discardPile.append(returnedCard)

            executor.shutdown(wait=True)

            # After the round, show updated board again
            board_str = self.gameBoard.printBoard()
            self.broadcast("\nBoard After Round:\n")
            self.broadcast(board_str + "\n")

            if rounds % Constants.CARDS_PER_HAND == 0:
                self.distributeCards()

            if self.endGame():
                break
