from typing import Optional

from . import cards
from .cards import Card, DeckOfCards


PlayerID = int


class Game:

    SPECIAL_CARD_VALUES = {
        cards.Value.JACK: 1,
        cards.Value.QUEEN: 2,
        cards.Value.KING: 3,
        cards.Value.ACE: 4,
    }

    def __init__(self, num_players: int = 2):
        self.num_players = num_players
        self.next_player = 0
        # Take cards from the start of the player hands lists.
        self._player_hands: dict[int, list[Card]] = {p: [] for p in range(self.num_players)}
        # Add cards to the end of the centre cards.
        self.centre_pile: list[Card] = []
        self._cards_until_collect: Optional[int] = None
        self.loser: Optional[PlayerID] = None
        deck = DeckOfCards()
        deck.shuffle()
        player_idx = 0
        while deck:
            self._player_hands[player_idx].append(deck.pop())
            player_idx = (player_idx + 1) % self.num_players

    @property
    def remaining_players(self) -> list[PlayerID]:
        return list(self._player_hands)

    def next_action(self):
        if self.loser is not None:
            raise RuntimeError(f"Game already finished, player {self.loser} lost")

        # If cards need collecting then do this.
        if self._cards_until_collect == 0:
            self._player_hands[self.next_player].extend(self.centre_pile)
            self.centre_pile = []
            self._cards_until_collect = None
            return

        # Play the next card
        next_card = self._player_hands[self.next_player].pop(0)
        self.centre_pile.append(next_card)

        # Special cards always reset the counter and pass on to next player.
        if next_card.value in self.SPECIAL_CARD_VALUES:
            self._update_next_player()
            self._cards_until_collect = self.SPECIAL_CARD_VALUES[next_card.value]
        # Otherwise need to check whether cards need to be collected.
        elif self._cards_until_collect is None:
            self._update_next_player()
        else:
            self._cards_until_collect -= 1

    def get_player_hand_size(self, player: PlayerID) -> int:
        if player < 0 or player >= self.num_players:
            raise ValueError(f"Unexpected player ID {player!r}")
        elif player not in self._player_hands:
            return 0
        else:
            return len(self._player_hands[player])

    def _check_for_game_over(self) -> bool:
        if len(self.remaining_players) == 1:
            self.loser = self.remaining_players[0]
            return True
        assert len(self.remaining_players) > 1
        return False

    def _update_next_player(self) -> None:
        if self._check_for_game_over():
            return
        next_player = (self.next_player + 1) % self.num_players
        while next_player not in self.remaining_players:
            next_player = (next_player + 1) % self.num_players
        self.next_player = next_player
