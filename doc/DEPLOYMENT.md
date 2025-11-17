# 🚀 Guía de Deployment - Detección de Cascos

Proyecto completo con Frontend Angular + Backend FastAPI + YOLOv8

## 📁 Estructura del Proyecto

```
├── deteccion-eep/    → Frontend Angular (Vercel)
└── iape/             → Backend FastAPI (Fly.io)
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

### 2️⃣ DEPLOY BACKEND EN FLY.IO (SEGUNDO)

#### A. Instalar Fly CLI

**Windows (PowerShell como Administrador):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Verificar instalación:**
```bash
fly version
```

#### B. Autenticarse en Fly.io

```bash
fly auth login
```
Se abrirá el navegador → Sign up con GitHub (gratis)

#### C. Desplegar el Backend

```bash
# Ir a la carpeta del backend
cd "c:/Users/alexi/Desktop/Curso UNSM/Poyecto grupo 5/deteccion-cascos/iape"

# Lanzar aplicación en Fly.io
fly launch

# Preguntas que te hará:
# 1. "Choose an app name" → deteccion-cascos (o el que prefieras)
# 2. "Choose a region" → gru (São Paulo - más cerca de Perú)
# 3. "Would you like to set up a PostgreSQL database?" → No
# 4. "Would you like to set up an Upstash Redis database?" → No
# 5. "Would you like to deploy now?" → Yes

# Espera 3-5 minutos mientras se construye y despliega
```

#### D. Configurar Variables de Entorno

```bash
# Agregar CORS para tu frontend
fly secrets set ALLOWED_ORIGINS="https://deteccion-cascos.vercel.app,http://localhost:4200"

# Las demás variables ya están en fly.toml
```

#### E. Obtener URL de tu API

```bash
fly status
```

Tu URL será: `https://deteccion-cascos.fly.dev`

---

### 3️⃣ ACTUALIZAR FRONTEND CON URL DEL BACKEND (TERCERO)

```bash
cd deteccion-eep
```

Editar `src/environments/environment.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://deteccion-cascos.fly.dev'  // ← Tu URL de Fly.io
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

```bash
# Ya lo hicimos en el paso 2D, pero si necesitas actualizar:
cd iape
fly secrets set ALLOWED_ORIGINS="https://deteccion-cascos.vercel.app,http://localhost:4200"
```

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
| Fly.io | Free | $0 (3 máquinas pequeñas + 160 GB transfer) |
| Vercel | Hobby | $0 |
| **TOTAL** | | **$0/mes** ✅ |

---

## ⚠️ LIMITACIONES DEL PLAN GRATUITO

### Fly.io Free:
- 3 máquinas compartidas gratis (1 GB RAM cada una)
- Se "duerme" después de inactividad (auto_stop_machines = true)
- Primera petición tarda 5-10 segundos en despertar (más rápido que Render)
- 160 GB bandwidth/mes

### Vercel Hobby:
- Sin limitaciones prácticas para este proyecto
- 100 GB bandwidth/mes

---

## 🔧 COMANDOS ÚTILES FLY.IO

```bash
# Ver logs en tiempo real
fly logs

# Ver estado de la aplicación
fly status

# Abrir dashboard web
fly dashboard

# Redesplegar después de cambios
cd iape
fly deploy

# Ver máquinas activas
fly machine list

# SSH a la máquina (para debugging)
fly ssh console

# Escalar memoria (si necesitas más)
fly scale memory 2048  # 2 GB

# Ver uso de recursos
fly status

# Redesplegar Vercel
git push  # Automático
```

---

## 📝 SIGUIENTE PASO SI QUIERES DOMINIO PROPIO

1. Comprar dominio en Namecheap (~$8/año)
2. Configurar DNS en Vercel
3. ¡Listo!
