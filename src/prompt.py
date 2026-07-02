import pandas as pd

ESTILOS = ("estandar", "tecnico", "dramatico")

ROLES = {
    "estandar": (
        "Eres un periodista deportivo experto en fútbol inglés. "
        "Usá un tono dinámico y profesional."
    ),
    "tecnico": (
        "Eres un analista de estadísticas de fútbol. "
        "Usá un tono objetivo y analítico, centrado en números."
    ),
    "dramatico": (
        "Eres un comentarista deportivo apasionado. "
        "Usá metáforas, suspenso y lenguaje vívido."
    ),
}


def build_prompt(row: pd.Series, estilo: str = "estandar") -> str:
    if estilo not in ROLES:
        raise ValueError(f"Estilo inválido: {estilo}. Opciones: {', '.join(ESTILOS)}")

    resultado_map = {
        "H": f"ganó {row['HomeTeam']}",
        "A": f"ganó {row['AwayTeam']}",
        "D": "empate",
    }
    resultado_ht_map = {
        "H": f"ganaba {row['HomeTeam']}",
        "A": f"ganaba {row['AwayTeam']}",
        "D": "iban empatados",
    }
    sorpresa = "Sí, fue una sorpresa" if row["Upset"] else "No, ganó el favorito o empató"

    datos = f"""
--- DATOS DEL PARTIDO ---
Fecha: {row['MatchDate']}
Local: {row['HomeTeam']}
Visitante: {row['AwayTeam']}
Resultado final: {int(row['FTHome'])} - {int(row['FTAway'])} ({resultado_map[row['FTResult']]})
Al descanso: {int(row['HTHome'])} - {int(row['HTAway'])} ({resultado_ht_map[row['HTResult']]})

Estadísticas:
- Tiros (local / visitante): {int(row['HomeShots'])} / {int(row['AwayShots'])}
- Tiros al arco (local / visitante): {int(row['HomeTarget'])} / {int(row['AwayTarget'])}
- Corners (local / visitante): {int(row['HomeCorners'])} / {int(row['AwayCorners'])}
- Faltas (local / visitante): {int(row['HomeFouls'])} / {int(row['AwayFouls'])}
- Tarjetas amarillas (local / visitante): {int(row['HomeYellow'])} / {int(row['AwayYellow'])}
- Tarjetas rojas (local / visitante): {int(row['HomeRed'])} / {int(row['AwayRed'])}

Contexto:
- Favorito según cuotas: {row['Favorite']}
- ¿Fue sorpresa el resultado?: {sorpresa}
- Forma reciente local (últ. 5): {row['Form5Home']} pts
- Forma reciente visitante (últ. 5): {row['Form5Away']} pts
- Diferencia de Elo: {row['EloDiff']} puntos
"""

    return f"""{ROLES[estilo]}
Redactá una crónica periodística en español de aproximadamente 200 palabras sobre el siguiente partido de la Premier League.
La crónica debe tener un título atractivo y destacar los datos más relevantes. Acordate que si el nombre del equipo es Man significa Manchester, no lo acortes. Evitá repetir los nombres de los equipos en exceso y no uses abreviaturas. No incluyas información que no esté en los datos proporcionados.
{datos}"""
