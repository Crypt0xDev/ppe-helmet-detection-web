# 🛡️ Sistema de Detección de EPP con IA

<div align="center">

![Angular](https://img.shields.io/badge/Angular-20.3-DD0031?style=flat-square&logo=angular)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)

**Detección automática de equipos de protección personal mediante Computer Vision**

</div>

## 📋 Descripción

Sistema web que detecta el uso de **cascos de seguridad** en tiempo real mediante inteligencia artificial. Diseñado para entornos industriales y de construcción.

**Características principales:**
- Análisis de imágenes estáticas y video en tiempo real
- Alertas automáticas vía WhatsApp
- Panel de estadísticas en vivo
- Interfaz responsive y moderna

## 🛠️ Stack Tecnológico

**Frontend:** Angular 20, TypeScript, TailwindCSS  
**Backend:** FastAPI, Python  
**IA:** YOLO v8, OpenCV, PyTorch  
**Integraciones:** WhatsApp Business API

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/Crypt0xDev/deteccion-cascos.git
cd deteccion-cascos

# Instalar dependencias
npm install

# Iniciar aplicación
npm start
```

Aplicación disponible en `http://localhost:4200`

**Backend API:** Requiere Python 3.8+ y FastAPI corriendo en `http://localhost:8000`

## 📡 API Endpoints

```typescript
POST /detect/              → Análisis de imagen
POST /detect/image         → Imagen con anotaciones
POST /alert/whatsapp       → Envío de alertas
```

## 🏗️ Arquitectura

```
Frontend (Angular) → API (FastAPI) → Modelo IA (YOLO v8)
```

## 👥 Equipo

**Proyecto Grupo 5 - UNSM**  
Desarrollo, IA y Testing

## 📝 Licencia

Prototipo educativo - Universidad Nacional de San Martín

---

<div align="center">

**Desarrollado para mejorar la seguridad industrial** 🛡️

⚠️ Prototipo educativo · No usar en producción sin entrenamiento adicional

</div>

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
