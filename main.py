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
    if data.liked == '':
        print(f"cancel vote this response: index:{data.index}, content:{'|'.join(data.value)}")
    elif data.liked:
        print(f"liked this response: index:{data.index}, content:{'|'.join(data.value)}")
    else:
        print(f"unliked this response: index:{data.index}, content:{'|'.join(data.value)}")


with gr.Blocks() as demo:
    # Layout
    gr.Markdown("<h1 style='text-align: center;'>AI Chat</h1>")
    chatbot = gr.Chatbot(type="messages")
    chatbot.like(vote, None, None)
    msg = gr.Textbox(label="User:")
    with gr.Row():
        submitBtn = gr.Button("Submit" , elem_id="submit_btn")
        clearBtn = gr.Button("Clear")

    # Event handling
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    submitBtn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clearBtn.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.css = """
    #submit_btn {
        background-color: #FFCC99; /* 设置背景颜色为指定的浅橙色 */
        color: red; /* 设置文本颜色为橙色 */
        border-radius: 10px; /* 可选：设置圆角 */
        padding: 10px 20px; /* 可选：设置内边距 */
    }
    """
    demo.launch()
