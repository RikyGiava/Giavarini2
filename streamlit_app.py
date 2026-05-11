import math
import html
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="The Olympic Archive",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Roboto+Mono:wght@400;500;600&family=Roboto+Condensed:wght@700&family=Space+Mono&display=swap');

    :root {
        --paper: #f4efe3;
        --ink: #171717;
        --muted: #68645c;
        --brass: #b88a2e;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--paper);
        color: var(--ink);
    }

    .stApp {
        background-color: #f4efe3;
        background-image: radial-gradient(rgba(0,0,0,0.06) 1px, transparent 1px);
        background-size: 6px 6px;
    }

    [data-testid="stHeader"] {
        background-color: rgba(244, 239, 227, 0);
    }

    .block-container {
        padding-top: 0rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Force Streamlit widgets text to black */
    [data-testid="stSlider"] label,
    [data-testid="stSlider"] span,
    [data-testid="stSlider"] div,
    [data-testid="stSlider"] *,
    [data-testid="stMetric"],
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] div,
    [data-testid="stMetricValue"],
    [data-testid="stMetric"] *,
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] *,
    [data-testid="stSelectSlider"] label,
    [data-testid="stSelectSlider"] div,
    [data-testid="stSelectSlider"] span,
    [data-testid="stSelectSlider"] * {
        color: #171717 !important;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(38px, 5vw, 62px);
        text-align: center;
        margin-bottom: 0px;
        color: var(--ink);
        line-height: 1.05;
    }

    .intro-section {
        text-align: center;
        margin-top: 34px;
        margin-bottom: 38px;
    }

    .intro-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin: 22px auto 22px auto;
    }

    .intro-divider span:not(.intro-star) {
        display: block;
        width: 88px;
        height: 1px;
        background: rgba(23, 23, 23, 0.35);
    }

    .intro-star {
        font-size: 18px;
        color: var(--brass);
    }

    .intro-copy {
        max-width: 760px;
        margin: 0 auto 8px auto;
        text-align: center;
    }

    .intro-kicker {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.42em;
        color: var(--brass);
        margin-bottom: 10px;
    }

    .subtitle {
        max-width: 760px;
        margin: 0 auto;
        text-align: center;
        font-style: italic;
        color: rgba(23,23,23,0.78);
        font-size: 18px;
        line-height: 1.7;
    }

    .section-kicker {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: var(--muted);
        margin-bottom: 16px;
    }

    .section-kicker::before,
    .section-kicker::after {
        content: "";
        width: 55px;
        height: 1px;
        background-color: rgba(23,23,23,0.4);
    }

    .section-title {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: clamp(32px, 4vw, 46px);
        margin-bottom: 32px;
        color: var(--ink);
    }

    .summer-only {
        text-align: center;
        margin-top: 14px;
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: var(--brass);
    }

    div.stButton > button {
        width: 100%;
        border: 2px solid var(--ink);
        border-radius: 0;
        background-color: var(--paper);
        color: var(--ink);
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        padding: 0.65rem 1rem;
        transition: all 0.18s ease;
        box-shadow: none;
    }

    div.stButton > button:hover {
        border-color: var(--ink);
        background-color: var(--ink);
        color: var(--paper);
        transform: translateY(-1px);
        box-shadow: 5px 5px 0px var(--brass);
    }

    div.stButton > button:focus {
        border-color: var(--ink);
        color: var(--ink);
        box-shadow: none;
    }

    .active-era {
        width: 100%;
        border: 2px solid #171717;
        background: #171717;
        color: #f4efe3;
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        padding: 0.65rem 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        border-top: 2px solid var(--ink);
        border-bottom: 2px solid var(--ink);
        margin: 46px 0;
    }

    .stat-box {
        text-align: center;
        padding: 28px 10px;
    }

    .stat-box:not(:first-child) {
        border-left: 2px solid var(--ink);
    }

    .stat-value {
        font-family: 'Playfair Display', serif;
        font-size: clamp(36px, 5vw, 58px);
        color: var(--ink);
        line-height: 1;
    }

    .stat-label {
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: var(--muted);
        margin-top: 10px;
    }

    .dispatch-card {
        background-color: var(--paper);
        border: 2px solid var(--ink);
        padding: 26px;
        min-height: 230px;
        transition: all 0.22s ease;
        margin-bottom: 8px;
    }

    .dispatch-card:hover {
        background-color: rgba(184,138,46,0.10);
        transform: translateY(-2px);
    }

    .dispatch-card-active {
        background-color: var(--ink);
        color: var(--paper);
        border: 2px solid var(--ink);
        padding: 26px;
        min-height: 230px;
        margin-bottom: 8px;
    }

    .stamp {
        display: inline-block;
        border: 1.5px solid currentColor;
        padding: 5px 10px;
        font-family: 'Roboto Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.25em;
        color: inherit;
    }

    .glyph {
        float: right;
        font-family: 'Playfair Display', serif;
        font-size: 38px;
        color: var(--brass);
        line-height: 1;
    }

    .card-title {
        clear: both;
        font-family: 'Playfair Display', serif;
        font-size: 27px;
        line-height: 1.15;
        margin-top: 26px;
        margin-bottom: 12px;
    }

    .card-desc {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        line-height: 1.7;
        color: rgba(23,23,23,0.72);
    }

    .card-desc-active {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        line-height: 1.7;
        color: rgba(244,239,227,0.80);
    }

    .tap-label {
        font-family: 'Roboto Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-top: 20px;
        color: var(--muted);
    }

    .tap-label-active {
        font-family: 'Roboto Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        margin-top: 20px;
        color: var(--paper);
    }

    .paper-panel {
        background-color: var(--paper);
        border: 2px solid var(--ink);
        padding: 26px;
        margin-top: 30px;
        margin-bottom: 18px;
    }

    .panel-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }

    .panel-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(28px, 4vw, 40px);
        margin: 0;
        color: var(--ink);
        line-height: 1.1;
    }

    .italic-desc {
        font-style: italic;
        color: rgba(23,23,23,0.72);
        margin: 8px 0 16px 0;
        font-size: 16px;
        line-height: 1.5;
    }

    .ring-panel {
        border: 2px solid var(--ink);
        background-color: rgba(255,255,255,0.12);
        padding: 24px 32px;
        margin-top: 36px;
        margin-bottom: 22px;
        box-shadow: 5px 5px 0px #171717;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 0;
    }

    .mono-small {
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: var(--muted);
    }

    .athlete-card {
        border: 2px solid var(--ink);
        background-color: var(--paper);
        padding: 22px;
        margin-bottom: 18px;
    }

    .athlete-name {
        font-family: 'Playfair Display', serif;
        font-size: clamp(34px, 5vw, 52px);
        margin: 8px 0 0 0;
        color: var(--ink);
        line-height: 1.05;
    }

    .tag-wrapper {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .mini-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        border: 1.5px solid var(--ink);
        padding: 6px 10px;
        font-family: 'Playfair Display', serif;
        font-size: 14px;
        background-color: var(--paper);
        color: var(--ink);
    }

    .mono-tag {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
    }

    .trivia-card {
        border: 2px solid var(--ink);
        background-color: var(--paper);
        padding: 20px;
        min-height: 180px;
        transition: background-color 0.2s ease;
        margin-bottom: 8px;
    }

    .trivia-card:hover {
        background-color: rgba(184,138,46,0.10);
    }

    .trivia-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }

    .trivia-question-mark {
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        color: var(--brass);
    }

    .trivia-question {
        font-family: 'Playfair Display', serif;
        font-size: 21px;
        line-height: 1.2;
        color: var(--ink);
    }

    .trivia-answer {
        border: 2px solid var(--ink);
        padding: 16px;
        margin-bottom: 18px;
        background-color: var(--paper);
    }

    .trivia-answer-main {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        color: var(--brass);
        margin-bottom: 6px;
    }

    .trivia-detail {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        line-height: 1.6;
        color: rgba(23,23,23,0.7);
    }

    .section-box {
        border: 2px solid #171717;
        background: rgba(255,255,255,0.18);
        padding: 26px;
        margin: 28px auto;
        box-shadow: 6px 6px 0px #171717;
    }

    .cartography-title {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: clamp(38px, 5vw, 58px);
        color: #171717;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .cartography-subtitle {
        text-align: center;
        font-family: 'Roboto Mono', monospace;
        letter-spacing: 0.3em;
        font-size: 12px;
        color: #b88a2e;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    .host-row {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px dotted rgba(17,24,39,0.45);
        padding: 7px 0;
        font-size: 14px;
        color: #171717 !important;
    }

    .host-year {
        font-family: 'Playfair Display', serif;
        font-size: 18px;
        font-weight: bold;
        color: #171717 !important;
    }

    .host-city {
        font-style: italic;
        color: #171717 !important;
    }

    .footer {
        border-top: 2px solid var(--ink);
        margin-top: 56px;
        padding: 25px 0 5px 0;
        text-align: center;
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: var(--muted);
    }

    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: 1fr;
        }

        .stat-box:not(:first-child) {
            border-left: none;
            border-top: 2px solid var(--ink);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA
# ============================================================

REQUIRED_COLUMNS = [
    "ID", "Name", "Sex", "Age", "Height", "Weight", "Team", "NOC",
    "Games", "Year", "Season", "City", "Sport", "Event", "Medal"
]


@st.cache_data(show_spinner=False)
def clean_dataframe(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.error(f"Mancano queste colonne nel file Excel: {missing}")
        st.write("Colonne presenti nel file:")
        st.write(df.columns.tolist())
        st.stop()

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)

    for col in ["Season", "Sport", "Event", "Name", "NOC", "City", "Games", "Team"]:
        df[col] = df[col].astype(str).str.strip()

    df = df[df["Season"].str.lower() == "summer"].copy()

    df["Medal"] = df["Medal"].replace(
        {
            "NA": pd.NA,
            "nan": pd.NA,
            "None": pd.NA,
            "": pd.NA
        }
    )

    df_medals = df[df["Medal"].notna()].copy()

    return df, df_medals


@st.cache_data(show_spinner="Loading Olympic Excel dataset...")
def load_excel_from_path(path):
    df = pd.read_excel(
        path,
        usecols=REQUIRED_COLUMNS,
        engine="openpyxl"
    )
    return clean_dataframe(df)


@st.cache_data(show_spinner="Loading uploaded Olympic Excel dataset...")
def load_excel_from_upload(uploaded_file):
    df = pd.read_excel(
        uploaded_file,
        usecols=REQUIRED_COLUMNS,
        engine="openpyxl"
    )
    return clean_dataframe(df)


# ============================================================
# HELPERS
# ============================================================

ERAS = ["1896-1936", "1937-1976", "1977-2016", "ALL"]


def era_range(era):
    if era == "ALL":
        return 1896, 2016
    a, b = era.split("-")
    return int(a), int(b)


def era_label(era):
    if era == "ALL":
        return "ALL · 1896–2016"
    return era.replace("-", "–")


def year_to_era(year):
    if 1896 <= year <= 1936:
        return "1896-1936"
    if 1937 <= year <= 1976:
        return "1937-1976"
    if 1977 <= year <= 2016:
        return "1977-2016"
    return "Other"


def safe_js(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
        .replace("\n", " ")
    )


def sport_emoji(sport):
    emojis = {
        "Archery": "🏹",
        "Athletics": "🏃",
        "Badminton": "🏸",
        "Baseball": "⚾",
        "Basketball": "🏀",
        "Beach Volleyball": "🏐",
        "Boxing": "🥊",
        "Canoeing": "🛶",
        "Cycling": "🚴",
        "Diving": "🤿",
        "Equestrian": "🐎",
        "Equestrianism": "🐎",
        "Fencing": "🤺",
        "Football": "⚽",
        "Golf": "⛳",
        "Gymnastics": "🤸",
        "Handball": "🤾",
        "Hockey": "🏑",
        "Judo": "🥋",
        "Modern Pentathlon": "🎖️",
        "Rowing": "🚣",
        "Rugby": "🏉",
        "Rugby Sevens": "🏉",
        "Sailing": "⛵",
        "Shooting": "🎯",
        "Softball": "🥎",
        "Swimming": "🏊",
        "Synchronized Swimming": "🏊",
        "Table Tennis": "🏓",
        "Taekwondo": "🥋",
        "Tennis": "🎾",
        "Trampolining": "🤸",
        "Triathlon": "🏊",
        "Volleyball": "🏐",
        "Water Polo": "🤽",
        "Weightlifting": "🏋️",
        "Wrestling": "🤼",
        "Art Competitions": "🎨",
        "Tug-Of-War": "🪢",
        "Polo": "🏇",
        "Lacrosse": "🥍",
        "Cricket": "🏏",
        "Croquet": "🎯",
        "Jeu De Paume": "🎾",
        "Racquets": "🎾",
        "Motorboating": "🚤",
        "Basque Pelota": "🏐",
        "Alpinism": "⛰️",
        "Aeronautics": "✈️",
        "Roque": "🏅",
    }

    return emojis.get(str(sport), "🏅")


@st.cache_data(show_spinner=False)
def filter_era_data(df, df_medals, era):
    start_year, end_year = era_range(era)

    df_era = df[
        (df["Year"] >= start_year) &
        (df["Year"] <= end_year)
    ].copy()

    df_medals_era = df_medals[
        (df_medals["Year"] >= start_year) &
        (df_medals["Year"] <= end_year)
    ].copy()

    return df_era, df_medals_era


@st.cache_data(show_spinner=False)
def build_sport_stats_for_rings(period_df):
    period_df = period_df.copy()

    sport_counts = (
        period_df.groupby("Sport")
        .size()
        .sort_values(ascending=False)
    )

    sports_to_show = sport_counts.head(52).index.tolist()

    medals_mask = period_df["Medal"].notna()

    base_stats = (
        period_df
        .groupby("Sport")
        .agg(
            disciplines=("Event", "nunique"),
            athletes=("Name", "nunique"),
            rows=("ID", "count")
        )
        .reset_index()
    )

    medal_stats = (
        period_df[medals_mask]
        .groupby("Sport")
        .size()
        .reset_index(name="medals")
    )

    unique_medals = (
        period_df[medals_mask]
        .drop_duplicates(subset=["Year", "Sport", "Event", "Medal", "NOC"])
    )

    if unique_medals.empty:
        top_country_table = pd.DataFrame(
            columns=["Sport", "top_country", "top_country_medals"]
        )
    else:
        country_table = (
            unique_medals
            .groupby(["Sport", "NOC"])
            .size()
            .reset_index(name="top_country_medals")
            .sort_values(["Sport", "top_country_medals"], ascending=[True, False])
        )

        top_country_table = (
            country_table
            .drop_duplicates("Sport")
            .rename(columns={"NOC": "top_country"})
        )

    merged = (
        base_stats
        .merge(medal_stats, on="Sport", how="left")
        .merge(
            top_country_table[["Sport", "top_country", "top_country_medals"]],
            on="Sport",
            how="left"
        )
    )

    merged["medals"] = merged["medals"].fillna(0).astype(int)
    merged["top_country"] = merged["top_country"].fillna("No medals")
    merged["top_country_medals"] = merged["top_country_medals"].fillna(0).astype(int)

    merged = merged[merged["Sport"].isin(sports_to_show)]

    sport_stats = {}

    for _, row in merged.iterrows():
        sport = row["Sport"]

        sport_stats[sport] = {
            "icon": sport_emoji(sport),
            "disciplines": int(row["disciplines"]),
            "athletes": int(row["athletes"]),
            "medals": int(row["medals"]),
            "top_country": str(row["top_country"]),
            "top_country_medals": int(row["top_country_medals"]),
        }

    return sports_to_show, sport_stats


# ============================================================
# MAIN COMPONENTS
# ============================================================

def masthead():
    components.html(
        """
        <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Roboto+Mono:wght@400;500;600&display=swap');

                body {
                    margin: 0;
                    background: #f4efe3;
                    color: #171717;
                }

                .masthead-newspaper {
                    border-bottom: 4px double #171717;
                    padding: 26px 24px 24px 24px;
                    background-color: #f4efe3;
                }

                .masthead-wrap {
                    max-width: 1280px;
                    margin: 0 auto;
                    text-align: center;
                }

                .masthead-meta {
                    font-family: 'Roboto Mono', monospace;
                    font-size: 11px;
                    text-transform: uppercase;
                    letter-spacing: 0.35em;
                    color: #68645c;
                    margin-bottom: 16px;
                }

                .masthead-title {
                    display: block;
                    font-family: 'Playfair Display', serif;
                    font-size: clamp(44px, 7vw, 82px);
                    color: #171717;
                    line-height: 0.95;
                    text-align: center;
                    text-decoration: none;
                    margin: 0;
                }

                .masthead-subtitle {
                    max-width: 760px;
                    margin: 16px auto 0 auto;
                    text-align: center;
                    font-style: italic;
                    font-size: 18px;
                    line-height: 1.5;
                    color: #6a5640;
                }
            </style>
        </head>

        <body>
            <header class="masthead-newspaper">
                <div class="masthead-wrap">
                    <div class="masthead-meta">
                        Vol. 1 · No. 120 · Established 1896
                    </div>

                    <div class="masthead-title">
                        The Olympic Archive
                    </div>

                    <div class="masthead-subtitle">
                        An interactive Olympic history experience for sports fans, curious minds and data explorers.
                    </div>
                </div>
            </header>
        </body>
        </html>
        """,
        height=190,
        scrolling=False
    )


def intro():
    intro_html = """
    <section class="intro-section">
        <h1 class="main-title">One Hundred &amp; Twenty Years of Sport</h1>
        <div class="intro-divider">
            <span></span>
            <span class="intro-star">✦</span>
            <span></span>
        </div>
        <div class="intro-copy">
            <div class="intro-kicker">Choose an era.</div>
            <p class="subtitle">
                Explore the Summer Games through sports, champions, nations and host cities.
            </p>
        </div>
    </section>
    """
    st.markdown(intro_html, unsafe_allow_html=True)


def era_controls():
    st.markdown('<div class="section-kicker">Select Era</div>', unsafe_allow_html=True)

    cols = st.columns(len(ERAS))

    for col, era in zip(cols, ERAS):
        with col:
            if st.session_state.era == era:
                st.markdown(
                    f'<div class="active-era">{era_label(era)}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(era_label(era), key=f"era_{era}", use_container_width=True):
                    st.session_state.era = era
                    st.session_state.active_block = None
                    st.session_state.page = "main"
                    st.rerun()

    st.markdown(
        '<div class="summer-only">◆ Summer Games Only ◆</div>',
        unsafe_allow_html=True
    )


def stats_strip(editions, athlete_entries, medals_awarded):
    st.markdown(
        f"""
        <section class="stats-container">
            <div class="stat-box">
                <div class="stat-value">{editions:,}</div>
                <div class="stat-label">Editions</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{athlete_entries:,}</div>
                <div class="stat-label">Athlete Entries</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{medals_awarded:,}</div>
                <div class="stat-label">Medal Entries</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )


def dispatch_card(block_id, stamp, title, desc, glyph):
    active = st.session_state.get("active_block") == block_id

    card_class = "dispatch-card-active" if active else "dispatch-card"
    desc_class = "card-desc-active" if active else "card-desc"
    tap_class = "tap-label-active" if active else "tap-label"
    tap_text = "▼ Open below" if active else "Tap to open →"

    st.markdown(
        f"""
        <div class="{card_class}">
            <span class="stamp">{stamp}</span>
            <span class="glyph">{glyph}</span>
            <div class="card-title">{title}</div>
            <div class="{desc_class}">{desc}</div>
            <div class="{tap_class}">{tap_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Open", key=f"open_{block_id}", use_container_width=True):
        st.session_state.active_block = block_id
        st.rerun()


def footer():
    st.markdown(
        """
        <div class="footer">
            Compiled from the Athlete Events Register · 1896 — 2016
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# YEAR EXPLORER PAGE
# ============================================================

def year_archive_explorer(df, df_medals):
    st.markdown(
        """
        <div class="cartography-title">Explore a Single Olympic Year</div>
        <div class="cartography-subtitle">◆ Olympic editions only · Summer Games ◆</div>
        """,
        unsafe_allow_html=True
    )

    back_col1, back_col2, back_col3 = st.columns([1, 1.2, 1])

    with back_col2:
        if st.button("← Back to Olympic Archive", key="back_from_year"):
            st.session_state.page = "main"
            st.rerun()

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">Olympic Year Explorer</h2>
                <span class="stamp">Olympic editions only</span>
            </div>
            <p class="italic-desc">
                Move through the Olympic timeline and choose how to visualize the data from a specific Summer Games edition.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    available_years = sorted(df["Year"].dropna().unique().astype(int).tolist())

    selected_year = st.select_slider(
        "Choose an Olympic year",
        options=available_years,
        value=available_years[-1]
    )

    year_df = df[df["Year"] == selected_year].copy()
    year_medals_df = df_medals[df_medals["Year"] == selected_year].copy()

    city = year_df["City"].dropna().iloc[0]
    games = year_df["Games"].dropna().iloc[0]

    athletes = year_df["Name"].nunique()
    athlete_entries = len(year_df)
    sports = year_df["Sport"].nunique()
    events = year_df["Event"].nunique()
    nations = year_df["NOC"].nunique()
    medal_entries = len(year_medals_df)

    st.markdown(
        f"""
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">{int(selected_year)} · {html.escape(str(city))}</h2>
                <span class="stamp">{html.escape(str(games))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Athletes", f"{athletes:,}")
    c2.metric("Entries", f"{athlete_entries:,}")
    c3.metric("Sports", sports)
    c4.metric("Events", events)
    c5.metric("Nations", nations)
    c6.metric("Medal entries", medal_entries)

    chart_choice = st.selectbox(
        "Choose chart",
        [
            "Top countries by medals",
            "Athlete entries by sport",
            "Events by sport",
            "Gender distribution",
            "Medal types distribution"
        ]
    )

    if chart_choice == "Top countries by medals":
        if year_medals_df.empty:
            st.info("No medal data available for this year.")
            return

        chart_df = (
            year_medals_df
            .groupby("NOC")
            .size()
            .sort_values(ascending=False)
            .head(15)
            .reset_index(name="Medal entries")
        )

        fig = px.bar(
            chart_df,
            x="NOC",
            y="Medal entries",
            text="Medal entries",
            title=f"Top Countries by Medal Entries · {selected_year}"
        )

        fig.update_traces(
            marker_color="#b88a2e",
            marker_line_color="#171717",
            marker_line_width=1.2,
            textposition="outside"
        )

    elif chart_choice == "Athlete entries by sport":
        chart_df = (
            year_df
            .groupby("Sport")
            .size()
            .sort_values(ascending=False)
            .head(15)
            .reset_index(name="Athlete entries")
        )

        fig = px.bar(
            chart_df,
            x="Athlete entries",
            y="Sport",
            orientation="h",
            text="Athlete entries",
            title=f"Athlete Entries by Sport · {selected_year}"
        )

        fig.update_traces(
            marker_color="#171717",
            marker_line_color="#171717",
            marker_line_width=1.2,
            textposition="outside"
        )

        fig.update_layout(yaxis=dict(autorange="reversed"))

    elif chart_choice == "Events by sport":
        chart_df = (
            year_df
            .groupby("Sport")["Event"]
            .nunique()
            .sort_values(ascending=False)
            .head(15)
            .reset_index(name="Events")
        )

        fig = px.bar(
            chart_df,
            x="Sport",
            y="Events",
            text="Events",
            title=f"Events by Sport · {selected_year}"
        )

        fig.update_traces(
            marker_color="#b88a2e",
            marker_line_color="#171717",
            marker_line_width=1.2,
            textposition="outside"
        )

        fig.update_layout(xaxis_tickangle=-35)

    elif chart_choice == "Gender distribution":
        chart_df = (
            year_df
            .groupby("Sex")
            .size()
            .reset_index(name="Athlete entries")
        )

        fig = px.pie(
            chart_df,
            names="Sex",
            values="Athlete entries",
            title=f"Gender Distribution · {selected_year}",
            hole=0.45
        )

        fig.update_traces(
            marker=dict(line=dict(color="#171717", width=1.5))
        )

    else:
        if year_medals_df.empty:
            st.info("No medal data available for this year.")
            return

        chart_df = (
            year_medals_df
            .groupby("Medal")
            .size()
            .reindex(["Gold", "Silver", "Bronze"])
            .dropna()
            .reset_index(name="Count")
        )

        fig = px.bar(
            chart_df,
            x="Medal",
            y="Count",
            text="Count",
            title=f"Medal Types Distribution · {selected_year}"
        )

        fig.update_traces(
            marker_color="#b88a2e",
            marker_line_color="#171717",
            marker_line_width=1.2,
            textposition="outside"
        )

    fig.update_layout(
        height=460,
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        font=dict(family="Roboto Mono", color="#171717"),
        title_font=dict(family="Playfair Display", size=26),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# OLYMPIC RINGS
# ============================================================

def olympic_rings(period_df, era):
    sports_to_show, sport_stats = build_sport_stats_for_rings(period_df)

    sports_number = len(sports_to_show)
    selected_period = era_label(era)
    safe_selected_period = html.escape(selected_period)

    def generate_positions(number_of_sports):
        ring_centers = [
            (230, 260),
            (505, 260),
            (780, 260),
            (365, 430),
            (640, 430),
        ]

        radius = 122
        positions = []

        for i in range(number_of_sports):
            ring_index = i % 5
            angle_index = i // 5
            angle = (angle_index * 38 + ring_index * 11) % 360
            angle_rad = math.radians(angle)
            cx, cy = ring_centers[ring_index]
            x = cx + radius * math.cos(angle_rad) - 22
            y = cy + radius * math.sin(angle_rad) - 22
            positions.append((x, y))

        return positions

    positions = generate_positions(len(sports_to_show))

    rings_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&family=Space+Mono&display=swap');

    body {{
        margin: 0;
        background: transparent;
        overflow: hidden;
    }}

    .rings-container {{
        position: relative;
        width: 1050px;
        height: 650px;
        border: 2px solid #111827;
        border-radius: 22px;
        margin: 0 auto;
        background-color: rgba(255,255,255,0.20);
        overflow: hidden;
        box-shadow: 8px 8px 0px #111827;
    }}

    .period-label {{
        position: absolute;
        top: 28px;
        left: 48px;
        border: 2px solid #111827;
        border-radius: 12px;
        padding: 8px 18px;
        font-family: 'Space Mono', monospace;
        font-size: 14px;
        letter-spacing: 2px;
        background: #f7f0e3;
        z-index: 20;
        color: #111827;
    }}

    .discipline-label {{
        position: absolute;
        top: 35px;
        right: 58px;
        font-family: 'Space Mono', monospace;
        font-size: 15px;
        letter-spacing: 6px;
        color: #111827;
        z-index: 20;
    }}

    .instruction {{
        position: absolute;
        bottom: 28px;
        width: 100%;
        text-align: center;
        font-family: 'Space Mono', monospace;
        letter-spacing: 4px;
        font-size: 13px;
        color: #111827;
        z-index: 20;
    }}

    .ring {{
        position: absolute;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: transparent;
        z-index: 1;
    }}

    .ring-blue {{
        left: 105px;
        top: 135px;
        border: 17px solid #1d5f9f;
    }}

    .ring-yellow {{
        left: 380px;
        top: 135px;
        border: 17px solid #e6b31e;
    }}

    .ring-black {{
        left: 655px;
        top: 135px;
        border: 17px solid #1f2933;
    }}

    .ring-green {{
        left: 240px;
        top: 305px;
        border: 17px solid #2e7d4f;
    }}

    .ring-red {{
        left: 515px;
        top: 305px;
        border: 17px solid #c74639;
    }}

    .sport-badge {{
        position: absolute;
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: #f8f3e7;
        border: 2px solid #111827;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        z-index: 10;
        box-shadow: 3px 3px 0px #111827;
        transition: all 0.18s ease-in-out;
        text-decoration: none;
        font-family: inherit;
        padding: 0;
    }}

    .sport-badge:hover {{
        transform: scale(1.22) rotate(-5deg);
        background: #ffffff;
        box-shadow: 5px 5px 0px #a16207;
        z-index: 30;
    }}

    .sport-tooltip {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        bottom: 54px;
        left: 50%;
        transform: translateX(-50%);
        background: #111827;
        color: #f8f3e7;
        border-radius: 8px;
        padding: 6px 10px;
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        white-space: nowrap;
        transition: opacity 0.15s ease-in-out;
        pointer-events: none;
    }}

    .sport-badge:hover .sport-tooltip {{
        visibility: visible;
        opacity: 1;
    }}

    .info-panel {{
        position: absolute;
        left: 45px;
        bottom: 70px;
        width: 405px;
        border: 2px solid #111827;
        border-radius: 18px;
        background: #f8f3e7;
        box-shadow: 6px 6px 0px #111827;
        padding: 18px;
        z-index: 60;
        display: none;
    }}

    .info-panel.show {{
        display: block;
    }}

    .info-title {{
        font-family: 'Roboto Condensed', sans-serif;
        font-size: 34px;
        letter-spacing: 2px;
        color: #111827;
        margin-bottom: 10px;
        padding-right: 35px;
    }}

    .info-row {{
        display: flex;
        justify-content: space-between;
        gap: 18px;
        border-top: 1px solid rgba(17,24,39,0.35);
        padding: 9px 0;
        font-family: 'Space Mono', monospace;
        font-size: 13px;
        color: #111827;
    }}

    .info-label {{
        letter-spacing: 1px;
    }}

    .info-value {{
        font-weight: bold;
        text-align: right;
    }}

    .close-info {{
        position: absolute;
        top: 8px;
        right: 12px;
        border: 2px solid #111827;
        background: #111827;
        color: #f8f3e7;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        font-family: 'Space Mono', monospace;
        cursor: pointer;
    }}

    .close-info:hover {{
        background: #a16207;
    }}
    </style>
    </head>

    <body>
    <div class="rings-container">
        <div class="period-label">SUMMER · {safe_selected_period}</div>
        <div class="discipline-label">{sports_number} SPORTS</div>

        <div class="ring ring-blue"></div>
        <div class="ring ring-yellow"></div>
        <div class="ring ring-black"></div>
        <div class="ring ring-green"></div>
        <div class="ring ring-red"></div>
    """

    for sport, position in zip(sports_to_show, positions):
        x, y = position
        icon = sport_stats[sport]["icon"]
        safe_sport_html = html.escape(str(sport))
        safe_sport_js = safe_js(sport)

        disciplines_count = sport_stats[sport]["disciplines"]
        athletes_count = sport_stats[sport]["athletes"]
        medals_count = sport_stats[sport]["medals"]
        top_country = sport_stats[sport]["top_country"]
        top_country_medals = sport_stats[sport]["top_country_medals"]

        rings_html += f"""
        <button class="sport-badge"
           onclick="openSportInfo(
                `{safe_sport_js}`,
                `{safe_js(icon)}`,
                `{disciplines_count}`,
                `{athletes_count}`,
                `{medals_count}`,
                `{safe_js(top_country)}`,
                `{top_country_medals}`
           )"
           title="{safe_sport_html}"
           style="left:{x}px; top:{y}px;">
           {icon}
           <span class="sport-tooltip">{safe_sport_html}</span>
        </button>
        """

    rings_html += f"""
        <div id="infoPanel" class="info-panel">
            <button class="close-info" onclick="closeSportInfo()">×</button>

            <div id="infoTitle" class="info-title">Sport</div>

            <div class="info-row">
                <div class="info-label">PERIOD</div>
                <div class="info-value">{safe_selected_period}</div>
            </div>

            <div class="info-row">
                <div class="info-label">DISCIPLINES</div>
                <div id="infoDisciplines" class="info-value">-</div>
            </div>

            <div class="info-row">
                <div class="info-label">ATHLETES</div>
                <div id="infoAthletes" class="info-value">-</div>
            </div>

            <div class="info-row">
                <div class="info-label">TOTAL MEDAL ENTRIES</div>
                <div id="infoMedals" class="info-value">-</div>
            </div>

            <div class="info-row">
                <div class="info-label">BEST COUNTRY</div>
                <div id="infoCountry" class="info-value">-</div>
            </div>

            <div class="info-row">
                <div class="info-label">UNIQUE MEDALS</div>
                <div id="infoCountryMedals" class="info-value">-</div>
            </div>
        </div>

        <div class="instruction">
            HOVER A BADGE TO READ ITS SPORT · CLICK TO OPEN THE DISPATCH
        </div>
    </div>

    <script>
    function openSportInfo(sport, icon, disciplines, athletes, medals, country, countryMedals) {{
        document.getElementById("infoPanel").classList.add("show");
        document.getElementById("infoTitle").innerHTML = icon + " " + sport;
        document.getElementById("infoDisciplines").innerHTML = disciplines;
        document.getElementById("infoAthletes").innerHTML = athletes;
        document.getElementById("infoMedals").innerHTML = medals;
        document.getElementById("infoCountry").innerHTML = country;
        document.getElementById("infoCountryMedals").innerHTML = countryMedals;
    }}

    function closeSportInfo() {{
        document.getElementById("infoPanel").classList.remove("show");
    }}
    </script>

    </body>
    </html>
    """

    components.html(rings_html, height=700, scrolling=False)


# ============================================================
# ATHLETE EXPLORER
# ============================================================

@st.cache_data(show_spinner=False)
def build_athlete_stats(df_medals):
    athlete_stats = (
        df_medals
        .groupby(["Name", "NOC"])
        .agg(
            gold=("Medal", lambda x: (x == "Gold").sum()),
            silver=("Medal", lambda x: (x == "Silver").sum()),
            bronze=("Medal", lambda x: (x == "Bronze").sum()),
            total=("Medal", "count"),
            sports=("Sport", lambda x: sorted(x.dropna().unique())),
            eras=("Year", lambda x: sorted(set(year_to_era(y) for y in x)))
        )
        .reset_index()
        .sort_values(["total", "gold", "silver", "bronze"], ascending=False)
    )

    return athlete_stats


def athlete_explorer(df_medals):
    athlete_stats = build_athlete_stats(df_medals)

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">Detailed Zone · Athlete Explorer</h2>
                <span class="stamp">Search the Champions</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <p class="italic-desc">
            Search any of the {len(athlete_stats):,} medal-winning athletes indexed across the Summer Games.
        </p>
        """,
        unsafe_allow_html=True
    )

    q = st.text_input(
        "Search athlete",
        placeholder="Type a name or country code, for example USA, GBR, ITA…",
        label_visibility="collapsed"
    )

    if q.strip():
        t = q.lower()
        results = athlete_stats[
            athlete_stats["Name"].str.lower().str.contains(t, na=False) |
            athlete_stats["NOC"].str.lower().str.contains(t, na=False)
        ].head(12)
    else:
        results = athlete_stats.head(12)

    if results.empty:
        st.info("No athlete found.")
        return

    col_left, col_right = st.columns([1, 2])

    with col_left:
        options = [
            f"{row.Name} · {row.NOC} · {row.total} medals"
            for row in results.itertuples()
        ]

        picked_label = st.radio(
            "Results",
            options,
            label_visibility="collapsed"
        )

        picked_index = options.index(picked_label)
        picked = results.iloc[picked_index]

    with col_right:
        st.markdown(
            f"""
            <div class="athlete-card">
                <div class="mono-small">{html.escape(str(picked["NOC"]))}</div>
                <h3 class="athlete-name">{html.escape(str(picked["Name"]))}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Gold", int(picked["gold"]))
        c2.metric("Silver", int(picked["silver"]))
        c3.metric("Bronze", int(picked["bronze"]))
        c4.metric("Total", int(picked["total"]))

        st.markdown("#### Disciplines")

        sports_html = ""
        for sport in picked["sports"]:
            sports_html += f"""
            <span class="mini-tag">
                {sport_emoji(sport)} {html.escape(str(sport))}
            </span>
            """

        st.markdown(
            f"""
            <div class="tag-wrapper">
                {sports_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("#### Eras")

        eras_html = ""
        for e in picked["eras"]:
            eras_html += f"""
            <span class="mini-tag mono-tag">
                {era_label(e) if e != "Other" else "Other"}
            </span>
            """

        st.markdown(
            f"""
            <div class="tag-wrapper">
                {eras_html}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ATHLETE RACE
# ============================================================

def athlete_race(df_medals):
    athlete_stats = build_athlete_stats(df_medals)

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">The Great Race · Athletes</h2>
                <span class="stamp">Cumulative Medal Race</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    top_athletes = athlete_stats.head(40).copy()

    options = [
        f'{row["Name"]} · {row["NOC"]} · {int(row["total"])} medals'
        for _, row in top_athletes.iterrows()
    ]

    if len(options) < 2:
        st.info("Not enough athletes to compare.")
        return

    col1, col2 = st.columns(2)

    with col1:
        athlete_a_label = st.selectbox("Athlete A", options, index=0)

    with col2:
        athlete_b_label = st.selectbox("Athlete B", options, index=1)

    athlete_a_name = top_athletes.iloc[options.index(athlete_a_label)]["Name"]
    athlete_b_name = top_athletes.iloc[options.index(athlete_b_label)]["Name"]

    athlete_year_counts = (
        df_medals[df_medals["Name"].isin([athlete_a_name, athlete_b_name])]
        .groupby(["Year", "Name"])
        .size()
        .reset_index(name="Medals")
        .sort_values("Year")
    )

    years = sorted(df_medals["Year"].dropna().unique())
    rows = []

    for athlete in [athlete_a_name, athlete_b_name]:
        sub = athlete_year_counts[athlete_year_counts["Name"] == athlete]
        medal_by_year = dict(zip(sub["Year"], sub["Medals"]))

        cumulative = 0
        for year in years:
            cumulative += medal_by_year.get(year, 0)
            rows.append(
                {
                    "Year": year,
                    "Athlete": athlete,
                    "Cumulative medals": cumulative
                }
            )

    chart_df = pd.DataFrame(rows)

    st.line_chart(
        chart_df,
        x="Year",
        y="Cumulative medals",
        color="Athlete",
        use_container_width=True
    )


# ============================================================
# NATION DUEL
# ============================================================

def nation_duel(df_medals):
    medal_by_year_noc = (
        df_medals
        .groupby(["Year", "NOC"])
        .size()
        .reset_index(name="Medals")
    )

    top_nocs = (
        df_medals
        .groupby("NOC")
        .size()
        .sort_values(ascending=False)
        .head(30)
        .index
        .tolist()
    )

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">The Great Duel · Nations</h2>
                <span class="stamp">Cumulative Medal Race</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if len(top_nocs) < 2:
        st.info("Not enough nations to compare.")
        return

    col1, col2 = st.columns(2)

    with col1:
        nation_a = st.selectbox(
            "Nation A",
            top_nocs,
            index=top_nocs.index("USA") if "USA" in top_nocs else 0
        )

    with col2:
        nation_b = st.selectbox(
            "Nation B",
            top_nocs,
            index=top_nocs.index("URS") if "URS" in top_nocs else min(1, len(top_nocs) - 1)
        )

    years = sorted(df_medals["Year"].dropna().unique())
    rows = []

    for nation in [nation_a, nation_b]:
        sub = medal_by_year_noc[medal_by_year_noc["NOC"] == nation]
        medal_by_year = dict(zip(sub["Year"], sub["Medals"]))

        cumulative = 0
        for year in years:
            cumulative += medal_by_year.get(year, 0)
            rows.append(
                {
                    "Year": year,
                    "Nation": nation,
                    "Cumulative medals": cumulative
                }
            )

    chart_df = pd.DataFrame(rows)

    st.line_chart(
        chart_df,
        x="Year",
        y="Cumulative medals",
        color="Nation",
        use_container_width=True
    )


# ============================================================
# TRIVIA
# ============================================================

def curiosity_cards():
    curiosities = [
        {
            "q": "Which country appears most often at the top of the Summer medal table?",
            "a": "USA",
            "detail": "Across the modern Summer Games, the United States is one of the dominant nations in total medals."
        },
        {
            "q": "Why can one sport have many more medals than another?",
            "a": "Events",
            "detail": "A sport with many events, categories or distances offers more medal opportunities than a sport with only a few events."
        },
        {
            "q": "Why are athlete entries higher than unique athletes?",
            "a": "Repeated participation",
            "detail": "The same athlete can appear in multiple events and in multiple Olympic editions."
        },
        {
            "q": "Why do some countries have historical codes such as URS?",
            "a": "Historical NOCs",
            "detail": "Some NOC codes refer to historical national teams that no longer compete under the same code."
        },
        {
            "q": "Why does filtering by era change the rings?",
            "a": "Era-specific sports",
            "detail": "Only sports appearing in the selected historical period are placed on the rings."
        },
    ]

    if "revealed_trivia" not in st.session_state:
        st.session_state.revealed_trivia = {}

    st.markdown('<div class="section-kicker">Did You Know?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Olympic Trivia from the Archive</div>', unsafe_allow_html=True)

    cols = st.columns(3)

    for i, c in enumerate(curiosities):
        with cols[i % 3]:
            open_card = st.session_state.revealed_trivia.get(i, False)

            st.markdown(
                f"""
                <div class="trivia-card">
                    <div class="trivia-head">
                        <span class="stamp">Trivia №{i + 1}</span>
                        <span class="trivia-question-mark">?</span>
                    </div>
                    <p class="trivia-question">{html.escape(c["q"])}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Hide answer" if open_card else "Tap to reveal →",
                key=f"trivia_{i}",
                use_container_width=True
            ):
                st.session_state.revealed_trivia[i] = not open_card
                st.rerun()

            if open_card:
                st.markdown(
                    f"""
                    <div class="trivia-answer">
                        <div class="trivia-answer-main">{html.escape(c["a"])}</div>
                        <p class="trivia-detail">{html.escape(c["detail"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# HOST CITY CARTOGRAPHY
# ============================================================

def show_host_city_cartography(df):
    st.markdown(
        '<div class="cartography-title">Cartography of Host Cities</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="cartography-subtitle">◆ Summer Olympic Games Host Cities ◆</div>',
        unsafe_allow_html=True
    )

    back_col1, back_col2, back_col3 = st.columns([1, 1.2, 1])

    with back_col2:
        if st.button("← Back to Olympic Archive"):
            st.session_state.page = "main"
            st.rerun()

    city_coordinates = {
        "Athina": (37.9838, 23.7275),
        "Athens": (37.9838, 23.7275),
        "Paris": (48.8566, 2.3522),
        "St. Louis": (38.6270, -90.1994),
        "London": (51.5074, -0.1278),
        "Stockholm": (59.3293, 18.0686),
        "Antwerpen": (51.2194, 4.4025),
        "Antwerp": (51.2194, 4.4025),
        "Amsterdam": (52.3676, 4.9041),
        "Los Angeles": (34.0522, -118.2437),
        "Berlin": (52.5200, 13.4050),
        "Helsinki": (60.1699, 24.9384),
        "Melbourne": (-37.8136, 144.9631),
        "Roma": (41.9028, 12.4964),
        "Rome": (41.9028, 12.4964),
        "Tokyo": (35.6762, 139.6503),
        "Mexico City": (19.4326, -99.1332),
        "Munich": (48.1351, 11.5820),
        "Montreal": (45.5017, -73.5673),
        "Moskva": (55.7558, 37.6173),
        "Moscow": (55.7558, 37.6173),
        "Seoul": (37.5665, 126.9780),
        "Barcelona": (41.3874, 2.1686),
        "Atlanta": (33.7490, -84.3880),
        "Sydney": (-33.8688, 151.2093),
        "Beijing": (39.9042, 116.4074),
        "Rio de Janeiro": (-22.9068, -43.1729),
    }

    host_df = (
        df[["Year", "City"]]
        .drop_duplicates()
        .sort_values("Year")
        .reset_index(drop=True)
    )

    host_df["Latitude"] = host_df["City"].map(lambda city: city_coordinates.get(city, (None, None))[0])
    host_df["Longitude"] = host_df["City"].map(lambda city: city_coordinates.get(city, (None, None))[1])
    host_map_df = host_df.dropna(subset=["Latitude", "Longitude"])

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Map of Summer Olympic Host Cities</div>', unsafe_allow_html=True)

    fig_map = px.scatter_geo(
        host_map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        text="Year",
        projection="natural earth",
    )

    fig_map.update_traces(
        marker=dict(
            size=13,
            color="#b88a2e",
            line=dict(width=1.5, color="#171717")
        ),
        textposition="top center",
        textfont=dict(size=11, color="#171717")
    )

    fig_map.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#555555",
            showland=True,
            landcolor="#d5cbb9",
            showocean=True,
            oceancolor="#f4efe3",
            showcountries=True,
            countrycolor="#555555",
            bgcolor="#f4efe3",
        ),
        font=dict(
            family="Roboto Mono",
            color="#171717"
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Growth of the Olympiad</div>', unsafe_allow_html=True)

    growth_df = (
        df.groupby("Year")
        .agg(
            Athlete_entries=("ID", "count"),
            Sports=("Sport", "nunique"),
            Events=("Event", "nunique")
        )
        .reset_index()
        .sort_values("Year")
    )

    fig_growth = go.Figure()

    fig_growth.add_trace(
        go.Scatter(
            x=growth_df["Year"],
            y=growth_df["Athlete_entries"],
            mode="lines+markers",
            name="Athlete entries",
            line=dict(width=3, color="#b88a2e"),
            marker=dict(size=7, color="#f4efe3", line=dict(width=2, color="#b88a2e"))
        )
    )

    fig_growth.add_trace(
        go.Scatter(
            x=growth_df["Year"],
            y=growth_df["Events"],
            mode="lines+markers",
            name="Events",
            line=dict(width=3, color="#171717"),
            marker=dict(size=7, color="#f4efe3", line=dict(width=2, color="#171717")),
            yaxis="y2"
        )
    )

    fig_growth.update_layout(
        height=430,
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        margin=dict(l=40, r=40, t=20, b=40),
        font=dict(family="Roboto Mono", color="#171717"),
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="rgba(17,24,39,0.18)",
            tickmode="array",
            tickvals=growth_df["Year"],
            tickangle=45
        ),
        yaxis=dict(
            title="Athlete entries",
            showgrid=True,
            gridcolor="rgba(17,24,39,0.18)"
        ),
        yaxis2=dict(
            title="Events",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor="center"
        )
    )

    st.plotly_chart(fig_growth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Register of Host Cities</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    host_columns = [col1, col2, col3]

    for index, row in host_df[["Year", "City"]].iterrows():
        selected_col = host_columns[index % 3]

        with selected_col:
            st.markdown(
                f"""
                <div class="host-row">
                    <span class="host-year">{int(row["Year"])} ✣</span>
                    <span class="host-city">{html.escape(str(row["City"]))}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================

def main():
    if "active_block" not in st.session_state:
        st.session_state.active_block = None

    if "era" not in st.session_state:
        st.session_state.era = "ALL"

    if "page" not in st.session_state:
        st.session_state.page = "main"

    default_path = Path("olympic_clean_summer.xlsx")

    with st.sidebar:
        st.markdown("### Data source")

        uploaded_file = st.file_uploader(
            "Upload Olympic Excel file",
            type=["xlsx"]
        )

        st.markdown(
            """
            Required columns:

            `ID, Name, Sex, Age, Height, Weight, Team, NOC, Games, Year, Season, City, Sport, Event, Medal`
            """
        )

    if uploaded_file is not None:
        df, df_medals = load_excel_from_upload(uploaded_file)
    elif default_path.exists():
        df, df_medals = load_excel_from_path(default_path)
    else:
        st.warning("Upload your Excel file from the sidebar to start.")
        st.stop()

    masthead()

    if st.session_state.page == "hosts":
        show_host_city_cartography(df)
        footer()
        return

    if st.session_state.page == "year_explorer":
        year_archive_explorer(df, df_medals)
        footer()
        return

    intro()
    era_controls()

    era = st.session_state.era
    df_era, df_medals_era = filter_era_data(df, df_medals, era)

    editions = df_era["Games"].nunique()
    athlete_entries = len(df_era)
    medals_awarded = len(df_medals_era)

    stats_strip(editions, athlete_entries, medals_awarded)

    if era == "ALL":
        c1, c2, c3 = st.columns([1, 2.2, 1])

        with c2:
            if st.button(
                "✦ Explore a Single Olympic Year ✦",
                key="open_year_explorer",
                use_container_width=True
            ):
                st.session_state.page = "year_explorer"
                st.rerun()

        st.markdown('<div class="section-kicker">Detailed Zone</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Choose Your Dispatch</div>', unsafe_allow_html=True)

        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        with row1_col1:
            dispatch_card(
                "explorer",
                "Search",
                "Detailed Zone · Athlete Explorer",
                "Cerca tra i campioni indicizzati e leggi il loro palmarès completo.",
                "◎"
            )

        with row1_col2:
            dispatch_card(
                "race",
                "Compare",
                "The Great Race · Athletes",
                "Phelps vs Spitz e oltre: confronta due atleti lungo una timeline cumulativa.",
                "▶"
            )

        with row2_col1:
            dispatch_card(
                "duel",
                "Duel",
                "The Great Duel · Nations",
                "Due nazioni, una timeline. Confronta i medaglieri cumulativi.",
                "⚔"
            )

        with row2_col2:
            dispatch_card(
                "trivia",
                "Trivia",
                "Olympic Trivia from the Archive",
                "Curiosità a tema: prova a indovinare e poi rivela la risposta.",
                "?"
            )

        active = st.session_state.active_block

        if active == "explorer":
            athlete_explorer(df_medals)

        elif active == "race":
            athlete_race(df_medals)

        elif active == "duel":
            nation_duel(df_medals)

        elif active == "trivia":
            curiosity_cards()

    else:
        sports = sorted(df_era["Sport"].dropna().unique())

        st.markdown(
            f"""
            <section class="ring-panel">
                <div class="panel-header">
                    <span class="stamp">Summer · {era_label(era)}</span>
                    <span class="mono-small">
                        {len(sports)} disciplines
                    </span>
                </div>
            </section>
            """,
            unsafe_allow_html=True
        )

        olympic_rings(df_era, era)

        c1, c2, c3 = st.columns([1, 2.2, 1])

        with c2:
            if st.button(
                "✦ View the Cartography of Host Cities ✦",
                key="open_hosts",
                use_container_width=True
            ):
                st.session_state.page = "hosts"
                st.rerun()

        show_data = st.checkbox("Show filtered dataset")

        if show_data:
            columns_to_show = [
                "ID", "Name", "Sex", "Age", "Height", "Weight", "Team", "NOC",
                "Games", "Year", "Season", "City", "Sport", "Event", "Medal"
            ]

            existing_columns = [col for col in columns_to_show if col in df_era.columns]

            st.dataframe(
                df_era[existing_columns],
                use_container_width=True
            )

    footer()


if __name__ == "__main__":
    main()
