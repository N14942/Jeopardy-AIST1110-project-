# Create a simple single player interface,,,,,,
#Haven't add the count interface
import pygame
import sys
import math
import random
import os

class Button:
    def __init__(self, x, y, width, height, text, font, 
                 bg_color=(139, 69, 19), 
                 hover_color=(160, 82, 45),
                 text_color=(255, 255, 255),
                 action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
        #color
        self.base_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.used_bg = (200, 200, 200)
        self.used_text = (0, 0, 0)
        
        self.current_bg = bg_color
        self.is_answered = False
        self.action = action

    def draw(self, screen):
        if self.is_answered:
            self.current_bg = self.used_bg
            txt_color = self.used_text
        else:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.current_bg = self.hover_color
            else:
                self.current_bg = self.base_color
            txt_color = self.text_color

        pygame.draw.rect(screen, self.current_bg, self.rect)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 2) # 边框

        text_surf = self.font.render(self.text, True, txt_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if self.is_answered: 
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

class Interface:
    def __init__(self, game_logic=None, width=900, height=600, title="Jeopardy Game"):
        pygame.init()

        pygame.mixer.init()
        #music resource
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_path_1 = os.path.join(base_dir, "music", "humansandmonsterslivedtogetherinharmonymix.ogg")
        self.music_path_2 = os.path.join(base_dir, "music", "n-Dimensions (Main Theme).mp3")
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
        asset_dir = os.path.join(base_dir, "assets")
        self.button1_img = pygame.image.load(os.path.join(asset_dir, "button1.png")).convert_alpha()

        self.button2_img = pygame.image.load(os.path.join(asset_dir, "button2.png")).convert_alpha()
        self.button1_img = pygame.transform.scale(self.button1_img, (80, 80))
        self.button2_img = pygame.transform.scale(self.button2_img, (80, 80))

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

        self.used_button_bg = (200, 200, 200)   # 浅灰色
        self.used_button_text = (0, 0, 0)


        self.font = pygame.font.SysFont(None, 56)
        self.small_font = pygame.font.SysFont(None, 30)

        #start option on initial interface
        self.scene = "start"
        self.start_button = pygame.Rect(350, 300, 200, 80)

        #choose field or enter
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

        self.input_box = pygame.Rect(220, 420, 460, 60)
        self.input_text = ""
        self.input_active = False
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
        

    def create_choices(self):
        self.choices = []
        start_x = 30
        start_y =110
        box_width = 200
        box_height = 80
        gap = 10

        scores = [200, 400, 600, 1000]

        for col in range(4):
            for row in range(5):
                x = start_x + col * (box_width + gap)
                y = start_y + row * (box_height + gap)
                
                if row == 0:
                    text_content = self.fields[col]
                else:
                    text_content = f"${scores[row - 1]}"
                q_idx = col * 4 + (row - 1) if row > 0 else -1
                
                new_button = Button(x, y, box_width, box_height, 
                                    text_content, self.font, q_idx)
                
                self.choices.append(new_button)

    def reset_choosed_choice(self, index):
        for button in self.choices:
            if button.action_index == index:
                button.is_answered = True
                break

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
        self.scene = "round"
        self.round_start_ticks = pygame.time.get_ticks()
        self.update_music_by_round()

    def run(self):
        while self.running:
            self.handle_events()

            # draw differnt interface: initial interface, choose question interface, answering interface and caculating counts
            if self.scene == "start":
                self.draw_initial_interface()
            elif self.scene == "setting":
                self.setting_field()
            elif self.scene == "choose":
                  self.draw_choose_question()
            elif self.scene == "final_category":
                    self.draw_final_category()
            elif self.scene == "round":
                self.draw_round_info()
            elif self.scene == "buzz":
                self.draw_buzz()
            elif self.scene == "buzz_success":
                self.draw_buzz_success()
            elif self.scene == "question":
                self.draw_question_screen()
            elif self.scene == "count":
                self.draw_counting()
            pygame.display.flip()
            self.clock.tick(180) #trust your computer
            if self.scene == "buzz":
                self.update_buzz_scene()
            if self.scene == "buzz_success":
                elapsed = (pygame.time.get_ticks() - self.buzz_success_start_ticks) / 1000

                if elapsed >= self.buzz_success_duration:
                    self.current_button_img = self.button1_img
                    player = self.game.players[self.answering_player_index]
                    if hasattr(player, "start_thinking"):
                        player.start_thinking()
                    self.current_question.reset_time()
                    self.scene = "question"
            #check whether times out

            if self.scene == "round":
                elapsed = (pygame.time.get_ticks() - self.round_start_ticks) / 1000
                if elapsed >= self.round_limit:
                    if self.game.current_round == 3:
                        self.enter_final_category_scene()
                    else:
                        self.scene = "choose"
                        self.choose_start_ticks = pygame.time.get_ticks()
            if self.scene == "final_category":
                elapsed = (pygame.time.get_ticks() - self.final_category_start_ticks) / 1000
                if elapsed >= self.final_category_duration:
                    self.answering_player_index = 0
                    self.current_question.reset_time()
                    self.scene = "question"
            if self.scene == "choose" and self.get_choose_time_left() <= 0:
                print("time out")
                self.enter_round_scene()
                self.current_question_index = random.randint(4, 15)
                print(self.current_question_index)

            if self.scene == "draw_count":
                elapsed = (pygame.time.get_ticks() - self.result_start_ticks) / 1000
                if elapsed >= self.result_display_time:
                    self.enter_round_scene()



        pygame.quit()
        sys.exit()



    def handle_events(self):
        for event in pygame.event.get():

            # close it by click 'X'
            if event.type == pygame.QUIT:
                self.running = False

        

            # All Clicking action
            if event.type == pygame.MOUSEBUTTONDOWN:
                # turn to choose question page by clicking start
                if self.scene == "start":
                    if self.start_button.collidepoint(event.pos):
                        self.enter_round_scene()
                        
                # choose some specific fields
                elif self.scene == "setting":
                    for i, rect in enumerate(self.field_buttons):
                        if rect.collidepoint(event.pos):
                            self.selected_field = self.fields[i]
                            print("selected field:", self.selected_field)
                            self.scene = "start"
                            #self.choose_start_ticks = pygame.time.get_ticks()
                    self.input_active = self.input_box.collidepoint(event.pos)
                # choose questions by clicking the box
                elif self.scene == "choose":
                    for i, rect in enumerate(self.choices):
                        if rect.collidepoint(event.pos):
                            row = i % 5
                            col = i // 5

                            if row == 0:
                                print("This is category row, not a question.")
                                return
                            q_index = col * 4 + (row - 1)
                            print("clicked choice index:", i)
                            print("question index:", q_index)

                            self.current_question = self.game.all_question[q_index]
                            self.game.current_question = self.current_question
                            if self.current_question is None:
                                print("No valid question selected.")
                                return
                            self.enter_buzz_scene()

            # All typing action
            if event.type == pygame.KEYDOWN:
                if self.scene == "buzz" and self.game is not None and self.current_question is not None:
                    human = self.game.players[0]

                    if human.buzz and human.check_buzz(event):
                        if self.current_question.get_buzzing_time_left() > 0:
                            print("Human Player buzzed!")
                            self.current_button_img = self.button2_img
                            self.enter_buzz_success_scene(0)
                elif self.scene == "question" and self.game is not None and self.current_question is not None:
                    key_to_answer = {pygame.K_1: 0,pygame.K_2: 1,pygame.K_3: 2,pygame.K_4: 3,}

                    if event.key in key_to_answer:
                        answer_index = key_to_answer[event.key]

                        player = self.game.players[self.answering_player_index]
                        q = self.current_question
                        answered = player.get_answer(q, answer_index)
                        print(answered)
                        is_correct = player.update_score(q)
                        self.scene = "count"
                elif self.scene == "count":
                        if self.game is not None and self.current_question is not None:
                            self.game.reset_question_states()

                        self.current_question = None
                        self.answering_player_index = None
                        self.game.reset_board()
                        self.enter_round_scene()
                        #start next round
                elif self.scene == "field" and self.input_active:
                 if event.key == pygame.K_RETURN:
                    if self.input_text.strip() != "":
                        self.selected_field = self.input_text.strip()
                        print("typed field:", self.selected_field)
                        self.scene = "choose"
                        self.choose_start_ticks = pygame.time.get_ticks()

                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]

                else:
                    self.input_text += event.unicode
                if self.scene == "setting" and self.input_active:

                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip() != "":
                            self.selected_field = self.input_text.strip()
                            print("typed field:", self.selected_field)
                            self.scene = "choose"
                            self.choose_start_ticks = pygame.time.get_ticks()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    else:
                        self.input_text += event.unicode
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

    def setting_field(self):
        self.screen.fill(self.bg_color)
        title = self.font.render("Choose or Type Any Field you like !", True, self.text_color)
        self.screen.blit(title, (110, 60))

    
        for i, rect in enumerate(self.field_buttons):
            pygame.draw.rect(self.screen, self.button_bg, rect)
            pygame.draw.rect(self.screen, self.frame_color, rect, 3)
            text = self.font.render(self.fields[i], True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 25, rect.y + 18))

   
        box_color = (255, 255, 255) if self.input_active else (220, 220, 220)
        pygame.draw.rect(self.screen, box_color, self.input_box)
        pygame.draw.rect(self.screen, self.frame_color, self.input_box, 3)
        typed_text = self.font.render(self.input_text, True, self.text_color)
        self.screen.blit(typed_text, (self.input_box.x + 15, self.input_box.y + 15))
        hint_font = pygame.font.SysFont(None, 30)
        hint = hint_font.render("Click box -> Type a field -> Press Enter", True, self.text_color)
        self.screen.blit(hint, (220, 490))

    
    def draw_choose_question(self):
        self.screen.fill(self.bg_color)

        for button in self.choices:
            button.draw(self.screen)

        time_left = math.ceil(self.get_choose_time_left())
        time_text = self.font.render(f"Time: {time_left}", True, (0,0,0))
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
            self.screen.blit(question_text_2, (70, 50))
            self.screen.blit(question_text_3, (70, 80))
        for i, option in enumerate(q.options):
            option_text = self.font.render(f"{i + 1}. {option}", True, self.text_color)
            self.screen.blit(option_text, (120, 200 + i * 80))
    
    
    #all is buzz interface.....
    def enter_buzz_scene(self):
        if self.current_question is None:
            print("No current question. Cannot enter buzz scene.")
            return

        self.scene = "buzz"
        self.answering_player_index = None
        self.buzz_hint = "Press SPACE to buzz!"
        self.current_button_img = self.button1_img
        self.human_buzz_time = None

        self.current_question.reset_time()

        if self.game is not None:
            human = self.game.players[0]
            human.buzz_reset()
                
    def enter_buzz_success_scene(self, player_index):
        self.scene = "buzz_success"
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
        self.screen.fill((30, 30, 30))    
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
        hint_text = score_font.render("Press any key to continue...", True, (200, 200, 200))    
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
