import os

from forms import Form
from prompt import get_prompt, get_questions, get_title_and_description
from utils import colorful_print

# You should change these files with yours (see README.md)
CREDENTIALS_FILE = 'credentials.json'
CLIENT_SECRETS_FILE = 'client_secrets.json'
FILE = CLIENT_SECRETS_FILE

# You might replace with your Form ID if you want to reuse the same form
# If you want to create a new one, just keep this as None
FORM_ID = None

SCOPES = ['https://www.googleapis.com/auth/forms.body']
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# Some fun stuff :D
SHOW_HI_MESSAGE = True
HI_MESSAGE = """
👋 Hi there, thank you so much, for giving a try to this project!
🚀 For getting started, please take a look at `README.md`
📚 For learning more about forms please take a look at `forms.py`
💡 For learning more about prompts please take a look at `prompt.py`
🥴 There's not much to see about `utils.py`, but choice is yours

------------------------------QUICK START------------------------------
🔍 You need to create client_secrets.json file using Google Cloud Console.
   The instructions are given `README.md`.
   Once you've created this file;
   ✨ Set `CLIENT_SECRETS_FILE` to /path/to/client_secrets.json.
   ✨ Set `FILE` variable to `CLIENT_SECRETS_FILE` (if not set already!)
   ✨ Then, run `python main.py`
   ✨ Enjoy!
🔍 For updating a form instead of creating a new one:
   ✨ You need to set `FORM_ID` variable.
      To learn the form id, you need to check the link given to you:
      The link will have this format: https://docs.google.com/forms/d/{FORM_ID}
      You can just copy this id into your `FORM_ID` variable.
"""


def main():

    if SHOW_HI_MESSAGE:
        colorful_print(HI_MESSAGE, r=0, g=255, b=255)

    prompt = get_prompt()
    questions = get_questions(prompt)
    title, description = get_title_and_description(prompt)

    if not os.path.exists(FILE):
        colorful_print(
            "You need to create credentials.json and/or client_secrets.json\n"
            "For more information, see README.md!\n"
            "Once you've created either of them, change `file` accordingly.\n",
            "Aborting!",
            r=255, g=0, b=0
        )
        exit(1)

    if FILE == CLIENT_SECRETS_FILE:
        form = Form(file_type='client_secrets', file=FILE,
                    discovery_doc=DISCOVERY_DOC, scopes=SCOPES,
                    form_id=FORM_ID, title=title, description=description)
    else:
        form = Form(file_type='credentials', file=FILE,
                    discovery_doc=DISCOVERY_DOC, scopes=SCOPES,
                    form_id=FORM_ID, title=title, description=description)

    form.clear_form()

    for question in questions:
        form.add_question(question=question.question,
                          index=question.index,
                          qtype=question.qtype,
                          choices=question.choices)

    form.request_updates()
    colorful_print(
        "The link to the form can be found here: ",
        r=150, g=150, b=255
    )
    colorful_print(
        form.get_link_to_form() + "\n",
        r=255, g=150, b=150
    )


if __name__ == '__main__':
    main()
