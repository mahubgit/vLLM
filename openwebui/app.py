import gradio as gr
import openai
import os

openai.api_base = os.getenv("OPENAI_API_BASE", "http://vllm:8000/v1")
openai.api_key = os.getenv("OPENAI_API_KEY", "not-needed")

def generate_response(message):
    try:
        completion = openai.ChatCompletion.create(
            model="local-model",
            messages=[{"role": "user", "content": message}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your message here..."),
    outputs="text",
    title="vLLM Chat Interface",
    description="Chat with your local LLM model using vLLM"
)

interface.launch(server_name="0.0.0.0", server_port=8080)