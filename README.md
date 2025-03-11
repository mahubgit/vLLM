TGI Model Manager with OpenWebUI

Solution intégrée combinant Text Generation Inference (TGI) avec une interface de gestion des modèles et OpenWebUI.

PRÉREQUIS
- Docker avec support NVIDIA
- Token Hugging Face (pour télécharger les modèles)
- NVIDIA GPU avec au moins 12GB de VRAM

ARCHITECTURE

.
├── docker-compose.yml      # Configuration des services
├── models/                 # Stockage persistant des modèles
│   └── .gitkeep
├── model-manager/         # Service de gestion des modèles
│   ├── Dockerfile
│   ├── requirements.txt   # Dépendances Python
│   └── app/
│       ├── main.py       # Application FastAPI
│       └── static/       # Interface utilisateur
│           └── index.html

SERVICES

Text Generation Inference (TGI)
- Port: 8081 
- API: http://localhost:8081/v1
- Rôle: Service d'inférence avec API compatible OpenAI
- Santé: http://localhost:8081/health
- Volume: ./models:/data/models (persistance des modèles)

Gestionnaire de Modèles
- Port: 8082
- URL: http://localhost:8082
- Rôle: Interface de gestion des modèles
- Fonctionnalités:
  * Liste des modèles disponibles
  * Téléchargement de nouveaux modèles
  * Chargement/déchargement des modèles
  * Suppression des modèles
  * Indication du modèle actif
- Volume: ./models:/models (accès aux modèles)

OpenWebUI
- Port: 8080
- URL: http://localhost:8080
- Rôle: Interface de chat

CONFIGURATION

Variables d'Environnement (.env):
- HF_TOKEN: Token Hugging Face pour le téléchargement des modèles

DÉMARRAGE

1. Créer le fichier .env:
   echo HF_TOKEN=votre_token > .env

2. Créer les dossiers nécessaires:
   mkdir models

3. Démarrer les services:
   docker-compose up -d

4. Accéder aux interfaces:
   - Gestion des modèles: http://localhost:8082
   - Interface de chat: http://localhost:8080

UTILISATION

1. Ouvrir l'interface de gestion (http://localhost:8082)
2. Télécharger un modèle en utilisant son ID Hugging Face
3. Charger le modèle souhaité
4. Utiliser l'interface de chat (http://localhost:8080)

Note: Le premier téléchargement de modèle peut prendre plusieurs minutes selon votre connexion internet.