from fastapi.testclient import TestClient
from rest import app
import psycopg2
import json
from db.db_connector import DatabaseConnector


client = TestClient(app)
db = DatabaseConnector()
db.connect("db/database.ini")


body = {"customer_id": 1717171717,
    "main_account_loan_no": 4,
    "main_account_active_loan_no": 3,
    "main_account_overdue_no": 3,
    "main_account_outstanding_loan": 111111,
    "main_account_sanction_loan": 666207,
    "main_account_disbursed_loan": 666207,
    "sub_account_loan_no": 0,
    "sub_account_active_loan_no": 0,
    "sub_account_overdue_no": 0,""
    "sub_account_outstanding_loan": 0,
    "sub_account_sanction_loan": 0,
    "sub_account_disbursed_loan": 0,
    "disbursed_amount": 4444,
    "asset_cost": 444444,
    "branch_id": 0,
    "supplier_id": 44,
    "manufacturer_id": 3,
    "area_id": 3,
    "employee_code_id": 3,
    "mobileno_flag": 3,
    "idcard_flag": 3,
    "Driving_flag": 4,
    "passport_flag": 4,
    "credit_score": 400,
    "main_account_monthly_payment": 3333,
    "sub_account_monthly_payment": 0,
    "last_six_month_new_loan_no": 1,
    "last_six_month_defaulted_no": 0,
    "average_age": 10,
    "credit_history": 333,
    "enquirie_no": 33,
    "loan_to_asset_ratio": 3,
    "total_account_loan_no": 33,
    "sub_account_inactive_loan_no": 33,
    "total_inactive_loan_no": 33,
    "main_account_inactive_loan_no": 333,
    "total_overdue_no": 3333,
    "total_outstanding_loan": 3333,
    "total_sanction_loan": 33333,
    "total_disbursed_loan": 33333,
    "total_monthly_payment": 3333,
    "outstanding_disburse_ratio": 1.3,
    "main_account_tenure": 0,
    "sub_account_tenure": 1,
    "disburse_to_sactioned_ratio": 2.3,
    "active_to_inactive_act_ratio": 3.0,
    "year_of_birth": 1998,
    "disbursed_date": 2020,
    "Credit_level": 1,
    "employment_type": 0, "age": 24, "loan_default": 0, "username": "colum"}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
    
    
def read_test_insert_user():
    
    response = client.post("/register", data=json.dumps({"username" : "test444", "password": "test6"}))
    assert response.status_code == 201
    assert response.json() == None
    
def test_username_taken():
      
    try:
        db.insert_user("test", "test")
    except psycopg2.errors.UniqueViolation:
        pass 
    
    response = client.post("/register", data=json.dumps({"username" : "test", "password": "test"}))
    assert response.status_code == 422
    assert response.json() == {"detail": "Username is taken"}

    
def test_successful_login():       
    response = client.post("/login", data=json.dumps({"username" : "colum", "password": "secret_password"}))
    assert response.status_code == 200
    assert response.json()["token"] is not None
    
def test_bad_username():       
    response = client.post("/login", data=json.dumps({"username" : "bad_login", "password": "secret_password"}))
    assert response.status_code == 401
    
def test_bad_password():       
    response = client.post("/login", data=json.dumps({"username" : "colum", "password": "secret_password1"}))
    assert response.status_code == 401
    
def test_valid_prediction():
    
    response = client.post("/login", data=json.dumps({"username" : "colum", "password": "secret_password"}))
    token = response.json()["token"]
    headers = {"Authorization": "Bearer {token}".format(token=token)}
  
    response = client.post("/predict", data=json.dumps(body), headers=headers)
    prediction = response.json()["prediction"]
    
    assert response.status_code == 200
    assert prediction == 1 or prediction == 0
    
def test_prediction_bad_token():
    
    response = client.post("/login", data=json.dumps({"username" : "colum", "password": "secret_password"}))
    token = response.json()["token"]
    token+="x"
    headers = {"Authorization": "Bearer {token}".format(token=token)}
  
    response = client.post("/predict", data=json.dumps(body), headers=headers)
    assert response.status_code == 401
