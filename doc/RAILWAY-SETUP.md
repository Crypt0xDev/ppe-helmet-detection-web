# 🚂 GUÍA PASO A PASO: DEPLOYMENT A RAILWAY

## ✅ VENTAJAS DE RAILWAY

- ✅ **512 MB RAM** (vs 256 MB en Render)
- ✅ **NO requiere tarjeta de crédito**
- ✅ **$5 de crédito gratis/mes** (500 horas)
- ✅ **Deploy desde GitHub automático**
- ✅ **Mejor para proyectos universitarios**

---

## 📋 PASOS A SEGUIR

### PASO 1: Crear cuenta en Railway

1. Ve a: https://railway.app
2. Haz clic en **"Login"**
3. Selecciona **"Login with GitHub"**
4. Autoriza Railway

---

### PASO 2: Crear nuevo proyecto

1. En Railway Dashboard, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona: `Crypt0xDev/deteccion-cascos`
4. Railway detectará automáticamente Python

---

### PASO 3: Configurar el servicio

1. **Root Directory**: Escribe `iape`
2. **Start Command**: Escribe `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
3. Haz clic en **"Deploy"**

---

### PASO 4: Agregar Variables de Entorno

En tu proyecto Railway:

1. Haz clic en tu servicio
2. Ve a la pestaña **"Variables"**
3. Agrega las siguientes:

```
MODEL_PATH=best.pt
CONFIDENCE_THRESHOLD=0.1
WHATSAPP_API_KEY=7457414
WHATSAPP_PHONE=51969833318
ALLOWED_ORIGINS=https://deteccion-cascos.vercel.app,http://localhost:4200
PORT=8080
```

4. Haz clic en **"Add"**

---

### PASO 5: Generar dominio público

1. Ve a la pestaña **"Settings"**
2. Busca **"Networking"**
3. Haz clic en **"Generate Domain"**
4. Copia tu URL: `https://deteccion-cascos-production.up.railway.app`

---

### PASO 6: Actualizar Frontend

Edita `deteccion-cascos/src/environments/environment.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://deteccion-cascos-production.up.railway.app'  // ← Tu URL de Railway
};
```

---

### PASO 7: Guardar cambios

```bash
cd "c:/Users/alexi/Desktop/Curso UNSM/Poyecto grupo 5/deteccion-cascos"

git add .
git commit -m "Update: Backend URL to Railway"
git push
```

Vercel se actualizará automáticamente.

---

## 🎯 VERIFICAR QUE FUNCIONE

1. **Prueba tu API directamente:**
   Visita: `https://tu-url.up.railway.app/`

2. **Prueba el frontend:**
   Visita: `https://deteccion-cascos.vercel.app`
   Sube una imagen → Debería detectar cascos

---

## 📊 COMANDOS ÚTILES

En Railway Dashboard:

- **Ver logs**: Pestaña "Deployments" → Click en el deployment → Ver logs
- **Ver métricas**: Pestaña "Metrics"
- **Redesplegar**: Se hace automático con cada `git push`
- **Ver variables**: Pestaña "Variables"

---

## 💰 PLAN GRATUITO

| Recurso | Cantidad |
|---------|----------|
| **RAM** | 512 MB |
| **CPU** | Shared |
| **Crédito mensual** | $5 (≈500 horas) |
| **Bandwidth** | 100 GB |
| **Builds** | Ilimitados |

---

## ❌ SOLUCIÓN DE PROBLEMAS

### Error en Build:
1. Ve a "Deployments"
2. Haz clic en el deployment fallido
3. Revisa los logs
4. Si hay error de dependencias, verifica `requirements.txt`

### App no responde:
1. Verifica que `PORT` esté en las variables
2. Verifica que el Start Command sea correcto
3. Revisa los logs en tiempo real

---

## ✅ VENTAJAS SOBRE RENDER

| Característica | Render Free | Railway Free |
|---------------|-------------|--------------|
| **RAM** | 256 MB ❌ | 512 MB ✅ |
| **Tarjeta requerida** | No | No |
| **Sleep automático** | 15 min | Variable |
| **Build time** | Lento | Rápido ⚡ |
| **Dashboard** | Básico | Moderno ✨ |

---

## 🎉 ¡LISTO!

Tu aplicación está desplegada en Railway con más memoria y mejor rendimiento.

**URL Backend:** `https://tu-app.up.railway.app`  
**URL Frontend:** `https://deteccion-cascos.vercel.app`

---

## 🔗 RECURSOS

- Dashboard Railway: https://railway.app/dashboard
- Documentación: https://docs.railway.app
- Soporte: https://discord.gg/railway
