from typing import List
from Card import Card
from renderers.BoardRenderer import BoardRenderer


class Player:

    def __init__(self, name: str, conn, addr):
        self.name = name
        self.conn = conn
        self.addr = addr
        self.cards: List[Card] = []
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

    def sendMessage(self, message: str):
        try:
            self.conn.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to {self.name}: {e}")

    def receiveMessage(self) -> str:
        try:
            return self.conn.recv(1024).decode().strip()
        except Exception as e:
            print(f"Error receiving message from {self.name}: {e}")
            return ""


    def playCard(self, boardRows, allPlayers: List['Player'], renderer: BoardRenderer) -> dict:
        while True:
            view = [
                renderer.clearScreen(),
                renderer.renderHeader(),
                renderer.renderGameBoard(boardRows, allPlayers),
                renderer.renderHand(self),
                renderer.renderFooter(),
                renderer.renderPrompt()
            ]
            self.sendMessage("\n".join(view))

            inputStr = self.receiveMessage()
            try:
                cardNum = int(inputStr)
            except ValueError:
                self.sendMessage("Invalid input. Enter a number.\n")
                continue

            for i, card in enumerate(self.cards):
                if card.getValue() == cardNum:
                    selected = self.cards.pop(i)
                    return {"card": selected, "player": self}

            self.sendMessage("Card not in hand. Try again.\n")

    def getRowToAdd(self, card: Card, boardRows, allPlayers: List['Player'], renderer: BoardRenderer) -> int:
        view = [
                renderer.clearScreen(),
                renderer.renderHeader(),
                renderer.renderGameBoard(boardRows, allPlayers),
                renderer.renderHand(self),
                renderer.renderFooter(),
            ]
        self.sendMessage("\n".join(view))
        self.sendMessage(f"\n Choose a row (0-3) to add card {card} to: ")
        while True:
            response = self.receiveMessage()
            try:
                rowIndex = int(response)
                if 0 <= rowIndex <= 3:
                    return rowIndex
            except ValueError:
                pass
            self.sendMessage("Invalid row number. Try again (0-3): ")
        
    def closeConnection(self):
        self.conn.close()