from ultralytics import YOLO
import cv2
import os
import winsound  # ALERTA SONORA EN WINDOWS

# Ruta absoluta del modelo entrenado
model_path = r"D:\gaaaaaaaaa\iape\iape\best.pt"

# Verificar modelo
if not os.path.exists(model_path):
    print(f"❌ No se encontró el modelo en {model_path}")
    exit()

# Cargar modelo
model = YOLO(model_path)
print("✅ Modelo cargado correctamente")

# Inicializar cámara
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("❌ No se pudo acceder a la cámara.")
    exit()

print("🎥 Cámara iniciada. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar detección
    results = model.predict(source=frame, conf=0.4, save=False, verbose=False)
    res = results[0]

    # Contadores
    helmet_detected = False
    head_detected = False

    # Procesar detecciones
    for box in res.boxes:
        cls = int(box.cls[0])
        label = res.names[cls]
        conf = float(box.conf[0])

        # Coordenadas
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Colores para dibujar
        if label == "helmet":
            helmet_detected = True
            color = (0, 255, 0)
        elif label == "head":
            head_detected = True
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)

        # Dibujar caja
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {conf:.2f}", 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 

                    0.6, color, 2)

    # ------------ MENSAJES Y ALERTAS --------------
    if head_detected and not helmet_detected:
        status = "🚨 CASO DETECTADO: Persona sin casco"
        color_status = (0, 0, 255)

        # ALERTA SONORA (una vez por frame)
        winsound.Beep(1000, 300)  # frecuencia 1000Hz, 300ms

    elif helmet_detected:
        status = "🟢 CASCO DETECTADO: EPP correcto"
        color_status = (0, 255, 0)
    else:
        status = "⚠️ Sin personas detectadas"
        color_status = (0, 255, 255)

    # Mostrar mensaje en pantalla
    cv2.putText(frame, status, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                color_status, 3)

    # Mostrar ventana con resultados
    cv2.imshow("Detección de Casco y Cabeza (EPP)", frame)

    # Salida con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
