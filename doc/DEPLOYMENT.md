# 🚀 Guía de Deployment - Detección de Cascos

Proyecto completo con Frontend Angular + Backend FastAPI + YOLOv8

## 📁 Estructura del Proyecto

```
├── deteccion-eep/    → Frontend Angular (Vercel)
└── iape/             → Backend FastAPI (Render)
```

## 🎯 PASO A PASO - DEPLOYMENT GRATUITO

### 1️⃣ SUBIR A GITHUB (PRIMERO)

#### Opción A: Un repositorio con ambos proyectos
```bash
cd "c:/Users/alexi/Desktop/Curso UNSM/Poyecto grupo 5/Github"
git init
git add .
git commit -m "Initial commit: Frontend Angular + Backend FastAPI"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/deteccion-cascos.git
git push -u origin main
```

#### Opción B: Dos repositorios separados (Recomendado)
```bash
# Backend
cd iape
git init
git add .
git commit -m "Backend: API detección cascos YOLOv8"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/deteccion-cascos-backend.git
git push -u origin main

# Frontend
cd ../deteccion-eep
git init
git add .
git commit -m "Frontend: Angular detección cascos"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/deteccion-cascos-frontend.git
git push -u origin main
```

---

### 2️⃣ DEPLOY BACKEND EN RENDER (SEGUNDO)

1. **Ir a** → https://render.com
2. **Sign Up** → Con tu cuenta de GitHub (gratis)
3. **New +** → **Web Service**
4. **Conectar repositorio** → `deteccion-cascos-backend` (o `deteccion-cascos` si usaste monorepo)
5. **Configurar:**
   - **Name**: `deteccion-cascos-api`
   - **Region**: Oregon (más cerca a Perú)
   - **Root Directory**: `iape` (si es monorepo) o déjalo vacío
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free** ✅

6. **Environment Variables** (muy importante):
   ```
   MODEL_PATH=best.pt
   CONFIDENCE_THRESHOLD=0.1
   WHATSAPP_API_KEY=7457414
   WHATSAPP_PHONE=51969833318
   ALLOWED_ORIGINS=http://localhost:4200
   ```

7. **Create Web Service** → Espera 5-10 minutos

8. **Copiar URL** → Ejemplo: `https://deteccion-cascos-api.onrender.com`

---

### 3️⃣ ACTUALIZAR FRONTEND CON URL DEL BACKEND (TERCERO)

```bash
cd deteccion-eep
```

Editar `src/environments/environment.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://deteccion-cascos-api.onrender.com'  // ← Tu URL de Render
};
```

Guardar y hacer commit:
```bash
git add .
git commit -m "Update: Backend URL de Render"
git push
```

---

### 4️⃣ DEPLOY FRONTEND EN VERCEL (CUARTO)

1. **Ir a** → https://vercel.com
2. **Sign Up** → Con tu cuenta de GitHub (gratis)
3. **Add New** → **Project**
4. **Import** → `deteccion-cascos-frontend`
5. **Configurar:**
   - **Framework Preset**: Angular ✅ (detecta automáticamente)
   - **Root Directory**: `deteccion-eep` (si es monorepo) o déjalo vacío
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `dist/deteccion-eep/browser` (automático)

6. **Deploy** → Espera 2-3 minutos

7. **Copiar URL** → Ejemplo: `https://deteccion-cascos.vercel.app`

---

### 5️⃣ ACTUALIZAR CORS EN BACKEND (QUINTO)

1. Ir a **Render Dashboard** → Tu servicio
2. **Environment** → Editar `ALLOWED_ORIGINS`
3. Cambiar a:
   ```
   https://deteccion-cascos.vercel.app,http://localhost:4200
   ```
4. **Save Changes** → Se reiniciará automáticamente

---

## ✅ VERIFICAR QUE TODO FUNCIONE

1. Abrir `https://deteccion-cascos.vercel.app`
2. Subir una imagen
3. Debería detectar cascos correctamente

---

## 💰 COSTOS

| Servicio | Plan | Costo |
|----------|------|-------|
| GitHub | Free | $0 |
| Render | Free | $0 (750 hrs/mes) |
| Vercel | Hobby | $0 |
| **TOTAL** | | **$0/mes** ✅ |

---

## ⚠️ LIMITACIONES DEL PLAN GRATUITO

### Render Free:
- Se "duerme" después de 15 minutos sin uso
- Primera petición tarda 30-60 segundos en despertar
- 750 horas/mes (suficiente para 1 mes)

### Vercel Hobby:
- Sin limitaciones prácticas para este proyecto
- 100 GB bandwidth/mes

---

## 🔧 COMANDOS ÚTILES

```bash
# Ver logs en Render
# → Dashboard → Logs (en tiempo real)

# Redesplegar Vercel
git push  # Automático

# Redesplegar Render
git push  # Automático
```

---

## 📝 SIGUIENTE PASO SI QUIERES DOMINIO PROPIO

1. Comprar dominio en Namecheap (~$8/año)
2. Configurar DNS en Vercel
3. ¡Listo!
