# forms-ai
Create forms automatically using ChatGPT.

## 🚀 Getting Started
For getting started using this project, you will need to create `client_secrets.json` file using Google Cloud Console:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project if you do not have one already.
3. Go to `Enabled APIs & Services` using the menu on the left.
4. Click on `ENABLE APIs AND SERVICES`.
5. Type Google Forms API in the search box.
6. Click `ENABLE`.
7. Go to `CREDENTIALS` using the menu on the left.
8. Click on `CREATE CREDENTIALS`, and choose `OAuth Client ID`.
9. You may need to configure your application first!
10. Choose `Desktop Application` as your application type, then click `Create`.
11. Go back to `Credentials` using the menu on the left.
12. You will see a client under OAuth 2.0 Client IDs. You need to click download button.
13. BINGO! You have your `client_secrets.json` file. (You may need to rename it and move it to your project folder.) You're good to go!

## 🤔 How do I use it?
Using this program is really simple:
1. You will need to install the requirements. To do so, run `pip install -r requirements.txt`.
2. Run `main.py` (`python3 main.py`)
3. Enter how many questions you want to have in your form.
4. Enter your description of the form.
5. Copy the output given from the program that will be asked to ChatGPT, manually.
6. Paste the response into the running program.
7. You need to authorize your application. Most probably, there will be an error message saying "Google hasn't verified this app.". You need to click to `Advanced` button, and then click to `Go to {YOUR_APP_NAME} (unsafe)` button. Note: Please make sure you are logged in with the correct Google account that you have created the project with, as the authorization will only apply to the account that you are currently logged in with.
8. Once the the authorization is done, the program will create/update your form.
9. When the program is done, you will be given the link to your form.

## 🐛 Bugs & Issues
If you encounter any bugs, please [open up an issue](https://github.com/yunusey/forms-ai/issues).

## 🤝 Contributions
Any contributions are welcome.

## 📌 TODO
- [ ] Use [OpenAI API](https://beta.openai.com/docs/api-reference/completions).
- [ ] Create user interface.

## 🌅 Closing Words
Thanks for using this program, please feel free to star the repo if you liked it! For questions, please open an issue.
