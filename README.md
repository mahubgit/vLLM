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

SERVICES

Text Generation Inference (TGI)
- Port: 8081 
- API: http://localhost:8081/v1
- Rôle: Service d'inférence avec API compatible OpenAI
- Santé: http://localhost:8081/health

Gestionnaire de Modèles
- Port: 8082
- Rôle: Gestion du cycle de vie des modèles
- API:
  - Liste des modèles: GET http://localhost:8082/models
  - Téléchargement: POST http://localhost:8082/models/download/{model_id}
  - Suppression: DELETE http://localhost:8082/models/{model_name}

OpenWebUI
- Port: 8080
- URL: http://localhost:8080
- Rôle: Interface utilisateur web

EXEMPLES D'UTILISATION

Lister les Modèles:
curl http://localhost:8082/models

Télécharger un Modèle:
curl -X POST http://localhost:8082/models/download/mistralai/Mistral-7B-Instruct-v0.3

Supprimer un Modèle:
curl -X DELETE http://localhost:8082/models/mistralai/Mistral-7B-Instruct-v0.3

Tester l'API TGI:
curl http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.3",
    "messages": [{"role": "user", "content": "Bonjour!"}]
  }'

CONFIGURATION

Variables d'Environnement:
- HF_TOKEN: Token Hugging Face pour le téléchargement des modèles
- MODEL_PATH: Chemin de stockage des modèles (défaut: /models)
- TGI_HOST: URL du service TGI (défaut: http://tgi:80)

DÉMARRAGE

1. Configurer le token Hugging Face:
   echo HF_TOKEN=votre_token > .env

2. Démarrer les services:
   docker-compose up -d

3. Accéder à l'interface web: http://localhost:8080