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
        
        #color
        self.bg_color = (251,226,162)
        self.text_color = (140,140,148)
        self.button_bg = (163,111,90)
        self.frame_color = (217,179,140)

        self.font = pygame.font.SysFont(None, 56)
        self.small_font = pygame.font.SysFont(None, 30)

        #start option on initial interface
        self.scene = "start"
        self.start_button = pygame.Rect(350, 300, 200, 80)

        #choose field or enter
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

        self.create_choices()
        #time
        self.choose_time_limit = 5
        self.choose_start_ticks = 0
        

    def create_choices(self):
        self.choices = []
        start_x = 30
        start_y =110
        box_width = 200
        box_height = 80
        gap = 10

        for row in range(5):
            for col in range(4):
                x = start_x + col * (box_width + gap)
                y = start_y + row * (box_height + gap)
                rect = pygame.Rect(x, y, box_width, box_height)
                self.choices.append(rect)

    def run(self):
        while self.running:
            self.handle_events()

            # draw differnt interface: initial interface, choose question interface, answering interface and caculating counts
            if self.scene == "start":
                self.draw_initial_interface()
            elif self.scene == "setting":
                self.setting_field()
            elif self.scene == "choose":
                #self.choose_start_ticks = pygame.time.get_ticks()
                self.draw_choose_question()
            elif self.scene == "round":
                self.draw_round_info()
            elif self.scene == "buzz":
                self.dra_buzz()
            elif self.scene == "question":
                self.draw_question_screen()
            elif self.scene == "count":
                self.draw_counting
            pygame.display.flip()
            self.clock.tick(180) #trust your computer

            #check whether times out
            if self.scene == "choose" and self.get_choose_time_left() <= 0:
                print("time out")
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
                        self.scene = "choose"
                        self.choose_start_ticks = pygame.time.get_ticks()
                        
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
                        print("clicked question box:", i)
                        self.current_question_index = i
                        
                        ''' I edited here for connections with main.py - Yuri - '''
                        # Category and score settings (I set them with examples temporarily for now)
                        #category = "General"
                        #score = (i % 4 + 1) * 100
                        # Retrieving questions from API via game_logic
                        self.current_data = self.game.select_question(w, score, i)
                        ''' Edited to this point. delete here if it doesn't work well because of 'main.py' errors '''
                        
                        self.scene = "round"

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

        scores = [200, 400, 600, 1000]

        for index, rect in enumerate(self.choices):
            row = index // 4
            col = index % 4

            pygame.draw.rect(self.screen, self.button_bg, rect)
            pygame.draw.rect(self.screen, self.frame_color, rect, 3)

            if row == 0:
                text_content = self.fields[col]
            else:
                text_content = f"${scores[row - 1]}"

            text = self.font.render(text_content, True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 5, rect.y + 25))

        time_left = math.ceil(self.get_choose_time_left())
        time_text = self.font.render(f"Time: {time_left}", True, self.text_color)
        self.screen.blit(time_text, (650, 35))

    #def draw_round_info(self):


    #def draw_buzz(self)

    def draw_question_screen(self):
        self.screen.fill(self.bg_color)
        q = self.current_question

        question_text = self.font.render(q.ques, True, self.text_color)
        self.screen.blit(question_text, (80, 80))

        for i, option in enumerate(q.options):
            option_text = self.font.render(f"{i + 1}. {option}", True, self.text_color)
            self.screen.blit(option_text, (120, 180 + i * 80))
    
    #def draw_count(self)


#test
#ui = Interface()
#ui.run()
