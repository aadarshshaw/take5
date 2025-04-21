from utils.Constants import Constants

class RoomRenderer:
    def __init__(self):
        pass

    def renderRoomHeader(self, roomName: str) -> str:
        return "\033[2J\033[H" + f"=== ROOM: {roomName} ===\n"

    def renderPlayers(self, players) -> str:
        output = "Connected Players:\n"
        for p in players:
            output += f"- {p.getName()} (Penalty: {p.getPenaltyPoints()} pts)\n"
        return output

    def renderInstructions(self, canStart: bool) -> str:
        if canStart:
            return f"\nMinimum {Constants.MIN_PLAYERS} players reached.\nFirst player can type 'start' to begin the game.\n"
        else:
            return f"\nWaiting for more players to join...\n"

    def renderRoom(self, roomName: str, players, canStart: bool) -> str:
        return (
            self.renderRoomHeader(roomName) +
            self.renderPlayers(players) +
            self.renderInstructions(canStart)
        )
