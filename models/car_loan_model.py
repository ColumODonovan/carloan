from asyncio import base_futures
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action="ignore", category=DataConversionWarning)
warnings.filterwarnings(action="ignore", category=FutureWarning)



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from pandas.plotting import scatter_matrix

from seaborn import scatterplot, stripplot, lmplot

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit

from sklearn.metrics import accuracy_score
from sklearn.metrics import plot_confusion_matrix

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import OneHotEncoder

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest

from sklearn.impute import SimpleImputer

from sklearn.datasets import load_iris

from joblib import dump, load





class CarLoanModel():
    
    model = None
    columns = None
    base_features = None
    
    def read_csv(self, filename):
        df = pd.read_csv("datasets/car_loan_trainset.csv")


        # Shuffle the dataset
        df = df.sample(frac=1, random_state=2)
        df.reset_index(drop=True, inplace=True)
        self.columns = df.columns
        df.shape
        return df


    def clean_dataset(self, df):
        assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
        df.dropna(inplace=True)
        indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
        return df[indices_to_keep]  

    def get_base_features(self, df):
        base_features = list(df.columns)[1:52]

        base_features.remove("year_of_birth")
        base_features.remove("supplier_id")
        base_features.remove("branch_id")
        base_features.remove("Driving_flag")
        base_features.remove("mobileno_flag")
        base_features.remove("passport_flag")
        base_features.remove("employee_code_id")
        base_features.remove("manufacturer_id")
        base_features.remove("area_id")

        self.base_features = base_features
        return base_features



    def split_dataset(self, df):


        # Split off the test set: 30% of the dataset. Note the stratification
        rest_of_df, test_df = train_test_split(df, train_size=0.7, stratify=df["loan_default"], random_state=2)

        # Extract the features but leave as a DataFrame

        base_features = self.get_base_features(df)
        rest_of_X = rest_of_df[base_features]
        test_X = test_df[base_features]

        rest_of_y = rest_of_df["loan_default"]
        test_y = test_df["loan_default"]

        # Create the object that shuffles and splits the rest of the data
        # Why 0.75? Because 0.75 of 80% of the data is 20% of the original dataset.
        ss = StratifiedShuffleSplit(n_splits=1, train_size=0.75, test_size=0.25, random_state=2)

        return rest_of_df, test_df, rest_of_X, test_X, rest_of_y, test_y, ss 



    def create_logistic_model(self, rest_of_X, rest_of_y, ss, preprocessor):
        

        
        # Create a pipeline that combines the preprocessor with logistic regression
        logistic = Pipeline([
            #("preprocessor", preprocessor),
            ("predictor", LogisticRegression(max_iter=20000 ))])

        logistic_param_grid = {"predictor__penalty" : ['l2'],
                               "predictor__solver" : ['sag'],#sag
                               "predictor__C": [0.7, 1.1, 1.4]}
                               #"preprocessor__num__scaler__transformer": [StandardScaler()]}#, StandardScaler()]}

        logistic_gs = GridSearchCV(logistic, logistic_param_grid, scoring="accuracy", cv=ss)
        logistic_gs.fit(rest_of_X, rest_of_y)
        
        return logistic, logistic_gs.best_params_






    def train_model(self, model, best_params, rest_of_X, rest_of_y, ss):

        model.set_params(**best_params) 
        scores = cross_validate(model, rest_of_X, rest_of_y, cv=ss, 
                                scoring="accuracy", return_train_score=True)
        print("Training accuracy: ", np.mean(scores["train_score"]))
        print("Validation accuracy: ", np.mean(scores["test_score"]))

        return model
  
    def accuracy_score(self, model, test_X, test_y):
        return accuracy_score(test_y, model.predict(test_X))

    def set_model(self, model_name):
        self.model = load(model_name)

    def predict_from_json(self, x):       
        df = pd.DataFrame(x.__dict__, index=[0])
        return int(self.model.predict(df.head(1)[self.get_base_features(df)])[0])
    
    

class TransformerFromHyperP(BaseEstimator, TransformerMixin):

    def __init__(self, transformer=None):
        self.transformer = transformer

    def fit(self, X, y=None):
        if self.transformer:
            self.transformer.fit(X, y)
        return self

    def transform(self, X, y=None):
        if self.transformer:
            return self.transformer.transform(X)
        else:
            return X
