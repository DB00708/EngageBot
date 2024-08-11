import tkinter as tk
from tkinter.ttk import Button, Entry
from tkinter import font, scrolledtext, Entry, Button


class ChatbotGUI:
    def __init__(self, root, chatbot_ai):
        self.root = root
        self.root.title("Chatbot")
        self.chat_history = []
        self.create_widgets()
        self.chatbot_ai = chatbot_ai

    def create_widgets(self):
        custom_font = font.Font(family="Roboto", size=12)
        self.root.config(bg="#1e1e1e")

        self.output_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=custom_font,
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            padx=10,
            pady=10
        )
        self.output_text.insert(tk.INSERT, "Chatbot: Hello! How can I help you today?\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=10)
        self.input_frame.pack(fill=tk.X)

        self.input_entry = Entry(
            self.input_frame,
            font=custom_font,
            width=50
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.handle_enter)
        self.input_entry.bind("<Shift-Return>", self.handle_shift_enter)

        self.send_button = Button(
            self.input_frame,
            text="Send",
            command=self.get_response,
            width=10
        )
        self.send_button.pack(side=tk.RIGHT)

    def handle_enter(self, event):
        self.get_response()
        return "break"

    def handle_shift_enter(self, event):
        self.input_entry.insert(tk.INSERT, "\n")
        return "break"

    def get_response(self):
        user_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if user_input:
            self.chat_history.append({"role": "user", "content": user_input})
            self.update_chat_history()

            response = self.chatbot_ai.get_llm_response(user_input, self.chat_history)
            self.chat_history.append({"role": "assistant", "content": response})
            self.update_chat_history()

    def update_chat_history(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        for message in self.chat_history:
            role = "You" if message["role"] == "user" else "Chatbot"
            self.output_text.insert(tk.END, f"{role}: {message['content']}\n\n")
            self.chatbot_ai.update_user_data(message)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)
