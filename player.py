from abc import ABC, abstractmethod
from typing import Any, Self
from question import Question
from enum import Enum
import pygame
import random
import time

class Score:
    def __init__(self, value: int):
        self.value = value

    def add(self, points: int):
        self.value += points

    def deduct(self, points: int):
        self.value -= points

    def __str__(self):
        return f"Score: {self.value}"
    
class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @property
    def ability(self):
        configs = {
            Difficulty.EASY:   {"accuracy": 0.5, "speed_range": (3.0, 5.5)},
            Difficulty.MEDIUM: {"accuracy": 0.7, "speed_range": (1.5, 3.5)},
            Difficulty.HARD:   {"accuracy": 0.85, "speed_range": (0.5, 2.5)}
        }
        return configs[self]

class Player(ABC):

    def __init__(self, name: str, image_path: str):
        self.name = name
        self.score = Score(0)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.is_active = False

    def update_score(self, answer: int, current_question: Question) -> bool:
        """Update score; if correct return True; else False."""
        if answer == current_question.answer:
            self.score.add(current_question.point)
            return True
        else:
            self.score.deduct(current_question.point)
            return False
        
    @abstractmethod
    def get_answer(self, limit: int = 5) -> int:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} (Score: {self.score})"
    

class HumanPlayer(Player):

    def get_answer(self, limit: int = 5) -> str:
        answer = input("")


class AIPlayer(Player):
    def __init__(self, name: str, image_path: str, difficulty: str = "medium"):
        super().__init__(name, image_path)
        self.difficulty = difficulty

        ability = difficulty.ability
        self.accuracy = ability["accuracy"]
        self.speed_range = ability["speed_range"]

        self.decision_time = 0

    def start_thinking(self):
        self.is_active = True
        self.decision_time = random.uniform(*self.speed_range)

    def get_answer(self, current_question: Question) -> int:
        """logic: get AIPlayer's answer """
        if not self.is_active:
            return None
        
        remaining_time = current_question.get_remaining_time()

        if self.decision_time >= current_question.timeout - remaining_time:
            self.is_active = False
            
            if random.random() < self.accuracy:
                return current_question.answer
            else:
                wrong_options = [opt for opt in current_question.options if opt != current_question.answer]
                return random.choice(wrong_options) if wrong_options else current_question.answer
        
        return None
    
    """Example use of get_answer in main round: (do not make recursion in Player class)
    ...
    while running:
    ...
    # bot get the chance to answer.
        bot.start_thinking()
        ans = bot.get_answer(correct_option, all_options)
        if ans:
            correctness = aiplayer1.update_score(answer, correct_option, points)
        ...
    """