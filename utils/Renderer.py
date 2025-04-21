class Renderer:
    WIDTH_MAIN = 54
    WIDTH_SIDE = 20
    MAX_LOG_LINES = 4

    def __init__(self):
        self.logs: list[str] = []

    def clearScreen(self) -> str:
        return "\033[2J\033[H"

    def renderHeader(self) -> str:
        return f"╔{'═'*self.WIDTH_MAIN}╦{'═'*self.WIDTH_SIDE}╗\n" + \
               f"║ {'🃏 6 Nimmt! Game'.center(self.WIDTH_MAIN - 2)} ║ {'Players'.center(self.WIDTH_SIDE - 2)} ║\n" + \
               f"╠{'═'*self.WIDTH_MAIN}╬{'═'*self.WIDTH_SIDE}╣"

    def renderGameBoard(self, gameBoardRows, players) -> str:
        output = [f"║ {'Game Board'.ljust(self.WIDTH_MAIN - 2)} ║ {self._playerLine(0, players)} ║"]
        for i, row in enumerate(gameBoardRows):
            cards = " ".join(str(card) for card in row)
            right = self._playerLine(i + 1, players)
            output.append(f"║ Row {i+1}: {cards.ljust(self.WIDTH_MAIN - 10)} ║ {right.ljust(self.WIDTH_SIDE - 2)} ║")
        return "\n".join(output) + f"\n╠{'═'*self.WIDTH_MAIN}╬{'═'*self.WIDTH_SIDE}╣"

    def renderHand(self, player) -> str:
        handLine = "  ".join(str(card) for card in player.getCards())
        return f"║ {'Your Hand'.ljust(self.WIDTH_MAIN - 2)} ║ {'Event Log'.ljust(self.WIDTH_SIDE - 2)} ║\n" + \
               f"║ {handLine.ljust(self.WIDTH_MAIN - 2)} ║ {self._logLine(0)} ║"

    def renderFooter(self, player) -> str:
        return f"╠{'═'*self.WIDTH_MAIN}╬{self._logLine(1).ljust(self.WIDTH_SIDE - 2)}╣\n" + \
               f"║ Player: {player.getName()} | Points: {player.getPenaltyPoints():>3} ║ {self._logLine(2).ljust(self.WIDTH_SIDE - 2)} ║\n" + \
               f"╚{'═'*self.WIDTH_MAIN}╩{self._logLine(3).ljust(self.WIDTH_SIDE - 2)}╝"

    def renderPrompt(self, promptText="Choose a card to play:") -> str:
        return f"\n{promptText}"

    def addLog(self, message: str):
        self.logs.append(message)
        self.logs = self.logs[-self.MAX_LOG_LINES:]

    def _playerLine(self, index: int, players) -> str:
        if index < len(players):
            p = players[index]
            return f"{p.getName()} | {p.getPenaltyPoints()} pts"
        return ""

    def _logLine(self, index: int) -> str:
        if index < len(self.logs):
            return f"- {self.logs[index]}"
        return ""
