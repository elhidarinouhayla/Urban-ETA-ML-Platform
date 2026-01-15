from fastapi import FastAPI, HTTPException,Depends
from app.database import Base, engine, get_db
from sqlalchemy.orm import session
from app.models.schema import UserCreate, UserResponse, UserVerify
from app.models.model import User
from .auth import create_token, verify_password, verify_token, hache_password




app = FastAPI()
Base.metadata.create_all(bin=engine)



# creation d'un username :
@app.post("/register", response_model=UserResponse)
def create_user(user:UserCreate, db: session=Depends(get_db)):
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







