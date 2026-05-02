import os
import pygame
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY") 

class Question:
    def __init__(self, category, point, clue="", answer="", options=None):
        self.category = category
        self.point = point
        self.clue = clue
        self.answer = answer
        self.options = options if options else []
        self.timeout = 5
        self.buzzing_time = 5
        self.start_ticks = 0

    def reset_time(self):
        self.start_ticks = pygame.time.get_ticks()

    def get_remaining_time(self) -> float:
        current_ticks = pygame.time.get_ticks()
        elapsed_time = (current_ticks - self.start_ticks) / 1000
        return max(0, self.timeout - elapsed_time)

class QuestionManager:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
            api_key=AZURE_API_KEY,
            default_headers={"api-key": AZURE_API_KEY},
        )

    def fetch_question(self, category, score):
        data = self._parse_response(raw_text)
        return Question(
            category=category,
            point=score,
            clue=data.get('clue'),
            answer=data.get('answer'),
            options=data.get('options')
        )

    def _parse_response(self, text):
        # ... (유리가 짠 파싱 로직) ...
        return data
