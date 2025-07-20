from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode("utf-8")), skipinitialspace=True)

    df.columns = [col.strip().lower() for col in df.columns]

    category_col = [col for col in df.columns if "category" in col][0]
    amount_col = [col for col in df.columns if "amount" in col or "spent" in col][0]

    df[category_col] = df[category_col].astype(str).str.strip().str.lower()
    df[amount_col] = df[amount_col].astype(str).str.replace(r"[^\d\.\-]", "", regex=True)
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")

    total = df[df[category_col].str.contains("food", na=False)][amount_col].sum()

    return {
        "answer": round(float(total), 2),
        "email": "24f3000061@ds.study.iitm.ac.in",  # ← Replace with your real email
        "exam": "tds-2025-05-roe"
    }
