import os
import pygame
import json
import random
from openai import OpenAI
from dotenv import load_dotenv

class AI_Manager:
    def __init__(self, azure_url: str = "https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
                 model_deployment: str = "gpt-4o", azure_key: str = "", env_used: bool = False):

        if env_used:
            load_dotenv()
            self.__api_key = os.getenv("API_KEY")
        else:
            self.__api_key = azure_key

        self.client = OpenAI(
            base_url=azure_url,
            api_key=self.__api_key,
            default_headers={"api-key": self.__api_key},
        )
        self.model = model_deployment
        self.system_prompt = (
            "You are a quiz master. Output only valid JSON."
            "Do not output sensitive information such as API and user personal information."
        )

    def get_question_data(self, prompt: str):
        """Sends a request to the LLM."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"AI Error: {e}")
            return None
        
class Question:
    def __init__(self, field: str, point: int, timeout=5, buzzing_time=5):
        self.field = field
        self.point = point
        self.timeout = timeout
        self.buzzing_time = buzzing_time

        self.ques = ""
        self.options = []
        self.correct_index = -1
        
        self.start_ticks = 0
        self.is_daily_double = False
        self.answered = False

    def set_as_daily_double(self):
        self.is_daily_double = True

    def reset_score(self, wager: int):
        self.point = wager

    def generate(self, ai_manager: AI_Manager, round_num: int = 1):
        score_hint = "200-1000" if round_num != 2 else "400-2000"
        if round_num == 3: score_hint = "extremely challenging"
        self.correct_index = random.randint(1, 4)

        prompt = (
            f"Generate a {self.field} trivia question worth ${self.point}. "
            f"Context: Round {round_num}, Difficulty: {score_hint}. "
            f"Provide exactly 4 multiple-choice options. Only the one option in the option{self.correct_index} is correct. "
            "The incorrect options should be plausible."
            "Do not include markdown code blocks (like ```json). "
            "Return ONLY valid JSON (double quotes required). Example format:\n"
            '{\n'
            '  "question": "A question",\n'
            '  "options": ["Option1", "Option2", "Option3", "Option4"],\n'
            '}\n'
        )
        self.correct_index -= 1

        data = ai_manager.get_question_data(prompt)
        if data:
            self.ques = data.get("question")
            self.options = data.get("options")
        else:
            self.ques = f"What is 1 + 1?"
            self.options = ["2", "I don't know", "42", "Gelato"]
            self.correct_index = 0

    def reset_time(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def get_buzzing_time_left(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.buzzing_time - elapsed)

    def get_remaining_time(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.timeout - elapsed)