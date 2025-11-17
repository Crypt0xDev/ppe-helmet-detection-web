# API de Detección de Cascos - Backend

Backend para detección de cascos usando YOLOv8 y FastAPI.

## 🚀 Deployment en Render

1. Crear cuenta en [Render.com](https://render.com)
2. Conectar repositorio de GitHub
3. Crear nuevo "Web Service"
4. Configurar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `MODEL_PATH=best.pt`
     - `CONFIDENCE_THRESHOLD=0.1`
     - `WHATSAPP_API_KEY=tu_key`
     - `WHATSAPP_PHONE=51969833318`
     - `ALLOWED_ORIGINS=https://tu-app.vercel.app`

## 🏠 Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Estructura

```
iape/
├── best.pt              # Modelo entrenado YOLOv8
├── requirements.txt     # Dependencias Python
├── src/
│   └── app.py          # API FastAPI
└── .env                # Variables de entorno (local)
```
