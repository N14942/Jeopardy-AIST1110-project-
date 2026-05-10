from abc import ABC, abstractmethod
from question import Question
from enum import Enum
import pygame
import random

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

    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.current_choice = None
        self.buzz = True

    def buzz_reset(self):
        # Allow player to buzz.
        self.buzz = True

    def update_player_info(self, name: str):
        self.name = name
        
    @abstractmethod
    def check_buzz(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def get_answer(self, current_question, **kwargs) -> int:
        pass
    
class HumanPlayer(Player):
    def check_buzz(self, event):
        """Check whether human player press SPACE to buzz in, return True if Yes."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False

    def update_score(self, current_question: Question) -> bool:
        if self.current_choice == current_question.correct_index:
            self.score += current_question.point
            current_question.answered = True
            return True
        else:
            self.score -= current_question.point
            # Ban buzzing of this player this round.
            self.buzz = False
            return False
        
    def update_answer(self, answer):
        self.current_choice = answer
    def get_answer(self, current_question: Question, answer: int = None) -> bool:
        remaining_time = current_question.get_remaining_time()

        if remaining_time <= 0:
            self.current_choice = -1
            return False

        if answer is not None:
            self.current_choice = answer
            return True

        return None
    


class AIPlayer(Player):
    def __init__(self, name: str, difficulty = Difficulty.MEDIUM):
        super().__init__(name)
        self.difficulty = difficulty
        ability = self.difficulty.ability
        self.accuracy = ability["accuracy"]
        self.speed_range = ability["speed_range"]
        self.reaction_time = ability["reaction_time"]
        self.decision_time = 0
        self.target_buzz_time = 0

    def start_thinking(self):
        self.decision_time = random.uniform(*self.speed_range)

    def start_buzzing(self):
        self.target_buzz_time = random.uniform(*self.reaction_time)

    def update_score(self, current_question: Question) -> bool:
        if self.current_choice == current_question.correct_index:
            self.score += current_question.point
            current_question.answered = True
            return True
        else:
            self.score -= current_question.point
            # Ban buzzing of this player this round.
            self.buzz = False
            return False

    def check_buzz(self, current_question: Question) -> bool:
        remaining_time = current_question.get_buzzing_time_left()
        return remaining_time >= current_question.buzzing_time - self.target_buzz_time
    
    def do_wager(self, max_value, round = 1):
        if round == 3:
            return random.randint(0, int(self.score))
        else:
            return random.randint(5, int(max(self.score, max_value)))
        
    def select_question(self, q: list[Question]):
        pygame.time.delay(1000) 
        valid = [x for x in q if x.answered == False]
        return random.choice(valid)

    def get_answer(self, current_question: Question) -> bool:
        """logic: get AIPlayer's answer and store in the Player. 
            Return True if answered successfully in time limit.
            False if out of time.
            None if no answer.
            (Design purpose: deal with valid answer/ timeout/ wait for answer)"""
        
        remaining_time = current_question.get_remaining_time()

        if remaining_time <= 0:
            self.current_choice = -1
            return False

        if self.decision_time >= current_question.timeout - remaining_time:         
            if random.random() < self.accuracy:
                self.current_choice = current_question.answer
                return True
            else:
                wrong_indices = [i for i in range(len(current_question.options)) if i != current_question.answer]
                self.current_choice = random.choice(wrong_indices)
                return True

        return None