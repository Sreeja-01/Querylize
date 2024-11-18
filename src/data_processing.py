import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def clean_data(df):
    """Perform advanced data cleaning on the provided dataframe."""
    # Removing duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    for column in df.columns:
        if df[column].dtype == 'object':  # Categorical columns
            df[column] = df[column].fillna(df[column].mode()[0])  # Fill with mode
        else:  # Numerical columns
            df[column] = df[column].fillna(df[column].mean())  # Fill with mean

    return df

def preprocess_data(df):
    """Preprocess the data for analysis."""
    # Standardize numerical columns
    scaler = StandardScaler()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # One-hot encode categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=categorical_cols)

    return df
