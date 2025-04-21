import threading
import time
from typing import List
from Game import Game
from Player import Player
from utils.Constants import Constants
from renderers.RoomRenderer import RoomRenderer


class Room:

    def __init__(self, name: str, password: str = None, maxPlayers: int = Constants.MAX_PLAYERS_PER_ROOM):
        self.players: List[Player] = []
        self.gameStarted: bool = False
        self.name: str = name
        self.password: str = password
        self.maxPlayers: int = maxPlayers
        self.Game: Game | None = None
        self.entryStopped: bool = False
        self.renderer = RoomRenderer()
        self.logs = []
        self.waitForPlayers()
    
    def addLog(self, message:str):
        self.logs.insert(0, message)

    def addPlayer(self, player: Player):
        if len(self.players) >= self.maxPlayers:
            player.sendMessage("Maximum number of players reached.\n")
            return
        if self.entryStopped:
            player.sendMessage("Player entry has been stopped.\n")
            return

        self.players.append(player)

        # Notify new player
        player.sendMessage(f"\nWelcome to room '{self.name}', {player.getName()}!\n")

        # Broadcast player joined message and updated view
        self.broadcast(f"\n{player.getName()} has joined the room!\n")
        self.updateRoomView()

    def removePlayer(self, player: Player):
        if player in self.players:
            self.players.remove(player)
            self.broadcast(f"{player.getName()} has left the room.\n")
            self.updateRoomView()

    def stopEntry(self):
        self.entryStopped = True

    def hasGameStarted(self) -> bool:
        return self.gameStarted

    def start(self, players: List[Player]):
        self.gameStarted = True
        self.Game = Game(players)
        self.Game.startGame()

    def waitForPlayers(self):
        def wait_loop():
            while not self.gameStarted:
                if len(self.players) >= Constants.MIN_PLAYERS:
                    first_player = self.players[0]
                    try:
                        first_player.sendMessage(
                            f"\nMinimum {Constants.MIN_PLAYERS} players joined.\n"
                            f"Type 'start' to begin the game or wait for more players.\n> "
                        )
                        response = first_player.conn.recv(1024).decode().strip().lower()
                        if response == "start":
                            self.stopEntry()
                            self.broadcast(f"\nGame is starting with {len(self.players)} players!\n")
                            for i in range(5, 0, -1):
                                self.broadcast(f"Starting in {i}...\n")
                            self.start(self.players)
                            break
                    except Exception as e:
                        print(f"[ERROR] Could not communicate with the first player: {e}")
                        print(f"[ERROR] Removing player from room: {first_player.getName()}")
                        self.players[0].closeConnection()
                        time.sleep(2)

                time.sleep(1)

        thread = threading.Thread(target=wait_loop, daemon=True)
        thread.start()

    def broadcast(self, message: str, render: bool = False):
        if not render: 
            self.addLog(message.strip())
        for player in self.players:
            try:
                player.sendMessage(message)
            except Exception as e:
                print(f"[ERROR] Failed to send message to {player.getName()}: {e}")

    def updateRoomView(self):
        """Render and broadcast the current room state to all players."""
        canStart = len(self.players) >= Constants.MIN_PLAYERS
        rendered = self.renderer.renderRoom(self.name, self.players, canStart, self.gameStarted, self.logs)
        self.broadcast(rendered, render = True)
