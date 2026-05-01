from abc import ABC, abstractmethod
from question import Question
from enum import Enum
import pygame
import random

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
            Difficulty.EASY:   {"accuracy": 0.5, "speed_range": (3.0, 5.5), "reaction_time": (4.0, 7.0)},
            Difficulty.MEDIUM: {"accuracy": 0.7, "speed_range": (1.5, 3.5), "reaction_time": (2.5, 4.0)},
            Difficulty.HARD:   {"accuracy": 0.85, "speed_range": (0.5, 2.5), "reaction_time": (0.5, 2.0)}
        }
        return configs[self]


class Player(ABC):

    def __init__(self, name: str, image_path: str):
        self.name = name
        self.score = Score(0)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.current_choice = None
        self.buzz = True

    def buzz_reset(self):
        # Allow player to buzz.
        self.buzz = True

    def update_score(self, current_question: Question) -> bool:
        """Update score; if correct return True; else False."""
        if self.current_choice == current_question.answer:
            self.score.add(current_question.point)
            self.current_choice = None
            return True
        else:
            self.score.deduct(current_question.point)
            self.current_choice = None
            # Player cannot buzz for this question.
            self.buzz = False
            return False
        
    @abstractmethod
    def check_buzz(self) -> bool:
        pass

    def get_answer(self) -> int:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} (Score: {self.score})"
    

class HumanPlayer(Player):
    def check_buzz(self, event):
        """Check whether human player press SPACE to buzz in, return True if Yes."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False

    def get_answer(self, current_question: Question, answer: int = None) -> bool:
        """logic: Update HumanPlayer's answer and store in the Player. 
            Return True if answered successfully in time limit.
            False if no answer.
            None if no answer.
            (Design purpose: deal with valid answer/ timeout/ wait for answer)"""
        remaining_time = current_question.get_remaining_time()

        if remaining_time <= 0:
            self.current_choice = 10
            return False
        
        if answer != None:
            self.current_choice = answer
            return True

        return None


class AIPlayer(Player):
    def __init__(self, name: str, image_path: str, difficulty = Difficulty.MEDIUM):
        super().__init__(name, image_path)
        self.difficulty = difficulty
        ability = self.difficulty.ability
        self.accuracy = ability["accuracy"]
        self.speed_range = ability["speed_range"]
        self.reaction_time = ability["reaction_time"]

    def start_thinking(self):
        self.decision_time = random.uniform(*self.speed_range)

    def start_buzzing(self):
        self.buzzing_time = random.uniform(*self.reaction_time)

    def check_buzz(self, current_question: Question) -> bool:
        remaining_time = current_question.get_buzzing_time_left()
        if remaining_time >= self.reaction_time:
            return True
        return False

    def get_answer(self, current_question: Question) -> bool:
        """logic: get AIPlayer's answer and store in the Player. 
            Return True if answered successfully in time limit.
            False if no answer.
            None if no answer.
            (Design purpose: deal with valid answer/ timeout/ wait for answer)"""
        
        remaining_time = current_question.get_remaining_time()

        if remaining_time <= 0:
            self.current_choice = 10
            return False

        if self.decision_time >= current_question.timeout - remaining_time:         
            if random.random() < self.accuracy:
                self.current_choice = current_question.answer
                return True
            else:
                wrong_options = [opt for opt in current_question.options if opt != current_question.answer]
                self.current_choice = random.choice(wrong_options) if wrong_options else current_question.answer
                return True
        
        return None