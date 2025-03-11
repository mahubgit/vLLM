TGI Model Manager with OpenWebUI

Solution intégrée combinant Text Generation Inference (TGI) avec une interface de gestion des modèles et OpenWebUI.

ARCHITECTURE

.
├── docker-compose.yml      # Configuration des services
├── models/                 # Stockage persistant des modèles
│   └── .gitkeep
├── model-manager/         # Service de gestion des modèles
│   ├── Dockerfile
│   ├── requirements.txt   # Dépendances Python
│   └── app/
│       └── main.py       # Application FastAPI

CARACTÉRISTIQUES

- Multi-GPU optimisé (2x RTX A5000)
- Chargement automatique des modèles existants
- Configuration optimisée pour les performances
- Interface de gestion des modèles
- Persistance des modèles

CONFIGURATION MATÉRIELLE RECOMMANDÉE
- 2x NVIDIA RTX A5000 (24GB chacune)
- 64GB+ RAM recommandé
- SSD pour le stockage des modèles

SERVICES

Text Generation Inference (TGI)
- Port: 8081 
- API: http://localhost:8081/v1
- Configuration optimisée:
  * Sharding sur 2 GPUs
  * Batch processing optimisé
  * Utilisation mémoire GPU: 95%
  * Requêtes concurrentes: 64

Gestionnaire de Modèles
- Port: 8082
- API Endpoints:
  * GET /models - Liste des modèles
  * POST /models/download/{model_id} - Téléchargement
  * DELETE /models/{model_name} - Suppression
  * POST /api/load-model/{model_name} - Chargement
  * GET /api/current-model - Modèle actif
  * GET /api/config - Configuration actuelle

OpenWebUI
- Port: 8080
- URL: http://localhost:8080

DÉMARRAGE

1. Configuration:
   echo HF_TOKEN=votre_token > .env

2. Démarrage:
   docker-compose up -d

3. Interfaces:
   - Gestion: http://localhost:8082
   - Chat: http://localhost:8080

PERFORMANCES

- Chargement rapide grâce au multi-GPU
- Modèles persistants entre redémarrages
- Démarrage automatique avec modèles existants
- Configuration optimisée pour les RTX A5000

Note: Le premier téléchargement d'un modèle peut prendre plusieurs minutes selon votre connexion internet.