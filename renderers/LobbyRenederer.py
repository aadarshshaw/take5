class LobbyRenderer:
    def __init__(self):
        pass

    def renderLobbyHeader(self) -> str:
        return "\033[2J\033[H" + "=== LOBBY ===\n"

    def renderRooms(self, rooms: dict) -> str:
        if not rooms:
            return "No rooms available.\n"

        output = "Available Rooms:\n"
        for roomName, room in rooms.items():
            playerCount = len(room.players)
            output += f"- {roomName} ({playerCount}/{room.maxPlayers})\n"
        return output

    def renderLobby(self, rooms: dict) -> str:
        return self.renderLobbyHeader() + self.renderRooms(rooms)
