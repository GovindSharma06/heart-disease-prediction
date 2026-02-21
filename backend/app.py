from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os
import joblib

app = FastAPI(title="Heart Disease Prediction API")

# allow streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
model_path = os.path.join(os.path.dirname(__file__), "model", "rf_heart_model.pkl")
model = joblib.load(model_path)


class PatientData(BaseModel):
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/predict")
def predict(data: PatientData):

    input_df = pd.DataFrame([data.dict()])

    # IMPORTANT: create missing-flag feature exactly like training
    input_df["Cholesterol_missing"] = (input_df["Cholesterol"] == 0).astype(int)

    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    return {
        "prediction": prediction,
        "risk_probability": probability
    }
