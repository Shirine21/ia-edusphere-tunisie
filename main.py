from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="IA EDUSPHERE KIDS Tunisie",
    description="IA pédagogique pour analyser les réponses des élèves",
    version="1.0"
)

# Modèles de données
class ReponseEleve(BaseModel):
    texte: str
    eleve_id: str = "anonyme"
    langue: str = "fr"

class SuggestionCorrection(BaseModel):
    erreur: str
    correction: str
    explication: str
    exercice: str

class ResultatAnalyse(BaseModel):
    success: bool
    eleve: str
    texte: str
    suggestions: List[SuggestionCorrection]
    timestamp: str

# Règles pédagogiques de base
REGLE_CORRECTIONS = [
    {
        "erreur": "sa va",
        "correction": "ça va",
        "explication": "'sa' montre la possession (sa maison), 'ça' montre (ça va bien)",
        "exercice": "h5p/homophones1",
        "langue": "fr"
    },
    {
        "erreur": "je suis aller",
        "correction": "je suis allé",
        "explication": "Avec le verbe 'être', on accorde le participe passé avec le sujet",
        "exercice": "scorm/passe-compose",
        "langue": "fr"
    },
    {
        "erreur": "cinq fois six",
        "correction": "5 × 6 = 30",
        "explication": "Table de multiplication par 6",
        "exercice": "quiz/tables-multiplication",
        "langue": "fr"
    }
]

@app.get("/")
def accueil():
    return {
        "application": "IA Pédagogique EDUSPHERE KIDS",
        "status": "✅ EN LIGNE",
        "version": "1.0",
        "region": "Tunisie",
        "endpoints": {
            "accueil": "GET /",
            "sante": "GET /sante",
            "regles": "GET /regles",
            "analyser": "POST /analyser"
        }
    }

@app.get("/sante")
def sante():
    return {"status": "healthy", "time": datetime.now().isoformat()}

@app.get("/regles")
def regles():
    return {
        "total": len(REGLE_CORRECTIONS),
        "regles": REGLE_CORRECTIONS
    }

@app.post("/analyser")
def analyser(donnees: ReponseEleve):
    suggestions = []
    
    texte_minuscule = donnees.texte.lower()
    
    for regle in REGLE_CORRECTIONS:
        if regle["langue"] == donnees.langue and regle["erreur"] in texte_minuscule:
            suggestions.append({
                "erreur": regle["erreur"],
                "correction": regle["correction"],
                "explication": regle["explication"],
                "exercice": regle["exercice"]
            })
    
    return {
        "success": True,
        "eleve": donnees.eleve_id,
        "texte": donnees.texte,
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat(),
        "message": f"{len(suggestions)} suggestion(s) trouvée(s)" if suggestions else "✅ Aucune erreur détectée"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)    
