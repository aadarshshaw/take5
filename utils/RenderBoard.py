from collections import deque
from typing import Union

from utils.Constants import Constants

def generate_card(number: str, star_count: int, width: int = 10, height: int = Constants.CARD_HEIGHT) -> list[str]:
    card_lines = []

    card_lines.append("+" + "-" * (width - 2) + "+")
    card_lines.append("|{:^{w}}|".format("*" * star_count, w=width - 2))
    # card_lines.append("|{:^{w}}|".format("", w=width - 2))
    card_lines.append("|{:^{w}}|".format(number, w=width - 2))
    card_lines.append("+" + "-" * (width - 2) + "+")
    return card_lines

def render_cards_grid(data: Union[list[deque], list]) -> str:
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

            ascii_cards = [generate_card(str(card), getattr(card, 'bulls', 0)) for card in row]
            for i in range(card_height):
                rendered_lines.append("  ".join(card[i] for card in ascii_cards))
            rendered_lines.append("")
    else:
        if not data:
            return "(no cards to display)"

        ascii_cards = [generate_card(str(card), getattr(card, 'bulls', 0)) for card in data]
        for i in range(card_height):
            rendered_lines.append("  ".join(card[i] for card in ascii_cards))
        rendered_lines.append("")

    return "\n".join(rendered_lines)

