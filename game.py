from class import HumanPlayer, AIPlayer  # Alex의 클래스 불러오기

''' question generator '''

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")  # KEY Need to be entered
 
class QuestionManager:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://cuhk-apip.azure-api.net/openai-eus2/openai/v1",
            api_key=AZURE_API_KEY,
            default_headers={"api-key": AZURE_API_KEY},
        )

    def fetch_question(self, category, difficulty):
        prompt = f"""
        Generate a Jeopardy question about '{category}' for ${difficulty}.
        Follow these rules strictly:
        1. The answer must start with 'What is' or 'Who is'.
        2. Provide 3 multiple-choice options (including the correct answer).
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
        return self._parse_response(raw_text)

    def _parse_response(self, text):
        lines = text.strip().split('\n')
        data = {}
        for line in lines:
            if line.startswith("Clue:"):
                data['clue'] = line.replace("Clue:", "").strip()
            elif line.startswith("Answer:"):
                data['answer'] = line.replace("Answer:", "").strip()
            elif line.startswith("Options:"):
                options_text = line.replace("Options:", "").replace("[", "").replace("]", "").strip()
                data['options'] = [opt.strip() for opt in options_text.split(',')]
        
        if 'answer' in data and not (data['answer'].startswith("What is") or data['answer'].startswith("Who is")):
            data['answer'] = "What is " + data['answer']
            
        return data

qm = QuestionManager()
question_data = qm.fetch_question("Python", 200)
print(question_data['clue'])
print(question_data['answer'])

''' game '''

class JeopardyGame:
    def __init__(self, question_manager):
        self.qm = question_manager
        self.players = [
            HumanPlayer("Player", "player_img.png"), # yet image names are just for example / delete if not needed
            AIPlayer("AI_1", "ai1_img.png"),
            AIPlayer("AI_2", "ai2_img.png")
        ]
        self.current_round = 1
        
    def load_question(self, category, score):
        # 유리가 만든 fetch_question 사용!
        data = self.qm.fetch_question(category, score)
        return data
