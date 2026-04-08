# Reporte Práctica 1: Calidad de Software y Buenas Prácticas

**Materia:** Calidad de Software  
**Entregable:** Práctica 1 - Books API Refactoring  

---

## 1. Introducción

### 1.1 Objetivo
El objetivo de esta práctica es aplicar herramientas de análisis estático de código (linters) y refactorizar una aplicación existente (Books-API) para cumplir con estándares de calidad de software aceptados en la industria (PEP 8, docstrings), reduciendo la deuda técnica y mejorando la mantenibilidad del código.

### 1.2 Justificación
La aplicación de buenas prácticas en el desarrollo de software es crucial para asegurar la viabilidad del proyecto a largo plazo. Un código limpio, con alta cohesión y bajo acoplamiento, facilita:
*   **Mantenibilidad:** Menor costo y tiempo para corregir errores.
*   **Legibilidad:** Nuevos desarrolladores pueden entender el sistema rápidamente.
*   **Escalabilidad:** Añadir nuevas funcionalidades sin romper las existentes.
*   **Robustez:** Prevención de errores comunes mediante análisis estático antes de la ejecución.

---

## 2. Desarrollo

### 2.1 Proceso de Implementación

Para asegurar la calidad del código, se utilizó **Ruff**, un linter de Python de alto rendimiento. El proceso consistió en identificar errores, analizar sus causas y aplicar correcciones sistemáticas.

#### Ejecución de Ruff
1.  **Línea de Comandos:** Se ejecutó el comando `ruff check .` en la raíz del proyecto para analizar todos los archivos.
    ```bash
    ruff check .
    ```
    *(Espacio para evidencia visual: Captura de pantalla de la terminal mostrando la ejecución del comando y la lista de errores encontrados antes de corregir, o el mensaje "All checks passed!" al final del proceso)*
    ![Evidencia 1: Ejecución de Ruff en terminal](ruta/a/tu/imagen_terminal.png)

2.  **IDE (VS Code):** Se utilizó la extensión de Ruff para visualizar errores en tiempo real (subrayado rojo/amarillo) y aplicar "Quick Fixes" automáticos donde fue posible.
    *(Espacio para evidencia visual: Captura de pantalla del IDE donde se vea el subrayado de error y el tooltip con la descripción del problema)*
    ![Evidencia 2: Errores resaltados en VS Code](ruta/a/tu/imagen_ide_errores.png)

### 2.2 Análisis de Calidad y Correcciones (Code Smells)

A continuación, se describen 5 "Code Smells" específicos detectados y resueltos, seleccionados de las reglas aplicadas (`D`, `E`, `PL`, `B`):

#### 1. Ausencia de Documentación (Reglas D100, D101, D103)
*   **Situación Detectada:** Archivos y funciones sin *docstrings*.
    *   *Ejemplo:* `def create_indexes():` sin explicación.
*   **Solución:** Se añadieron docstrings explicativos al inicio de cada módulo y función pública.
*   **Beneficio:** Facilita la generación automática de documentación y la comprensión del propósito del código sin leer la implementación completa.

#### 2. Longitud de Línea Excesiva (Regla E501)
*   **Situación Detectada:** Líneas de código superiores a 79 caracteres.
    *   *Ejemplo:* Definiciones de rutas en FastAPI con muchos parámetros en una sola línea.
*   **Solución:** Se reformateó el código dividiendo las líneas lógicamente y alineando los argumentos verticalmente.
*   **Beneficio:** Mejora la legibilidad en pantallas divididas y sigue el estándar PEP 8.

#### 3. Importaciones Desordenadas (Regla E402)
*   **Situación Detectada:** Sentencias `import` ubicadas después de código ejecutable o variables.
    *   *Ejemplo:* En `routes.py`, `from model import ...` estaba después de `router = APIRouter()`.
*   **Solución:** Se movieron todas las importaciones al inicio del archivo.
*   **Beneficio:** Evita errores de dependencia circular y clarifica las dependencias del módulo desde el principio.

