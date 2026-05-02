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
        prompt = f"""
        Generate a Jeopardy question about '{category}' for ${score}.
        Follow these rules strictly:
        1. The answer must start with 'What is' or 'Who is'.
        2. Provide exactly 3 multiple-choice options (including the correct answer).
        3. Format your response exactly like this:
        Clue: [Question text]
        Answer: [Correct Answer]
        Options: [Option1, Option2, Option3]
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Jeopardy game host."},
                {"role": "user", "content": prompt}
            ]
        )
        
        raw_text = response.choices[0].message.content
        data = self._parse_response(raw_text)
        
        return Question(
            category=category,
            point=score,
            clue=data.get('clue'),
            answer=data.get('answer'),
            options=data.get('options')
        )

    def _parse_response(self, text):
        lines = text.strip().split('\n')
        data = {'clue': '', 'answer': '', 'options': []}
        
        for line in lines:
            line = line.strip()
            if line.startswith("Clue:"):
                data['clue'] = line.replace("Clue:", "").strip()
            elif line.startswith("Answer:"):
                data['answer'] = line.replace("Answer:", "").strip()
            elif line.startswith("Options:"):
                options_raw = line.replace("Options:", "").replace("[", "").replace("]", "").strip()
                data['options'] = [opt.strip() for opt in options_raw.split(',')]
        
        if data['answer'] and not (data['answer'].lower().startswith("what is") or data['answer'].lower().startswith("who is")):
            data['answer'] = "What is " + data['answer']
        return data
