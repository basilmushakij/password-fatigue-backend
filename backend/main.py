from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from model_logic import extract_features
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ตั้งค่า CORS สำหรับเชื่อมต่อกับ Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌟 โหลดสุดยอดสมอง "สภา AI" (ตรวจสอบให้แน่ใจว่าเอาไฟล์นี้ไปไว้ในโฟลเดอร์ model/ แล้ว)
model = joblib.load("model/model.pkl")

# โครงสร้างรับข้อมูล
class PasswordInput(BaseModel):
    password: str

# API Endpoint สำหรับทำนายผล
@app.post("/predict")
def predict_fatigue(data: PasswordInput):
    # 1. สกัดตัวเลข 4 ตัวจากรหัสผ่าน (เรียกใช้จาก model_logic.py)
    features = extract_features(data.password)
    
    # 2. ให้โมเดลทำนายผล (เอา features ใส่ใน list [ ] เพื่อให้เป็น 2D Array ตามที่ AI ต้องการ)
    prediction = model.predict([features])[0]
    
    # 3. ส่งผลลัพธ์ (0, 1, 2) กลับไปให้หน้าเว็บ
    return {"risk_level": int(prediction)}