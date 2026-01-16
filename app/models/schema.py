from pydantic import BaseModel


class UserCreate(BaseModel):
    username : str
    email : str
    password : str


class UserVerify(BaseModel):
    username : str
    password : str

class UserResponse(UserCreate):
    id : int





class User_request(BaseModel):
    trip_distance : float
    RatecodeID :  int
    fare_amount : float
    tip_amount :  float
    tolls_amount : float
    total_amount : float
    Airport_fee : float
    pickup_hour : int
    month : int
    payment_type : int


class output_predict(BaseModel):
   duration_log : float
