import gradio as gr
from openai import OpenAI
import os
import time
import requests
from requests.exceptions import ConnectionError

client = OpenAI(
    api_key="not-needed",
    base_url=os.getenv("OPENAI_API_BASE", "http://vllm:8000/v1")
)

def wait_for_service(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(2)
    return False

def generate_response(message):
    try:
        # Check if vLLM is available
        if not wait_for_service(os.getenv("OPENAI_API_BASE", "http://vllm:8000/v1") + "/models"):
            return "Error: vLLM service is not available. Please make sure a model is loaded."

        completion = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": message}],
            timeout=30
        )
        return completion.choices[0].message.content
    except ConnectionError:
        return "Error: Cannot connect to vLLM service. Please ensure the service is running and a model is loaded."
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