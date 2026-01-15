from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_prediction_fonctionne():
   
    donnees_test = {
        "trip_distance": 10.5,
        "pickup_hour": 8,
        "passenger_count": 2
       }
    
    
    reponse = client.post("/predict", json=donnees_test)
    
   
    assert reponse.status_code == 200
    
    resultat = reponse.json()
    
    assert "estimated_duration" in resultat
    
    assert resultat["estimated_duration"] > 0