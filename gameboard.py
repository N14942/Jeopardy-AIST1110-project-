from player import HumanPlayer, AIPlayer, Difficulty
from question import Question, AI_Manager
from enum import Enum
import random

class Gameboard:
    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM, 
                 player_number: int = 3, 
                 buzzing_time: int = 5, 
                 timeout: int = 5, 
                 env_used: bool = True, 
                 categories = ["Science", "History", "Geography", "Culture"]):
        self.player_number = player_number
        self.difficulty = difficulty
        self.buzzing_time = buzzing_time
        self.timeout = timeout
        self.ai_manager = AI_Manager(env_used=env_used)
        # Manage player list
        self.players = [HumanPlayer("You")]
        self.ranking = []
        self.current_round = 1
        self.current_question = None

        self.categories = categories
        self.all_question = []
        self.used_questions = 0
        
    def generate_aiplayers(self):
        name_pool = ["Jacky", "Lily", "L", "Bocchi", "Oblivious", "Yagami", "Kita", "Tomorin", "Ryo", "Solo_leveling", "OMGkawaiiAngel"]
        def diff_set():
            if self.difficulty == "Random":
                return random.choice([Difficulty.MEDIUM, Difficulty.EASY, Difficulty.HARD])
            else:
                return self.difficulty
        for i in range(self.player_number - 1):
            name = random.choice(name_pool)
            self.players.append(AIPlayer(name, diff_set()))
            name_pool.remove(name)

    def generate_questions(self):
        if self.current_round == 3:
            field = random.choice(self.categories)
            final_question = Question(field=field, point=0, timeout=10) 
            final_question.generate(self.ai_manager, round_num=3)
            self.all_question = final_question
        else:
            point_list = [200, 400, 600, 1000]
            point_list = [x * self.current_round for x in point_list]

            double_coords = set()
            while len(double_coords) < self.current_round:
                double_coords.add((random.randint(0, 3), random.randint(0, 3)))

            for i in range(4):
                for j in range(4):
                    q = Question(
                        field = self.categories[i], 
                        point = point_list[j], 
                        timeout = self.timeout, 
                        buzzing_time = self.buzzing_time
                        )
                    if (i, j) in double_coords:
                        q.set_as_daily_double()
                    q.generate(ai_manager=self.ai_manager, round_num = self.current_round)
                    self.all_question.append(q)
                
            
    def reset_board(self):
        self.all_question = []
        self.used_questions = 0
        self.current_round += 1

    def reset_question_states(self):
        self.used_questions += 1
        self.current_question.answered = True
        self.update_rankings()

        for player in self.players:
            player.buzz_reset()
            player.current_choice = None

    def get_max_board_value(self) -> int:
        if self.current_round == 1:
            return 1000
        elif self.current_round == 2:
            return 2000
        return 0

    def update_rankings(self):
        self.ranking = sorted(self.players, key=lambda x: x.score, reverse=True)