import os
import pygame
import json
from dotenv import load_dotenv
from openai import OpenAI
import random

class AI_Environment:
    def __init__(self, azure_url: str = "https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
                 model_deployment: str = "gpt-5.1", azure_key: str = "", env_used: bool = False):

        if env_used:
            load_dotenv()
            self.__api_key = os.getenv("API_KEY")
            assert self.__api_key is not None
        else:
            self.__api_key = azure_key

        self.client = OpenAI(
            base_url=azure_url,
            api_key=self.__api_key,
            default_headers={"api-key": self.__api_key},
        )
        self.model = model_deployment
        self.system_prompt = "You are a quiz master. Output only valid JSON. Do not output sensitive information such as API and user personal information."

    def fetch_ai_completion(self, user_prompt: str):
        """
        Sends a request to the LLM and enforces JSON object response format.
       
        """
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
    def __init__(self, field: str, point: int, timeout = 5):
        self.field = field
        self.score = point
        self.ques = ""
        self.options = [1, 2, 3, 4]
        self.answer = 0
        self.timeout = timeout

        self.is_answered = False
        self.start_ticks = 0

    def generate_question(self, ai_env: AI_Environment):
        prompt = (
            f"Generate a {self.field} question worth {self.score} points/(Point range: 200-1000). "
            "Provide 4 options. Return JSON: {'question': str, 'options': list, 'answer': int}"
        )

        try:
            response = ai_env.fetch_ai_completion(prompt)
            data = json.loads(response.choices[0].message.content)

            self.ques = data["question"]
            self.options = data["options"]
            self.answer = data["answer"]
            
            if self.answer not in self.options:
                self.options[random.randint(0, 3)] = self.answer
            random.shuffle(self.options)

        except Exception as e:
            print(f"Error generating question: {e}")
            self.ques = "Default: What is Python?"
            self.options = ["Language", "Snake", "Both", "None"]
            self.answer = "Both"

    def check_answer(self, user_answer: str) -> bool:
        return user_answer == self.answer
    
    def get_remaining_time(self) -> float:
        current_ticks = pygame.time.get_ticks()
        elapsed_time = (current_ticks - self.start_ticks) / 1000
        remaining = self.timeout - elapsed_time
        return max(0, remaining)