from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from typing import List
import huggingface_hub
import requests

app = FastAPI(
    title="Model Manager API",
    description="API for managing LLM models",
    version="1.0.0"
)

MODELS_DIR = "/models"
VLLM_HOST = "http://vllm:8000"

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Only mount static files if directory exists
if os.path.exists("static"):
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

@app.post("/models/initialize/{model_name}")
async def initialize_model(model_name: str):
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Stop the current vLLM instance
        requests.post(f"{VLLM_HOST}/v1/models/stop")
        
        # Start vLLM with the new model
        response = requests.post(
            f"{VLLM_HOST}/v1/models/start",
            json={
                "name": model_name,
                "model": model_path,
                "tensor_parallel_size": 2
            }
        )
        
        if response.status_code == 200:
            return {"status": "success", "message": f"Model {model_name} initialized"}
        else:
            return {"status": "error", "message": f"Failed to initialize model: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/models/download-and-initialize/{org_name}/{model_name}")
async def download_and_initialize_with_org(org_name: str, model_name: str):
    try:
        model_id = f"{org_name}/{model_name}"
        # Download the model
        huggingface_hub.snapshot_download(
            repo_id=model_id,
            local_dir=f"{MODELS_DIR}/{model_name}",  # Use only model_name for local storage
            token=os.getenv("HF_TOKEN")
        )
        
        # Initialize the model
        result = await initialize_model(model_name)  # Pass only model_name
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Keep the original endpoint for models without organization
@app.get("/models/download-and-initialize/{model_id}")
async def download_and_initialize(model_id: str):
    try:
        # Download the model
        huggingface_hub.snapshot_download(
            repo_id=model_id,
            local_dir=f"{MODELS_DIR}/{model_id}",
            token=os.getenv("HF_TOKEN")
        )
        
        # Initialize the model
        result = await initialize_model(model_id)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    model_path = os.path.join(MODELS_DIR, model_name)
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
        return {"status": "success", "message": f"Model {model_name} deleted successfully"}
    return {"status": "error", "message": "Model not found"}