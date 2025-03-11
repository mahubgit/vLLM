from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import httpx
import os
import shutil
from huggingface_hub import snapshot_download
from pathlib import Path

app = FastAPI()
MODEL_PATH = os.getenv("MODEL_PATH", "/models")
TGI_HOST = os.getenv("TGI_HOST", "http://tgi:80")
HF_TOKEN = os.getenv("HF_TOKEN")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.get("/api/current-model")
async def get_current_model():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TGI_HOST}/v1/models")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-model/{model_name}")
async def load_model(model_name: str):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{TGI_HOST}/reload", json={"model_id": model_name})
        return {"status": "success", "message": f"Model {model_name} loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    models_dir = Path(MODEL_PATH)
    return [d.name for d in models_dir.iterdir() if d.is_dir()]

@app.post("/models/download/{model_id}")
async def download_model(model_id: str):
    try:
        model_path = Path(MODEL_PATH) / model_id
        snapshot_download(
            repo_id=model_id,
            local_dir=model_path,
            token=HF_TOKEN
        )
        # Reload TGI with new model
        async with httpx.AsyncClient() as client:
            await client.post(f"{TGI_HOST}/reload", json={"model_id": model_id})
        return {"status": "success", "message": f"Model {model_id} downloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    try:
        model_path = Path(MODEL_PATH) / model_name
        if model_path.exists():
            shutil.rmtree(model_path)
            return {"status": "success", "message": f"Model {model_name} deleted"}
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))