from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

app = FastAPI(title="DemoML API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    Height: List[float]
    Weight: List[float]


model = joblib.load(MODEL_PATH)


@app.get("/")
def healthcheck():
    return {
        "message": "This backend is working",
        "model": type(model).__name__,
        "endpoint": "/predict",
    }


@app.post("/predict")
def getData(data: PredictionRequest):
    if len(data.Height) != len(data.Weight):
        raise HTTPException(
            status_code=400,
            detail="Height and Weight must contain the same number of values.",
        )

    if len(data.Height) < 2:
        raise HTTPException(
            status_code=400,
            detail="Send at least two samples so clustering can be performed.",
        )

    samples = np.column_stack((data.Height, data.Weight))
    predictions = model.fit_predict(samples).tolist()

    return {
        "predictions": predictions,
        "sample_count": len(predictions),
    }
