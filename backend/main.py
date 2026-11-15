from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
from model_logic import extract_features
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Only the demo frontend (port 4000) may call this API from a browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000", "http://127.0.0.1:4000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Loaded once when the server starts, not on every request.
# Note: joblib uses pickle, so this is only safe because model.pkl is our own file from this repo.
model = joblib.load("model/model.pkl")


class PasswordInput(BaseModel):
    # Validation: 1-128 characters. Anything else is rejected with HTTP 422 before it reaches the model.
    password: str = Field(min_length=1, max_length=128)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict_fatigue(data: PasswordInput):
    features = extract_features(data.password)
    prediction = model.predict([features])[0]
    avg_dist, length, unique_ratio, seq_ratio = features
    return {
        "risk_level": int(prediction),
        "avg_dist": avg_dist,
        "unique_ratio": unique_ratio,
    }