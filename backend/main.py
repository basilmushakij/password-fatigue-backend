from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd 
from model_logic import extract_features
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("model/model.pkl")

class PasswordInput(BaseModel):
    password: str

@app.post("/predict")
def predict_fatigue(data: PasswordInput):
    features = extract_features(data.password)
    prediction = model.predict([features])[0]
    return {"risk_level": int(prediction)}
