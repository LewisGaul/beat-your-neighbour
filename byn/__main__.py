import tkinter as tk

from .game import Game
from .widgets import CardPileWidget


app = tk.Tk()

game = Game()

player_piles: dict[int, CardPileWidget] = {
    p: CardPileWidget(app, num_cards=game.get_player_hand_size(p), show_card=False)
    for p in game.remaining_players
}
centre_pile = CardPileWidget(app)

player_piles[0].pack(side=tk.LEFT)
centre_pile.pack(side=tk.LEFT)
player_piles[1].pack(side=tk.LEFT)


def next_card(_=None):
    player = game.next_player
    game.next_action()
    player_piles[player].update_cards(new_num=game.get_player_hand_size(player))
    centre_pile.update_cards(
        game.centre_pile[-1] if len(game.centre_pile) > 0 else None,
        new_num=len(game.centre_pile),
    )
    print(
        f"Next player: {game.next_player}  ({game.get_player_hand_size(0)}-{game.get_player_hand_size(1)})"
    )


app.bind("<ButtonRelease-1>", next_card)

app.mainloop()
