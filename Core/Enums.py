from enum import Enum, auto


class GameMode:
    STEALING = auto()
    NO_STEALING = auto()


class MaxMinPlayer:
    MAX_PLAYER = "min"
    MIN_PLAYER = "max"


class Difficulty(Enum):
    EASY = 6
    MEDIUM = 7
    HARD = 8
