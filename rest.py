
from csv import excel
from typing import Union
from pydantic import BaseModel

from auth.auth import AuthorizationHandler
from db.db_connector import DatabaseConnector
from models.car_loan_model import CarLoanModel, TransformerFromHyperP
from schemas.customer import Customer
from schemas.auth_details import AuthDetails

from joblib import load

from fastapi import FastAPI, Path, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

model = CarLoanModel()
model.set_model("models/saved_models/final_model.pkl")

app = FastAPI()


db = DatabaseConnector()
db.connect(config="db/database.ini",)
db.create_users()

auth_handler = AuthorizationHandler()

@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if (db.get_user(auth_details.username) is not None):
        raise HTTPException(status_code=422, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    db.insert_user(auth_details.username, hashed_password)
    return

@app.post('/login')
def login(auth_details: AuthDetails):
    user = db.get_user(auth_details.username)
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user[1])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user[0])
    return { 'token': token }

@app.post("/predict")
async def create_item(customer: Customer, username=Depends(auth_handler.auth_wrapper)):   
    db.insert_customer(customer)
    prediction = model.predict_from_json(customer)
    db.insert_prediction(customer.customer_id, prediction)
    return {"prediction" : prediction}


