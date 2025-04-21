# -*- coding: utf-8 -*-
from Player import Player
from utils.Constants import Constants

class RoomRenderer:

    WIDTH = 100
    
    def __init__(self):
        pass

    def renderRoomScreen(self, roomName: str, players: list[Player], started: bool, logs: list[str]) -> str:
        output = [Constants.CLEAR_SCREEN]

        # Header
        header = f" ROOM: {roomName} "
        output.append(f"+{header:─^95}+")
        output.append("|                                                                                               |")
        status = "In-Game" if started else "Waiting for players..."
        output.append(f"|  Status: {status:<85}|")
        output.append("|                                                                                               |")
        output.append("|  Players:                                                                                     |")

        # Player Table Header
        output.append("|  ┌────────────────────────────────────────────┐                                               |")
        output.append("|  │ Name                                       │                                               |")
        output.append("|  ├────────────────────────────────────────────┤                                               |")

        # Player Rows
        if not players:
            output.append("|  │ No players joined yet                      │                                               |")
        else:
            for player in players:
                name = player.getName()[:42]
                output.append(f"|  │ {name:<42} │                                               |")

        output.append("|  └────────────────────────────────────────────┘                                               |")
        output.append("|                                                                                               |")

        # Logs Table
        output.append("|  Logs:                                                                                        |")
        output.append("|  ┌────────────────────────────────────────────────────────────────────────────────────────┐   |")
        if logs:
            for log in logs[-5:]:  # Last 5 logs
                output.append(f"|  │ {log:<87}|   |")
        else:
            output.append("|  │ No logs yet.                                                                           │   |")
        output.append("|  └────────────────────────────────────────────────────────────────────────────────────────┘   |")
        output.append("|                                                                                               |")
        output.append("+───────────────────────────────────────────────────────────────────────────────────────────────+")

        return "\n".join(output)

    def renderInstructions(self, canStart: bool) -> str:
        if canStart:
            return f"\nMinimum {Constants.MIN_PLAYERS} players reached.\nFirst player can type 'start' to begin the game.\n"
        else:
            return f"\nWaiting for more players to join...\n"

    def renderRoom(self, roomName: str, players, canStart: bool, gameStarted: bool, logs: list[str]) -> str:
        return (
            self.renderRoomScreen(roomName, players, gameStarted, logs) +
            self.renderInstructions(canStart)
        )
