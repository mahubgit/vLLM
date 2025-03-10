#!/bin/bash

# Start vLLM server with required arguments
exec python3 -m vllm.entrypoints.openai.api_server \
    --host "0.0.0.0" \
    --port 8000 \
    --model "/models/TinyLlama-1.1B-Chat-v1.0" \
    --trust-remote-code \
    --dtype auto