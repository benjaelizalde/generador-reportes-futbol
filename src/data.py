from pathlib import Path

import pandas as pd

from src.paths import DATA_PATH, INDICE_CRONICAS, REPORTS_DIR


def load_matches(path=DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def get_teams(df: pd.DataFrame) -> list[str]:
    teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).dropna().unique()
    return sorted(teams.tolist())


def search_matches(df: pd.DataFrame, equipo: str) -> pd.DataFrame:
    mask = (
        df["HomeTeam"].str.contains(equipo, case=False, na=False)
        | df["AwayTeam"].str.contains(equipo, case=False, na=False)
    )
    return (
        df.loc[mask, ["MatchDate", "HomeTeam", "AwayTeam", "FTHome", "FTAway"]]
        .reset_index()
        .sort_values("MatchDate", ascending=False)
        .reset_index(drop=True)
    )


def format_match_label(row: pd.Series) -> str:
    return (
        f"{row['MatchDate']} | {row['HomeTeam']} "
        f"{int(row['FTHome'])}-{int(row['FTAway'])} {row['AwayTeam']}"
    )


def list_saved_chronicles() -> pd.DataFrame:
    if not INDICE_CRONICAS.exists():
        archivos = sorted(REPORTS_DIR.glob("*.txt"))
        if not archivos:
            return pd.DataFrame(columns=["label", "path"])
        return pd.DataFrame(
            {
                "label": [f.stem.replace("_", " ") for f in archivos],
                "path": archivos,
            }
        )

    indice = pd.read_csv(INDICE_CRONICAS)
    indice["path"] = indice["archivo"].apply(
        lambda p: (REPORTS_DIR / Path(p).name) if isinstance(p, str) else p
    )
    indice["label"] = indice.apply(
        lambda r: f"{r['MatchDate']} | {r['HomeTeam']} vs {r['AwayTeam']}",
        axis=1,
    )
    return indice[["label", "path", "MatchDate", "HomeTeam", "AwayTeam"]]


def read_saved_chronicle(path) -> str:
    return Path(path).read_text(encoding="utf-8")
