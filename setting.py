from interface import Interface
from gameboard import Gameboard
from player import AIPlayer, HumanPlayer, Difficulty
from question import Question
import pygame

class Session:
    def __init__(self, ui: Interface):
        self.ui = ui
        self.game = ui.game
        self.round = 1
        self.game.generate_aiplayers()
    
    def game_setting(self):
        """Interface: Accept setting and apply on gameboard(timeout, difficulty...)."""
        pass

    def buzz_session(self) -> AIPlayer | HumanPlayer | None:
        self.ui.enter_buzz_scene()
        q = self.game.current_question

        valid_p = [p for p in self.game.players if p.buzz == True]
        if not valid_p:
            return None
        
        for p in valid_p:
            if isinstance(p, AIPlayer):
                p.start_buzzing()

        while self.ui.scene == "buzz":
            self.ui.handle_events()
            self.ui.update_buzz_scene()
            self.ui.draw_buzz()
            pygame.display.flip()

            for p in valid_p:
                if isinstance(p, AIPlayer)and p.check_buzz(q):
                    self.ui.enter_buzz_success_scene(self.game.players.index(p))
                    break

            if q.get_buzzing_time_left() <= 0:
                #Add interface:No one buzz
                self.ui.scene = "choose"
                return None

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:
            self.ui.draw_buzz_success()
            pygame.display.flip()
            
        return self.game.players[self.ui.answering_player_index]
                
    def select_question_session(self):
        self.ui.scene = "choose"
        self.ui.choose_start_ticks = pygame.time.get_ticks()

        if self.round == 1:
            chooser_idx = self.game.used_questions % self.game.player_number
            chooser = self.game.players[self.game.used_questions % self.game.player_number]
        else:
            chooser = self.game.ranking[-1]
            chooser_idx = self.game.players.index(chooser)

        while self.ui.scene == "choose":
            if isinstance(chooser, AIPlayer):
                selected_q = chooser.select_question(self.game.all_question)
                self.game.current_question = selected_q
                self.ui.enter_question_scene()
            else:
                self.ui.handle_events()
                self.ui.draw_choose_question()
                if self.ui.get_choose_time_left() <= 0:
                    valid_qs = [q for q in self.game.all_question if not q.answered]
                    import random
                    self.game.current_question = random.choice(valid_qs)
                    self.ui.enter_question_scene()
        pygame.display.flip()
        self.ui.clock.tick(60)
    
    def get_answer_of_player(self, player: AIPlayer | HumanPlayer) -> bool:
        q = self.game.current_question
        q.reset_time()
        if isinstance(player, AIPlayer):
                player.start_thinking()
        while self.ui.scene == "question":
            self.ui.handle_events()
            self.ui.draw_question_screen()
            pygame.display.flip()

            if isinstance(player, AIPlayer):
                res = player.get_answer(q)
                if res is not None:
                    is_correct = player.update_score(q)
                    #self.ui.show_result_animation(is_correct)
                    return is_correct
                

                if not isinstance(player, AIPlayer) and player.current_choice is not None:
                    is_correct = player.update_score(q)
                    #self.ui.show_result_animation(is_correct)
                    return is_correct
                
                if q.get_remaining_time() <= 0:
                    player.update_answer(-1)
                    player.update_score(q)
                    #self.show_result_animation(False)
                    return False

                
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
        self.ui.scene = "round_info"
        self.ui.reset_time()
        while self.ui.scene == "round_info":
            self.ui.handle_events()
            self.ui.draw_round_info()
            pygame.display.flip()

        self.game.generate_questions()

        while self.game.used_questions < 16:
            self.select_question_session()
            q = self.game.current_question

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
        self.round = self.game.current_round
        
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
