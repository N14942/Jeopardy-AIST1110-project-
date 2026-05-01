import os
import pygame
import json
from openai import OpenAI

class AI_Environment:
    def __init__(self, azure_url: str = "https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
                 model_deployment: str = "gpt-4o", azure_key: str = "", env_used: bool = False):

        if env_used:
            from dotenv import load_dotenv
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

    def fetch_ai_completion(self, user_prompt: str):
        """Sends a request to the LLM."""

        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )

class Question:
    def __init__(self, field: str, point: int, timeout = 5, buzzing_time = 5):
        self.field = field
        self.point = point
        self.ques = ""
        self.options = []
        self.answer = -1
        self.timeout = timeout
        self.buzzing_time = buzzing_time

        self.is_answered = False
        self.start_ticks = 0

    def generate_question(self, ai: AI_Environment):
        prompt = (
            f"Generate a {self.field} trivia question worth {self.point}."
             "(Score range:200(easy)-1000(difficult)). "
            "Provide exactly 4 options, only one of them is correct."
             "Return JSON in the format: "
            "{'question': str, 'options': list, 'correct_answer_index': int} "
            "The correct_answer_index must be 0, 1, 2, or 3, corresponding to the index of correct answer in the list."
        )

        try:
            response = ai.fetch_ai_completion(prompt)
            data = json.loads(response.choices[0].message.content)

            self.ques = data["question"]
            self.options = data["options"]
            self.answer = int(data["correct_answer_index"])
            
        except Exception as e:
            print(f"Error: {e}")
            self.ques = "1+1=?"
            self.options = ["2", "I don't know.", "42", "obtuse angle"]
            self.answer = 0

    def reset_time(self):
        self.start_ticks = pygame.time.get_ticks()
    
    def get_buzzing_time_left(self) -> float:
        current_ticks = pygame.time.get_ticks()
        elapsed_time = (current_ticks - self.start_ticks) / 1000
        remaining = self.buzzing_time - elapsed_time
        return max(0, remaining)

    def get_remaining_time(self) -> float:
        current_ticks = pygame.time.get_ticks()
        elapsed_time = (current_ticks - self.start_ticks) / 1000
        remaining = self.timeout - elapsed_time
        return max(0, remaining)