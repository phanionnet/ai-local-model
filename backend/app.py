from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# # Serve frontend
# app.mount(
#     "/",
#     StaticFiles(directory=".", html=True),
#     name="frontend"
# )

# Enable CORS (for file:// and localhost access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

@app.get("/describe/{animal}")
def describe(animal: str):
    prompt = f"""
    You are an educational AI.
    Provide a short, simple one-paragraph description of the animal '{animal}'.
    """

    response = requests.post(
        OLLAMA_API,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return {"animal": animal, "description": response.json()["response"]}
