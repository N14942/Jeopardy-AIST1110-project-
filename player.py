from abc import ABC, abstractmethod
from typing import Any, Self
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

class Player(ABC):

    def __init__(self, name: str, image_path: str):
        self.name = name
        self.score = Score(0)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.is_active = False

    def update_score(self, answer: str, correct_option: str, points: int) -> bool:
        """Update score; if correct return True; else False."""
        if answer == correct_option:
            self.score.add(points)
            return True
        else:
            self.score.deduct(points)
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
        abilities = {
            "easy":   {"accuracy": 0.5, "min_speed": 3.0, "max_speed": 5.5},
            "medium": {"accuracy": 0.7, "min_speed": 1.5, "max_speed": 3.5},
            "hard":   {"accuracy": 0.85, "min_speed": 0.5, "max_speed": 2.5}
        }
        ability = abilities.get(difficulty, abilities["medium"])
        self.accuracy = ability["accuracy"]
        self.min_speed = ability["min_speed"]
        self.max_speed = ability["max_speed"]

        self.is_thinking = False
        self.start_time = 0
        self.wait_time = 0

    def start_thinking(self):
        self.is_thinking = True
        self.start_time = pygame.time.get_ticks()
        self.wait_time = random.uniform(self.min_speed, self.max_speed) * 1000

    def get_answer(self, correct_option: str, all_options: list) -> str:
        """logic: get AIPlayer's answer """
        if not self.is_thinking:
            return None
        
        current_time = pygame.time.get_ticks()
        if current_time >= self.think_start_time + self.target_wait_time:
            self.is_thinking = False
            
            if random.random() < self.accuracy:
                return correct_option
            else:
                wrong_options = [opt for opt in all_options if opt != correct_option]
                return random.choice(wrong_options) if wrong_options else correct_option
        
        return None
    
    """Example use of get_answer in main round: (do not make recursion in Player class)
    ...
    while running:
    ...
    # aiplayer1 get the chance to answer.
        ans = bot.get_answer(correct_option, all_options)
        if ans:
            correctness = aiplayer1.update_score(self, answer, correct_option, points)
        ...
    """