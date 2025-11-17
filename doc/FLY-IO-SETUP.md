# 🚀 GUÍA PASO A PASO: DEPLOYMENT A FLY.IO

## ✅ ARCHIVOS CREADOS

Ya he creado todos los archivos necesarios en `iape/`:
- ✅ `Dockerfile` - Configuración de contenedor Docker
- ✅ `.dockerignore` - Archivos a ignorar en Docker
- ✅ `fly.toml` - Configuración de Fly.io

## 📋 PASOS A SEGUIR

### PASO 1: Instalar Fly CLI

**Abre PowerShell como Administrador** y ejecuta:

```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Cierra y vuelve a abrir PowerShell**, luego verifica:

```bash
fly version
```

Deberías ver: `flyctl v0.x.xxx ...`

---

### PASO 2: Crear cuenta en Fly.io

```bash
fly auth login
```

Se abrirá tu navegador:
1. Haz clic en **"Sign up with GitHub"**
2. Autoriza Fly.io
3. Regresa a la terminal

---

### PASO 3: Ir a la carpeta del backend

```bash
cd "c:/Users/alexi/Desktop/Curso UNSM/Poyecto grupo 5/deteccion-cascos/iape"
```

---

### PASO 4: Lanzar la aplicación

```bash
fly launch
```

**Responde a las preguntas:**

```
? Choose an app name: 
  → deteccion-cascos (o presiona Enter para que genere uno automático)

? Choose a region for deployment: 
  → gru (São Paulo, Brazil - más cerca de Perú)
  
? Would you like to set up a PostgreSQL database now? 
  → N (No)

? Would you like to set up an Upstash Redis database now? 
  → N (No)

? Would you like to deploy now? 
  → y (Yes)
```

**Espera 3-5 minutos** mientras se construye y despliega. Verás:
```
==> Building image
==> Pushing image
==> Creating release
==> Monitoring deployment
```

---

### PASO 5: Configurar CORS

Una vez desplegado, ejecuta:

```bash
fly secrets set ALLOWED_ORIGINS="https://deteccion-cascos.vercel.app,http://localhost:4200"
```

Esto reiniciará automáticamente tu app.

---

### PASO 6: Obtener tu URL

```bash
fly status
```

Tu URL será algo como: `https://deteccion-cascos.fly.dev`

**O también:**

```bash
fly open
```

Esto abrirá tu API en el navegador.

---

### PASO 7: Actualizar Frontend

```bash
cd "../deteccion-cascos/src/environments"
```

**Edita `environment.ts`** y cambia la URL:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://deteccion-cascos.fly.dev'  // ← Tu URL de Fly.io
};
```

---

### PASO 8: Commit y Push

```bash
cd "c:/Users/alexi/Desktop/Curso UNSM/Poyecto grupo 5/deteccion-cascos"

git add .
git commit -m "Deploy: Migrado a Fly.io"
git push
```

Vercel se actualizará automáticamente.

---

## 🎯 VERIFICAR QUE FUNCIONE

1. **Prueba tu API directamente:**
   ```bash
   fly open
   ```
   O visita: `https://tu-app.fly.dev/`

2. **Prueba el frontend:**
   Visita: `https://deteccion-cascos.vercel.app`
   Sube una imagen → Debería detectar cascos

---

## 📊 COMANDOS ÚTILES

```bash
# Ver logs en tiempo real
fly logs

# Ver estado
fly status

# Redesplegar después de cambios
fly deploy

# Abrir dashboard web
fly dashboard

# Ver máquinas activas
fly machine list

# SSH para debugging
fly ssh console
```

---

## 🔧 SI NECESITAS MÁS MEMORIA

Por defecto tienes 1 GB. Si necesitas más:

```bash
fly scale memory 2048  # 2 GB (aún gratis)
```

---

## ❌ SOLUCIÓN DE PROBLEMAS

### Error: "dockerfile not found"
```bash
# Verifica que estás en la carpeta iape/
pwd
# Debe mostrar: .../deteccion-cascos/iape
```

### Error: "failed to fetch an image"
```bash
# Reconstruye la imagen
fly deploy --build-only
fly deploy
```

### Ver logs de error:
```bash
fly logs
```

---

## ✅ VENTAJAS DE FLY.IO

- ✅ **1 GB RAM** (vs 256 MB en Render)
- ✅ **Más rápido** para despertar (5-10s vs 30-60s)
- ✅ **Mejor para ML** (modelos pesados)
- ✅ **3 máquinas gratis**
- ✅ **160 GB bandwidth/mes**

---

## 🎉 ¡LISTO!

Tu aplicación está desplegada en Fly.io con más memoria y mejor rendimiento.

**URL Backend:** `https://tu-app.fly.dev`  
**URL Frontend:** `https://deteccion-cascos.vercel.app`
