from enum import Enum, auto


class GameMode(Enum):
    STEALING = auto
    NO_STEALING = auto


class MaxMinPlayer(Enum):
    MAX_PLAYER = auto
    MIN_PLAYER = auto

class Difficulty(Enum):
    EASY = auto
    MEDIUM = auto
    HARD = auto
