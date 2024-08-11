import os
import nltk
import tkinter as tk
from src.chatbot.chatbot_ai import ChatbotAI
from src.chatbot.chatbot_ui import ChatbotGUI
from src.chatbot.dependancies import is_nltk_data_downloaded, is_spacy_model_downloaded


def gather_user_data():
    root = tk.Tk()
    chatbot_ai = ChatbotAI()
    ChatbotGUI(root, chatbot_ai)
    root.mainloop()
    user_data = chatbot_ai.user_data
    if not is_nltk_data_downloaded('vader_lexicon'):
        nltk.download('vader_lexicon')

    if not is_spacy_model_downloaded('en_core_web_sm'):
        os.system("python -m spacy download en_core_web_sm")

    name = user_data.get("name")
    age = int(user_data.get("age", 0))
    email = user_data.get("email")
    phone_number = user_data.get("phone_number")
    location = user_data.get("location")

    return name, age, email, phone_number, location
