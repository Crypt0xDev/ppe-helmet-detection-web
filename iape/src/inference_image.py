from ultralytics import YOLO
import os
import cv2

# --- CONFIGURACIÓN ---
model_path = r"D:\gaaaaaaaaa\iape\iape\best.pt"
image_path = r"D:\gaaaaaaaaa\iape\iape\src\gonald.jpeg"

confidence_threshold = 0.3  # nivel mínimo de confianza

# --- CARGAR MODELO ---
model = YOLO(model_path)
print(f"✅ Modelo cargado: {model_path}")

# --- REALIZAR DETECCIÓN ---
results = model.predict(source=image_path, conf=confidence_threshold, save=True, show=False)

# --- PROCESAR RESULTADOS ---
res = results[0]
detections = res.boxes.data.cpu().numpy() if res.boxes is not None else []

helmet_count = 0
head_count = 0

# Contar detecciones por clase
for box in res.boxes:
    cls_id = int(box.cls[0])
    cls_name = res.names[cls_id]
    if cls_name.lower() == "helmet":
        helmet_count += 1
    elif cls_name.lower() == "head":
        head_count += 1

# --- MOSTRAR RESULTADOS EN CONSOLA ---
print("\n📊 RESULTADOS DE DETECCIÓN:")
print(f"- Casco(s) detectado(s): {helmet_count}")
print(f"- Cabeza(s) detectada(s): {head_count}")

if helmet_count > 0:
    print("🟢 Se detectó equipo de protección (casco).")
elif head_count > 0:
    print("🔴 Se detectaron personas sin casco (riesgo).")
else:
    print("⚠️ No se detectaron personas ni cascos en la imagen.")

# --- GUARDAR Y MOSTRAR IMAGEN ---
output_dir = os.path.join(os.path.dirname(image_path), "runs/detect/predict")
if os.path.exists(res.save_dir):
    output_dir = res.save_dir

output_image = os.path.join(output_dir, os.path.basename(image_path))
print(f"\n📁 Resultado guardado en: {output_image}")

# Mostrar resultado si el entorno lo permite (sin errores Wayland)
try:
    annotated_image = res.plot()
    cv2.imshow("Resultado de detección", annotated_image)
    print("Presiona 'q' para cerrar la ventana...")
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
except Exception as e:
    print(f"(ℹ️ No se puede mostrar ventana: {e})")
