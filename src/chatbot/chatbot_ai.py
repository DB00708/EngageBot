import html
import os
import re
import torch
import spacy
from groq import Groq
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()


class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = [{"entity": ent.text, "label": ent.label_} for ent in doc.ents]
        return entities

    def extract_phone_number(self, text):
        us_mob_no_regex = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$"
        indian_mob_no_regex = r"(\+91[\-\s]?)?[789]\d{9}"
        return bool(re.search(us_mob_no_regex, text)) or bool(re.search(indian_mob_no_regex, text))

    def extract_email(self, text):
        email_regex = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        return bool(re.search(email_regex, text))

    def extract_number(self, text):
        pattern = r'-?\d+(?:\.\d+)?'
        match = re.search(pattern, text)
        if match:
            return int(match.group())
        return None


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text):
        sentiment_scores = self.analyzer.polarity_scores(text)
        return sentiment_scores

    def get_sentiment(self, sentiment_scores):
        if sentiment_scores['compound'] >= 0.05:
            return "positive"
        elif sentiment_scores['compound'] <= -0.05:
            return "negative"
        else:
            return "neutral"

    def construct_prompt_based_on_sentiment(self, sentiment):
        if sentiment == "positive":
            return """
                You are a friendly and upbeat AI assistant. Celebrate the user's positivity and smoothly gather information like name, email, phone number, location, and age. Engage in light-hearted small talk and keep the conversation lively. Here's the conversation so far:
                """
        elif sentiment == "negative":
            return """
                You are a friendly and empathetic AI assistant. The user seems to be feeling down. Offer support and understanding, and gently guide the conversation to gather information like name, email, phone number, location, and age. If the user hesitates, show empathy and engage in comforting small talk. Here's the conversation so far:
                """
        else:
            return """
                You are a friendly and empathetic AI assistant. Your goal is to make the user comfortable and gather information like name, email, phone number, location, and age. Be empathetic, address concerns, and smoothly transition between topics. If the user hesitates, engage in small talk and return to data collection later. Here's the conversation so far:
                """


class ChatbotAI:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.user_data = {}
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.sentiment_analyzer = SentimentAnalyzer()
        self.nlp_processor = NLPProcessor()

    def sanitize_input(self, user_input):
        """
        Sanitizes user input to prevent prompt injection attacks.
        """
        # Escape any HTML or special characters
        sanitized_input = html.escape(user_input)

        # Remove or neutralize patterns that could manipulate the prompt
        sanitized_input = re.sub(r'(\b(?:system|bot|assistant|user|human|ai)\b\s*:\s*)', '', sanitized_input, flags=re.IGNORECASE)
        sanitized_input = re.sub(r'(--|\.\.|``)', '', sanitized_input)

        max_input_length = 512
        if len(sanitized_input) > max_input_length:
            sanitized_input = sanitized_input[:max_input_length]

        return sanitized_input

    def get_llm_response(self, user_input, chat_history):
        user_input = self.sanitize_input(user_input)
        sentiment_scores = self.sentiment_analyzer.analyze(user_input)
        sentiment = self.sentiment_analyzer.get_sentiment(sentiment_scores)
        prompt_based_on_sentiment = self.sentiment_analyzer.construct_prompt_based_on_sentiment(sentiment)
        conversation_history_summary = self.summarize_chat(chat_history)

        prompt = f"""{prompt_based_on_sentiment} {conversation_history_summary}.
        The user's current sentiment is {sentiment}.
        Human: {user_input}
        AI:"""

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        return response

    def summarize_chat(self, chat_history):
        full_conversation = "\n".join(
            [f"{'Human' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in chat_history])

        prompt = f"""
        Please provide a concise summary of the following conversation:

        {full_conversation}

        Summary:
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        summary = chat_completion.choices[0].message.content
        return summary

    def update_user_data(self, message):
        content = message["content"]
        if message["role"] == "user":
            email = self.nlp_processor.extract_email(content)
            phone_number = self.nlp_processor.extract_phone_number(content)

            if email:
                self.user_data["email"] = content
            if phone_number:
                self.user_data["phone_number"] = content

        if message["role"] == "assistant":
            entities = self.nlp_processor.extract_entities(content)
            for entity in entities:
                label = entity["label"]
                if label == "PERSON":
                    self.user_data["name"] = entity["entity"]
                if label == "GPE":
                    self.user_data["location"] = entity["entity"]
                if label in ["CARDINAL", "QUANTITY", "DATE"]:
                    text = entity["entity"]
                    age = self.nlp_processor.extract_number(text)
                    if age:
                        self.user_data["age"] = age
        return self.user_data
