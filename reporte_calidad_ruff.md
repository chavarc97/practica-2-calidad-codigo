# Análisis de calidad de código con Ruff

## Ejecución de Ruff
Se ha realizado el análisis estático del código fuente del proyecto **Books-API** utilizando la herramienta **Ruff**.

### Línea de comandos
El análisis se ejecutó sobre el directorio raíz del proyecto para abarcar todos los archivos fuente (`main.py`, `client.py`, `routes.py`, `model.py`, etc.).

**Comando ejecutado:**
```bash
ruff check .
```
*(Nota: Aunque la instrucción sugería `ruff check Tests`, se ejecutó sobre `.` para analizar todo el código fuente del proyecto, ya que es donde residían los archivos principales).*

### Ejecución desde el IDE
Se verificó la integración con **Visual Studio Code**, donde la extensión de Ruff resalta los errores en tiempo real y permite aplicar correcciones rápidas (Quick Fixes) directamente en el editor.

## Documentación de errores identificados y correcciones

A continuación, se describen las categorías principales de errores detectados por Ruff, su origen y la solución aplicada para cada uno.

### 1. Ausencia de Docstrings (Reglas D100, D101, D103, D106)
*   **Error:** `Missing docstring in public module/class/function`.
*   **Origen:** El código carecía de documentación explicativa en módulos, clases y funciones públicas, lo cual dificulta la mantenibilidad y comprensión del código.
*   **Archivos afectados:** `client.py`, `main.py`, `model.py`, `routes.py`, `create_index.py`, `data/populate.py`.
*   **Corrección aplicada:**
    *   Se agregaron *docstrings* (comentarios entre triples comillas `"""..."""`) al inicio de cada archivo (módulo) describiendo su propósito.
    *   Se documentaron las clases (`Book`, `Book_Update`) y sus clases anidadas `Config`.
    *   Se documentaron todas las funciones públicas describiendo brevemente su acción (ej. `"""Update a book by ID."""`).

### 2. Longitud de línea excesiva (Regla E501)
*   **Error:** `Line too long (X > 79)`.
*   **Origen:** Varias líneas de código excedían el límite de 79 caracteres establecido por PEP 8 (configurado en `pyproject.toml`). Esto ocurría frecuentemente en definiciones de funciones con muchos argumentos o en consultas largas a la base de datos.
*   **Archivos afectados:** `client.py`, `routes.py`, `create_index.py`.
*   **Corrección aplicada:**
    *   Se reformateó el código dividiendo las líneas largas en múltiples líneas.
    *   En definiciones de funciones, se alinearon los argumentos verticalmente.
    *   En llamadas a funciones y cadenas de texto largas, se utilizó concatenación implícita o saltos de línea dentro de paréntesis.

### 3. Exceso de argumentos en funciones (Reglas PLR0913, PLR0917)
*   **Error:** `Too many arguments in function definition` y `Too many positional arguments`.
*   **Origen:** Funciones como `update_book` o `list_books` requerían muchos parámetros individuales para manejar todos los campos de un libro (título, autor, rating, etc.).
*   **Archivos afectados:** `client.py`, `routes.py`.
*   **Corrección aplicada:**
    *   Dado que estos argumentos son necesarios para la funcionalidad de la API y CLI actual, se optó por suprimir explícitamente estas advertencias utilizando comentarios `# noqa: PLR0913, PLR0917` en las líneas afectadas. Esto indica a Ruff que "ignore" esta regla intencionalmente en esos casos específicos.

### 4. Uso incorrecto de funciones de salida (Regla PLR1722)
*   **Error:** `Use sys.exit() instead of exit`.
*   **Origen:** Uso de la función `exit()` (pensada para la shell interactiva) en lugar de `sys.exit()` en un script de producción.
*   **Archivos afectados:** `client.py`.
*   **Corrección aplicada:**
    *   Se importó el módulo `sys`.
    *   Se reemplazaron las llamadas `exit(1)` por `sys.exit(1)`.

### 5. Importaciones mal ubicadas (Regla E402)
*   **Error:** `Module level import not at top of file`.
*   **Origen:** Sentencias `import` ubicadas después de código ejecutable o definiciones de variables, rompiendo la convención de tenerlas todas al inicio.
*   **Archivos afectados:** `routes.py`, `create_index.py`, `data/populate.py`.
*   **Corrección aplicada:**
    *   Se movieron todas las importaciones al principio del archivo, justo después del *docstring* del módulo.

### 6. Uso de llamadas a funciones en argumentos por defecto (Regla B008)
*   **Error:** `Do not perform function call Body in argument defaults`.
*   **Origen:** En FastAPI es común usar `Body(...)` o `Query(...)` como valores por defecto en los argumentos de las funciones de ruta. Ruff (vía flake8-bugbear) alerta sobre esto porque en Python los argumentos por defecto se evalúan una sola vez al definir la función.
*   **Archivos afectados:** `routes.py`.
*   **Corrección aplicada:**
    *   Se agregó `# noqa: B008` en las definiciones de rutas donde se utiliza esta inyección de dependencias de FastAPI, ya que es el patrón idiomático y correcto para este framework, a pesar de la advertencia general de Python.

---
**Estado Final:** Tras aplicar estas correcciones, el proyecto pasa la validación de Ruff sin reportar errores.
