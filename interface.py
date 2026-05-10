import pygame
import sys
import math
import random
import os
from enum import Enum

class Scene(Enum):
    START = "start"
    ROUND = "round"
    CHOOSE = "choose"
    BUZZ = "buzz"
    BUZZ_SUCCESS = "buzz_success"
    QUESTION = "question"
    COUNT = "count"
    FINAL_CATEGORY = "final_category"

class Interface:
    def __init__(self, game_logic=None, width=900, height=600, title="Jeopardy Game"):
        pygame.init()
        pygame.mixer.init()

        #music resource
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.asset_music()
        self.current_music_path = None
        self.game = game_logic
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.human_buzz_time = None

        # buzz button
        self.asset_button()
        self.current_button_img = self.button1_img

        self.current_question = None
        self.answering_player_index = None
        self.buzz_hint = "Press SPACE to buzz!"
        self.buzz_success_start_ticks = 0
        self.buzz_success_duration = 2
        self.buzz_success_message = ""

        #color
        self.bg_color = (141,166,210)
        self.text_color = (249,215,124)
        self.button_bg = (163,111,90)
        self.frame_color = (217,179,140)
        self.used_color_button_bg = (192,192,192)
        self.used_color_button_frame = (128,128,128)
        self.used_text = (96,96,96)
        
        #text
        self.font = pygame.font.SysFont(None, 56)
        self.small_font = pygame.font.SysFont(None, 30)

        #start option on initial interface
        self.scene = Scene.START
        self.start_button = pygame.Rect(350, 300, 200, 80)

        #choose field
        self.creat_field_choice()
        self.selected_field = None
        self.create_choices()

        #time
        self.round_limit = 2
        self.round_start_ticks = 0
        self.choose_time_limit = 5
        self.choose_start_ticks = 0
        self.final_category_start_ticks = 0
        self.final_category_duration = 2
        self.play_music(self.music_path_1)
        


