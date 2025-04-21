from Room import Room
from utils.Constants import Constants

class LobbyRenderer:

    def __init__(self):
        pass


    def renderLobby(self, username: str, rooms: dict) -> str:
        output = [Constants.CLEAR_SCREEN]

        # Header
        output.append(" +──────────────────────────────────────────── LOBBY ────────────────────────────────────────────+")
        output.append(f" |  Welcome, {username:<80}    |")
        output.append(" |                                                                                               |")
        output.append(" |  Available Rooms:                                                                             |")

        # Table Header
        output.append(" |  ┌──────────────┬─────────────┬──────────────┐                                                |")
        output.append(" |  │  Room Name   │  Players    │   Status     │                                                |")
        output.append(" |  ├──────────────┼─────────────┼──────────────┤                                                |")
        output.append(" |  │              │             │              │                                                |")

        # Table Rows
        if not rooms:
            output.append(" |  │              │             │              │                                                |")
        else:
            for room_name in rooms.keys():
                room: Room = rooms[room_name]
                players = f"{len(room.players)} / {room.maxPlayers}"
                status = "In-Game" if room.gameStarted else "Waiting"
                output.append(f" |  │  {room_name:<11} │   {players:<9} │   {status:<10} │                                                |")

        output.append(" |  └──────────────┴─────────────┴──────────────┘                                                |")
        output.append(" |                                                                                               |")
        output.append(" |  [1] Create Room   [2] Join Room   [3] How to Play   [4] Exit                                 |")
        output.append(" |                                                                                               |")
        output.append(" +───────────────────────────────────────────────────────────────────────────────────────────────+\n\n")

        return "\n".join(output)