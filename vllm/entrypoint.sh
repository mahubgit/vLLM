#!/bin/bash

# Start vLLM server with required arguments
exec python3 -m vllm.entrypoints.openai.api_server \
    --host "0.0.0.0" \
    --port 8000 \
    --trust-remote-code \
    --dtype auto