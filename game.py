from player import HumanPlayer, AIPlayer
from api_manager import QuestionManager
from enum import Enum
import random

class GameRound(Enum):
    JEOPARDY = 1
    DOUBLE_JEOPARDY = 2
    FINAL_JEOPARDY = 3

class JeopardyGame:
    def __init__(self):
        self.qm = QuestionManager()
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
            
        self.used_questions.append(index)
        self.current_question_value = score
        
        self.current_question = self.qm.fetch_question(category, score)
        return self.current_question

    def process_answer(self, player_index, provided_answer):
        # Check first if the question exists
        if not self.current_question:
            return False
        
        """ Check if the player's chosen answer is correct and update the score! """
        player = self.players[player_index]
        correct_answer = self.current_question['answer']

        # Use strip().lower() to reduce case or spacing errors
        if provided_answer.strip().lower() == correct_answer.strip().lower():
            # Convert the score received from fetch_question into a number and add it.
            # (Be careful for now: the score value in current_question can be a string)
            player.score.add(self.current_question_value)
            return True
        else:
            player.score.deduct(self.current_question_value)
            return False
