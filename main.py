from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="IA Pédagogique EDUSPHERE KIDS Tunisie",
    description="IA adaptative pour analyser les réponses des élèves",
    version="2.0"
)

# ==================== MODÈLES DE DONNÉES ====================
class AnalyseRequest(BaseModel):
    texte: str
    eleve_id: str = "anonyme"
    langue: str = "fr"

class Correction(BaseModel):
    erreur: str
    correction: str
    type_erreur: str
    explication: str
    exercice_suggere: str

class AnalyseResponse(BaseModel):
    success: bool
    timestamp: str
    eleve_id: str
    texte_analyse: str
    corrections: List[Correction]
    exercices_suggestion: List[str]
    message: str

# ==================== BASE DE CONNAISSANCES ====================
# RÈGLES PÉDAGOGIQUES TUNISIENNES - À ENRICHIR PLUS TARD
REGLES_PEDAGOGIQUES = [
    # Français - erreurs courantes en Tunisie
    {
        "erreur": "sa va",
        "correction": "ça va",
        "type": "homophone",
        "explication": "'sa' est possessif (sa maison), 'ça' est démonstratif",
        "exercice": "h5p/homophones-sa-ca",
        "langue": "fr",
        "niveau": "CE1-CM2"
    },
    {
        "erreur": "je suis aller",
        "correction": "je suis allé",
        "type": "conjugaison",
        "explication": "Avec 'être', le participe passé s'accorde avec le sujet",
        "exercice": "scorm/accord-participe",
        "langue": "fr",
        "niveau": "CE2-CM2"
    },
    {
        "erreur": "ils croivent",
        "correction": "ils croient",
        "type": "conjugaison",
        "explication": "Le verbe 'croire' au présent : je crois, tu crois, il croit, nous croyons, vous croyez, ils croient",
        "exercice": "h5p/conjugaison-croire",
        "langue": "fr",
        "niveau": "CM1-CM2"
    },
    {
        "erreur": "cinq fois six",
        "correction": "5 × 6 = 30",
        "type": "maths",
        "explication": "Table de multiplication de 6",
        "exercice": "quiz/tables-multiplication",
        "langue": "fr",
        "niveau": "CE1-CM2"
    },
    # Arabe - exemples de base
    {
        "erreur": "الولد ذهب",
        "correction": "الولد ذهبَ",
        "type": "grammaire",
        "explication": "Marque du accusatif manquante",
        "exercice": "h5p/grammaire-arabe",
        "langue": "ar",
        "niveau": "tous"
    },
]

# ==================== ENDPOINTS API ====================
@app.get("/")
async def root():
    """Page d'accueil - Vérifie que l'IA est en ligne"""
    return {
        "application": "IA Pédagogique EDUSPHERE KIDS",
        "version": "2.0",
        "status": "🟢 EN LIGNE",
        "region": "Tunisie",
        "developpe_par": "EDUSPHERE Team",
        "endpoints_disponibles": {
            "accueil": "GET /",
            "sante": "GET /sante",
            "regles": "GET /regles",
            "analyser": "POST /analyser",
            "ajouter_regle": "POST /regles"
        },
        "message": "Prêt à être intégré avec kids.edusphere.tn"
    }

@app.get("/sante")
async def check_health():
    """Vérifie la santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ia-edusphere-tunisie",
        "regles_chargees": len(REGLES_PEDAGOGIQUES)
    }

@app.get("/regles")
async def get_rules(langue: Optional[str] = None):
    """Récupère toutes les règles pédagogiques"""
    if langue:
        regles_filtrees = [r for r in REGLES_PEDAGOGIQUES if r["langue"] == langue]
        return {
            "langue": langue,
            "total": len(regles_filtrees),
            "regles": regles_filtrees
        }
    
    return {
        "total": len(REGLES_PEDAGOGIQUES),
        "par_langue": {
            "francais": len([r for r in REGLES_PEDAGOGIQUES if r["langue"] == "fr"]),
            "arabe": len([r for r in REGLES_PEDAGOGIQUES if r["langue"] == "ar"])
        },
        "regles": REGLES_PEDAGOGIQUES
    }

@app.post("/analyser", response_model=AnalyseResponse)
async def analyser_texte(request: AnalyseRequest):
    """
    Analyse une réponse d'élève et propose des corrections
    """
    corrections_trouvees = []
    exercices_suggérés = []
    
    texte_minuscule = request.texte.lower()
    
    # Recherche des erreurs dans le texte
    for regle in REGLES_PEDAGOGIQUES:
        # Si langue spécifiée, ne chercher que dans cette langue
        if request.langue and regle["langue"] != request.langue:
            continue
            
        if regle["erreur"].lower() in texte_minuscule:
            correction = Correction(
                erreur=regle["erreur"],
                correction=regle["correction"],
                type_erreur=regle["type"],
                explication=regle["explication"],
                exercice_suggere=regle["exercice"]
            )
            corrections_trouvees.append(correction)
            exercices_suggérés.append(regle["exercice"])
    
    # Préparation de la réponse
    message = "✅ Analyse terminée"
    if corrections_trouvees:
        message = f"🔍 {len(corrections_trouvees)} correction(s) suggérée(s)"
    
    return AnalyseResponse(
        success=True,
        timestamp=datetime.now().isoformat(),
        eleve_id=request.eleve_id,
        texte_analyse=request.texte,
        corrections=corrections_trouvees,
        exercices_suggestion=list(set(exercices_suggérés)),  # Évite les doublons
        message=message
    )

@app.post("/regles")
async def ajouter_regle(
    erreur: str,
    correction: str,
    type_erreur: str = "personnalise",
    explication: str = "",
    exercice: str = "",
    langue: str = "fr",
    niveau: str = "tous"
):
    """Ajoute une nouvelle règle pédagogique"""
    nouvelle_regle = {
        "erreur": erreur,
        "correction": correction,
        "type": type_erreur,
        "explication": explication or f"Correction de '{erreur}' en '{correction}'",
        "exercice": exercice or f"h5p/personnalise-{type_erreur}",
        "langue": langue,
        "niveau": niveau,
        "date_ajout": datetime.now().isoformat()
    }
    
    REGLES_PEDAGOGIQUES.append(nouvelle_regle)
    
    return {
        "success": True,
        "message": f"Règle ajoutée : '{erreur}' → '{correction}'",
        "total_regles": len(REGLES_PEDAGOGIQUES),
        "regle": nouvelle_regle
    }

# ==================== CONFIGURATION SERVEUR ====================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print("=" * 50)
    print("🚀 IA EDUSPHERE KIDS TUNISIE")
    print(f"📚 Règles chargées : {len(REGLES_PEDAGOGIQUES)}")
    print(f"🌍 URL : http://localhost:{port}")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=port)
@app.post("/decision")
def decision(data: dict):
    score = data.get("score", 0)

    if score >= 80:
        decision = "avancer"
    elif score >= 50:
        decision = "consolider"
    else:
        decision = "changer_modalite"

    return {
        "decision": decision,
        "message": "Décision pédagogique générée"
    }
