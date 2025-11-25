<div align="center">

# 🛡️ PPE Helmet Detection System

### Intelligent Safety Compliance Monitoring with Computer Vision

[![Angular](https://img.shields.io/badge/Angular-20.3-DD0031?style=for-the-badge&logo=angular&logoColor=white)](https://angular.io/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Detection-00FFFF?style=for-the-badge&logo=pytorch&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)](https://deteccion-cascos.vercel.app/)

[🚀 **Live Demo**](https://deteccion-cascos.vercel.app/) • [🔧 **API Backend**](https://huggingface.co/spaces/Crypt0xDev/PPE-Helmet-Detection-API) • [📝 **Report Issue**](https://github.com/Crypt0xDev/PPE-Helmet-Detection-Web/issues)

---

</div>

## 📋 Overview

> **Advanced web-based system for real-time detection of proper safety helmet usage using computer vision technology.**

Designed specifically for **industrial environments**, **construction sites**, and **mining operations** to ensure workplace safety compliance and reduce accidents.

<div align="center">

| 🎯 Accurate Detection | 🎥 Real-Time Analysis | 🚨 Instant Alerts |
|:---:|:---:|:---:|
| Validates helmet position | Live camera monitoring | WhatsApp notifications |

</div>

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Smart Detection
- **Position Validation**: Verifies helmet is properly worn on head
- **Dual Detection**: Separate detection for helmets and heads
- **Spatial Association**: IoU > 0.1 with horizontal overlap > 30%
- **False Positive Prevention**: Identifies helmets in hands/ground

</td>
<td width="50%">

### 📊 Real-Time Monitoring
- **Live Camera Feed**: Continuous webcam surveillance
- **Instant Analysis**: Real-time processing with YOLOv8
- **Live Statistics**: Updated safety metrics dashboard
- **Visual Feedback**: Annotated detection results

</td>
</tr>
<tr>
<td width="50%">

### 🚨 Alert System
- **WhatsApp Integration**: Automatic notifications
- **Audio Alerts**: Sound warnings for violations
- **Visual Indicators**: Color-coded status display
- **Compliance Tracking**: Historical data analysis

</td>
<td width="50%">

### 💻 Modern Interface
- **Responsive Design**: Mobile, tablet, desktop optimized
- **Professional UI**: Dark theme with gradient effects
- **Smooth Animations**: 60fps transitions
- **Intuitive Controls**: User-friendly operation

</td>
</tr>
</table>

## 🎯 Problem Solved

<div align="center">

### ❌ Before vs ✅ After

| Previous System | Our Solution |
|:---|:---|
| ❌ Counted helmets in hands as "worn" | ✅ Validates helmet is on head |
| ❌ False positives with carried helmets | ✅ Spatial association verification |
| ❌ Inaccurate compliance reporting | ✅ Precise position detection |

</div>

**Technical Approach:**
```python
# Validation Algorithm
✅ Dual Detection: Helmets + Heads detected separately
✅ Horizontal Overlap: > 30% required
✅ Vertical Distance: Validated positioning
✅ IoU Threshold: > 0.1 (Intersection over Union)
⚠️  Unmatched Helmets: Flagged as not worn
```

---

## 🛠️ Technology Stack

**Frontend:**
- Angular 20.3 with Signals Architecture
- TypeScript 5.9 for type safety
- TailwindCSS for modern styling
- Standalone Components

**Backend (API):**
- FastAPI (Python) - High-performance API
- YOLOv8 for object detection
- OpenCV for image processing
- Hugging Face Spaces deployment

**Integrations:**
- WhatsApp Business API
- Real-time notification system

---

## 🚀 Installation & Usage

### Prerequisites

- Node.js 18+ and npm
- Git

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/Crypt0xDev/PPE-Helmet-Detection-Web.git
cd PPE-Helmet-Detection-Web

# Instalar dependencias
npm install

# Iniciar en modo desarrollo
npm start
```

La aplicación estará disponible en `http://localhost:4200`

### Compilar para Producción

```bash
npm run build:prod
```

Los archivos compilados estarán en `dist/`

---

## ⚙️ Configuration

### Environment Variables

The project uses two configuration files in `src/environments/`:

**`environment.development.ts`** (Desarrollo):
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:7860'  // API local
};
```

**`environment.ts`** (Producción):
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://crypt0xdev-ppe-helmet-detection-api.hf.space'
};
```

---

## 📡 API Backend

La API está desplegada en Hugging Face Spaces:

**URL:** `https://crypt0xdev-ppe-helmet-detection-api.hf.space`

### Endpoints Principales

**GET /** - Health check
```json
{
  "status": "ok",
  "message": "API de Detección de Cascos funcionando."
}
```

**POST /detect/** - Analizar imagen
- Input: `multipart/form-data` con archivo de imagen
- Output: JSON con resultados de detección

```json
{
  "message": "🔴 RIESGO: Se detectaron 3 persona(s) sin casco PUESTO.",
  "safe": false,
  "total": 3,
  "con_casco": 0,
  "sin_casco": 3,
  "unmatched_helmets": 3,
  "warning": "⚠️ 3 casco(s) detectado(s) pero NO puesto(s) en la cabeza"
}
```

**POST /detect/image** - Obtener imagen anotada
- Input: `multipart/form-data` con archivo de imagen
- Output: Imagen con detecciones dibujadas

**POST /alert/whatsapp** - Enviar alerta
- Input: JSON con mensaje
```json
{ "message": "⚠️ Alerta de seguridad" }
```

---

## 📂 Estructura del Proyecto

```
PPE-Helmet-Detection-Web/
├── src/
│   ├── app/
│   │   ├── app.ts              # Componente principal
│   │   ├── app.html            # Template
│   │   ├── app.css             # Estilos
│   │   ├── app.config.ts       # Configuración
│   │   └── app.routes.ts       # Rutas
│   ├── environments/
│   │   ├── environment.ts              # Producción
│   │   └── environment.development.ts  # Desarrollo
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── public/                     # Assets estáticos
├── .github/                    # GitHub Actions
├── angular.json
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🎨 Modos de Operación

### 1. Análisis de Imagen Estática
Carga una fotografía para obtener un análisis detallado de uso de EPP con resultados instantáneos y precisos.

### 2. Monitoreo en Tiempo Real
Activa la cámara para vigilancia continua con alertas automáticas ante detección de riesgos de seguridad.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Crypt0xDev**
- GitHub: [@Crypt0xDev](https://github.com/Crypt0xDev)
- Hugging Face: [@Crypt0xDev](https://huggingface.co/Crypt0xDev)

---

## 🙏 Agradecimientos

- Universidad Nacional de San Martín (UNSM)
- Ultralytics por YOLOv8
- Comunidad de Angular
- Hugging Face por el hosting gratuito

---

## 📊 Estado del Proyecto

✅ **Producción** - Sistema estable y funcionando correctamente

### Próximas Mejoras
- [ ] Soporte para detección de otros EPP (arneses, guantes, gafas)
- [ ] Dashboard de administración
- [ ] Exportación de reportes PDF
- [ ] Multi-idioma (i18n)
- [ ] Modo offline con IndexedDB

---

<div align="center">

**🎓 Academic Project**
Developed for Universidad Nacional de San Martín (UNSM) • 2025

[⬆ Back to top](#️-ppe-helmet-detection---ai-safety-system)

</div>
