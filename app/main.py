from fastapi import FastAPI, HTTPException,Depends
from .database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.schema import UserCreate, UserResponse, UserVerify, output_predict, User_request
from app.models.model import User
from .auth import create_token, verify_password, verify_token, hache_password
from .services.service_prediction import predict




app = FastAPI()
Base.metadata.create_all(bind=engine)



# creation d'un username :
@app.post("/register", response_model=UserResponse)
def create_user(user:UserCreate, db: Session=Depends(get_db)):
    exist = db.query(User).filter(User.username == user.username).first()

    if exist:
        raise HTTPException(status_code=400, detail= "username existe deja")
    
    # haching password
    hashed_pwd = hache_password(user.password)
    
    new_user = User(username=user.username, password=hashed_pwd, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




# verifier l'identifiant et encoder token
@app.post("/login")
def login(user:UserVerify, db: Session=Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
        ).first()
    
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400, detail="username or password incorect")
    
    token = create_token(db_user.username)

    return {"token" : token}


# creation d'endpoint de prediction

@app.post("/predict", response_model=output_predict)
def prediction(data: User_request, user: dict=Depends(verify_token)):

    df = data.dict()
    duration = predict(df)

    return {"duration_log": duration}





# la durée moyenne des trajets par heure

@app.post("/analytics/avg_duration_by_hour")
def avg_duration_by_hour(db: Session = Depends(get_db), user: str = Depends(verify_token)):
    
    sql = text("""
            SELECT
        pickup_hour AS hour,
        AVG(trip_duration) AS average_duration
        FROM silver_table
        GROUP BY pickup_hour
        ORDER BY pickup_hour ASC;
    """)
    
    result_data = db.execute(sql)
    
    final_results = []
    for row in result_data:
        dictionary = {
            "hour": row.hour,
            "average_duration": round(row.average_duration, 2)
        }
        final_results.append(dictionary)
    
    return final_results




# Comparaison durée moyenne par type de paiement

@app.post("/analytics/payment_analysis")
def payment_analysis(db: Session = Depends(get_db), user: str = Depends(verify_token)):
    
    sql = text("""
        SELECT
    payment_type,
    COUNT(*) AS total_trips,
    AVG(trip_duration) AS average_duration
    FROM silver_table
    GROUP BY payment_type;
    """)
    
    result_data = db.execute(sql).fetchall()
    
    final_results = []
    for row in result_data:
        data_item = {
            "payment_type": row.payment_type,
            "total_trips": row.total_trips,
            "average_duration": round(row.average_duration, 2)
        }
        final_results.append(data_item)
        
    return final_results