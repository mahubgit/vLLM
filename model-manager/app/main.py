from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
import os
import shutil
from huggingface_hub import snapshot_download
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Model Manager API")

# Environment variables with validation
MODEL_PATH = os.getenv("MODEL_PATH", "/models")
TGI_HOST = os.getenv("TGI_HOST", "http://tgi:80")
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    logger.warning("HF_TOKEN not set - model downloads may fail")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except Exception as e:
    logger.error(f"Failed to mount static files: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    try:
        return FileResponse("app/static/index.html")
    except Exception as e:
        logger.error(f"Failed to serve index.html: {e}")
        raise HTTPException(status_code=500, detail="Failed to load UI")

@app.get("/api/current-model")
async def get_current_model():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TGI_HOST}/v1/models")
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="TGI service timeout")
    except Exception as e:
        logger.error(f"Error getting current model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-model/{model_name}")
async def load_model(model_name: str):
    try:
        model_path = Path(MODEL_PATH) / model_name
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="Model not found")

        # Add after environment variables
        TGI_CONFIG = {
            "sharded": True,
            "num_shard": 2,
            "max_batch_prefill_tokens": 2048,
            "max_batch_total_tokens": 12288,
            "max_concurrent_requests": 64,
            "cuda_memory_fraction": 0.95
        }

        async def _load_model_with_config(model_id: str, client: httpx.AsyncClient):
            config = {"model_id": model_id, **TGI_CONFIG}
            return await client.post(f"{TGI_HOST}/reload", json=config)

        # Then update all model loading calls to use this function
        # For example in load_model():
        async with httpx.AsyncClient(timeout=60.0) as client:
            await _load_model_with_config(model_name, client)
        return {"status": "success", "message": f"Model {model_name} loaded"}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="TGI service timeout")
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    try:
        models_dir = Path(MODEL_PATH)
        if not models_dir.exists():
            logger.warning(f"Models directory {MODEL_PATH} does not exist")
            return []
        return [d.name for d in models_dir.iterdir() if d.is_dir()]
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/download/{model_id}")
async def download_model(model_id: str):
    try:
        if not HF_TOKEN:
            raise HTTPException(status_code=401, detail="HF_TOKEN not configured")

        model_path = Path(MODEL_PATH) / model_id
        if model_path.exists():
            raise HTTPException(status_code=409, detail="Model already exists")

        snapshot_download(
            repo_id=model_id,
            local_dir=model_path,
            token=HF_TOKEN
        )
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(f"{TGI_HOST}/reload", json={"model_id": model_id})
        return {"status": "success", "message": f"Model {model_id} downloaded"}
    except Exception as e:
        logger.error(f"Error downloading model {model_id}: {e}")
        if model_path.exists():
            shutil.rmtree(model_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    try:
        # Check if model is currently loaded
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TGI_HOST}/v1/models")
            current_model = response.json().get("model", "")
            if current_model == model_name:
                raise HTTPException(
                    status_code=400, 
                    detail="Cannot delete currently loaded model"
                )

        model_path = Path(MODEL_PATH) / model_name
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="Model not found")
            
        shutil.rmtree(model_path)
        return {"status": "success", "message": f"Model {model_name} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add after environment variables
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

@app.on_event("startup")
async def startup_event():
    try:
        # Check for existing models
        models_dir = Path(MODEL_PATH)
        if not models_dir.exists():
            models_dir.mkdir(parents=True)
            
        existing_models = [d.name for d in models_dir.iterdir() if d.is_dir()]
        
        if existing_models:
            # Load first available model
            model_to_load = existing_models[0]
            logger.info(f"Loading existing model: {model_to_load}")
            async with httpx.AsyncClient(timeout=60.0) as client:
                await client.post(f"{TGI_HOST}/reload", json={
                    "model_id": model_to_load,
                    "sharded": True,
                    "num_shard": 2,
                    "max_batch_prefill_tokens": 2048,
                    "max_batch_total_tokens": 12288,
                    "max_concurrent_requests": 64,
                    "cuda_memory_fraction": 0.95
                })
        else:
            # Download default model if no models exist
            logger.info(f"No models found. Downloading default model: {DEFAULT_MODEL}")
            model_path = Path(MODEL_PATH) / DEFAULT_MODEL
            snapshot_download(
                repo_id=DEFAULT_MODEL,
                local_dir=model_path,
                token=HF_TOKEN
            )
            # Load the default model
            async with httpx.AsyncClient(timeout=60.0) as client:
                await client.post(f"{TGI_HOST}/reload", json={
                    "model_id": DEFAULT_MODEL,
                    "sharded": True,
                    "num_shard": 2,
                    "max_batch_prefill_tokens": 2048,
                    "max_batch_total_tokens": 12288,
                    "max_concurrent_requests": 64,
                    "cuda_memory_fraction": 0.95
                })
    except Exception as e:
        logger.error(f"Startup error: {e}")

@app.get("/api/config")
async def get_config():
    return {
        "tgi_config": TGI_CONFIG,
        "default_model": DEFAULT_MODEL,
        "model_path": MODEL_PATH
    }