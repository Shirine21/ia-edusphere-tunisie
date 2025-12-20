from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"app": "IA EDUSPHERE", "status": "online"}

@app.get("/sante")
def sante():
    return {"status": "healthy", "time": datetime.now().isoformat()}

@app.get("/regles")
def get_rules():
    """Retourne toutes les règles pédagogiques disponibles"""
    return {
        "total": 3,
        "regles": [
            {
                "erreur": "sa va",
                "correction": "ça va",
                "type": "homophone",
                "explication": "'sa' = possession, 'ça' = démonstratif",
                "exercice": "h5p/homophones-sa-ca",
                "niveau": "CE1-CM2"
            },
            {
                "erreur": "je suis aller",
                "correction": "je suis allé",
                "type": "conjugaison",
                "explication": "Accord du participe passé avec 'être'",
                "exercice": "scorm/passe-compose",
                "niveau": "CE2-CM2"
            },
            {
                "erreur": "cinq fois six",
                "correction": "5 × 6 = 30",
                "type": "maths",
                "explication": "Table de multiplication par 6",
                "exercice": "quiz/tables-multiplication",
                "niveau": "CE1-CM2"
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/analyser")
def analyser(texte: str = "test"):
    """Analyse un texte avec TOUTES les règles pédagogiques"""
    
    # Règles pédagogiques (mêmes que dans /regles)
    regles_pedagogiques = [
        {"erreur": "sa va", "correction": "ça va", "type": "homophone"},
        {"erreur": "je suis aller", "correction": "je suis allé", "type": "conjugaison"},
        {"erreur": "cinq fois six", "correction": "5 × 6 = 30", "type": "maths"},
        {"erreur": "ils croivent", "correction": "ils croient", "type": "conjugaison"},
        {"erreur": "plus meilleur", "correction": "meilleur", "type": "pléonasme"}
    ]
    
    corrections = []
    texte_minuscule = texte.lower()
    
    # Vérifier chaque règle
    for regle in regles_pedagogiques:
        if regle["erreur"].lower() in texte_minuscule:
            corrections.append({
                "erreur": regle["erreur"],
                "correction": regle["correction"],
                "type": regle.get("type", "general")
            })
    
    return {
        "texte": texte,
        "corrections": corrections,
        "timestamp": datetime.now().isoformat(),
        "nombre_corrections": len(corrections)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
