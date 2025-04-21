from collections import deque
from typing import Union
from utils.Constants import Constants

class BoardRenderer:
    WIDTH_MAIN = 120
    WIDTH_SIDE = 30
    MAX_LOG_LINES = 7

    def __init__(self):
        self.logs: list[str] = []

    def clearScreen(self) -> str:
        return "\033[2J\033[H"

    def generateCard(
        self,
        number: str,
        star_count: int,
        width: int = Constants.CARD_WIDTH,
        height: int = Constants.CARD_HEIGHT,
    ) -> list[str]:
        card_lines = []

        card_lines.append("+" + "-" * (width - 2) + "+")
        card_lines.append("|{:^{w}}|".format("*" * star_count, w=width - 2))
        # card_lines.append("|{:^{w}}|".format("", w=width - 2))
        card_lines.append("|{:^{w}}|".format(number, w=width - 2))
        card_lines.append("+" + "-" * (width - 2) + "+")
        return card_lines

    def renderCardsGrid(self, data: Union[list[deque], list]) -> list[str]:
        card_height = Constants.CARD_HEIGHT
        rendered_lines = []

        if not data:
            return "(no cards to display)"

        # Determine if this is a list of rows (deques) or a flat list of cards
        is_row_grid = isinstance(data[0], (deque, list))

        if is_row_grid:
            for row in data:
                if not row:
                    rendered_lines.append("(empty row)")
                    rendered_lines.append("")
                    continue
                ascii_cards = [
                    self.generateCard(str(card), getattr(card, "bulls", 0)) for card in row
                ]
                for i in range(card_height):
                    rendered_lines.append("  ".join(card[i] for card in ascii_cards))
                rendered_lines.append("")
        else:
            if not data:
                return "(no cards to display)"

            ascii_cards = [
                self.generateCard(str(card), getattr(card, "bulls", 0)) for card in data
            ]
            for i in range(card_height):
                rendered_lines.append("  ".join(card[i] for card in ascii_cards))
            rendered_lines.append("")

        return rendered_lines

    def renderHeader(self) -> str:
        return (
            f"╔{'═'*self.WIDTH_MAIN}╦{'═'*self.WIDTH_SIDE}╗\n"
            + f"║ {' 6 Nimmt! Game'.center(self.WIDTH_MAIN - 2)} ║ {'Players'.center(self.WIDTH_SIDE - 2)} ║\n"
            + f"╠{'═'*self.WIDTH_MAIN}╬{'═'*self.WIDTH_SIDE}╣"
        )

    def renderGameBoard(self, gameBoardRows, players) -> str:
        output = [
            f"║ {'Game Board'.ljust(self.WIDTH_MAIN - 2)} ║ {self._playerLine(0, players).ljust(self.WIDTH_SIDE - 2)} ║"
        ]
        grid_lines = self.renderCardsGrid(gameBoardRows)
        for i, row in enumerate(grid_lines):
            right = self._playerLine(i + 1, players)
            output.append(
                f"║ {row.ljust(self.WIDTH_MAIN - 2)} ║ {right.ljust(self.WIDTH_SIDE - 2)} ║"
            )
        return "\n".join(output) + f"\n╠{'═'*self.WIDTH_MAIN}╬{'═'*self.WIDTH_SIDE}╣"

    def renderHand(self, player) -> str:
        output = f"║ {'Your Hand'.ljust(self.WIDTH_MAIN - 2)} ║ {self._logLine(0).ljust(self.WIDTH_SIDE - 2)} ║\n"
        for i, row in enumerate(self.renderCardsGrid(player.getCards())):
            left = f"║ {row.ljust(self.WIDTH_MAIN - 2)} ║"
            right = f" {self._logLine(i+1).ljust(self.WIDTH_SIDE - 2)} ║"
            output += left + right + "\n"
        return (
            output
            + f"║{' '*self.WIDTH_MAIN}║ {self._logLine(5).ljust(self.WIDTH_SIDE - 1)}║"
        )

    def renderFooter(self) -> str:
        return (
            "║"
            + f" ".ljust(self.WIDTH_MAIN)
            + "║ "
            + self._logLine(6).ljust(self.WIDTH_SIDE - 1)
            + "║\n"
            + f"╚{'═'*self.WIDTH_MAIN}╩{'═'*self.WIDTH_SIDE}╝\n"
        )

    def renderPrompt(self, promptText="Choose a card to play:") -> str:
        return f"\n{promptText}"

    def addLog(self, message: str):
        self.logs.insert(0, message)
        self.logs = self.logs[: self.MAX_LOG_LINES]

    def _playerLine(self, index: int, players) -> str:
        if index < len(players):
            p = players[index]
            return f"{p.getName()} | {p.getPenaltyPoints()} pts"
        return ""

    def _logLine(self, index: int) -> str:
        if index < len(self.logs):
            return f"- {self.logs[index]}"
        return ""
