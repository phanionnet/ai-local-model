You will build:

A local AI model hosted on your Ubuntu laptop

A simple chatbot

Input: single animal word (Lion)

Output: 1-paragraph description

Open-source only

No cloud

No “magic” one-click tools

🧠 Learning Path Overview

You’ll go through 4 clear layers:

GPU + AI Runtime Setup

Run a Pre-trained Open-Source LLM locally

Wrap it with your own backend (API)

Build a simple chatbot UI

You can stop at any layer and still learn something useful.

🧩 Layer 1: GPU & System Readiness (Very Important)
1.1 Verify NVIDIA GPU & Drivers
nvidia-smi


You should see:

GPU name

Driver version

CUDA version

If this fails → install NVIDIA drivers before proceeding.

1.2 Verify CUDA Toolkit (Optional but Helpful)
nvcc --version


If missing:

sudo apt install nvidia-cuda-toolkit


⚠️ Ollama does not require CUDA manually, but this helps later for fine-tuning.

🧩 Layer 2: Local AI Model (Your “In-House Pre-trained Model”)
Why this approach?

You host the model

You control inputs

You can later fine-tune

Zero ML math needed initially

2.1 Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh


Start service:

ollama serve


Verify:

ollama --version

2.2 Pull a Model (GPU Optimized)
Recommended for your hardware
ollama pull phi3:mini


Alternative (lighter):

ollama pull tinyllama

2.3 Validate Model Is Using GPU

Run:

ollama run phi3:mini


In another terminal:

nvidia-smi


You should see GPU memory usage increase → ✅ GPU acceleration working.

2.4 Understand What You Have Now (Important)

At this point:

You did not train anything

You own a local copy of a pre-trained model

This is now your in-house AI model

💡 This is exactly how most real companies start.

🧩 Layer 3: Your Own AI Backend (Learning Core)

Now you’ll wrap the model with your own logic.

3.1 Install Python Environment
sudo apt install python3 python3-pip python3-venv -y


Create virtual environment:

python3 -m venv animalbot-env
source animalbot-env/bin/activate

3.2 Install Backend Libraries
pip install fastapi uvicorn requests

3.3 Build Your AI API (Manual & Clear)

Create app.py:

from fastapi import FastAPI
import requests

app = FastAPI()

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"

@app.get("/describe/{animal}")
def describe(animal: str):

    prompt = f"""
    You are an educational AI.
    Provide a short, clear, one-paragraph description of the animal '{animal}'.
    Avoid scientific jargon.
    """

    response = requests.post(
        OLLAMA_API,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return {
        "animal": animal,
        "description": response.json()["response"]
    }

3.4 Run Backend
uvicorn backend.app:app --reload


Test:

curl http://localhost:8000/describe/lion


🎉 You now own a local AI inference API.

🧩 Layer 4: Chatbot UI (Simple but Educational)
4.1 Create UI

Create index.html:

<!DOCTYPE html>
<html>
<head>
    <title>Animal Chatbot</title>
</head>
<body>
    <h2>Local Animal AI Bot</h2>

    <input type="text" id="animal" placeholder="Enter animal name" />
    <button onclick="ask()">Ask</button>

    <p id="output"></p>

    <script>
        async function ask() {
            const animal = document.getElementById("animal").value;
            const res = await fetch(`http://localhost:8000/describe/${animal}`);
            const data = await res.json();
            document.getElementById("output").innerText = data.description;
        }
    </script>
</body>
</html>


Open in browser → ✅ Done.