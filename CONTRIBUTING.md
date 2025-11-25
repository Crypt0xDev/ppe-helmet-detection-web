# Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Detección de EPP! 🎉

## Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/deteccion-cascos.git
cd deteccion-cascos
```

### 2. Crea una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 3. Realiza tus Cambios

- Escribe código limpio y bien documentado
- Sigue las convenciones de código del proyecto
- Agrega pruebas si es necesario
- Actualiza la documentación

### 4. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/nueva-funcionalidad
```

### 5. Crea un Pull Request

- Ve a GitHub y crea un Pull Request
- Describe claramente los cambios realizados
- Referencia cualquier issue relacionado

## Convenciones de Código

### TypeScript/Angular

- Usa TypeScript estricto
- Sigue las guías de estilo de Angular
- Usa señales (signals) para el manejo de estado
- Componentes standalone cuando sea posible

### Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Formato de código (sin cambios funcionales)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

### Ejemplo

```
feat: agregar detección de arneses de seguridad

- Implementa nuevo modelo YOLOv8 para arneses
- Agrega endpoint /detect/harness a la API
- Actualiza UI con nueva sección de arneses
- Documenta nuevos parámetros en README

Closes #42
```

## Reportar Bugs

Usa el [issue tracker](https://github.com/Crypt0xDev/deteccion-cascos/issues) para reportar bugs:

1. Verifica que el bug no haya sido reportado antes
2. Usa el template de issue para bugs
3. Incluye pasos para reproducir el problema
4. Agrega capturas de pantalla si es relevante
5. Especifica tu entorno (OS, navegador, versión)

## Sugerir Mejoras

¿Tienes una idea para mejorar el proyecto?

1. Abre un issue con el tag `enhancement`
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil
4. Provee ejemplos de uso si es posible

## Desarrollo Local

### Requisitos

- Node.js 18+
- npm o yarn
- Git

### Setup

```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm start

# Ejecutar tests
npm test

# Build para producción
npm run build:prod
```

### API Backend

Para desarrollo completo, necesitas la API corriendo localmente:

```bash
# Clonar repositorio de la API
git clone https://huggingface.co/spaces/Crypt0xDev/PPE-Helmet-Detection-API
cd PPE-Helmet-Detection-API

# Instalar dependencias Python
pip install -r requirements.txt

# Ejecutar API
python app.py
```

## Preguntas

Si tienes preguntas, puedes:

- Abrir un issue con el tag `question`
- Contactar al equipo de desarrollo

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia MIT del proyecto.

---

¡Gracias por contribuir! 🚀
