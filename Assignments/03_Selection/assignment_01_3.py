import random

class Question:

    accepted_answers = ['ja', 'nein']

    def __init__(self, question, answer):
        self.__question = question
        self.__answer = answer

    @staticmethod
    def __valid_answer(answer):
        return str(answer).lower() in Question.accepted_answers

    def ask_question(self):
        valid_answer_pending = True

        while valid_answer_pending:
            user_input = input(self.__question + '\n')

            if not Question.__valid_answer(user_input):
                print('Bitte antworte nur mit (Ja / Nein)')
                continue

            return self.__check_answer(user_input)

        return None

    def __check_answer(self, answer):
        return str(answer).lower() == self.__answer.lower()


available_questions = [
    Question('Sind jemals Bienen im Weltall gewesen?', 'Ja'),
    Question('Ist die Flagge von Nepal rechteckig?', 'Nein'),
    Question('Gibt es einen Buchstaben im Alphabet der nicht im Periodensystem vorkommt?', 'Ja'),
    Question('Ist die Chinesische Mauer länger als die Distanz zwischen London und Peking?', 'Ja'),
    Question('Wird Kaffee aus Beeren hergestellt?', 'Ja')
]

asked_questions = 3
correct_questions = 0

selected_questions = random.sample(available_questions, asked_questions)

for question in selected_questions:
    if question.ask_question():
        correct_questions += 1

print('Ende! ' + str(correct_questions) + ' / ' + str(asked_questions) + ' korrekt beantwortet')