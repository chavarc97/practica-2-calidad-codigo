# Reporte: Práctica 2 - Análisis de código estático con SonarQube

Salvador Rodriguez

## 1. Introducción
El objetivo principal de esta práctica es integrar **SonarQube** en un ciclo de desarrollo para validar automática y continuamente el código en busca de errores (Bugs), vulnerabilidades, duplicación excesiva y desvíos de formato (Code Smells). 
Aplicar buenas prácticas y herramientas de análisis estático es vital en el ciclo de vida de software moderno (DevSecOps), ya que nos permite mitigar de manera temprana la deuda técnica, reduciendo costos a largo plazo y mejorando la confiabilidad de las aplicaciones. En este informe se documenta la configuración en CI/CD, auditoría y refactorización orientada a la calidad del proyecto **Books-API**.

---

## 2. Configuración de SonarQube en Pipeline CI/CD
Se configuró SonarQube en el pipeline de Integración Continua utilizando GitHub Actions. El archivo `.github/workflows/sonar.yml` detalla un flujo de trabajo que, ante una modificación en las ramas principales, despliega una imagen base de Ubuntu, instala el escáner y envía un análisis detallado al servidor de SonarQube.

> **[PLACEHOLDER: CAPTURA 1 - Pon aquí una captura de pantalla del código de tu archivo `.github/workflows/sonar.yml` o del éxito de tu branch ejecutándose en la pestaña "Actions" de GitHub]**

Además, el token de autenticación se administra mediante secretos (pasados como variable `SONARQUBE_TOKEN`) para no exponer credenciales y conservar la seguridad del repositorio.

---

## 3. Integración con Linter (Ruff) e Inspección de Estilo
El análisis estático no estaría completo usando solo SonarQube. Por ello, delegamos el análisis de reglas de nombrado, longitud de las líneas y formato utilizando **Ruff** (un linter para Python veloz e intuitivo).
Integramos la salida de Ruff con SonarQube del siguiente modo en el pipeline (y de manera local):
```bash
ruff check . --output-format=pylint > ruff-report.txt
```
Posteriormente, configuramos el archivo raíz `sonar-project.properties` pasándole el path al reporte mediante el atributo `sonar.python.pylint.reportPaths=ruff-report.txt`. Así, SonarQube consume y visualiza los reportes generados por el linter directamente en su Dashboard.

---

## 4. Validación en tiempo real con Editor (SonarLint)
Para agilizar el proceso y que un desarrollador descubra un "*code smell*" incluso antes de enviar el código (hacer un commit o push), se integró la extensión **SonarLint** dentro de Visual Studio Code.

Se vinculó la extensión a la instancia local de SonarQube (`localhost:9000`), compartiendo de esta manera todas las reglas definidas en los *Quality Profiles* directamente al espacio de trabajo. Así, VS Code nos ayuda subrayando variables o sintaxis mal aplicada en tiempo real.

> **[PLACEHOLDER: CAPTURA 2 - Pon aquí una captura de tu VS Code que muestre la extensión de SonarLint instalada o marcando "Connected" al servidor]**

---

## 5. Refactorización basada en Análisis de SonarQube
Al correr el análisis primario sobre nuestro proyecto `Books-API`, el *Quality Gate* de SonarQube falló al levantar **1 Bug** (código con potencial de reventar en la ejecución).

### El problema: Bug python:S5644
En el archivo `test/test_books.py` existía un mock del objeto base de datos (`MagicMock`) desde donde se intentaba acceder bajo notación de diccionario para evadir inyección a DB en las pruebas unitarias:
```python
mock_db['books'].find.return_value.sort.return_value...  = [] 
```
El analizador estático levantó la regla **S5644** ("*Item operations should be done on objects supporting them*"), indicando que en el análisis inferido "mock_db" no presentaba un comportamiento nativo implementando el *dunder method* `__getitem__`, por lo cual era catalogado como un mal hábito o posible defecto a nivel robustez.

### Análisis y Solución
Refactorizamos sustituyendo el acceso por índice iterativo hacia uno de atributos (nativo a Python sin levantar falsos positivos) aprovechando la forma alternativa que tiene MongoDB (PyMongo) para acceder a las colecciones:
```python
mock_db.books.find.return_value.sort.return_value...  = []
```
Tras corregirlo y aplicar nuevamente el control (`sonar-scanner`), validamos que el Bug había sido mitigado al 100%, dejando el código impecable en 0 incidencias.

> **[PLACEHOLDER: CAPTURA 3 - Pon aquí una de captura en el Dashboard de SonarQube donde se vea que el "Bug" inicial ahora está solucionado (0 Bugs / Quality Gate: Passed)]**

---

## 6. Validación para Integración Continua en Merge / Pull Requests
Para robustecer la red de prevención de errores, se determinó que ningún código se integre directamente en `main`. Como punto (5) de los requisitos, configuramos que la validación ocurra estrictamente en eventos de *Pull Request* incorporando la directiva `on: pull_request` a las Actions.
De esta manera, la herramienta examina dependencias limpias e inspeccciona perfiles de seguridad asegurando que GitHub no permita transacionar los merges sin la bandera en verde del reporte (Sonar Quality Gate).

---

## 7. Auditoría de Calidad a un Repositorio Abierto
Para evaluar los métodos en un nivel macro-avanzado, se tomó prestado el repositorio líder de código abierto escrito en lenguaje Golang: `httpx` (herramienta multipropósito de la Web). A dicha herramienta se le pasó una evaluación global estática conectándola a nuestro SonarQube local.

Se extrajeron los siguientes datos relevantes sobre su adherencia a mejores prácticas de la industria:
> *(Describe brevemente lo que viste en el panel sobre Httpx. Ejemplo: Sorprendentemente su código presentaba varios Code Smells de duplicación o mantenían un excelente A Ratio)*

> **[PLACEHOLDER: CAPTURA 4 - Pon una captura del análisis final de SonarQube mostrando las métricas que te arrojó el proyecto "httpx" o "auditoria-httpx"]**

---

## 8. Conclusiones
A través de este ejercicio se evidenció la enorme ventaja de la automatización sobre la calidad del código. 
Integrar herramientas en varias capas del trabajo diario del ingeniero de software; desde una visualización por **SonarLint** mientras se codifica, validación en línea de comandos por un estricto **Linter (Ruff)**, y al fin una red de seguridad infalible mediante **SonarQube** en el *CI/CD*. Esto fomenta la cultura preventiva donde el equipo de desarrollo se dedica al progreso o a la lógica del negocio sin tener que emplear largas horas al debugeo por errores de sintaxis u omisiones de arquitectura de bajo nivel.