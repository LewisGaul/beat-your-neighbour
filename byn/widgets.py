__all__ = ("CardPileWidget",)

import tkinter as tk
from typing import Optional

from . import IMG_DIR
from .cards import Card


class CardPileWidget(tk.Frame):
    """Widget representing a pile of cards."""

    def __init__(
        self,
        master,
        *,
        top_card: Optional[Card] = None,
        num_cards: int = 0,
        show_card: bool = True,
        **kwargs,
    ):
        if num_cards < 0:
            raise ValueError("Number of cards must not be negative")
        if top_card and num_cards == 0:
            raise ValueError("Unexpected top card when number of cards is zero")
        kwargs = {**dict(height=400, width=240, padx=10, pady=10), **kwargs}
        super().__init__(master, **kwargs)
        self.num_cards = num_cards
        self.show_card = show_card
        self._top_card_widget: Optional[CardWidget] = None
        if num_cards > 0:
            self._update_top_card(top_card)

    def update_cards(
        self, new_top_card: Optional[Card] = None, *, new_num: int
    ) -> None:
        self.num_cards = new_num
        if self.num_cards:
            self._update_top_card(new_top_card)
        else:
            self._top_card_widget.destroy()
            self._top_card_widget = None

    def _update_top_card(self, card: Optional[Card]):
        if self._top_card_widget:
            self._top_card_widget.destroy()
        self._top_card_widget = CardWidget(self, card if self.show_card else None)
        self._top_card_widget.pack()


class CardWidget(tk.Label):
    def __init__(self, master, card: str | Card | None, **kwargs):
        if isinstance(card, str):
            card = Card.from_str(card)
        self.card = card
        self._image = tk.PhotoImage(
            file=IMG_DIR / (self._get_img_filename(card) + ".png")
        )
        kwargs["image"] = self._image
        super().__init__(master, **kwargs)

    @staticmethod
    def _get_img_filename(card: Optional[Card]) -> str:
        if not card:
            # No card back image, so just use joker...
            return "black_joker"
        if 2 <= card.value.value <= 10:
            val_str = str(card.value.value)
        else:
            val_str = card.value.name
        return f"{val_str}_of_{card.suit.name}".lower()
