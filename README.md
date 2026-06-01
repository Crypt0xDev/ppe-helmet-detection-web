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
| Validates helmet position on head | Live camera monitoring | WhatsApp notifications |

</div>

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 Smart Detection
- **Position Validation**: Verifies helmet is properly worn on head
- **Dual Detection**: Separate classes for `helmet` (worn) and `head` (exposed)
- **False Positive Prevention**: Ignores helmets held in hands or on the ground
- **Confidence Threshold**: Filters detections below 35% confidence

</td>
<td width="50%">

### 📊 Real-Time Monitoring
- **Live Camera Feed**: Continuous webcam surveillance every 800ms
- **Instant Analysis**: Frame-by-frame processing with YOLOv8
- **Live Statistics**: Safe/unsafe detection counter with timestamps
- **Visual Feedback**: Annotated image with bounding boxes

</td>
</tr>
<tr>
<td width="50%">

### 🚨 Alert System
- **WhatsApp Integration**: Automatic alerts via CallMeBot API
- **Audio Alerts**: Web Audio API sound on violation detected
- **Visual Indicators**: Green (safe) / Red (risk) color-coded status
- **Keep-Alive**: GitHub Actions pings API every 25 min to prevent cold starts

</td>
<td width="50%">

### 💻 Modern Interface
- **Responsive Design**: Mobile, tablet, desktop optimized
- **Angular Signals**: Reactive UI with zero boilerplate
- **Warm-up Banner**: Notifies user when AI service is starting
- **Two Modes**: Static image upload + real-time camera detection

</td>
</tr>
</table>

## 🛠️ Technology Stack

**Frontend:**
- Angular 20.3 with Signals Architecture
- TypeScript 5.9 for type safety
- TailwindCSS for styling
- Standalone Components (no NgModules)

**Backend (API):**
- FastAPI (Python) — high-performance async API
- YOLOv8 (Ultralytics) for object detection
- OpenCV for image processing and annotation
- Deployed on Hugging Face Spaces (free tier)

**Infrastructure:**
- Vercel — frontend hosting with auto-deploy on push
- GitHub Actions — keep-alive ping every 25 min to HF Spaces

---

## 🚀 Installation & Usage

### Prerequisites

- Node.js 18+ and npm
- Git

### Local Setup

```bash
# Clone repository
git clone https://github.com/Crypt0xDev/PPE-Helmet-Detection-Web.git
cd PPE-Helmet-Detection-Web

# Install dependencies
npm install

# Start in development mode
npm start
```

App available at `http://localhost:4200`

The dev environment points to `http://localhost:7860` by default. To use the production API instead, edit [`src/environments/environment.development.ts`](src/environments/environment.development.ts).

### Build for Production

```bash
npm run build:prod
```

---

## ⚙️ Configuration

The project uses Angular environment files — no `.env` file needed.

**`src/environments/environment.development.ts`** — local development:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:7860'
};
```

**`src/environments/environment.ts`** — production:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://crypt0xdev-ppe-helmet-detection-api.hf.space'
};
```

To run the backend locally, clone the API repo and follow its setup instructions:
```bash
git clone https://huggingface.co/spaces/Crypt0xDev/PPE-Helmet-Detection-API
cd PPE-Helmet-Detection-API
pip install -r requirements.txt
python app.py
```

---

## 📡 API Endpoints

**Base URL:** `https://crypt0xdev-ppe-helmet-detection-api.hf.space`  
**Docs:** `/docs` (Swagger UI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/detect/` | Detect helmets → JSON response |
| `POST` | `/detect/image` | Detect helmets → annotated image |
| `POST` | `/alert/whatsapp` | Send WhatsApp alert via CallMeBot |

**Example JSON response from `/detect/`:**
```json
{
  "message": "🔴 RIESGO: Se detectaron 2 persona(s) sin casco PUESTO.",
  "safe": false,
  "total": 3,
  "con_casco": 1,
  "sin_casco": 2,
  "porcentaje_con_casco": 33.33,
  "porcentaje_sin_casco": 66.67
}
```

---

## 📂 Project Structure

```
PPE-Helmet-Detection-Web/
├── src/
│   ├── app/
│   │   ├── app.ts              # Main component — all detection logic
│   │   ├── app.html            # UI template
│   │   ├── app.css             # Component styles
│   │   ├── app.config.ts       # Angular bootstrap config
│   │   └── app.routes.ts       # Routes (single-page, currently empty)
│   ├── environments/
│   │   ├── environment.ts              # Production API URL
│   │   └── environment.development.ts  # Local API URL
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── .github/
│   └── workflows/
│       └── keep-alive.yml      # Pings HF Spaces API every 25 min
├── public/
├── angular.json
├── package.json
└── README.md
```

---

## 👨‍💻 Author

**Crypt0xDev**
- GitHub: [@Crypt0xDev](https://github.com/Crypt0xDev)
- Hugging Face: [@Crypt0xDev](https://huggingface.co/Crypt0xDev)

---

## 🙏 Acknowledgements

- Universidad Nacional de San Martín (UNSM)
- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLOv8
- Angular team for the Signals API
- Hugging Face for free ML model hosting

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**🎓 Academic Project**  
Developed for Universidad Nacional de San Martín (UNSM) · 2025

[⬆ Back to top](#️-ppe-helmet-detection-system)

</div>
