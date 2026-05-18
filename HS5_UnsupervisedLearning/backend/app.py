from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load trained model
model = joblib.load("model.pkl")

class Customer(BaseModel):
    annual_income: float
    spending_score: float
    
@app.get("/")
def home():
    return {"message":"welcome to bked"}

@app.post("/predict")
def predict_cluster(data: Customer):
    df = pd.DataFrame([{
        "annual_income": data.annual_income,
        "spending_score": data.spending_score
    }])

    cluster = model.predict(df)[0]
    return {"cluster": int(cluster)}

