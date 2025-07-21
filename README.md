# AHS-Compressor v2.0

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/rcdrodrigo/ahs-compressor?style=social)](https://github.com/rcdrodrigo/ahs-compressor/stargazers)

> Una herramienta para comprimir código Python en una **Estructura Jerárquica Abstracta (AHS)**, diseñada para optimizar el análisis e interacción de código con Modelos de Lenguaje Grande (LLMs).

---

## 🎯 ¿Qué problema resuelve?

Los LLMs tienen una ventana de contexto limitada. Analizar o modificar repositorios de código grandes es ineficiente y a menudo imposible, ya que el código fuente completo no cabe en el prompt del modelo.

**AHS-Compressor** aborda este problema a través de "compresión de contexto". No reduce el tamaño del archivo sino que transforma el código en una estructura de alto nivel (el AHS) y un mapa de código correspondiente. Esto permite a un LLM:

1. **Ver la "arquitectura" del proyecto** (la estructura AHS) sin necesidad de ver cada línea de código
2. **Navegar el código inteligentemente**, solicitando solo los fragmentos específicos que necesita del mapa de código
3. **Modificar código de forma segura**, ya que reconstruir el código desde el AHS y el mapa preserva el 100% del formato original, incluyendo comentarios (gracias a `libCST`)

## ✨ Características Clave

- **🔄 Preservación de Formato:** Gracias a `libCST`, todos los comentarios, espacios en blanco y estructura del código se mantienen intactos
- **📋 Estructura JSON:** El formato AHS es ahora un JSON estructurado, facilitando su análisis y extensión
- **🏗️ Soporte a Nivel de Proyecto:** El CLI puede procesar directorios completos, generando un único AHS para todo el proyecto
- **⚡ API y CLI:** Ofrece tanto interfaz de línea de comandos (`ahs-cli`) para uso local como API web (FastAPI) para integraciones
- **📦 Listo para Instalar:** Disponible como paquete de Python via `pip`

## 🧠 Entendiendo AHS-Compressor: Utilidad Real y Flujo de Trabajo

La verdadera utilidad de AHS-Compressor radica en su capacidad para **superar las limitaciones de la ventana de contexto de los LLMs**, especialmente modelos locales.

### 📚 La Analogía del Libro

Imagina un LLM como un estudiante muy inteligente que solo puede leer una página de un libro a la vez. Si le das un libro completo (un proyecto de software grande), se abruma y no puede captar la trama general o dónde encontrar información específica.

**AHS-Compressor transforma el "libro" en:**

1. **📑 Un "Índice" (el AHS):** Una representación compacta de la estructura del proyecto - qué archivos existen, qué clases y funciones contienen, cómo se relacionan. Este "índice" es tan pequeño que el LLM puede leerlo completamente.

2. **📖 Un "Diccionario" (el Mapa de Código):** Contiene el texto exacto de cada fragmento de código referenciado en el índice.

### 🎯 Beneficios Clave

- **🗜️ Compresión Semántica de Contexto:** Reduce "información irrelevante" que el LLM necesita procesar para entender la estructura
- **🧭 Navegación Inteligente:** Permite al LLM "saltar" directamente a secciones de código relevantes sin cargar el archivo completo
- **✅ Fidelidad Perfecta:** La reconstrucción del código es 100% idéntica al original, incluyendo comentarios y formato
- **🏠 Empoderando LLMs Locales:** Los modelos locales con ventanas de contexto más pequeñas se vuelven mucho más útiles para tareas de ingeniería de software

### 🔄 Cómo Usar: El Flujo de Trabajo Completo

Usar AHS-Compressor involucra un flujo de trabajo iterativo entre tú y el LLM.

#### Paso 1: Codificar el Proyecto (Acción Humana)
Usa el CLI para transformar tu proyecto al formato AHS + Mapa:
```bash
ahs-cli encode ./mi_proyecto -o contexto_proyecto.json
```
Esto genera un archivo JSON con dos claves principales: `"ahs"` (la estructura) y `"map"` (el contenido).

#### Paso 2: Interactuar con el LLM (Humano + LLM)
1. **Proporciona la estructura AHS** al LLM
2. **Dale una tarea al LLM** (ej: "Refactoriza la función `calcular_suma`")
3. **El LLM identifica la `ref` relevante** (ej: `@5`)
4. **Tú proporcionas el contenido** del mapa de código para esa `ref`
5. **El LLM procesa y devuelve la versión modificada**
6. **Tú actualizas el mapa de código** con los cambios

#### Paso 3: Decodificar el Proyecto (Acción Humana)
Reconstruye el proyecto completo con tus cambios:
```bash
ahs-cli decode contexto_proyecto.json -o ./proyecto_restaurado
```

## 💬 Configuración de Interacción con LLM

### Plantilla de Prompt del Sistema Recomendada

```
Eres un asistente experto en análisis y refactorización de código Python. Te daré una estructura de proyecto en un formato especial llamado AHS (Abstract Hierarchical Structure).

Tu tarea es ayudarme a entender y modificar el código basándote en esta estructura. Primero te daré la estructura completa. Luego, puedes solicitar el código de cualquier parte usando su `ref` (por ejemplo, `@5`). No inventes código, solo solicítalo a través de su `ref`.

---
Eres un asistente experto en análisis y refactorización de código Python. Voy a darte la estructura de un proyecto en un formato especial llamado AHS (Abstract Hierarchical Structure).

Tu tarea es ayudarme a entender y modificar el código basándote en esta estructura. Yo te daré la estructura completa primero. Luego, tú me puedes pedir el código de cualquier parte usando su `ref` (por ejemplo, `@5`). No debes inventar código, solo pedirlo a través de su `ref`.

---
ESTRUCTURA DEL PROYECTO (AHS):

[
    { "type": "Import", "ref": "@0" },
    { "type": "Import", "ref": "@1" },
    { "type": "Import", "ref": "@2" },
    { "type": "Import", "ref": "@3" },
    { "type": "Import", "ref": "@4" },
    { "type": "FunctionDef", "ref": "@5", "name": "ejecutar_powershell" },
    { "type": "FunctionDef", "ref": "@6", "name": "guardar_log" },
    { "type": "FunctionDef", "ref": "@7", "name": "escanear_procesos" },
    { "type": "FunctionDef", "ref": "@8", "name": "conexiones_red" },
    { "type": "FunctionDef", "ref": "@9", "name": "archivos_malformados" },
    { "type": "FunctionDef", "ref": "@10", "name": "escaneo_sfc" },
    { "type": "FunctionDef", "ref": "@11", "name": "escaneo_dism" },
    { "type": "FunctionDef", "ref": "@12", "name": "limpiar_temporales" },
    { "type": "FunctionDef", "ref": "@13", "name": "liberar_memoria" },
    { "type": "FunctionDef", "ref": "@14", "name": "listar_inicio" },
    { "type": "FunctionDef", "ref": "@15", "name": "comprimir_y_abrir_logs" }
]
---

Hecho esto, espera mi primera instrucción
---

****
--**Flujo de Interacción de Ejemplo:**

**Tú:** "Quiero optimizar la función de limpieza de memoria. ¿Puedes analizar la función liberar_memoria?"

**LLM:** "Puedo ver la función liberar_memoria en la estructura (ref: @13). Para analizarla y optimizarla, necesito ver la implementación actual. Por favor proporciona el contenido de @13."

**Tú:** [Copia el contenido de tu mapa JSON para "@13"]

**LLM:** [Analiza la función y sugiere optimizaciones]

Este flujo de trabajo permite al LLM:
- 🎯 Enfocarse inmediatamente en secciones de código relevantes
- 🧠 Entender el contexto sin verse abrumado
- 🔄 Trabajar iterativamente en mejoras específicas
- 📊 Ver el panorama general de la arquitectura de tu proyecto

## 🤖 Ejemplo Completo con Claude

¿Quieres ver AHS-Compressor en acción refactorizando un proyecto real de 2000+ líneas?

### 👉 [Complete Example: AHS-Compressor + Claude](Complete%20Example:%20AHS-Compressor%20+%20Claude.md)

Este ejemplo detallado demuestra:

- **🎯 Flujo completo paso a paso** - Desde codificación hasta reconstrucción
- **💬 Conversación real con Claude** - Interacciones específicas y prompts optimizados  
- **⚡ Refactorización de sistema de seguridad** - Proyecto complejo con múltiples módulos
- **📊 Métricas de rendimiento** - 5x más rápido que métodos tradicionales
- **🛠️ Mejores prácticas** - Estrategias comprobadas para máxima eficiencia

**Resultados del ejemplo:**
- ✅ 2,180 líneas analizadas sin perder contexto
- ✅ 15+ funciones optimizadas con mejores prácticas  
- ✅ 8 bugs encontrados y corregidos proactivamente
- ✅ Solo ~1,200 tokens por iteración (vs 8,000+ tradicional)

### 🚀 Casos de Uso Destacados

- **Legacy Code Modernization** - Actualizar sistemas antiguos
- **Architecture Reviews** - Análisis profundo de diseño  
- **Performance Optimization** - Identificar y resolver cuellos de botella
- **Code Quality Improvement** - Aplicar patrones y mejores prácticas



## 🚀 Instalación

### Método Recomendado: Usando pipx

#### 🔧 ¿Por qué usar `pipx`? (La Analogía de la Caja de Herramientas)

Piensa en tu computadora como un gran taller donde cada proyecto necesita sus propias herramientas especiales:

- **❌ Instalación Global:** Como tirar todas las herramientas en una caja gigante - ¡se produce caos!
- **⚠️ Entornos Virtuales:** Como cajas de herramientas separadas - organizadas pero inconvenientes
- **✅ pipx (Lo Mejor de Ambos Mundos):** Crea cajas de herramientas aisladas pero pone las herramientas principales en una pared pública para fácil acceso

#### Guía de Instalación Paso a Paso

**1. Instala `pipx`** (una vez en tu vida):
```bash
pip install pipx


**2. Agrega `pipx` a tu sistema:**
```bash
pipx ensurepath

*(Reinicia tu terminal después de este paso)*

**3. Instala `AHS-Compressor`:**
```bash
pipx install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

**4. Verifica la Instalación:**
```bash
ahs-cli --help
```

### Métodos de Instalación Alternativos

#### Para Desarrolladores (Desarrollo Local)
```bash
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor
pip install -e .
```

#### Usando pip (No Recomendado para Usuarios Finales)
```bash
pip install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

### Comandos de Mantenimiento

**Actualizar a la última versión:**
```bash
pipx upgrade ahs-compressor
```

**Desinstalar:**
```bash
pipx uninstall ahs-compressor
```

## 📘 Uso

### Interfaz de Línea de Comandos (CLI)

**Codificar un proyecto completo:**
```bash
ahs-cli encode ./mi_proyecto -o proyecto_comprimido.json
```

**Decodificar un proyecto:**
```bash
ahs-cli decode proyecto_comprimido.json -o ./mi_proyecto_restaurado
```

### 🌐 API Web

Inicia el servidor FastAPI:
```bash
uvicorn app.main:app --reload
```

Servidor disponible en `http://localhost:8000`

**Endpoints Principales:**
- `POST /compress-text`: Comprime un fragmento de código
- `POST /decompress-text`: Descomprime un AHS y mapa
- `GET /health`: Endpoint de verificación de salud

## 🛠️ Desarrollo

### Comenzando
```bash
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor
pip install -e .
```

### 🗺️ Hoja de Ruta

- [ ] 📦 Publicar paquete en PyPI
- [ ] 🌐 Implementar compresión a nivel de proyecto en API con tareas en segundo plano
- [ ] 🔧 Agregar soporte para más lenguajes (JavaScript, Java)
- [ ] 🐍 Crear cliente Python para interacción más fácil con la API
- [ ] 🔌 Desarrollo de plugin para VS Code

## 💡 Mejores Prácticas

### Maximizando la Eficiencia

1. **🎯 Iteraciones Focalizadas:** Trabaja en funciones o clases individuales, no en proyectos completos de una vez
2. **📝 Prompting Claro:** Sé explícito sobre el formato AHS y patrones de interacción
3. **🔄 Flujo de Trabajo Dirigido por Pruebas:** Codificar → LLM modifica → Actualizar mapa → Decodificar → Probar → Repetir
4. **📚 Análisis Estratégico:** Usa AHS para análisis de arquitectura e identificación de dependencias
5. **🔧 Control de Versiones:** Siempre trabaja en ramas de Git y haz commit después de cada ciclo

❤️ Apoya Este Proyecto

AHS-Compressor es un proyecto gratuito y de código abierto que requiere tiempo y esfuerzo para mantener y mejorar. Si encuentras esta herramienta útil, considera apoyar su desarrollo:

🌟 Maneras de Apoyar

[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/rcdrodrigo)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/rcdrodrigo)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/rcdrodrigo)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/rcdrodrigo)

### 🚀 Otras formas de contribuir

⭐ **Estrella el repositorio:** La forma más rápida de mostrar apoyo y ayudar al proyecto a ganar visibilidad

💝 **Contribuye:** ¿Encontraste un error? ¿Tienes una idea de mejora? ¡Los pull requests son bienvenidos!

📢 **Difunde la palabra:** Comparte el proyecto con otros desarrolladores que puedan encontrarlo útil

🐛 **Reporta bugs:** Ayúdanos a mejorar reportando problemas en [Issues](https://github.com/rcdrodrigo/ahs-compressor/issues)

📖 **Mejora la documentación:** La documentación siempre puede ser mejor

---

## 🤝 Contribuyendo

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ve el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto

- **GitHub:** [@rcdrodrigo](https://github.com/rcdrodrigo)
- **Issues:** [Reportar un problema](https://github.com/rcdrodrigo/ahs-compressor/issues)

---

<div align="center">

**¿Te ha sido útil AHS-Compressor?** ⭐ ¡Dale una estrella al repo!

</div>
