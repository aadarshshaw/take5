import socket
from Card import Card
from utils.RenderBoard import render_cards_grid


class Player:

    def __init__(self, name: str, conn: socket.socket):
        self.name = name
        self.conn = conn  # Socket connection to player
        self.cards = []
        self.penaltyPoints = 0

    def getName(self) -> str:
        return self.name

    def addCards(self, card: list[Card]):
        self.cards.extend(card)

    def removeCard(self, card: Card):
        self.cards.remove(card)

    def getCards(self) -> list[Card]:
        return self.cards

    def getPenaltyPoints(self) -> int:
        return self.penaltyPoints

    def addPenaltyPoints(self, points: int):
        self.penaltyPoints += points

    def send_message(self, message: str):
        """Send a message to the player via socket."""
        self.conn.sendall(message.encode())

    def receive_message(self) -> str:
        """Receive a complete message (line) from the player via socket."""
        data = b""
        while True:
            chunk = self.conn.recv(1024)
            if b"\n" in chunk:
                data += chunk.split(b"\n")[0]  # Add the part before the newline
                break
            else:
                data += chunk
        return data.decode().strip()  # Return the entire message as a string


    def playCard(self):
        cardToPlay = None
        while True:
            self.send_message(f"Player {self.name}, your cards are:\n")
            self.send_message(render_cards_grid(self.cards))
            self.send_message(f"Player {self.name}, your penalty points are: {self.penaltyPoints}\n")
            self.send_message(f"Choose a card to play: ")
            try:
                cardNum = int(self.receive_message())
                cardFound = False
                for i in range(len(self.cards)):
                    if self.cards[i].getValue() == cardNum:
                        cardFound = True
                        cardToPlay = self.cards.pop(i)
                        break
                if cardFound:
                    break
                self.send_message("Invalid card number, try again.\n")
            except ValueError as e:
                self.send_message("Invalid command, try again\n")

        return {"card": cardToPlay, "player": self}

    def getRowToAdd(self, card: Card) -> int:
        self.send_message(f"Choose a row to add {card} to: ")
        inputRow = int(self.receive_message())
        return inputRow
