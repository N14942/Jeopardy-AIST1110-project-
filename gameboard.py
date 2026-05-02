from player import HumanPlayer, AIPlayer
from question import Question, AI_Environment
from enum import Enum
import random

class GameRound(Enum):
    JEOPARDY = 1
    DOUBLE_JEOPARDY = 2
    FINAL_JEOPARDY = 3

class JeopardyGame:
    def __init__(self):
        self.ai_env = AI_Environment(env_used=True)
        # Manage player list
        self.players = [
            HumanPlayer("Player", "assets/player.png"),
            AIPlayer("AI_1", "assets/ai1.png"),
            AIPlayer("AI_2", "assets/ai2.png")
        ]
        self.current_round = 1
        self.current_question = None
        self.used_questions = [] # Save index of already selected question

    def select_question(self, category, score, index):
        """ Select a question and retrieve it from the API. """
        if index in self.used_questions:
            return None # Preventing the re-selection of problems that have already been used
            
        new_q = Question(field, score)
        new_q.generate(self.current_round)
        self.current_question = new_q
        self.used_questions.append(index)
        return new_q

    def process_answer(self, player_index, provided_answer):
        if not self.current_question:
            return False
        
        """ Check if the player's chosen answer is correct and update the score."""
        player = self.players[player_index]
        correct_answer = self.current_question.answer

        if int(provided_answer) == int(correct_answer):
            player.score += self.current_question_value
            return True
        else:
            player.score -= self.current_question_value
            player.buzz = False
            return False
