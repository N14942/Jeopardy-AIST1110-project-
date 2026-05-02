import os
import pygame
import json
import random
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

class Question:
    def __init__(self, field, point, timeout=5, buzzing_time=5):
        self.field = field
        self.point = point
        self.ques = ""
        self.options = []
        self.answer = -1
        self.timeout = timeout
        self.buzzing_time = buzzing_time
        self.start_ticks = 0
        self.is_daily_double = False

    def set_as_daily_double(self):
        self.is_daily_double = True

    def reset_score(self, wager: int):
        self.point = wager

    def generate(self, round_num=1):
        api_key = os.getenv("AZURE_API_KEY")
        
        client = OpenAI(
            base_url="https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
            api_key=api_key,
            default_headers={"api-key": api_key},
        )

        score_hint = "200-1000" if round_num != 2 else "400-2000"
        if round_num == 3: score_hint = "challenging"

        prompt = f"""
        Generate a {self.field} question worth ${self.point}.
        Context: Round {round_num}, Difficulty: {score_hint}.
        Provide exactly 4 multiple-choice options. Only one is correct.
        Return ONLY valid JSON:
        {{
            "question": "text",
            "options": ["A", "B", "C", "D"],
            "correct_answer_index": 0
        }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a Jeopardy quiz master. Output ONLY JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            
            data = json.loads(response.choices[0].message.content)
            self.ques = data["question"]
            self.options = data["options"]
            self.answer = int(data["correct_answer_index"])
            
        except Exception as e:
            print(f"API error: {e}")
            self.ques = f"What is 1 + 1? (Error fallback for {self.field})"
            self.options = ["2", "3", "4", "5"]
            self.answer = 0    
            
    

    def reset_time(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def get_buzzing_time_left(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.buzzing_time - elapsed)

    def get_remaining_time(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.timeout - elapsed)
