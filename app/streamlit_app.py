import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import (  # noqa: E402
    format_match_label,
    get_teams,
    list_saved_chronicles,
    load_matches,
    read_saved_chronicle,
    search_matches,
)
from src.generator import generate_cronica, get_client  # noqa: E402
from src.prompt import ESTILOS, build_prompt  # noqa: E402

ESTILO_LABELS = {
    "estandar": "Estándar (periodístico)",
    "tecnico": "Técnico (analítico)",
    "dramatico": "Dramático (apasionado)",
}


@st.cache_data
def cached_matches():
    return load_matches()


@st.cache_resource
def cached_client():
    return get_client()


def render_match_stats(partido):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resultado final", f"{int(partido['FTHome'])} - {int(partido['FTAway'])}")
    col2.metric("Al descanso", f"{int(partido['HTHome'])} - {int(partido['HTAway'])}")
    col3.metric("Favorito", str(partido["Favorite"]))
    col4.metric("Elo diff.", f"{partido['EloDiff']:.1f}")

    st.caption(f"Fecha: {partido['MatchDate']}")

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f"**{partido['HomeTeam']} (local)**")
        st.write(f"Tiros: {int(partido['HomeShots'])} ({int(partido['HomeTarget'])} al arco)")
        st.write(f"Corners: {int(partido['HomeCorners'])}")
        st.write(
            f"Faltas: {int(partido['HomeFouls'])} | "
            f"Amarillas: {int(partido['HomeYellow'])} | "
            f"Rojas: {int(partido['HomeRed'])}"
        )
        st.write(f"Forma (últ. 5): {partido['Form5Home']} pts")
    with stat_col2:
        st.markdown(f"**{partido['AwayTeam']} (visitante)**")
        st.write(f"Tiros: {int(partido['AwayShots'])} ({int(partido['AwayTarget'])} al arco)")
        st.write(f"Corners: {int(partido['AwayCorners'])}")
        st.write(
            f"Faltas: {int(partido['AwayFouls'])} | "
            f"Amarillas: {int(partido['AwayYellow'])} | "
            f"Rojas: {int(partido['AwayRed'])}"
        )
        st.write(f"Forma (últ. 5): {partido['Form5Away']} pts")

    if partido["Upset"]:
        st.warning("Resultado sorpresa según las cuotas previas.")
    else:
        st.info("Resultado acorde al favorito o empate esperado.")


def tab_generar(df):
    st.subheader("Generar crónica en vivo")

    col_equipo, col_partido = st.columns(2)
    with col_equipo:
        equipos = get_teams(df)
        equipo = st.selectbox("Equipo", equipos, index=equipos.index("Liverpool") if "Liverpool" in equipos else 0)

    partidos = search_matches(df, equipo)
    if partidos.empty:
        st.warning("No se encontraron partidos para ese equipo.")
        return

    with col_partido:
        labels = [format_match_label(row) for _, row in partidos.iterrows()]
        partido_idx = st.selectbox("Partido", range(len(labels)), format_func=lambda i: labels[i])

    partido = df.loc[partidos.loc[partido_idx, "index"]]

    estilo = st.radio(
        "Estilo de la crónica",
        ESTILOS,
        format_func=lambda e: ESTILO_LABELS[e],
        horizontal=True,
    )

    comparar = st.checkbox("Comparar los 3 estilos (3 llamadas a la API)", value=False)

    st.markdown(f"### {partido['HomeTeam']} vs {partido['AwayTeam']}")
    render_match_stats(partido)

    if not st.button("Generar crónica", type="primary"):
        return

    try:
        client = cached_client()
    except RuntimeError as exc:
        st.error(str(exc))
        return

    estilos_a_generar = list(ESTILOS) if comparar else [estilo]

    for est in estilos_a_generar:
        titulo = ESTILO_LABELS[est] if comparar else "Crónica generada"
        with st.spinner(f"Generando con LLaMA 3.3 70B ({ESTILO_LABELS[est]})..."):
            try:
                cronica = generate_cronica(build_prompt(partido, estilo=est), client=client)
            except Exception as exc:
                st.error(f"Error al generar la crónica: {exc}")
                return

        st.markdown(f"#### {titulo}")
        st.markdown(cronica)
        if comparar and est != estilos_a_generar[-1]:
            st.divider()


def tab_cronicas_guardadas():
    st.subheader("Crónicas pre-generadas")
    st.caption("Plan B para la demo si la API no está disponible.")

    cronicas = list_saved_chronicles()
    if cronicas.empty:
        st.info("No hay crónicas guardadas en la carpeta reports/.")
        return

    seleccion = st.selectbox("Elegir crónica", cronicas["label"].tolist())
    fila = cronicas.loc[cronicas["label"] == seleccion].iloc[0]

    if not Path(fila["path"]).exists():
        st.error("No se encontró el archivo de la crónica seleccionada.")
        return

    st.markdown(read_saved_chronicle(fila["path"]))


def main():
    st.set_page_config(
        page_title="Generador de Crónicas",
        page_icon="⚽",
        layout="wide",
    )

    st.title("Generador de Reportes de Fútbol")
    st.markdown(
        "Sistema de **IA generativa** que transforma estadísticas reales de la "
        "**Premier League** en crónicas periodísticas. Modelo: **LLaMA 3.3 70B** (Groq)."
    )

    df = cached_matches()
    st.sidebar.metric("Partidos disponibles", f"{len(df):,}".replace(",", "."))

    tab_live, tab_saved = st.tabs(["Generar en vivo", "Crónicas guardadas"])

    with tab_live:
        tab_generar(df)

    with tab_saved:
        tab_cronicas_guardadas()


if __name__ == "__main__":
    main()
