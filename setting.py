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

    def next_round(self, n: int):
        self.game.current_round == n
        self.round == n

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
            chooser = self.game.players[self.game.used_questions % self.game.player_number]
        else:
            chooser = self.game.ranking[-1]

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
            min_v = 5 
            max_v = int(player.score)
        else:
            max_board_value = self.game.get_max_board_value()
            max_v = int(max(player.score, max_board_value))

        if isinstance(player, AIPlayer):
            wager = player.do_wager(max_v, round=self.round)
        else:
            wager = self.ui.handle_events()

        if self.round != 3 and q.is_daily_double:
            q.reset_score(wager)
            
        return wager
    
    def question_answering_session(self, player: AIPlayer | HumanPlayer) -> bool:
        q = self.game.current_question
        if q.is_daily_double:
            self.get_wager_of_player(player, round_num=self.round)
        return self.get_answer_of_player()

    def non_final_jeopardy(self, n: int):
        self.game.reset_board()
        self.next_round(n)

        self.ui.scene = "round_info"
        self.ui.reset_time()
        while self.ui.scene == "round_info":
            self.ui.handle_events()
            self.ui.draw_round_info()
            pygame.display.flip()

        self.game.generate_questions()

        while self.game.used_questions < 16:
            self.select_question_session()
            
            while True:
                cur_player = self.buzz_session()
                if cur_player is None:
                    break

                cur_player = self.buzz_session()
                if self.question_answering_session(cur_player):
                    #interface
                    break
                else:
                    #interface
                    pass #pass 为占位符
            
            self.game.reset_question_states()
        
    def final_jeopardy(self):
        self.game.reset_board()
        self.next_round(3)
        eligible_players = [p for p in self.game.players if p.score > 0]
        if not eligible_players:
            #No people > 0 mark :)
            return
        
        self.game.generate_questions() 
        final_q = self.game.all_question[0]
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
        self.non_final_jeopardy(1)
        self.non_final_jeopardy(2)
        self.final_jeopardy()
        self.summary()
        
        
        



def main():
    game_logic = Gameboard()
    ui = Interface(game_logic)
    game_logic.generate_questions()
    game_logic.generate_aiplayers()

    # Run Main Loop
    ui.run() # Run Function 'run()' in 'interface.py'


if __name__ == "__main__":
    main()
