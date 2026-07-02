# Generador de Reportes de Partidos de Fútbol

Trabajo Práctico Integrador — Ciencia de Datos 2026 — Grupo 9  
UTN Facultad Regional La Plata — Ingeniería en Sistemas de Información

---

## Descripción

Sistema de **IA Generativa** que, a partir de estadísticas reales de partidos de la **Premier League**, genera crónicas periodísticas automáticas en lenguaje natural.

El pipeline toma datos estructurados de un partido (resultado, tiros, corners, tarjetas, forma reciente, cuotas) y los transforma en un reporte narrativo coherente, utilizando el modelo **LLaMA 3.3 70B** a través de la API de **Groq**

---

## Integrantes

| Apellido | Nombre |
|----------|--------|
| Beneforti | Franco |
| Canu | Santiago |
| Capre | Rodrigo |
| Diez | Lucas |
| Elizalde | Benjamín |
| Moscuzza | Vicente |

---

## Estructura del Proyecto

```bash
   generador-reportes-futbol/
   ├── app/
   │   └── streamlit_app.py       # Interfaz web para la demo en clase
   ├── src/
   │   ├── data.py                # Carga del dataset y búsqueda de partidos
   │   ├── prompt.py              # Construcción del prompt
   │   └── generator.py           # Integración con Groq
   ├── data/
   │   ├── raw/                   # Dataset original (no versionado)
   │   └── processed/             # Dataset limpio generado por el pipeline
   ├── notebooks/
   │   ├── 00_download_dataset.ipynb # Descarga automática desde Kaggle
   │   ├── 01_eda.ipynb              # Análisis exploratorio de datos
   │   ├── 02_preprocessing.ipynb    # Limpieza y preparación
   │   ├── 03_prompting.ipynb        # Diseño del pipeline y generación
   │   ├── 04_evaluation.ipynb       # Evaluación de resultados
   │   └── 05_demo.ipynb             # Demostración en vivo (notebook)
   ├── reports/                   # Crónicas generadas
   ├── run_app.bat                # Atajo para levantar la interfaz (Windows)
   ├── .env                       # API Key (no versionado)
   ├── .gitignore
   ├── requirements.txt
   └── README.md
```

---

## Tecnologías Utilizadas

- **Python >= 3.10**
- **Pandas** — manipulación y limpieza de datos
- **Matplotlib / Seaborn** — visualización
- **Streamlit** — interfaz web para la demostración en vivo
- **LLaMA 3.3 70B vía Groq API** — modelo generativo de lenguaje
- **python-dotenv** — manejo de variables de entorno

---

## Dataset

**Club Football Match Data (2000–2025)**  
Fuente: [Kaggle](https://www.kaggle.com/datasets/adamgbor/club-football-match-data-2000-2025/data?select=Matches.csv)  
Liga utilizada: **Premier League (E0)**  
Partidos disponibles: **9.325** (temporadas 2000/01 a 2024/25)

> El archivo `Matches.csv` debe estar en `data/raw/`. Podés descargarlo manualmente desde Kaggle
> o ejecutar el notebook `notebooks/00_download_dataset.ipynb` (requiere credenciales de la API de Kaggle).

---

## Cómo Ejecutar

1. Clonar el repositorio
```bash
   git clone https://github.com/tu-usuario/generador-reportes-futbol.git
   cd generador-reportes-futbol
```

2. Instalar dependencias
```bash
   pip install -r requirements.txt
```

3. Configurar la API Key de Groq en un archivo `.env`

   `GROQ_API_KEY=tu_clave_acá`

4. Obtener el dataset en `data/raw/Matches.csv`:
   - **Automático:** ejecutar `notebooks/00_download_dataset.ipynb` (ver requisitos de credenciales Kaggle en el notebook).
   - **Manual:** descargar `Matches.csv` desde Kaggle y colocarlo en `data/raw/`.

5. Ejecutar los notebooks en orden dentro de la carpeta `notebooks/` (empezando por `01_eda.ipynb` si ya descargaste el dataset con el paso 4).

> Para la **exposición en clase**, se recomienda usar la interfaz web (ver sección siguiente) en lugar del notebook.

---

## Demo en vivo (interfaz web)

El proyecto incluye una interfaz **Streamlit** pensada para la presentación del TP. Permite buscar partidos, ver estadísticas y generar crónicas en tiempo real sin editar código.

### Levantar la interfaz

Desde la raíz del proyecto:

```bash
python -m streamlit run app/streamlit_app.py
```

Se abrirá automáticamente en el navegador en **http://localhost:8501**.

**Alternativa en Windows:** doble clic en `run_app.bat`.

> Usar `python -m streamlit` en lugar de `streamlit` directamente, ya que en algunas instalaciones de Python el ejecutable no queda en el PATH.

### Requisitos previos para la demo

- Tener instaladas las dependencias (`pip install -r requirements.txt`).
- Contar con el archivo `data/processed/epl_clean.csv` (generado al ejecutar `02_preprocessing.ipynb`).
- Configurar `GROQ_API_KEY` en el archivo `.env` para generar crónicas en vivo.

### Cómo usar la interfaz

1. **Generar en vivo**
   - Elegir un **equipo** de la Premier League.
   - Seleccionar un **partido** de la lista (ordenados del más reciente al más antiguo).
   - Elegir el **estilo** de la crónica: estándar, técnico o dramático.
   - Revisar las **estadísticas** del partido (resultado, tiros, corners, Elo, etc.).
   - Pulsar **Generar crónica** y esperar unos segundos mientras el modelo responde.
   - (Opcional) Activar **Comparar los 3 estilos** para ver las tres variantes del mismo partido.

2. **Crónicas guardadas**
   - Pestaña de respaldo si la API no está disponible durante la exposición.
   - Muestra crónicas pre-generadas almacenadas en `reports/`.

### Detener la aplicación

En la terminal donde se ejecutó Streamlit, presionar **`Ctrl+C`**.

Si la interfaz sigue accesible después de cerrar la terminal, puede quedar un proceso en segundo plano. Para verificar qué ocupa el puerto 8501:

```powershell
netstat -ano | findstr :8501
```

Si aparece una línea con `LISTENING`, finalizar el proceso con su PID:

```powershell
Stop-Process -Id <PID> -Force
```

Para usar otro puerto:

```bash
python -m streamlit run app/streamlit_app.py --server.port 8502
```

---

## Etapas del Proyecto

| Notebook | Descripción |
|----------|-------------|
| `00_download_dataset.ipynb` | Descarga de `Matches.csv` desde Kaggle hacia `data/raw/` |
| `01_eda.ipynb` | Exploración del dataset, visualización de distribuciones y patrones |
| `02_preprocessing.ipynb` | Selección de columnas, manejo de nulos y variables derivadas |
| `03_prompting.ipynb` | Diseño del prompt, integración con Groq y generación de crónicas |
| `04_evaluation.ipynb` | Análisis crítico de la calidad y coherencia del contenido generado |
| `05_demo.ipynb` | Demostración en vivo mediante notebook (alternativa a la interfaz web) |
| `app/streamlit_app.py` | Interfaz web recomendada para la demo en clase |

---

## Licencia

Proyecto académico — UTN FRLP 2026
