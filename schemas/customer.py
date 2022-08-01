from pydantic import BaseModel



class Customer(BaseModel):
    customer_id: int
    main_account_loan_no: int
    main_account_active_loan_no: int
    main_account_overdue_no: int
    main_account_outstanding_loan: int
    main_account_sanction_loan: int
    main_account_disbursed_loan: int
    sub_account_loan_no: int
    sub_account_active_loan_no: int
    sub_account_overdue_no: int
    sub_account_outstanding_loan: int
    sub_account_sanction_loan: int
    sub_account_disbursed_loan: int
    disbursed_amount: int
    asset_cost: int
    branch_id: int
    supplier_id: int
    manufacturer_id: int
    area_id: int
    employee_code_id: int
    mobileno_flag: int
    idcard_flag: int
    Driving_flag: int
    passport_flag: int
    credit_score: int
    main_account_monthly_payment: int
    sub_account_monthly_payment: int
    last_six_month_new_loan_no: int
    last_six_month_defaulted_no: int
    average_age: int
    credit_history: int
    enquirie_no: int
    loan_to_asset_ratio: float
    total_account_loan_no: int
    sub_account_inactive_loan_no: int
    total_inactive_loan_no: int
    main_account_inactive_loan_no: int
    total_overdue_no: int
    total_outstanding_loan: int
    total_sanction_loan: int
    total_disbursed_loan: int
    total_monthly_payment: int
    outstanding_disburse_ratio: float
    main_account_tenure: int
    sub_account_tenure: int
    disburse_to_sactioned_ratio: float
    active_to_inactive_act_ratio: float
    year_of_birth: int
    disbursed_date: int
    Credit_level: int
    employment_type: int
    age: int
    loan_default: int    


