# Create a simple single player interface,,,,,,
#Haven't add the category interface
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
        self.bg_color = (175, 238, 238)
        self.text_color = (0, 139, 139)

        #start option on initial interface
        self.scene = "start"
        self.start_button = pygame.Rect(350, 300, 200, 80)

        #choose question options on choosing interface
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
                rect = pygame.Rect(x, y, box_weight, box_height)
                self.choices.append(rect)


        self.font = pygame.font.SysFont(None, 60)
        #time
        self.choose_time_limit = 5
        self.choose_start_ticks = 0
        



    def run(self):
        while self.running:
            self.handle_events()

            # draw differnt interface: initial interface, choose question interface, answering interface and caculating counts
            if self.scene == "start":
                self.draw_initial_interface()
            elif self.scene == "choose":
                self.draw_choose_question()
            elif self.scene == "question":
                self.draw_question_screen()
            pygame.display.flip()
            self.clock.tick(180) #trust your computer

        pygame.quit()
        sys.exit()



    def handle_events(self):
        for event in pygame.event.get():

            # close it by click 'X'
            if event.type == pygame.QUIT:
                self.running = False

            if self.scene == "choose" and self.get_choose_time_left() <= 0:
                print("time out")
                self.scene = "question"
                self.current_question_index = random.randint(0,15)
                print(self.current_question_index)
            # turn to choose question page by clicking start
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.scene == "start":
                    if self.start_button.collidepoint(event.pos):
                        self.scene = "choose"
                        self.choose_start_ticks = pygame.time.get_ticks()
            # choose questions by clicking the box
                elif self.scene == "choose":
                 for i, rect in enumerate(self.choices):
                    if rect.collidepoint(event.pos):
                        print("clicked question box:", i)
                        self.current_question_index = i
                        
                        ''' I edited here for connections with main.py - Yuri - '''
                        # Category and score settings (I set them with examples temporarily for now)
                        category = "General"
                        score = (i % 4 + 1) * 100
                        # Retrieving questions from API via game_logic
                        self.current_question = self.game.select_question(category, score, i)
                        ''' Edited to this point. delete here if it doesn't work well because of 'main.py' errors '''
                        
                        self.scene = "question"

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
        for i, rect in enumerate(self.choices):
            pygame.draw.rect(self.screen, (0, 139, 139), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
            score = [200, 400, 600, 1000]
            j = i%4
            text = self.font.render(f"${score[j]}", True, (255, 255, 255))
            
            self.screen.blit(text, (rect.x + 15, rect.y + 25))
            time_left = math.ceil(self.get_choose_time_left())
            time_text = self.font.render(f"Time: {time_left}", True, self.text_color)
            self.screen.blit(time_text, (650, 35))

    def draw_question_screen(self):
        self.screen.fill(self.bg_color)
        q = self.current_question

        question_text = self.font.render(q.ques, True, self.text_color)
        self.screen.blit(question_text, (80, 80))

        for i, option in enumerate(q.options):
            option_text = self.font.render(f"{i + 1}. {option}", True, self.text_color)
            self.screen.blit(option_text, (120, 180 + i * 80))


#test
#ui = Interface()
#ui.run()
