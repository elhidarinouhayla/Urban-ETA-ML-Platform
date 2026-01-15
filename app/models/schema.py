from pydantic import BaseModel


class UserCreate(BaseModel):
    username : str
    email : str
    password : int


class UserVerify(BaseModel):
    username : str
    password : int

class UserResponse(UserCreate):
    id : int





class User_request(BaseModel):
    trip_distance : int
    RatecodeID :  int
    fare_amount : int
    tip_amount :  int
    tolls_amount : int
    total_amount : int
    Airport_fee : int
    pickup_hour : int
    month : int


class output_predict(BaseModel):
   duration_log : str