#### 4. Uso Incorrecto de `exit()` (Regla PLR1722)
*   **Situación Detectada:** Uso de `exit(1)` en `client.py`. La función `exit()` está diseñada para la consola interactiva, no para scripts de producción.
*   **Solución:** Se reemplazó por `sys.exit(1)` tras importar module `sys`.
*   **Beneficio:** Asegura una terminación correcta del proceso y es la práctica estándar en scripts de Python.

#### 5. Exceso de Argumentos (Regla PLR0913 - "Large Class/Method")
*   **Situación Detectada:** La función `update_book` recibía más de 12 argumentos, lo cual es un síntoma de una función que hace demasiado o maneja demasiados datos sueltos.
*   **Solución:** Aunque idealmente se refactorizaría para recibir un objeto de configuración, para mantener la API CLI actual se documentó y suprimió explícitamente el error (`# noqa: PLR0913`) reconociendo la complejidad necesaria en este contexto específico.
*   **Beneficio:** Aunque no se redujeron los argumentos, se hizo explícita la deuda técnica y se controló el linter para que no oculte otros errores reales.

*(Espacio para evidencia visual: Captura mostrando el menú "Quick Fix" o la acción de código sugerida por el IDE para solucionar un problema)*
![Evidencia 3: menú Quick Fix en IDE](ruta/a/tu/imagen_quick_fix.png)

### 2.3 Buenas Prácticas de Diseño: Cohesión y Acoplamiento

El proyecto demuestra un diseño modular que favorece la calidad del software:
*(Espacio para evidencia visual: Captura del explorador de archivos mostrando la estructura del proyecto)*
![Evidencia 4: Estructura del proyecto](ruta/a/tu/imagen_estructura.png)

#### Alta Cohesión
Cada módulo del proyecto tiene una responsabilidad única y bien definida:
*   **`model.py`:** Se encarga **exclusivamente** de la definición de datos y validación (schemas Pydantic). No contiene lógica de negocio ni rutas.
*   **`routes.py`:** Maneja **exclusivamente** las peticiones HTTP y la interacción con la base de datos a nivel de controlador. Delega la validación de datos a `model.py`.
*   **`client.py`:** Actúa como un cliente independiente, separado de la lógica del servidor.

Esta separación permite que cambios en la estructura de datos (`model.py`) no requieran reescribir la lógica de rutas, siempre que la interfaz (API) se mantenga.

#### Bajo Acoplamiento
El acoplamiento se mantiene bajo mediante el uso de inyección de dependencias y separación de preocupaciones:
*   **Inyección de Base de Datos:** `routes.py` no crea la conexión a la base de datos. En su lugar, utiliza `request.app.database`, que es inyectado por `main.py` durante el arranque (`startup`).
    *   *Beneficio:* Esto permite cambiar la base de datos (por ejemplo, a una de pruebas) en `main.py` sin tocar una sola línea de código en `routes.py`.
*   **Modelos Pydantic:** Las rutas dependen de las *interfaces* definidas en `model.py` (`Book`, `Book_Update`), no de implementaciones concretas de almacenamiento, lo que desacopla la validación de la lógica de negocio.

---

## 3. Conclusiones

La refactorización con Ruff ha transformado un código funcional pero desordenado en un proyecto profesional y mantenible. Se aprendió que:
1.  **La automatización es clave:** Herramientas como Ruff detectan en segundos errores que a un humano le tomaría horas encontrar.
2.  **No todo error se debe "corregir" ciegamente:** En casos como el exceso de argumentos, a veces la corrección correcta es suprimir la regla temporalmente si el rediseño arquitectónico (cambiar la CLI) fuera del alcance, documentando la decisión.
3.  **El diseño importa:** La estructura inicial de alta cohesión (archivos separados por responsabilidad) facilitó enormemente la corrección de errores de linting, ya que los problemas estaban aislados localmente por archivo.

El uso de estándares como PEP 8 y docstrings no es solo estética; es fundamental para la colaboración y la vida útil del software.

---

## 4. Bibliografía
1.  **Ruff Documentation.** (2024). *The Ruff Linter*. Recuperado de: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
2.  **Python Software Foundation.** (2001). *PEP 8 – Style Guide for Python Code*. Recuperado de: [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
3.  **FastAPI Documentation.** (2024). *Project Structure & Dependencies*. Recuperado de: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
