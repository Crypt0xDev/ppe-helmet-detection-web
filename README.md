# 🛡️ Sistema de Detección de EPP con IA

<div align="center">

![Angular](https://img.shields.io/badge/Angular-20.3-DD0031?style=flat-square&logo=angular)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?style=flat-square&logo=typescript)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production-success?style=flat-square)

**Detección automática de equipos de protección personal mediante Computer Vision**

[Demo en Vivo](#) • [API Backend](https://huggingface.co/spaces/Crypt0xDev/PPE-Helmet-Detection-API) • [Reportar Bug](https://github.com/Crypt0xDev/deteccion-cascos/issues)

</div>

---

## 📋 Descripción

Sistema web inteligente que detecta el **uso correcto de cascos de seguridad** en tiempo real mediante inteligencia artificial avanzada. Diseñado para entornos industriales, construcción y minería.

### ✨ Características Principales

- 🎯 **Detección Inteligente**: Verifica que el casco esté correctamente puesto en la cabeza (no solo detectado)
- 📸 **Análisis de Imágenes**: Procesamiento de fotografías estáticas con resultados instantáneos
- 🎥 **Monitoreo en Tiempo Real**: Vigilancia continua mediante cámara web
- 📊 **Estadísticas en Vivo**: Panel con métricas de seguridad actualizadas
- 🚨 **Alertas Automáticas**: Notificaciones vía WhatsApp ante detección de riesgos
- 📱 **Diseño Responsive**: Interfaz adaptable a móviles, tablets y escritorio
- ⚡ **Alto Rendimiento**: Procesamiento optimizado con YOLOv8

### 🎯 Problema Resuelto

**Antes:** Si 3 personas tenían cascos en las manos, el sistema contaba incorrectamente 3 personas "con casco".

**Ahora:** El sistema verifica mediante asociación espacial que el casco esté correctamente puesto sobre la cabeza:
- ✅ Detección dual: cascos y cabezas por separado
- ✅ Verificación de superposición horizontal > 30%
- ✅ Validación de distancia vertical y posición correcta
- ✅ IoU (Intersection over Union) > 0.1
- ⚠️ Identifica cascos no puestos (en manos, suelo, etc.)

---

## 🛠️ Stack Tecnológico

**Frontend:**
- Angular 20.3 con Signals
- TypeScript 5.9
- TailwindCSS para estilos
- Standalone Components

**Backend (API):**
- FastAPI (Python)
- YOLOv8 para detección
- OpenCV para procesamiento de imágenes
- Hugging Face Spaces para hosting

**Integraciones:**
- WhatsApp Business API
- Twilio para notificaciones

---

## 🚀 Instalación y Uso

### Prerrequisitos

- Node.js 18+ y npm
- Git

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/Crypt0xDev/deteccion-cascos.git
cd deteccion-cascos

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

## ⚙️ Configuración

### Variables de Entorno

El proyecto utiliza dos archivos de configuración en `src/environments/`:

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
deteccion-cascos/
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

**⚠️ Prototipo Educativo**  
Desarrollado como proyecto académico para UNSM • 2025

[⬆ Volver arriba](#️-sistema-de-detección-de-epp-con-ia)

</div>
