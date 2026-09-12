from fastapi import FastAPI

app = FastAPI(title="My FastAPI")
@app.get("/")
def home():
    return {     "message": "EnergyAI Copilot API is running"}