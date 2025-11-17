from ultralytics import YOLO
import cv2

# Cargar el modelo entrenado
model = YOLO("best.pt")  # asegúrate de que el archivo best.pt esté en la misma carpeta

# Ruta de imagen a probar
image_path = "test.jpg"  # pon aquí el nombre de tu imagen (por ejemplo una foto con casco)

# Realizar la detección
results = model.predict(source=image_path, conf=0.25, save=True, show=True)

# Mostrar información
for result in results:
    print(result.names)       # nombres de clases
    print(result.boxes.data)  # coordenadas, confianza, clase
