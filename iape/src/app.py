from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from ultralytics import YOLO
import cv2
import numpy as np
import io
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from typing import Optional
from urllib.parse import quote


# --- CONFIGURACIÓN DE LA API ---
app = FastAPI(
    title="API de Detección de Cascos YOLOv8",
    description="Permite subir una imagen y devuelve el conteo de cascos y la imagen anotada."
)

# Habilitar CORS para el frontend Angular (localhost:4200 y producción)
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", 
    "https://deteccion-cascos.vercel.app,http://localhost:4200,http://127.0.0.1:4200"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta del modelo (relativa desde la raíz del proyecto)
MODEL_PATH = os.getenv("MODEL_PATH", "best.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.1"))

# CallMeBot configuración
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "7457414")
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "51969833318")

model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = YOLO(MODEL_PATH)
        print("✅ Modelo YOLOv8 cargado con éxito.")
    except Exception as e:
        print(f"❌ Error al cargar el modelo en {MODEL_PATH}: {e}")
        raise RuntimeError("No se pudo cargar el modelo de detección.")

def _count_detections(res):
    helmet_count = 0
    head_count = 0
    for box in res.boxes:
        cls_id = int(box.cls[0])
        cls_name = res.names[cls_id]
        if cls_name.lower() == "helmet":
            helmet_count += 1
        elif cls_name.lower() == "head":
            head_count += 1
    return helmet_count, head_count

def _status_from_counts(helmet_count, head_count):
    if head_count > helmet_count:
        return "🔴 RIESGO: Se detectaron personas sin casco.", False
    elif head_count > 0 and helmet_count >= head_count:
        return "🟢 SEGURO: Todas las personas llevan casco.", True
    else:
        return "⚠️ No se detectaron personas.", True

@app.get("/")
def read_root():
    """Endpoint de prueba."""
    return {"status": "ok", "message": "API de Detección de Cascos funcionando."}

@app.post("/detect/")
async def detect_hard_hats(file: UploadFile = File(...)):
    """
    Recibe una imagen (multipart/form-data), realiza la detección
    de cascos y devuelve el conteo y la imagen anotada.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo subido no es una imagen válida.")
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen.")

    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False)
    res = results[0]
    helmet_count, head_count = _count_detections(res)
    annotated_frame = res.plot()
    is_success, buffer = cv2.imencode(".jpg", annotated_frame)
    if not is_success:
        raise HTTPException(status_code=500, detail="Error al codificar la imagen de resultado.")

    status_message, safe = _status_from_counts(helmet_count, head_count)
    metadata = {
        "status_message": status_message,
        "safe": safe,
        "helmet_count": helmet_count,
        "head_count": head_count
    }
    return metadata

@app.post("/detect/image")
async def detect_with_image(file: UploadFile = File(...)):
    """Devuelve la imagen anotada en lugar de JSON."""
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen.")

    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False)
    annotated_frame = results[0].plot()
    ok, buffer = cv2.imencode(".jpg", annotated_frame)
    if not ok:
        raise HTTPException(status_code=500, detail="Error al codificar.")
    return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

@app.get("/detect/from-file")
def detect_from_file(path: str = Query(..., description="Ruta absoluta del archivo de imagen"),
                     return_image: bool = Query(False, description="Devolver imagen anotada")):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"No existe el archivo: {path}")
    frame = cv2.imread(path)
    if frame is None:
        raise HTTPException(status_code=400, detail="No se pudo leer la imagen.")

    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False)
    res = results[0]
    helmet_count, head_count = _count_detections(res)
    status_message, safe = _status_from_counts(helmet_count, head_count)

    annotated_frame = res.plot()
    ok, buffer = cv2.imencode(".jpg", annotated_frame)
    if not ok:
        raise HTTPException(status_code=500, detail="Error al codificar la imagen de resultado.")

    if return_image:
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")
    else:
        return {
            "status_message": status_message,
            "safe": safe,
            "helmet_count": helmet_count,
            "head_count": head_count,
            "source": path
        }

@app.get("/camera/snapshot")
def camera_snapshot(index: int = Query(0), return_image: bool = Query(False)):
    """
    Toma un frame de la cámara, corre detección y devuelve JSON o imagen anotada.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado.")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise HTTPException(status_code=500, detail=f"No se pudo abrir la cámara index={index}.")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise HTTPException(status_code=500, detail="No se pudo capturar un frame.")

    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False)
    res = results[0]
    helmet_count, head_count = _count_detections(res)
    status_message, safe = _status_from_counts(helmet_count, head_count)

    annotated = res.plot()
    ok, buffer = cv2.imencode(".jpg", annotated)
    if not ok:
        raise HTTPException(status_code=500, detail="Error al codificar la imagen de resultado.")
    if return_image:
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")
    else:
        return {
            "status_message": status_message,
            "safe": safe,
            "helmet_count": helmet_count,
            "head_count": head_count
        }

# --- CallMeBot WhatsApp Alert ---
class WhatsAppAlert(BaseModel):
    message: str

@app.post("/alert/whatsapp")
def send_whatsapp_alert(payload: WhatsAppAlert):
    """
    Envía una alerta por WhatsApp usando CallMeBot.
    """
    encoded_text = quote(payload.message)

    url = (
        f"https://api.callmebot.com/whatsapp.php?"
        f"phone={WHATSAPP_PHONE}&apikey={WHATSAPP_API_KEY}&text={encoded_text}"
    )

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return {
                "status": "ok",
                "sent": payload.message,
                "encoded": encoded_text,
                "to": WHATSAPP_PHONE
            }
        else:
            raise HTTPException(status_code=500, detail=f"Error CallMeBot: {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excepción al enviar: {str(e)}")