from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NexaTest is running"}

# REQUIRED for Vercel
handler = Mangum(app)