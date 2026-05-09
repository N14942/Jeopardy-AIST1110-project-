from interface import Interface
from gameboard import Gameboard
from player import AIPlayer, HumanPlayer, Difficulty
from question import Question

class Round:
    def __init__(self):
        self.game = Gameboard(difficulty=Difficulty.MEDIUM)
        self.round = 1
        self.game.generate_aiplayers()
        self.game.generate_questions()

        self.ui = Interface(game_logic=self.game)
    
    def game_setting(self):
        """Accept a list of setting and apply on gameboard(timeout, difficulty...)."""
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
            
        return q
        


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
