# Dockerfile pour IA EDUSPHERE KIDS
FROM python:3.11-slim

WORKDIR /app

# 1. Création des fichiers
RUN echo "fastapi==0.104.1" > requirements.txt
RUN echo "uvicorn[standard]==0.24.0" >> requirements.txt

RUN echo '
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import os

app = FastAPI(title="IA EDUSPHERE KIDS - Version Tunisie")

# ========================
# RÈGLES PÉDAGOGIQUES DE BASE
# ========================
REGLES_TUNISIENNES = [
    # Français - erreurs courantes
    {"erreur": "sa va", "correction": "ça va", "type": "homophone", "exercice": "h5p/homophones1"},
    {"erreur": "et", "correction": "est", "type": "homophone", "exercice": "h5p/et_est"},
    {"erreur": "a", "correction": "à", "type": "homophone", "exercice": "h5p/accent"},
    {"erreur": "ses", "correction": "c"est", "type": "homophone", "exercice": "h5p/ses_cest"},
    {"erreur": "je suis aller", "correction": "je suis allé(e)", "type": "conjugaison", "exercice": "scorm/passe_compose"},
    {"erreur": "ils croivent", "correction": "ils croient", "type": "conjugaison", "exercice": "h5p/croire"},
    
    # Ajouts pour élèves tunisiens
    {"erreur": "je vai", "correction": "je vais", "type": "conjugaison", "exercice": "h5p/verbe_aller"},
    {"erreur": "j"ai faites", "correction": "j"ai fait", "type": "accord", "exercice": "scorm/accords"},
    
    # Maths
    {"erreur": "cinq fois six", "correction": "5 × 6 = 30", "type": "calcul", "exercice": "quiz/tables"},
    {"erreur": "deux plus deux", "correction": "2 + 2 = 4", "type": "calcul", "exercice": "quiz/additions"}
]

# ========================
# FONCTIONS DE L'IA
# ========================
def analyser_texte(texte, eleve_id="anonyme"):
    """Le cœur de l'IA pédagogique"""
    texte_lower = texte.lower()
    corrections = []
    exercices = []
    
    for regle in REGLES_TUNISIENNES:
        if regle["erreur"] in texte_lower:
            corrections.append({
                "erreur": regle["erreur"],
                "correction": regle["correction"],
                "type": regle["type"],
                "explication": f"Correction {regle[''type'']}"
            })
            if regle["exercice"]:
                exercices.append(regle["exercice"])
    
    return {
        "eleve": eleve_id,
        "texte_original": texte,
        "texte_detecte": texte_lower,
        "nombre_erreurs": len(corrections),
        "corrections": corrections,
        "exercices_suggérés": list(set(exercices)),
        "message_special": "✅ IA développée pour EDUSPHERE KIDS Tunisie"
    }

# ========================
# ENDPOINTS API
# ========================
@app.get("/")
def accueil():
    return {
        "projet": "IA Pédagogique EDUSPHERE KIDS",
        "version": "2.0-tunisie",
        "status": "🟢 EN LIGNE",
        "endpoints": {
            "accueil": "GET /",
            "santé": "GET /sante",
            "règles": "GET /regles",
            "analyser": "POST /analyser",
            "ajouter_règle": "POST /ajouter"
        },
        "message": "Prêt pour intégration avec kids.edusphere.tn"
    }

@app.get("/sante")
def sante():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "region": "Tunisie",
        "eleves_capacite": "illimité"
    }

@app.get("/regles")
def voir_regles():
    return {
        "total_regles": len(REGLES_TUNISIENNES),
        "regles_par_type": {
            "francais": [r for r in REGLES_TUNISIENNES if "conjugaison" in r["type"] or "homophone" in r["type"]],
            "maths": [r for r in REGLES_TUNISIENNES if "calcul" in r["type"]]
        }
    }

@app.post("/analyser")
async def analyser_endpoint(
    texte: str = Form(""),
    eleve_id: str = Form("eleve_tunisien")
):
    """Endpoint principal pour EDUSPHERE"""
    if not texte:
        return JSONResponse({
            "status": "error",
            "message": "Veuillez fournir un texte à analyser"
        }, status_code=400)
    
    resultat = analyser_texte(texte, eleve_id)
    
    return JSONResponse({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "serveur": "Render - IA EDUSPHERE",
        "data": resultat
    })

@app.post("/ajouter")
async def ajouter_regle(
    erreur: str = Form(...),
    correction: str = Form(...),
    type_regle: str = Form("personnalisee")
):
    """Pour ajouter vos propres règles pédagogiques"""
    nouvelle_regle = {
        "erreur": erreur,
        "correction": correction,
        "type": type_regle,
        "exercice": "h5p/personnalise",
        "ajoute_par": "enseignant",
        "date": datetime.now().isoformat()
    }
    
    REGLES_TUNISIENNES.append(nouvelle_regle)
    
    return {
        "status": "regle_ajoutee",
        "message": f"Nouvelle règle ajoutée : '{erreur}' → '{correction}'",
        "total_regles": len(REGLES_TUNISIENNES)
    }

# ========================
# DÉMARRAGE
# ========================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 IA EDUSPHERE KIDS démarrée sur le port {port}")
    print(f"🌍 Accès: http://localhost:{port}")
    print(f"📚 Règles chargées: {len(REGLES_TUNISIENNES)}")
    uvicorn.run(app, host="0.0.0.0", port=port)
' > main.py

# 2. Installation
RUN pip install --no-cache-dir -r requirements.txt

# 3. Exposition du port
EXPOSE 8000

# 4. Commande de démarrage
CMD ["python", "main.py"]
