import requests
from models.car_loan_model import CarLoanModel, TransformerFromHyperP
from db.db_connector import DatabaseConnector
import json

# Simple requests script which was used for testing

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
    "employment_type": 0,
    "age": 24,
    "loan_default": 0,
    "username": "colum"}

r = json.dumps(body)
loaded_r = json.loads(r)

endpoint = "http://localhost:8000/predict"
headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTkzOTI3NDgsImlhdCI6MTY1OTMwNjM0OCwic3ViIjoiY29sdW0ifQ.1J5Dsi88YOBDfzV0o5-fZDDlssqtrxidgAGnERY30C0"}


r = requests.post(endpoint, json=loaded_r, headers=headers, timeout=10)

print(r.status_code)
print(r.content.decode("utf-8"))