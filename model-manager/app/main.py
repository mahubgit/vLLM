from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os
from typing import List
import huggingface_hub

app = FastAPI()

MODELS_DIR = "/models"

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/models")
async def list_models():
    models = []
    for item in os.listdir(MODELS_DIR):
        if os.path.isdir(os.path.join(MODELS_DIR, item)):
            models.append({"name": item})
    return models

@app.post("/models/download/{model_id}")
async def download_model(model_id: str):
    try:
        huggingface_hub.snapshot_download(
            repo_id=model_id,
            local_dir=f"{MODELS_DIR}/{model_id}"
        )
        return {"status": "success", "message": f"Model {model_id} downloaded successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    model_path = os.path.join(MODELS_DIR, model_name)
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
        return {"status": "success", "message": f"Model {model_name} deleted successfully"}
    return {"status": "error", "message": "Model not found"}