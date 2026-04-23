from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NexaTest is running"}

# THIS is required for Vercel
handler = Mangum(app)