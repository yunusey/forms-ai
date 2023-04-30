from apiclient import discovery
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow


class Form:

    def __init__(self, file_type: str, file: str, discovery_doc: str,
                 scopes: list, form_id: [str, None] = None,
                 title: [str, None] = None, description: [str, None] = None):

        if file_type == 'client_secrets':
            flow = InstalledAppFlow. \
                from_client_secrets_file(file, scopes=scopes)
            self.credentials = flow.run_local_server(port=0)

        elif file_type == 'credentials':
            self.credentials = service_account.Credentials. \
                from_service_account_file(file, scopes=scopes)

        else:
            raise ValueError('Invalid file type for credentials.')

        self.form_service = discovery.build('forms', 'v1',
                                            credentials=self.credentials,
                                            discoveryServiceUrl=discovery_doc,
                                            static_discovery=False)

        self.form_id = form_id

        self.requests = []
        self.del_requests = []

        self.title = title
        self.description = description
        if self.form_id is None:
            self.create_form()
        self.modify_form(title=title, description=description)

    def add_question(self, question, index,
                     modify=False,
                     qtype="RADIO",
                     choices=[],
                     required=False
                     ):
        request = {
            "createItem": {
                "item": {
                    "title": question,
                    "questionItem": {
                        "question": {
                            "required": required,
                            "choiceQuestion": {
                                "type": qtype,
                                "options": self.create_choices(choices)
                            }
                        }
                    }
                },
                "location": {
                    "index": index
                }
            }
        }
        if modify:
            self.del_question(index)
        self.requests.append(request)

    def modify_form(self, title: str = None, description: str = None):
        request = {
            "updateFormInfo": {
                "info": {},
                "updateMask": ""
            }
        }
        if title:
            request['updateFormInfo']['info']['title'] = title
            request['updateFormInfo']['updateMask'] += 'title'
        if description:
            request['updateFormInfo']['info']['description'] = description
            request['updateFormInfo']['updateMask'] += \
                ',description' if request['updateFormInfo']['updateMask'] \
                else 'description'

        self.requests.append(request)

    def del_question(self, index):
        request = {
            "deleteItem": {
                "location": {
                    "index": index
                }
            }
        }
        self.del_requests.append(request)

    def create_choices(self, choices):
        nchoices = []
        for choice in choices:
            nchoices.append({'value': choice})

        return nchoices

    def create_form(self):

        title = self.title if self.title else 'Untitled Form'
        form = {
            "info": {
                "title": title,
            }
        }
        result = self.form_service.forms().create(body=form).execute()
        self.form_id = result['formId']

    def get_form(self):
        return self.form_service.forms().get(formId=self.form_id).execute()

    def clear_form(self):
        try:
            numq = len(self.get_form()['items'])
            for i in range(numq):
                self.del_question(i)
        except:
            """
            The form is just created. So does not contain any questions.
            """

    def request_updates(self):
        # When deleting questions, sort them in decreasing order.
        # The reason is that when deleted an element from the form,
        # the order of the questions will be changed. For example:
        # [Q1, Q2, Q3, Q4]
        # Let's delete Q3.
        # Now, let's try to delete Q4.
        # It will give an error: "The index is not valid"
        # Because the requests are done immediately.
        # This is why, we should start deleting from the end.
        self.del_requests.sort(
            key=lambda x: x['deleteItem']['location']['index'],
            reverse=True)

        if self.del_requests:
            self.form_service.forms(). \
                batchUpdate(formId=self.form_id,
                            body={'requests': self.del_requests}).execute()
        if self.requests:
            self.form_service.forms(). \
                batchUpdate(formId=self.form_id,
                            body={'requests': self.requests}).execute()

    def request(self, request):
        self.form_service.forms(). \
            batchUpdate(formId=self.form_id,
                        body={'requests': [request]}).execute()

    def get_link_to_form(self):
        return "https://docs.google.com/forms/d/{}".format(self.form_id)