#assets
    def create_choices(self):
        self.choices = []
        start_x = 30
        start_y =110
        box_width = 200
        box_height = 80
        gap = 10
        for col in range(4):
            for row in range(5):
                x = start_x + col * (box_width + gap)
                y = start_y + row * (box_height + gap)
                rect = pygame.Rect(x, y, box_width, box_height)
                self.choices.append(rect)

    def creat_field_choice(self):
        self.fields = self.game.categories if self.game is not None else ["Science", "History", "Art", "Culture"]
        self.field_buttons = []
        start_x = 150
        start_y = 150
        button_w = 255
        button_h = 70
        gap = 50
        for i in range (len(self.fields)):
            x = start_x + (i % 2) * (button_w + gap)
            y = start_y + (i // 2) * (button_h + gap)
            self.field_buttons.append(pygame.Rect(x, y, button_w, button_h))

    def asset_button(self):
        asset_dir = os.path.join(self.base_dir, "assets")
        self.button1_img = pygame.image.load(os.path.join(asset_dir, "button1.png")).convert_alpha()

        self.button2_img = pygame.image.load(os.path.join(asset_dir, "button2.png")).convert_alpha()
        self.button1_img = pygame.transform.scale(self.button1_img, (80, 80))
        self.button2_img = pygame.transform.scale(self.button2_img, (80, 80))
    
    def asset_music(self):
        self.music_path_1 = os.path.join(self.base_dir, "music", "humansandmonsterslivedtogetherinharmonymix.ogg")
        self.music_path_2 = os.path.join(self.base_dir, "music", "n-Dimensions (Main Theme).mp3")



#Music!
    def play_music(self, music_path):
        if self.current_music_path == music_path:
            return
        self.current_music_path = music_path
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def update_music_by_round(self):
        current_round = self.game.current_round if self.game is not None else 1

        if current_round == 3:
            self.play_music(self.music_path_2)
        else:
            self.play_music(self.music_path_1)

    def enter_round_scene(self):
        self.scene = Scene.ROUND
        self.round_start_ticks = pygame.time.get_ticks()
        self.update_music_by_round()

    def enter_final_category_scene(self):
        if self.game is None:
            print("No game object.")
            return

        if self.game.current_round != 3:
            return

        if self.game.current_question is None:
            if len(self.game.all_question) == 0:
                self.game.generate_questions()
            self.game.current_question = self.game.all_question[0]

        self.current_question = self.game.current_question
        self.scene = Scene.FINAL_CATEGORY
        self.final_category_start_ticks = pygame.time.get_ticks()





#Run
    def run(self):
        while self.running:
            self.handle_events()
            # draw differnt interface: initial interface, choose question interface, answering interface and caculating counts
            self.draw()
            pygame.display.flip()
            self.clock.tick(180) #trust your computer
            self.update()
        pygame.quit()
        sys.exit()

    def draw(self):
        if self.scene == Scene.START:
            self.draw_initial_interface()
        elif self.scene == Scene.CHOOSE:
            self.draw_choose_question()
        elif self.scene == Scene.FINAL_CATEGORY:
            self.draw_final_category()
        elif self.scene == Scene.ROUND:
            self.draw_round_info()
        elif self.scene == Scene.BUZZ:
            self.draw_buzz()
        elif self.scene ==Scene.BUZZ_SUCCESS:
            self.draw_buzz_success()
        elif self.scene == Scene.QUESTION:
            self.draw_question_screen()
        elif self.scene == Scene.COUNT:
            self.draw_counting()
    
    def update(self):
        if self.scene == Scene.BUZZ:
                self.update_buzz_scene()
        if self.scene == Scene.BUZZ_SUCCESS:
            elapsed = (pygame.time.get_ticks() - self.buzz_success_start_ticks) / 1000

            if elapsed >= self.buzz_success_duration:
                self.current_button_img = self.button1_img
                player = self.game.players[self.answering_player_index]
                if hasattr(player, "start_thinking"):
                    player.start_thinking()
                self.current_question.reset_time()
                self.scene = Scene.QUESTION
            #check whether times out

        if self.scene == Scene.ROUND:
            elapsed = (pygame.time.get_ticks() - self.round_start_ticks) / 1000
            if elapsed >= self.round_limit:
                if self.game.current_round == 3:
                    self.enter_final_category_scene()
                else:
                    self.scene = Scene.CHOOSE
                    self.choose_start_ticks = pygame.time.get_ticks()
        if self.scene == Scene.FINAL_CATEGORY:
            elapsed = (pygame.time.get_ticks() - self.final_category_start_ticks) / 1000
            if elapsed >= self.final_category_duration:
                self.answering_player_index = 0
                self.current_question.reset_time()
                self.scene = Scene.QUESTION
        if self.scene == "choose" and self.get_choose_time_left() <= 0:
            print("time out")
            valid_index = [i for i, q in enumerate(self.game.all_question) if q is not None and not q.answered]
            q_index = random.choice(valid_index)
            self.current_question_index = q_index
            self.current_question = self.game.all_question[q_index]
            self.game.current_question = self.current_question
            self.enter_buzz_scene()


#Events
    def handle_events(self):
        for event in pygame.event.get():
            # close it by click 'X'
            if event.type == pygame.QUIT:
                self.running = False
            # All Clicking action
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
                
            # All typing action
            if event.type == pygame.KEYDOWN:
                  self.handle_key_down(event)


    def handle_mouse_down(self,event):
        if self.scene == Scene.START:
            self.handle_start_click(event)
        elif self.scene == Scene.CHOOSE:
            self.handle_choose_click(event)
    
    def handle_key_down(self, event):
        if self.scene == Scene.BUZZ:
            self.handle_buzz_key(event)
        elif self.scene == Scene.QUESTION:
            self.handle_answer_key(event)
        elif self.scene == Scene.COUNT:
            self.handle_count_key(event)

    def handle_start_click(self,event):
        if self.start_button.collidepoint(event.pos):
            self.enter_round_scene()
    
    def handle_choose_click(self,event):
        if self.game is None:
            print("No game object.")
            return
        for i, rect in enumerate(self.choices):
            if rect.collidepoint(event.pos):
                row = i % 5
                col = i // 5

                if row == 0:
                    #print("This is category row")
                    return
                q_index = col * 4 + (row - 1)
                print("clicked choice index:", i)
                print("question index:", q_index)
                self.current_question = self.game.all_question[q_index]
                self.game.current_question = self.current_question

                if self.current_question is None:
                    print("No valid question selected.")
                    return

                if self.current_question.answered:
                    print("This question has already been answered.")
                    return

                self.enter_buzz_scene()
    
    def handle_buzz_key(self,event):
        if self.game is None or self.current_question is None:
            return
        human = self.game.players[0]

        if human.buzz and human.check_buzz(event):
            if self.current_question.get_buzzing_time_left() > 0:
                print("Human Player buzzed!")
                self.current_button_img = self.button2_img
                self.enter_buzz_success_scene(0)
    
    def handle_answer_key(self,event):
        if self.game is None or self.current_question is None:
            return

        if self.answering_player_index is None:
            print("No answering player.")
            return

        key_to_answer = {pygame.K_1: 0,pygame.K_2: 1,pygame.K_3: 2,pygame.K_4: 3,}

        if event.key not in key_to_answer:
            return

        answer_index = key_to_answer[event.key]

        player = self.game.players[self.answering_player_index]
        q = self.current_question

        answered = player.get_answer(q, answer_index)
        print("answered:", answered)

        if answered:
            is_correct = player.update_score(q)

            if is_correct:
                print("Correct!")
            else:
                print("Wrong!")

            print("player choice:", player.current_choice)
            print("correct index:", q.correct_index)
            print("current score:", player.score)

        self.scene = Scene.COUNT
    

    def handle_count_key(self,event):
        if self.game is None:
            return

        if self.current_question is not None:
            self.game.reset_question_states()

        self.current_question = None
        self.answering_player_index = None
        self.game.current_question = None
        self.game.next_round()

        if self.game.current_round > 3:
            print("Game finished.")
            self.running = False
        else:
            self.enter_round_scene()

                        

                
#timing function
    def get_choose_time_left(self):
        current_ticks = pygame.time.get_ticks()
        elapsed = (current_ticks - self.choose_start_ticks) / 1000
        remaining = self.choose_time_limit - elapsed
        return max(0, remaining)

#different interfaces
    def draw_initial_interface(self):
        self.screen.fill(self.bg_color)

        text = self.font.render("Jeopardy Game!!!", True, self.text_color)
        self.screen.blit(text, (280, 250))
        button_text = self.font.render("START", True, (255, 255, 255))
        self.screen.blit(button_text, (385, 325))


    
    def draw_choose_question(self):
        self.screen.fill(self.bg_color)

        scores = [200, 400, 600, 1000]

        for index, rect in enumerate(self.choices):
            row = index % 5
            col = index // 5
            box_bg_color=self.button_bg
            text_frame_color=self.frame_color 
            text_color = (255,255,255)
            if row == 0:
                text_content = self.fields[col]
            else:
                q_index = col * 4 + (row - 1)
                text_content = f"${scores[row - 1]}"
                if (self.game is not None and 0 <= q_index < len(self.game.all_question) and self.game.all_question[q_index].answered ):
                    box_bg_color = self.used_color_button_bg
                    text_frame_color = self.used_color_button_frame
                    text_color = self.used_text
                    text_content = "Answered"


            pygame.draw.rect(self.screen, box_bg_color, rect)
            pygame.draw.rect(self.screen, text_frame_color, rect, 3)
            text = self.font.render(text_content, True, text_color)
            self.screen.blit(text, (rect.x + 5, rect.y + 25))

        time_left = math.ceil(self.get_choose_time_left())
        time_text = self.font.render(f"Time: {time_left}", True, self.text_color)
        self.screen.blit(time_text, (650, 35))

    def draw_round_info(self):
        self.screen.fill(self.bg_color)
        current_round = self.game.current_round
        
        if current_round == 1:
            title_text = "Jeopardy Round"
            subtitle_text = "1 Daily Double is hidden!"
        elif current_round == 2:
            title_text = "Double Jeopardy Round"
            subtitle_text = "2 Daily Doubles are hidden!"
        elif current_round == 3:
            title_text = "Final Jeopardy"
            subtitle_text = "Final question!"

        title = self.font.render(title_text, True, self.button_bg)
        title_rect = title.get_rect(center=(self.width // 2, 240))
        self.screen.blit(title, title_rect)

        small_font = pygame.font.SysFont(None, 36)
        subtitle = small_font.render(subtitle_text, True, self.button_bg)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 320))
        self.screen.blit(subtitle, subtitle_rect)

    def draw_question_screen(self):
        self.screen.fill(self.bg_color)
        q = self.current_question
        #print(q.ques)
        question = q.ques
        question = question.split()
        #print(question)
        if len(question)<=11:
         fir = ' '.join(question[0:5])
         sec = ' '.join(question[5:11])
         question_text_1 = self.font.render(fir, True, self.text_color)
         question_text_2 = self.font.render(sec, True, self.text_color)
         self.screen.blit(question_text_1, (70, 50))
         self.screen.blit(question_text_2, (70, 100))
        else:
            fir = ' '.join(question[0:5])
            sec = ' '.join(question[5:11])
            thir = ' '.join(question[11:])
            question_text_1 = self.font.render(fir, True, self.text_color)
            question_text_2 = self.font.render(sec, True, self.text_color)
            question_text_3 = self.font.render(thir, True, self.text_color)
            self.screen.blit(question_text_1, (70, 20))
            self.screen.blit(question_text_2, (70, 60))
            self.screen.blit(question_text_3, (70, 100))
        for i, option in enumerate(q.options):
            option_text = self.font.render(f"{i + 1}. {option}", True, self.text_color)
            self.screen.blit(option_text, (120, 200 + i * 80))
    
    
    #all is buzz interface.....
    def enter_buzz_scene(self):
        if self.current_question is None:
            print("No current question. Cannot enter buzz scene.")
            return

        self.scene = Scene.BUZZ
        self.answering_player_index = None
        self.buzz_hint = "Press SPACE to buzz!"
        self.current_button_img = self.button1_img
        self.human_buzz_time = None

        self.current_question.reset_time()

        if self.game is not None:
            human = self.game.players[0]
            human.buzz_reset()
                
    def enter_buzz_success_scene(self, player_index):
        self.scene = Scene.BUZZ_SUCCESS
        self.answering_player_index = player_index
        self.buzz_success_start_ticks = pygame.time.get_ticks()

        player = self.game.players[player_index]
        self.buzz_success_message = f"{player.name} buzzed!"
        self.current_button_img = self.button2_img
        
    def update_buzz_scene(self):
        if self.current_question is None:
            return

        q = self.current_question

        if q.get_buzzing_time_left() <= 0:
            print("Buzz time out!")
            self.buzz_hint = "No one buzzed!"
            self.enter_round_scene()
            return
        
    def draw_buzz(self):
        self.screen.fill(self.bg_color)

        q = self.current_question

        # category + score
        title = self.font.render(f"{q.field} for ${q.point}", True, self.button_bg)
        title_rect = title.get_rect(center=(self.width // 2, 65))
        self.screen.blit(title, title_rect)

        # question
        question_text = self.small_font.render(q.ques, True, self.text_color)
        question_rect = question_text.get_rect(center=(self.width // 2, 135))
        self.screen.blit(question_text, question_rect)

    # hint
        hint = self.font.render(self.buzz_hint, True, self.button_bg)
        hint_rect = hint.get_rect(center=(self.width // 2, 215))
        self.screen.blit(hint, hint_rect)

    # button image
        button_rect = self.current_button_img.get_rect(center=(self.width // 2, 305))
        self.screen.blit(self.current_button_img, button_rect)

    # buzz countdown
        time_left = math.ceil(q.get_buzzing_time_left())
        time_text = self.font.render(f"Buzz Time: {time_left}", True, self.button_bg)
        time_rect = time_text.get_rect(center=(self.width // 2, 420))
        self.screen.blit(time_text, time_rect)

    # progress bar
        bar_x = 250
        bar_y = 460
        bar_w = 400
        bar_h = 25

        pygame.draw.rect(self.screen, self.frame_color, (bar_x, bar_y, bar_w, bar_h), 3)

        ratio = q.get_buzzing_time_left() / q.buzzing_time
        fill_w = int(bar_w * ratio)
        pygame.draw.rect(self.screen, self.button_bg, (bar_x, bar_y, fill_w, bar_h))

    #after buzz
    def draw_buzz_success(self):
        self.screen.fill(self.bg_color)
        title = self.font.render(self.buzz_success_message, True, self.button_bg)
        title_rect = title.get_rect(center=(self.width // 2, 160))
        self.screen.blit(title, title_rect)
        button_rect = self.current_button_img.get_rect(center=(self.width // 2, 300))
        self.screen.blit(self.current_button_img, button_rect)

        hint = self.small_font.render("Get ready to answer...", True, self.text_color)
        hint_rect = hint.get_rect(center=(self.width // 2, 420))
        self.screen.blit(hint, hint_rect)

    def draw_counting(self):  
        self.screen.fill(self.bg_color)   
        title_font = pygame.font.SysFont("malgungothic", 50, bold=True)    
        score_font = pygame.font.SysFont("malgungothic", 30)        
        title_text = title_font.render("--- Current Score Status ---", True, (255, 255, 255))    
        title_rect = title_text.get_rect(center=(self.width // 2, 80))    
        self.screen.blit(title_text, title_rect)    
        for i, player in enumerate(self.game.players):        
            y_pos = 180 + i * 80                
            name_text = score_font.render(f"{player.name}", True, (255, 255, 255))        
            self.screen.blit(name_text, (100, y_pos))                
            bar_x = 250        
            bar_max_width = 400        
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, y_pos, bar_max_width, 30))                
            score_ratio = min(max(player.score, 0) / 2000, 1.0)        
            bar_color = (0, 150, 255) if player.score >= 0 else (255, 50, 50)        
            current_bar_width = int(bar_max_width * score_ratio)                
            pygame.draw.rect(self.screen, bar_color, (bar_x, y_pos, current_bar_width, 30))                
            val_text = score_font.render(f"${player.score}", True, bar_color)        
            self.screen.blit(val_text, (bar_x + bar_max_width + 20, y_pos))    
        hint_text = score_font.render("Press SPACE to continue...", True, (200, 200, 200))    
        hint_rect = hint_text.get_rect(center=(self.width // 2, self.height - 100))    
        self.screen.blit(hint_text, hint_rect)

    def draw_final_category(self):
        self.screen.fill(self.bg_color)

        title = self.font.render("Final Jeopardy Category", True, self.button_bg)
        title_rect = title.get_rect(center=(self.width // 2, 180))
        self.screen.blit(title, title_rect)

        category = self.font.render(self.current_question.field, True, self.text_color)
        category_rect = category.get_rect(center=(self.width // 2, 280))
        self.screen.blit(category, category_rect)

        hint = self.small_font.render("Get ready for the final question...", True, self.text_color)
        hint_rect = hint.get_rect(center=(self.width // 2, 380))
        self.screen.blit(hint, hint_rect)

    def draw_summary(self):
        self.screen.fill((20, 20, 40)) # 深色背景

        all_players = self.ranking
        if not all_players: return

        score_groups = []
        if all_players:
            current_group = [all_players[0]]
            for p in all_players[1:]:
                if p.score == current_group[0].score:
                    current_group.append(p)
                else:
                    score_groups.append(current_group)
                    current_group = [p]
            score_groups.append(current_group)

        margin = 50
        available_width = self.width - 2 * margin
        podium_base_y = self.height - 80
        single_width = available_width // len(all_players)
        current_x = margin + (available_width - len(all_players) * single_width) // 2
        
        rank_colors = [
            (255, 215, 0),
            (192, 192, 192),
            (205, 127, 50),
            (100, 100, 150)
        ]

        total_drawn_count = 0
        for rank_idx, group in enumerate(score_groups):
            actual_rank = total_drawn_count + 1
            h = max(100, 300 - rank_idx * 60) 
            color = rank_colors[rank_idx] if rank_idx < 3 else rank_colors[-1]

            for player in group:
                podium_rect = pygame.Rect(current_x + 5, podium_base_y - h, single_width - 10, h)
                pygame.draw.rect(self.screen, color, podium_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), podium_rect, 2) # 白色边框

                rank_text = self.font.render(self.get_rank_suffix(actual_rank), True, (255, 255, 255))
                rank_rect = rank_text.get_rect(center=(podium_rect.centerx, podium_rect.bottom - 30))
                self.screen.blit(rank_text, rank_rect)

                name_font = pygame.font.SysFont("Arial", 24, bold=True)
                name_text = name_font.render(player.name, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(podium_rect.centerx, podium_rect.top - 40))
                self.screen.blit(name_text, name_rect)

                score_text = self.font.render(f"${player.score}", True, color)
                score_rect = score_text.get_rect(center=(podium_rect.centerx, podium_rect.top - 15))
                self.screen.blit(score_text, score_rect)

                current_x += single_width
            
            total_drawn_count += len(group)

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title_text = title_font.render("FINAL STANDINGS", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width//2 - title_text.get_width()//2, 30))

