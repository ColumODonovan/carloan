import csv
import os
import time, datetime

import pandas as pd
import numpy as np

from pandas.api.types import is_int64_dtype, is_float_dtype


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


from joblib import load, dump

from db.db_connector import DatabaseConnector
from models.car_loan_model import CarLoanModel, TransformerFromHyperP






def step_1():

    db = DatabaseConnector()
    db.connect(config="db/database.ini")
    
    
    df = pd.read_csv("datasets/car_loan_trainset.csv")
    columns = list(df.columns)

    location = "C:\\Users\\Colum\\Desktop\\\October\\datasets\\car_loan_trainset.csv"
    createCustomers = "CREATE TABLE CUSTOMERS (\n"
    copyCustomers = '''COPY customers({columns})
                   FROM '{loc}'
                   DELIMITER ','
                   CSV HEADER;'''.format(loc=location, columns=(', '.join(columns)))

    for i, dt in enumerate(list(df.dtypes)):    
        if is_int64_dtype(dt):
            createCustomers+=("\t" + str(columns[i]) + " bigint,\n")
        elif is_float_dtype(dt):
            createCustomers+=("\t" + str(columns[i])+" float8,\n")
        else:
            createCustomers+=("\t" + str(columns[i])+" text,\n")
    
    createCustomers  += "\tCONSTRAINT customer_id_pk PRIMARY KEY (customer_id)\n);"


    db.create_table_csv(createCustomers, copyCustomers)
    db.close_connection()

def step_2():

    car_loan = CarLoanModel()
    print("Reading and cleaning dataset...")
    df = car_loan.read_csv("datasets/car_loan_trainset.csv")
    df = car_loan.clean_dataset(df)
    print("Done.\n")
    base_features = car_loan.get_base_features(df)

    # Create the preprocessor
    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("scaler", TransformerFromHyperP())]),
            base_features)])

    print("Splitting dataset...")
    rest_of_df, test_df, rest_of_X, test_X, rest_of_y, test_y, ss  = car_loan.split_dataset(df)
    print("Done.\n")

    print("Finding the best logistic regression parameters...")
    logistic, logistic_best_params = car_loan.create_logistic_model(rest_of_X, rest_of_y, ss, preprocessor)
    print("Done.\n")

    print("Training the model...")
    final_model = car_loan.train_model(logistic, logistic_best_params, rest_of_X, rest_of_y, ss)
    print("Done.\n")

    print("Fitting the model...")
    final_model.fit(rest_of_X, rest_of_y)
    print("Done.\n")
    
    print("Model Accuracy:")
    print(car_loan.accuracy_score(final_model ,test_X, test_y))

    #plot_confusion_matrix(final_model, test_X, test_y)
    print("\nSaving model...")
    dump(final_model, 'models/saved_models/final_model.pkl')


def step_3():
    car_loan = CarLoanModel()
    db = DatabaseConnector()
    db.connect(config="db/database.ini")
    
    

    df = car_loan.read_csv("datasets/car_loan_trainset.csv")
    base_features = car_loan.get_base_features(df)

    loaded_model = load('models/saved_models/final_model.pkl')

    createPredictions = '''CREATE TABLE predictions(
                           prediction_id INT GENERATED ALWAYS AS IDENTITY,
                           customer_id INT,
                           prediction int ,
                           CONSTRAINT fk_customer
                            FOREIGN KEY(customer_id) 
                               REFERENCES customers(customer_id)
                        );'''


    location = "C:\\Users\\Colum\\Desktop\\\October\\predictions.csv"


    copyPredictions = '''COPY predictions(customer_id, prediction)
                   FROM '{loc}'
                   DELIMITER ','
                   CSV HEADER;'''.format(loc=location)


    f = open("predictions.csv", "w", newline='')
    writer = csv.writer(f)
    writer.writerow(['customer_id', 'prediction'])
    print("Running predictions...")
    for index, row in df.iterrows():

        try:
            prediction = loaded_model.predict(df.iloc[[index]][base_features])
        except:
            prediction = [""]

    
        writer.writerow([int(row['customer_id']) ,prediction[0]])


    f.close()        


    db.create_table_csv(createPredictions, copyPredictions)
    db.close_connection()

    os.remove("predictions.csv")



if __name__ == "__main__":
    
    start = time.time()
    
    print("********** [STEP 1/3] ********** ")
    step_1()
    print("********** [STEP 2/3] ********** ")
    step_2()
    print("********** [STEP 3/3] ********** ")    
    step_3()
    
    
    end =  time.time()
    print("Pipeline Finished in:", datetime.timedelta(end-start) )

