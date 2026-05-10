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
            "You are a JEOPARDY quiz master. Output only valid JSON."
            "Do not output sensitive information such as API and user personal information."
        )

    def get_question_data(self, field: str, round: int = 1):
        """Sends a request to the LLM."""
        if round ==3:
            self.correct_index = random.randint(1, 4)

            prompt = (
            f"Generate a {field} trivia really challenging question. "
            f"Context: Round {round}, Difficulty: challenging. "
            f"Provide exactly 4 multiple-choice options. Only the one option in the option{self.correct_index} is correct. "
            "The incorrect options should be plausible."
            "Do not include markdown code blocks (like ```json). "
            "Return ONLY valid JSON (double quotes required). Example format for one question, generate 4 question object:\n"
            '{\n'
            '  "question": "A question",\n'
            '  "options": ["Option1", "Option2", "Option3", "Option4"],\n'
            '}\n'
        )
            
        else:
            score_hint = "200, 400, 600, 1000" if round != 2 else "400, 800, 1200, 2000"
            prompt = (
            f"Generate four {field} trivia questions worth {score_hint}. "
            "Requirements:\n"
            "1. Each question must have exactly 4 multiple-choice options.\n"
            "2. For each question, specify the correct answer index n, n should be created randomly, in range 0-3:\n"
            "n=0: first option is correct. n=1:second option is correct, etc."
            "3. The incorrect options should be plausible.\n"
            "4. Return ONLY valid JSON in this format, do not include markdown code blocks:\n"
            "{\n"
            "  \"questions\": [\n"
            "    {\"question\": \"Q1\", \"options\": [\"Option1\", \"Option2\", \"Option3\", \"Option4\"], \"answer\": n},\n"
            "    {\"question\": \"Q2\", \"options\": [\"Option1\", \"Option2\", \"Option3\", \"Option4\"], \"answer\": n},\n"
            "    {\"question\": \"Q3\", \"options\": [\"Option1\", \"Option2\", \"Option3\", \"Option4\"], \"answer\": n},\n"
            "    {\"question\": \"Q4\", \"options\": [\"Option1\", \"Option2\", \"Option3\", \"Option4\"], \"answer\": n}\n"
            "  ]\n"
            "}"
            )
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
            result = json.loads(response.choices[0].message.content)
        
            if round == 3:
                return result
            else:
                return result.get("questions", [])
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

    def update_ques_info(self, data: dict):
        self.ques = data.get("question")
        self.options = data.get("options")
        self.correct_index = data.get("answer")

    def reset_time(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def get_buzzing_time_left(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.buzzing_time - elapsed)

    def get_remaining_time(self) -> float:
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        return max(0, self.timeout - elapsed)