from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI(title="NexusGo Food Spoilage Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Food Spoilage Detection API is running"}

@app.post("/detect_spoilage")
async def detect_spoilage(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = np.array(image)

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # ---- METRICS ----
    brightness = np.mean(hsv[:, :, 2])          # 0–255
    saturation = np.mean(hsv[:, :, 1])          # 0–255
    texture = np.var(gray)                      # roughness

    # Detect decay colors (brown / black / dark yellow)
    lower_decay = np.array([5, 50, 20])
    upper_decay = np.array([35, 255, 160])
    decay_mask = cv2.inRange(hsv, lower_decay, upper_decay)
    decay_ratio = np.sum(decay_mask > 0) / decay_mask.size

    # ---- FRESHNESS SCORE (0–100) ----
    freshness_score = 100

    freshness_score -= decay_ratio * 120        # strong penalty
    freshness_score -= max(0, (140 - brightness) * 0.4)
    freshness_score -= max(0, (900 - texture) * 0.02)

    freshness_score = int(np.clip(freshness_score, 0, 100))

    # ---- FINAL RULE-BASED DECISION ----
    if freshness_score < 50:
        status = "Spoiled"
        explanation = (
            "Visible discoloration, dark regions, and texture inconsistency were detected. "
            "These are strong indicators of spoilage similar to human visual judgment."
        )

    elif 50 <= freshness_score <= 70:
        status = "Neutral"
        explanation = (
            "Some freshness indicators are present, but mild discoloration or surface changes "
            "create uncertainty. Human inspection would require closer evaluation."
        )

    else:
        status = "Fresh"
        explanation = (
            "Color distribution, brightness, and surface texture appear healthy. "
            "No dominant spoilage indicators were found."
        )

    return {
        "status": status,
        "confidence": f"{freshness_score}%",
        "explanation": explanation
    }
