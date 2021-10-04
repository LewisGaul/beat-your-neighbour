from __future__ import annotations

from typing import Optional

from . import cards
from .cards import Card, DeckOfCards


PlayerID = int


class Game:
    def __init__(self, num_players: int = 2):
        self.num_players = num_players
        self.next_player: PlayerID = 0
        # Take cards from the start of player hands lists.
        self._player_hands: dict[PlayerID, list[Card]] = {i: [] for i in range(num_players)}
        # Add cards to the end of centre pile.
        self.centre_pile: list[Card] = []
        self._cards_until_collect: Optional[int] = None
        self.winner: Optional[PlayerID] = None
        # Deal out the cards.
        deck = DeckOfCards()
        deck.shuffle()
        player_idx = 0
        while deck:
            self._player_hands[player_idx].append(deck.pop())
            player_idx = (player_idx + 1) % self.num_players

    @property
    def remaining_players(self) -> list[PlayerID]:
        return list(self._player_hands.keys())

    def next_action(self):
        if self.winner is not None:
            raise RuntimeError(f"Game already finished, player {self.winner} already won")

        # Cards need collecting.
        if self._cards_until_collect == 0:
            self._player_hands[self.next_player].extend(self.centre_pile)
            self.centre_pile = []
            self._cards_until_collect = None
            return

        # Play the next card.
        next_card = self._player_hands[self.next_player].pop()
        self.centre_pile.append(next_card)

        move_to_next_player = True
        match next_card.value:
            case cards.Value.ACE:
                self._cards_until_collect = 4
            case cards.Value.KING:
                self._cards_until_collect = 3
            case cards.Value.QUEEN:
                self._cards_until_collect = 2
            case cards.Value.JACK:
                self._cards_until_collect = 1
            case _:
                if self._cards_until_collect is not None:
                    self._cards_until_collect -= 1
                    move_to_next_player = False

        if move_to_next_player:
            self._update_next_player()

    def _update_next_player(self) -> None:
        if self._check_for_game_over():
            return
        next_player = (self.next_player + 1) % self.num_players
        while next_player not in self.remaining_players:
            next_player = (self.next_player + 1) % self.num_players
        self.next_player = next_player

    def _check_for_game_over(self) -> bool:
        if len(self.remaining_players) == 1:
            self.winner = self.remaining_players[0]
            return True
        return False
