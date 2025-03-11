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
- Health: http://localhost:8081/health
- Configuration optimisée:
  * Sharding sur 2 GPUs
  * Batch processing optimisé
  * Utilisation mémoire GPU: 95%
  * Requêtes concurrentes: 64

Gestionnaire de Modèles
- Port: 8082
- URL: http://localhost:8082
- Health: http://localhost:8082/health
- API Endpoints:
  * GET http://localhost:8082/models - Liste des modèles
  * POST http://localhost:8082/models/download/{model_id} - Téléchargement
  * DELETE http://localhost:8082/models/{model_name} - Suppression
  * POST http://localhost:8082/api/load-model/{model_name} - Chargement
  * GET http://localhost:8082/api/current-model - Modèle actif
  * GET http://localhost:8082/api/config - Configuration actuelle

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

TROUBLESHOOTING

1. Service Health Checks:
   - TGI: http://localhost:8081/health
   - Model Manager: http://localhost:8082/health
   - OpenWebUI: http://localhost:8080

2. View Logs:
   docker-compose logs -f

3. Common Issues:
   - If model-manager shows wrong port, check PORT environment variable
   - If TGI shows "Unknown compute for card", this is normal for RTX A5000
   - First model load may take several minutes