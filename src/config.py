import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

TEMPERATURE = 0.3
TOP_P = 0.9
TOP_K = 40

# ✅ USAR RUTA LOCAL SIMPLE
MLFLOW_TRACKING_URI = "./mlruns"

MLFLOW_EXPERIMENT = "RAG_Informes_Economicos"