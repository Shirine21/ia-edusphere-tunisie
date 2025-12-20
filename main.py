from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"app": "IA EDUSPHERE", "status": "online"}

@app.get("/sante")
def sante():
    return {"status": "healthy", "time": datetime.now().isoformat()}

@app.get("/analyser")
def analyser(texte: str = "test"):
    corrections = []
    if "sa va" in texte.lower():
        corrections.append({"erreur": "sa va", "correction": "ça va"})
    
    return {
        "texte": texte,
        "corrections": corrections,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
