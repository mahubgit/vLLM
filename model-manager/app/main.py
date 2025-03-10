from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import huggingface_hub
import requests
import json

app = FastAPI(
    title="Model Manager API",
    description="API for managing LLM models"
)

MODELS_DIR = "/models"
TGI_HOST = os.getenv("TGI_HOST", "http://tgi:8000")

templates = Jinja2Templates(directory="templates")

@app.get("/models/current")
async def get_current_model():
    try:
        response = requests.get(f"{TGI_HOST}/info")
        if response.status_code == 200:
            data = response.json()
            return {"status": "success", "model": {"name": data.get("model_id", "Unknown")}}
        return {"status": "error", "model": None}
    except Exception as e:
        return {"status": "error", "model": None, "message": str(e)}

@app.post("/models/initialize/{model_name}")
async def initialize_model(model_name: str):
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Load model using TGI's API
        response = requests.post(
            f"{TGI_HOST}/model/load",
            json={"model_id": model_path}
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": f"Model {model_name} loaded successfully"}
        else:
            return {"status": "error", "message": f"Failed to load model: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}