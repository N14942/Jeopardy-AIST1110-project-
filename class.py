from abc import ABC, abstractmethod
from typing import Any, Self
from enum import Enum
import pygame

class GameRound(Enum):
    JEOPARDY = 1
    DOUBLE_JEOPARDY = 2
    FINAL_JEOPARDY = 3

class Score:
    def __init__(self, value: int):
        self.value = value

    def add(self, points: int):
        self.value += points

    def deduct(self, points: int):
        self.value -= points

    def __str__(self):
        return f"Score: {self.value}"

class Player(ABC):

    def __init__(self, name: str, image_path: str):
        self.name = name
        self.score = Score(0)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.is_active = False

    @abstractmethod
    def get_answer(self, limit: int = 5) -> int:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} (Score: {self.score})"
    

class HumanPlayer(Player):

    def get_answer(self, limit: int = 5) -> str:
        """logic: get Player's answer, and do score calculation"""
        pass


class AIPlayer(Player):
    def __init__(self, name: str, image_path: str, difficulty: str = "medium"):
        super().__init__(name, image_path)
        self.difficulty = difficulty

    def get_answer(self, timeout: int = 5) -> str:
        """logic: get AIPlayer's answer, and do score calculation"""
        pass