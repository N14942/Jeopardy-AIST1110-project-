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
    
    def get_answer_of_player(self, player) -> bool:
        q = self.game.current_question
        q.reset_time()
        if isinstance(player, AIPlayer):
            player.start_thinking()
            while True:
                status = player.get_answer(q)
                if status is True:
                    return player.update_score(q)
                elif status is False:
                    player.update_score(q) 
                    return False
                
        else:
            while True:
                answer = None #[hook]
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
                if q.get_remaining_time() <= 0:
                    self.current_choice = -1
                    player.update_score(q)
                    return False
                
                if answer is not None:
                    player.current_choice = answer
                    return player.update_score(q)
                
    def get_wager_of_player(self, player) -> int:
        """
        get wage of player.
        """
        q = self.game.current_question

        if self.round == 3:
            max_value = 0 # Final Jeopardy 的逻辑在 do_wager 内部会自动使用玩家的 score
        else:
            max_value = self.game.get_max_board_value()
            
        if isinstance(player, AIPlayer):
            wager = player.do_wager(max_value, round=self.round)
        else:
            """
                move human wager to interface:
                def do_wager(self, input, max_value, round = 1):
        if round == 3:
            min = 5
            max = self.score
        else:
            min = 0
            max = max(self.score, max_value)
        if input > max or input < min:
            return False
        else:
            return input
                """
            wager = 5 # Hook

        if self.round != 3 and q.is_daily_double:
            q.reset_score(wager)
            
        return wager
    
    def question_answering_session(self, player: AIPlayer | HumanPlayer) -> bool:
        q = self.game.current_question
        if q.is_daily_double:
            self.get_wager_of_player(player, round_num=self.round)
        return self.get_answer_of_player()

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
        self.game.current_round = 3
        self.round = 3
        self.game.generate_questions() 
        final_q = self.game.all_question
        self.game.current_question = final_q

        wagers = {}
        
        for p in eligible_players:
            wagers[p] = self.get_wager_of_player(p, round_num=3)

        #Final question reveal(interface)

        results = {}

        for p in eligible_players:
            final_q.point = wagers[p] 
            
            is_correct = self.get_answer_of_player(p)
            results[p] = is_correct

        # [INTERFACE HOOK]: Show result.

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
