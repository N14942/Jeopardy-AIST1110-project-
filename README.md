# Jeopardy-AIST1110-project-
This is a Jeopardy (AIST1110-project).
Reminder: 
1, Do not directly coding on the main branch, create new branch for adding functions/ debug.
2, If you use AI, please make the annotation and coding style less AI-like.
3, To get a good score, please make the structure clear. \

Sturcture design(current, you can edit if you have other ideas):
1, Player: Store information and activity of ai and human players.
2, Question: Give out ai-generated questions and answers.
3, Gameboard: Run the game (Round, question selection...).
4, interface: visualization / player operation -> gameboard.

Question-snawering logic:
1, Question promped: question + 4 options
2, Players(human and AI) buzzing in-->one get opportunity to answer, other wait for he/she/it to answer.
3, Answered corrctly->update score, show the answer, next question.
4(Harder), Answered wromgly->update score, shower the wrong answer made, give hint->step 2 (Who answered wrongly in this question cannot join the buzzing round).
4(Easier), Answered wromgly->update score, shower the correct answer, next question.