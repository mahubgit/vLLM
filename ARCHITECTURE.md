vLLM Project Architecture
------------------------

Core Components:
1. Text Generation Inference (TGI)
   - GPU-optimized inference engine
   - Multi-GPU support with sharding
   - Dynamic model loading
   - REST API endpoint: 8081

2. Model Manager
   - Model lifecycle management
   - REST API endpoint: 8082
   - Static web interface
   - Model operations (download/load/delete)

3. OpenWebUI
   - Chat interface
   - Model interaction
   - Web endpoint: 8080

Data Flow:
User -> OpenWebUI -> TGI (inference)
User -> Model Manager -> TGI (model management)