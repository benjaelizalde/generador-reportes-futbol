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
   ├── data/
   │   ├── raw/                   # Dataset original (no versionado)
   │   └── processed/             # Dataset limpio generado por el pipeline
   ├── notebooks/
   │   ├── 00_download_dataset.ipynb # Descarga automática desde Kaggle
   │   ├── 01_eda.ipynb              # Análisis exploratorio de datos
   │   ├── 02_preprocessing.ipynb    # Limpieza y preparación
   │   ├── 03_prompting.ipynb        # Diseño del pipeline y generación
   │   └── 04_evaluation.ipynb       # Evaluación de resultados
   │   └── 05_demo.ipynb             # Demostración en vivo
   ├── reports/                   # Crónicas generadas
   ├── .env                       # API Key (no versionado)
   ├── .gitignore
   ├── requirements.txt
   └── README.md
```

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Pandas** — manipulación y limpieza de datos
- **Matplotlib / Seaborn** — visualización
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

---

## Etapas del Proyecto

| Notebook | Descripción |
|----------|-------------|
| `00_download_dataset.ipynb` | Descarga de `Matches.csv` desde Kaggle hacia `data/raw/` |
| `01_eda.ipynb` | Exploración del dataset, visualización de distribuciones y patrones |
| `02_preprocessing.ipynb` | Selección de columnas, manejo de nulos y variables derivadas |
| `03_prompting.ipynb` | Diseño del prompt, integración con Groq y generación de crónicas |
| `04_evaluation.ipynb` | Análisis crítico de la calidad y coherencia del contenido generado |
| `05_demo.ipynb` | Búsqueda de partidos por equipo y generación de reportes en vivo |

---

## Licencia

Proyecto académico — UTN FRLP 2026
