import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Get OpenAI API key and base_url from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL")

MAX_HISTORY_LENGTH = 10

client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)


def user(user_message, history: list):
    return "", history + [{"role": "user", "content": user_message}]


def bot(history: list):
    history = history[len(history) - MAX_HISTORY_LENGTH:]
    response = client.chat.completions.create(
        model=model,
        messages=history,
        stream=True
    )
    history.append({"role": "assistant", "content": ""})
    for character in response:
        history[-1]['content'] += character.choices[0].delta.content
        yield history


def vote(data: gr.LikeData):
    if data.liked:
        print("liked this response: " + '|'.join(data.value))
    else:
        print("unliked this response: " + '|'.join(data.value))


with gr.Blocks() as demo:
    # Layout
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chatbot.like(vote, None, None)

    # Event handling
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()
