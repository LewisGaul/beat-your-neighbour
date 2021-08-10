import pathlib
import tkinter as tk

from .cards import Card

IMG_DIR = pathlib.Path("img")


app = tk.Tk()


class CardWidget(tk.Label):
    def __init__(self, master, card: str | Card, *args, **kwargs):
        if isinstance(card, str):
            card = Card.from_str(card)
        self.card = card
        self._image = tk.PhotoImage(
            file=IMG_DIR / (self._get_img_filename(card) + ".png")
        )
        kwargs["image"] = self._image
        super().__init__(master, *args, **kwargs)

    @staticmethod
    def _get_img_filename(card) -> str:
        if 2 <= card.value.value <= 10:
            val_str = str(card.value.value)
        else:
            val_str = card.value.name
        return f"{val_str}_of_{card.suit.name}".lower()


card = CardWidget(app, "As")
card.pack()

app.mainloop()
