from interface import Interface
from gameboard import Gameboard
from player import AIPlayer, HumanPlayer, Difficulty
from question import Question

class Round:
    def __init__(self):
        self.game = Gameboard()
        self.round = 1
        self.game.generate_aiplayers()
    
    def game_setting(self):
        """Accept setting and apply on gameboard(timeout, difficulty...)."""
        pass

    def buzz_session(self) -> AIPlayer | HumanPlayer:
        while True:
            for p in self.game.players:
                if p.check_buzz() == True:
                    #interface+(... get chance)
                    return p
                
    def select_question_session(self) -> Question:
        if self.round == 1:
            chooser = self.game.players[self.game.used_questions % self.game.player_number]
        else:
            chooser = self.game.ranking[-1]
        if isinstance(chooser, AIPlayer):
            #interface+(... is choosing problem)
            q = chooser.select_question(self.all_question)
        else:
            while True:
                index = chooser.select_question(
                """add a function return an index represent selected question by human(interface)""")
                if index != None:
                    q = self.game.all_question(index)
        return q
    
    def question_answering_session(player: AIPlayer | HumanPlayer):
        
        pass

    def non_final_jeopardy(self):
        self.game.generate_questions()
        while self.game.used_questions < 16:
            self.game.current_question = self.select_question_session()
            cur_player = self.buzz_session()



        self.game.reset_board()
        self.round += self.current_round
        
    def final_jeopardy():
        pass

    def summary():
        pass

    def gamerun(self):
        self.non_final_jeopardy()
        self.final_jeopardy()
        self.summary()
        
        
        



def main():
    game_logic = Gameboard()
    ui = Interface(game_logic)

    # Run Main Loop
    ui.run() # Run Function 'run()' in 'interface.py'


if __name__ == "__main__":
    main()
