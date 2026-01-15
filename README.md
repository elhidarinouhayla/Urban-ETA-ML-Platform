# Urban-ETA-ML-Platform


Smart LogiTrack est une solution complète de type "Control Tower" logistique. L'objectif est de prédire le temps d'arrivée (Estimated Time of Arrival - ETA) des taxis urbains en utilisant un pipeline de données distribué et du Machine Learning.


## Objectifs du ProjetPipeline 

- ETL Distribué : Traitement de gros volumes de données avec PySpark

- Stockage Structuré : Ingestion des données brutes (Bronze) vers des données nettoyées (Silver) dans PostgreSQL

- Machine Learning : Entraînement d'un modèle Random Forest performant 

- API de Service : Service de prédiction temps réel via FastAPI sécurisé par JWT

- Orchestration : Automatisation du workflow avec Apache Airflow



## Structure du Projet

Basé sur l'architecture modulaire visible dans l'explorateur :

```
 URBAN-ETA-ML-PLATFORM
├──  app                
│   ├──  models          
│   ├──  services         
│   └── main.py            
├──  dags                 
├──  ML                   
│   ├──  spark_model      
│   └── pipeline.py         
├──  Tests                
├── docker-compose.yml      
└── requirements.txt        

```


## Installation et Démarrage

1. Prérequis

- Docker & Docker Compose

- Python 3.10+

2. Lancement de l'infrastructure

L'ensemble de la stack (PostgreSQL, Airflow, FastAPI) se lance en une commande :

```shell
docker-compose up --build
```


3. Initialisation de la base de données
L'API crée automatiquement les tables au démarrage via SQLAlchemy :

- users : Gestion des accès.

- df_silver : Données nettoyées pour les analytics.

- eta_predictions : Historique des prédictions pour monitoring.




## Pipeline de Données (ETL)

Le nettoyage des données (Zone Silver) suit des règles strictes pour garantir la qualité du modèle :

Filtres : Suppression des trajets avec une distance <= 0 ou >= 200 miles

Durée : Exclusion des trajets aberrants (> 3 heures ou <= 0 min)

Enrichissement : Extraction de pickup_hour, day_of_week, et month

Target Engineering : Application de log1p sur la durée pour normaliser la distribution




## Points d'entrée de l'API (Endpoints)


POST,/register : Création d'un compte utilisateur

POST,/login : Authentification et réception du Token JWT

POST,/predict : Prédiction de l'ETA (Minutes)

GET,/analytics/avg-duration-by-hour : Stats SQL : Durée moyenne par heure,JWT Requis

GET,/analytics/payment-analysis : Stats SQL : Analyse par type de paiement,JWT Requis



## Tests

Pour garantir la stabilité du système, des tests unitaires sont disponibles :

```shell
pytest Tests/test_api.py
```