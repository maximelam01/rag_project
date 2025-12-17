FROM python:3.11-slim

WORKDIR /app

# Copier backend et frontend
COPY backend/ /app/backend
COPY frontend/ /app/frontend
COPY .env /app/

# Installer dépendances Python
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Expose le port
EXPOSE 8080

# Lancer FastAPI
CMD ["uvicorn", "backend.rag:app", "--host", "0.0.0.0", "--port", "8080"]
