# 🦺 Sistema de Detección de Cascos de Seguridad

Sistema de detección en tiempo real de cascos de seguridad usando YOLOv8 y Angular. Permite detectar si las personas llevan casco de protección mediante imágenes, cámara web o archivos.

## 🚀 Características

- **Detección por imagen**: Sube una imagen y obtén el análisis de seguridad
- **Detección en tiempo real**: Usa tu cámara web para monitoreo continuo
- **API REST**: Backend FastAPI con endpoints para diferentes tipos de detección
- **Alertas WhatsApp**: Notificaciones automáticas ante situaciones de riesgo
- **Interfaz moderna**: Frontend Angular con diseño responsivo

## 🛠️ Tecnologías

### Backend
- Python 3.11
- FastAPI
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy

### Frontend
- Angular 20
- TypeScript
- RxJS

## 📋 Requisitos

- Python 3.11+
- Node.js 18+
- npm o yarn
- Cámara web (para detección en tiempo real)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd deteccion-cascos
```

### 2. Configurar Backend (API)

```bash
cd iape
pip install -r requirements.txt
```

### 3. Configurar Frontend

```bash
cd deteccion-cascos
npm install
```

## ▶️ Ejecución

### Iniciar Backend

```bash
cd iape
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

### Iniciar Frontend

```bash
cd deteccion-cascos
npm start
```

La aplicación estará disponible en: `http://localhost:4200`

## 📡 API Endpoints

- `GET /` - Estado de la API
- `POST /detect/` - Detección con imagen (devuelve JSON)
- `POST /detect/image` - Detección con imagen (devuelve imagen anotada)
- `GET /detect/from-file` - Detección desde archivo local
- `GET /camera/snapshot` - Captura y detecta desde cámara
- `POST /alert/whatsapp` - Enviar alerta por WhatsApp

## ⚙️ Configuración

### Variables de entorno (Backend)

Crea un archivo `.env` en la carpeta `iape`:

```env
MODEL_PATH=best.pt
CONFIDENCE_THRESHOLD=0.1
ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
WHATSAPP_API_KEY=tu_api_key
WHATSAPP_PHONE=tu_telefono
```

### Configuración Frontend

Edita `deteccion-cascos/src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

## 📊 Modelo YOLOv8

El modelo `best.pt` está entrenado para detectar:
- **helmet**: Cascos de seguridad
- **head**: Cabezas sin protección

## 🎯 Uso

1. Selecciona el modo de detección:
   - **Subir imagen**: Carga una imagen desde tu dispositivo
   - **Tiempo real**: Activa tu cámara para monitoreo continuo

2. El sistema analizará y mostrará:
   - Número de cascos detectados
   - Número de personas sin casco
   - Estado de seguridad (Seguro/Riesgo)
   - Imagen anotada con las detecciones

## 👥 Grupo 5 - UNSM

Proyecto desarrollado para el curso de la Universidad Nacional de San Martín.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio.
