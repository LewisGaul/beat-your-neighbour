from __future__ import annotations


__all__ = ("Card", "DeckOfCards", "Suit", "Value")

import enum
import random


class Suit(enum.Enum):
    SPADES = enum.auto()
    DIAMONDS = enum.auto()
    CLUBS = enum.auto()
    HEARTS = enum.auto()

    @classmethod
    def from_str(cls, s: str):
        try:
            return getattr(cls, s.upper())
        except AttributeError:
            pass

        if val := {v.name[0]: v for v in cls}.get(s.upper()):
            return val

        raise ValueError(f"Unrecognised suit string {s!r}")


class Value(enum.IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __str__(self):
        if self in [Value.ACE, Value.TEN, Value.JACK, Value.QUEEN, Value.KING]:
            return self.name[0]
        else:
            return str(self.value)

    @classmethod
    def from_str(cls, s: str) -> Value:
        try:
            return getattr(cls, s.upper())
        except AttributeError:
            pass

        try:
            intval = int(s)
        except (TypeError, ValueError):
            pass
        else:
            return cls(intval)

        special_vals = [Value.ACE, Value.TEN, Value.JACK, Value.QUEEN, Value.KING]
        if val := {v.name[0]: v for v in special_vals}.get(s.upper()):
            return val

        raise ValueError(f"Unrecognised value string {s!r}")


class Card:
    """Representation of a card from a deck of playing cards."""

    __slots__ = ("value", "suit")

    value: Value
    suit: Suit

    def __init__(self, value: int | Value, suit: str | Suit):
        if isinstance(suit, str):
            for possible_suit in Suit:
                if suit.upper() in [possible_suit.name, possible_suit.name[0]]:
                    suit = possible_suit
                    break
            else:
                raise ValueError(f"Unrecognised suit {suit!r}")
        self.suit = suit

        if not isinstance(value, Value):
            value = Value(value)
        self.value = value

    @classmethod
    def from_str(cls, shorthand: str) -> Card:
        if len(shorthand) != 2:
            raise ValueError("Expected string of length 2, e.g. 4d or Ac")
        value = Value.from_str(shorthand[0])
        suit = Suit.from_str(shorthand[1])
        return cls(value, suit)

    def __repr__(self):
        return self.shorthand

    def __str__(self):
        return f"Card[{self.shorthand}]"

    def __eq__(self, other):
        try:
            return self.value == other.value and self.suit == other.suit
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.value, self.suit))

    @property
    def shorthand(self) -> str:
        return str(self.value) + self.suit.name[0].lower()


class DeckOfCards(list):
    def __init__(self):
        super().__init__(Card(v, s) for v in Value for s in Suit)

    def shuffle(self):
        random.shuffle(self)
