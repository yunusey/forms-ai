import re
from utils import colorful_print


def get_prompt() -> str:
    colorful_print("How many questions would you like to have in your form? ",
                   r=255, g=255, b=0)

    num_questions = int(input())
    colorful_print("Please enter your description for the form: ",
                   r=255, g=255, b=0)

    description = input()

    colorful_print("Please give the following text to ChatGPT:\n",
                   r=255, g=150, b=255)
    colorful_print(
        "------------------------------------------------------------------\n",
        r=150, g=255, b=150)

    prompt = (
        f"Hello ChatGPT, I want you to create a form for me: \n\n"
        f"You should start by giving the title and description of the form:\n"
        f"It should have this format:\n"
        f"[Info{{title={{title}}, description={{description}}]\n\n"
        f"The form should have {num_questions} questions."
        f"The questions should have this format: \n\n"
        f"[Question{{type=QTYPE}}]QUESTION_TEXT[END]{{CHOICES}}\n"
        f"* QTYPE can be 'RADIO' or 'CHECKBOX'\n"
        f"* QUESTION_TEXT is the text of the question\n"
        f"* CHOICES is a list of choices for the question and they should "
        f"be seperated by '|'. Such as: {{choice1|choice2|choice3}}\n"
        f"  Please note that there should be no blank lines between the "
        f"choices.\n"
        f"* When you wrote all the questions, you should write 'DONE'.\n\n"
        f"The description of the form is: {description}\n"
    )

    colorful_print(prompt, r=255, g=100, b=100)

    colorful_print(
        "------------------------------------------------------------------\n\n",
        r=150, g=255, b=150)

    answer = ""
    while "DONE" not in answer:
        answer += input() + '\n'

    return answer


class Question:
    def __init__(self, question, qtype, choices, index):
        self.question = question
        self.qtype = qtype
        self.choices = choices
        self.index = index

    def __str__(self):
        return "Question: {}, qtype: {}, choices: {}, index: {}". \
            format(self.question, self.qtype, self.choices, self.index)


def get_questions(prompt) -> list:
    pattern = r'\[Question\{type=(\w+)\}\](.*?)\[END\]\{(.+?)\}'
    matches = re.findall(pattern, prompt)

    questions, index = [], 0
    for match in matches:
        qtype = match[0]
        question = match[1]
        choices = match[2].split('|')
        questions.append(Question(question, qtype, choices, index))
        index += 1

    return questions


def get_title_and_description(prompt) -> (str, str):
    pattern = r'\[Info\{title=(.*?),.description=(.*?)\}\]'
    matches = re.findall(pattern, prompt)

    return matches[0][0], matches[0][1]
