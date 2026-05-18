from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load trained KNN model saved earlier as 'knn_model.pkl'
# Ensure this file is in the same folder as this script (backend/knn_model.pkl)
model = joblib.load("../notebook/knn_model.pkl")


class Customer(BaseModel):
    annual_income: float
    spending_score: float


@app.post("/predict")
def predict_cluster(data: Customer):
    df = pd.DataFrame([{
        "annual_income": data.annual_income,
        "spending_score": data.spending_score
    }])

    cluster = model.predict(df)[0]
    return {"cluster": int(cluster)}


@app.get("/health")
def health():
    return {"status": "ok"}