# Dockerfile simplifié pour IA EDUSPHERE
FROM python:3.11-slim

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers requis
COPY requirements.txt .
COPY main.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "main.py"]
