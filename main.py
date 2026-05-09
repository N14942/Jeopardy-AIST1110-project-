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

    def buzz_session(self) -> AIPlayer | HumanPlayer | None:
        valid_p = [p for p in self.game.players if p.buzz == True]
        if not valid_p:
            return None
        
        for p in valid_p:
            if isinstance(p, AIPlayer):
                p.start_buzzing()

        while True:
            if self.game.current_question.get_buzzing_time_left() <= 0:
                return None
            for p in valid_p:
                if isinstance(p, AIPlayer):
                    key = self.game.current_question
                else: 
                    key = None #interface:get_event
                if p.check_buzz(key) == True:
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
                index = None # index = self.ui.get_clicked_question_index()
                if index != None:
                    q = self.game.all_question(index)
        return q
    
    def question_answering_session(self, player: AIPlayer | HumanPlayer) -> bool:
        if isinstance(player, AIPlayer):
            player.start_thinking()

        if isinstance(player, AIPlayer):
            while True:
                if player.get_answer() == True:
                    is_correct =  player.update_score(self.game.current_question)
                    return is_correct
                if player.get_answer() == False:
                    player.update_score(self.game.current_question)
            
        else:
            while True:
                answer = 0 #[hook]
                """interface: logic: Detect HumanPlayer's answer. 
                    Return True if answered successfully in time limit.
                    False if no answer.
                    None if no answer.
                    (Design purpose: deal with valid answer/ timeout/ wait for answer)
                    Please help me move time-detecting to get_answer in interface.
                    time logic in previous player class:
                    def get_answer(self, current_question: Question, answer: int = None) -> bool:
                    (Design purpose: deal with valid answer/ timeout/ wait for answer)
        
        remaining_time = current_question.get_remaining_time()

        if remaining_time <= 0:
            self.current_choice = -1
            return False
        
        if answer is not None:
            self.current_choice = answer
            return True

        return None
                    """
                if answer == None:
                    #out of time:interface
                    return False
                else:
                    is_correct =  player.update_score(self.game.current_question)
                    return is_correct

    def non_final_jeopardy(self):
        self.game.generate_questions()

        while self.game.used_questions < 16:
            self.game.current_question = self.select_question_session()
            while True:
                cur_player = self.buzz_session()
                if cur_player is None:
                    # 无人抢答或所有人都因为答错被封锁了，跳过本题
                    # [INTERFACE HOOK]: 界面显示正确答案，停留 2 秒
                    break

                cur_player = self.buzz_session()
                if self.question_answering_session(cur_player):
                    #interface
                    break
                else:
                    #interface
                    pass #pass 为占位符
            
            self.game.reset_question_states()

        self.game.reset_board()
        self.round += self.current_round
        
    def final_jeopardy(self):
        eligible_players = [p for p in self.game.players if p.score > 0]
        if not eligible_players:
            #No people > 0 mark :)
            return
        self.game.generate_questions() 
        final_q = self.game.all_question
        self.game.current_question = final_q

    def summary():
        pass

    def gamerun(self):
        self.non_final_jeopardy()
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
