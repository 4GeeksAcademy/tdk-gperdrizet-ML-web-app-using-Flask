'''Helper functions.'''
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import QuantileTransformer

# load the .env file variables
load_dotenv()


def db_connect():
    import os
    engine = create_engine(os.getenv('DATABASE_URL'))
    engine.connect()
    return engine


def impute(data_df: pd.DataFrame, missing_data_features: list) -> pd.DataFrame:
    '''Takes pandas dataframe and feature list. Runs
    Scikit-learn's IterativeImputer on specified features.
    Returns an updated dataframe.'''

    # Save the feature names for later - the imputer will return a numpy array
    # and we might like to get out Pandas dataframe back
    feature_names=data_df.columns

    # Make a copy of the training features dataframe, in case we decide that this
    # is a bad idea
    imputed_training_features=data_df.copy()
    imputed_training_features[missing_data_features]=imputed_training_features[missing_data_features].replace({0:np.nan})

    # Quantile transform our target features - this is for the imputer, not the decision tree
    qt=QuantileTransformer(n_quantiles=10, random_state=0)
    qt.fit(imputed_training_features[missing_data_features])
    imputed_training_features[missing_data_features]=qt.transform(imputed_training_features[missing_data_features])

    # Run the imputation
    imp=IterativeImputer(max_iter=100, verbose=True, tol=1e-6, sample_posterior=True)
    imp.fit(imputed_training_features)
    imputed_training_features=imp.transform(imputed_training_features)

    # Convert back to pandas
    imputed_training_features=pd.DataFrame(data=imputed_training_features, columns=feature_names)

    return imputed_training_features
