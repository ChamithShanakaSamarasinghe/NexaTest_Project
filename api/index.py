from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NexaTest API deployed successfully 🚀"}