#!/bin/bash
python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL_PATH \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size $GPU_COUNT