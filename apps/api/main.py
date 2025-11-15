from fastapi import FastAPI
from pydantic import BaseModel

# --- IMPORT SERVICES ---
from apps.api.services.nlp import SymptomNLP
from apps.api.services.rules import detect_red_flags

# --- INIT APP ---
app = FastAPI(
    title="CURASENSE API",
    version="1.0.0",
    description="AI Symptom Screening & Triage Backend"
)

# --- INIT NLP ENGINE (only one model now — fast) ---
nlp_engine = SymptomNLP()


# -------------------------------
#       ROOT / HOMEPAGE
# -------------------------------
@app.get("/")
def home():
    return {
        "status": "CURASENSE API running",
        "message": "Welcome to CURASENSE - AI Symptom Triage Backend",
        "docs": "/docs",
        "triage_endpoint": "/api/v1/triage"
    }


# -------------------------------
#       REQUEST MODEL
# -------------------------------
class TriageRequest(BaseModel):
    text: str
    age_range: str | None = None
    sex: str | None = None
    chronic_conditions: list[str] | None = []


# -------------------------------
#      TRIAGE ENDPOINT
# -------------------------------
@app.post("/api/v1/triage")
async def triage(req: TriageRequest):

    user_text = req.text.strip()

    # 1️⃣ RED-FLAG OVERRIDE CHECK
    red_flags = detect_red_flags(user_text)
    if red_flags:
        return {
            "conditions": [],
            "urgency": "emergency",
            "red_flags": red_flags,
            "advice": {
                "selfcare": [],
                "escalate_when": ["Seek emergency care immediately."]
            },
            "trace_id": "rf-" + user_text[:6]
        }

    # 2️⃣ FAST HYBRID RANKING (embeddings + zero-shot names)
    ranked = nlp_engine.rank(user_text)

    # 3️⃣ RETURN TRIAGE RESPONSE
    return {
        "conditions": ranked[:5],   # Top 5
        "urgency": "routine",
        "red_flags": [],
        "advice": {
            "selfcare": ["Hydrate well", "Rest", "Monitor symptoms"],
            "escalate_when": ["Symptoms worsen", "Fever lasts >3 days"]
        },
        "trace_id": "ok-" + user_text[:6]
    }
