# Ì∂∫ Frontend - Sistema de Detecci√≥n de Cascos

Frontend Angular para sistema de detecci√≥n de cascos de seguridad usando YOLOv8.

## Ì∫Ä Deploy en Vercel

Aplicaci√≥n desplegada en: **https://deteccion-cascos.vercel.app**

### Configuraci√≥n

El frontend se conecta autom√°ticamente con el backend. Para cambiar la URL del backend:

1. Edita `src/environments/environment.ts`
2. Actualiza `apiUrl` con la URL de Railway
3. Commit y push (Vercel redespliega autom√°ticamente)

## Ìª†Ô∏è Desarrollo Local

### Requisitos

- Node.js 18+
- npm

### Instalaci√≥n

```bash
# Clonar repositorio
git clone https://github.com/Crypt0xDev/deteccion-cascos.git
cd deteccion-cascos

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm start
```

La aplicaci√≥n estar√° disponible en: http://localhost:4200

### Build de producci√≥n

```bash
npm run build
```

## Ì≥¶ Estructura del Proyecto

```
deteccion-cascos/
‚îú‚îÄ‚îÄ src/
‚îÇ   ‚îú‚îÄ‚îÄ app/               # Componentes Angular
‚îÇ   ‚îú‚îÄ‚îÄ environments/      # Configuraci√≥n de entornos
‚îÇ   ‚îî‚îÄ‚îÄ index.html
‚îú‚îÄ‚îÄ public/                # Archivos est√°ticos
‚îú‚îÄ‚îÄ angular.json           # Configuraci√≥n Angular
‚îú‚îÄ‚îÄ package.json
‚îî‚îÄ‚îÄ README.md
```

## Ì¥ß Tecnolog√≠as

- Angular 20
- TypeScript 5.6
- RxJS 7.8
- Zone.js 0.15

## Ìºê Caracter√≠sticas

- **Detecci√≥n por imagen**: Sube una imagen y obt√©n an√°lisis de seguridad
- **Detecci√≥n en tiempo real**: Usa c√°mara web para monitoreo continuo
- **Interfaz responsiva**: Dise√±o moderno y adaptable
- **Notificaciones**: Integraci√≥n con WhatsApp v√≠a backend

## Ì¥ó Enlaces

- **Backend**: https://github.com/Crypt0xDev/deteccion-cascos-backend
- **Despliegue**: https://deteccion-cascos.vercel.app

## Ì≥ù Configuraci√≥n de Entornos

### Production (`src/environments/environment.ts`)

```typescript
export const environment = {
  production: true,
  apiUrl: 'TU-URL-DE-RAILWAY'  // Actualizar con URL de Railway
};
```

### Development (`src/environments/environment.development.ts`)

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'  // Backend local
};
```

## Ì∫Ä Scripts Disponibles

```bash
npm start          # Servidor de desarrollo
npm run build      # Build de producci√≥n
npm test           # Ejecutar tests
npm run watch      # Build en modo watch
```
