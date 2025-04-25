from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pyotp

def convert_date(date):
    try:
        return datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected 'MM/DD/YYYY'.")

def add_one_day(date_string):
    try:
        return (datetime.strptime(date_string, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")

def process_date(date):

    try:
        year, month, day = date.split("-")
        return month.lstrip("0"), day.lstrip("0"), year
    except ValueError:
        raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")

def process_df(df):

    try:
        df.drop(columns=drop_columns, inplace=True, errors="ignore")
        df["Service Code"] = df["Service Code"].fillna("").astype(str)
        df["Clinician NPI"] = df["Clinician NPI"].fillna("").astype(str)
        df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")
        df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
        df.rename(columns=rename_dict, inplace=True)
        df["claim_serviceLines_0_serviceDateFrom"] = pd.to_datetime(
            df["claim_serviceLines_0_serviceDateFrom"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        df["patient_dob"] = pd.to_datetime(
            df["patient_dob"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")
        df["Date"] = df["claim_serviceLines_0_serviceDateFrom"]

        for col in all_columns:
            if col not in df.columns:
                df[col] = np.nan

        return df.to_json(orient="records")

    except Exception as e:
        raise ValueError(f"Error processing DataFrame: {str(e)}")


def get_otp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()

