# Create a simple single player interface,,,,,,
#Haven't add the round and count interface
import pygame
import sys
import math
import random

class Interface:
    def __init__(self, game_logic=None, width=900, height=600, title="Jeopardy Game"):
        pygame.init()
        self.game = game_logic
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # color
        self.bg_color = (251,226,162)
        self.text_color = (140,140,148)
        self.button_bg = (205,133,63)
        self.frame_color = (255,255,255)

        #start option on initial interface
        self.scene = "start"
        self.start_button = pygame.Rect(350, 300, 200, 80)

        # choose field or enter
        self.fields = ["Science", "Art", "2D culture", "Python"]
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

        # choose question options on choosing interface
        self.choices = []
        start_x = 100
        start_y = 120
        box_weight = 160
        box_height = 80
        gap = 20
        for i in range(4): 
            for j in range(4):
                x = start_x + i * (box_weight + gap)
                y = start_y + j * (box_height + gap)
                self.choices.append(pygame.Rect(x, y, box_weight, box_height))
        
        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)

        # time
        self.choose_time_limit = 10
        self.choose_start_ticks = 0
        self.current_data = None
        

    def run(self):
        while self.running:
            self.handle_events()

            # draw different interfaces: initial interface, choose question interface, answering interface, and calculating counts
            if self.scene == "start":
                self.draw_initial_interface()
            elif self.scene == "field":
                self.draw_choose_field()
            elif self.scene == "choose":
                #self.choose_start_ticks = pygame.time.get_ticks()
                self.draw_choose_question()
            elif self.scene == "round":
                self.draw_round_info()
            elif self.scene == "question":
                self.draw_question_screen()
            elif self.scene == "count":
                self.draw_counting()
            pygame.display.flip()
            self.clock.tick(180) # trust your computer 

            # check whether time out
            if self.scene == "choose" and self.get_choose_time_left() <= 0:
                print("TIME OUT")
                self.scene = "round"
                self.current_question_index = random.randint(0, 15)
                print(self.current_question_index)

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
                        self.scene = "field"
                        
                # choose some specific fields
                elif self.scene == "field":
                    for i, rect in enumerate(self.field_buttons):
                        if rect.collidepoint(event.pos):
                            self.selected_field = self.fields[i]
                            print("selected field:", self.selected_field)
                            self.scene = "choose"
                            self.choose_start_ticks = pygame.time.get_ticks()
                    self.input_active = self.input_box.collidepoint(event.pos)
                # choose questions by clicking the box
                elif self.scene == "choose":
                 for i, rect in enumerate(self.choices):
                    if rect.collidepoint(event.pos):
                        # print("clicked question box:", i)
                        # self.current_question_index = i
                        
''' I edited here again - Yuri - '''
                        # Category and score settings (I set them with examples temporarily for now)
                        category = self.selected_field
                        score_list = [200, 400, 600, 1000]
                        score = score_list[i % 4]
                        # Retrieving questions from API via game_logic
                        self.current_data = self.game.select_question(category, score, i)

                        if self.current_data:
                            self.current_data.reset_time()
                            self.scene = "question"
                            
''' Edited to this point. (in order to connect this with gameboard.py that I edited again) 
    Idk your specified purpose so if these codes do not suit your purpose,
    plz do not hesitate to edit or delete here.'''
                        
                        # self.scene = "round"

            # All typing action
            if event.type == pygame.KEYDOWN:
                if self.scene == "field" and self.input_active:
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
     
''' I added one more here (just a suggestion; feel free to use or delete this code) ''' 
                elif self.scene == "question": # scene "question": only recognize number keys
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        answer_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3}
                        user_choice = answer_map[event.key]
                            
                        is_correct = self.game.process_answer(0, user_choice)
                        print(f"Is it correct? {is_correct}!")

                        self.input_text = "" # Reset input_text
                        self.scene = "choose" # Return
                        self.choose_start_ticks = pygame.time.get_ticks() # Timer Reset

                
                
    def get_choose_time_left(self):
        current_ticks = pygame.time.get_ticks()
        elapsed = (current_ticks - self.choose_start_ticks) / 1000
        remaining = self.choose_time_limit - elapsed
        return max(0, remaining)

# different interfaces
    def draw_initial_interface(self):
        self.screen.fill(self.bg_color)

        text = self.font.render("Jeopardy Game!!!", True, self.text_color)
        self.screen.blit(text, (280, 250))
        button_text = self.font.render("START", True, (255, 255, 255))
        self.screen.blit(button_text, (385, 325))

    def draw_choose_field(self):
        self.screen.fill(self.bg_color)
        title = self.font.render("Choose or Type Any Field you like !", True, self.text_color)
        self.screen.blit(title, (110, 60))

    
        for i, rect in enumerate(self.field_buttons):
            pygame.draw.rect(self.screen, self.button_bg, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
            text = self.font.render(self.fields[i], True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 25, rect.y + 18))

   
        box_color = (255, 255, 255) if self.input_active else (220, 220, 220)
        pygame.draw.rect(self.screen, box_color, self.input_box)
        pygame.draw.rect(self.screen, self.text_color, self.input_box, 3)
        typed_text = self.font.render(self.input_text, True, self.text_color)
        self.screen.blit(typed_text, (self.input_box.x + 15, self.input_box.y + 15))
        hint_font = pygame.font.SysFont(None, 30)
        hint = hint_font.render("Click box -> Type a field -> Press Enter", True, self.text_color)
        self.screen.blit(hint, (220, 490))

    
    def draw_choose_question(self):
        self.screen.fill(self.bg_color)

''' Added scoreboard here '''
        if self.game and hasattr(self.game, 'players'):
            score_val = self.game.players[0].score
            score_display = self.font.render(f"Score: ${score_val}", True, (218, 165, 32))
            self.screen.blit(score_display, (20, 35))
        
        for i, rect in enumerate(self.choices):
            pygame.draw.rect(self.screen, self.button_bg, rect)
            pygame.draw.rect(self.screen, self.frame_color, rect, 3)
            score = [200, 400, 600, 1000]
            j = i%4
            text = self.font.render(f"${score[j]}", True, (255, 255, 255))
            
            self.screen.blit(text, (rect.x + 15, rect.y + 25))
            time_left = math.ceil(self.get_choose_time_left())
            time_text = self.font.render(f"Time: {time_left}", True, self.text_color)
            self.screen.blit(time_text, (650, 35))

    # def draw_round_info(self):


    def draw_question_screen(self):
        self.screen.fill(self.bg_color)

        if not self.current_data: # Escape without drawing if there is no data
            self.scene = "choose"
            return
        
        q = self.current_data

        question_font = pygame.font.SysFont(None, 30) # set font size to prevent long questions
        question_text = question_font.render(q.ques, True, self.text_color)
        self.screen.blit(question_text, (80, 80))

        for i, option in enumerate(q.options):
            option_text = self.font.render(f"{i + 1}. {option}", True, self.text_color)
            self.screen.blit(option_text, (120, 180 + i * 80))

        # timer
        rem_time = math.ceil(q.get_remaining_time())
        timer_text = self.font.render(f"Remaining: {rem_time}s", True, (200, 50, 50))
        self.screen.blit(timer_text, (600, 500))


    # def draw_count(self)


# test
# ui = Interface()
# ui.run()
