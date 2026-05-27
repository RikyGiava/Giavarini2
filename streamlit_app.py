import math
import html
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import base64
from PIL import Image, ImageOps

import pandas as pd
import streamlit as st
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="The Olympic Archive",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
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


    /* ============================================================
   FORCE SIDEBAR ARROW BLACK
============================================================ */

    /* Arrow when sidebar is collapsed */
    [data-testid="collapsedControl"],
    [data-testid="collapsedControl"] *,
    [data-testid="collapsedControl"] svg,
    [data-testid="collapsedControl"] svg path {
        color: #171717 !important;
        fill: #171717 !important;
        stroke: #171717 !important;
    }

    /* Arrow/button in the Streamlit header */
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] button *,
    [data-testid="stHeader"] button svg,
    [data-testid="stHeader"] button svg path {
        color: #171717 !important;
        fill: #171717 !important;
        stroke: #171717 !important;
    }

    /* Arrow when sidebar is expanded */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button *,
    [data-testid="stSidebar"] button svg,
    [data-testid="stSidebar"] button svg path {
        color: #171717 !important;
        fill: #171717 !important;
        stroke: #171717 !important;
    }

    /* Newer Streamlit sidebar buttons */
    button[kind="header"],
    button[kind="header"] *,
    button[kind="header"] svg,
    button[kind="header"] svg path {
        color: #171717 !important;
        fill: #171717 !important;
        stroke: #171717 !important;
    }



    footer {
        visibility: hidden;
    }

    [data-testid="stSlider"] *,
    [data-testid="stMetric"] *,
    [data-testid="stSelectbox"] *,
    [data-testid="stSelectSlider"] *,
    [data-testid="stRadio"] *,
    [data-testid="stCheckbox"] *,
    [data-testid="stMultiSelect"] *,
    label,
    p,
    span,
    div {
        color: #171717;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background-color: #f4efe3 !important;
        color: #171717 !important;
        border: 2px solid #171717 !important;
        border-radius: 0px !important;
    }

    [data-testid="stSelectbox"] input,
    [data-testid="stMultiSelect"] input {
        color: #171717 !important;
    }

    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg {
        fill: #171717 !important;
        color: #171717 !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] [role="listbox"] {
        background-color: #171717 !important;
        color: #f4efe3 !important;
    }

    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="option"] *,
    [data-baseweb="popover"] li *,
    [data-baseweb="popover"] div {
        background-color: #171717 !important;
        color: #f4efe3 !important;
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] [role="option"]:hover * {
        background-color: #b88a2e !important;
        color: #171717 !important;
    }

    [data-baseweb="tag"] {
        background-color: #171717 !important;
        border: 1.5px solid #171717 !important;
        border-radius: 0px !important;
    }

    [data-baseweb="tag"] *,
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] svg {
        color: #f4efe3 !important;
        fill: #f4efe3 !important;
    }

    .js-plotly-plot,
    .js-plotly-plot text,
    .js-plotly-plot .gtitle,
    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .xaxis-title,
    .js-plotly-plot .yaxis-title,
    .js-plotly-plot .legend text {
        fill: #171717 !important;
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
        margin: 22px auto;
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
        font-size: 24px;
        padding: 0.65rem 1rem;
        transition: all 0.18s ease;
        box-shadow: none;
        white-space: pre-line;
    }

    button[kind="primary"], 
    button[data-testid="baseButton-primary"] {
        font-size: 26px !important;
        padding: 1rem 1rem !important;
        background-color: var(--paper) !important;
        color: var(--ink) !important;
        border: 2px solid var(--ink) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        font-family: 'Playfair Display', serif !important;
        transition: all 0.18s ease !important;
    }

    button[kind="primary"] p, 
    button[data-testid="baseButton-primary"] p {
        font-size: 26px !important;
        margin: 0 !important;
    }

    button[kind="primary"]:hover, 
    button[data-testid="baseButton-primary"]:hover,
    div.stButton > button:hover {
        background-color: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
        box-shadow: 5px 5px 0px var(--brass) !important;
        transform: translateY(-1px) !important;
    }

    button[kind="primary"]:hover *, 
    button[data-testid="baseButton-primary"]:hover *,
    div.stButton > button:hover * {
        color: var(--paper) !important;
    }

    .active-era {
        width: 100%;
        border: 2px solid #171717;
        background: #171717;
        color: #f4efe3 !important;
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
        color: var(--paper) !important;
        border: 2px solid var(--ink);
        padding: 26px;
        min-height: 230px;
        margin-bottom: 8px;
    }

    .dispatch-card-active * {
        color: var(--paper) !important;
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
        color: var(--brass) !important;
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
        color: rgba(244,239,227,0.80) !important;
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
        color: var(--paper) !important;
    }

    .paper-panel {
        background-color: var(--paper);
        border: 2px solid var(--ink);
        padding: 26px;
        margin-top: 30px;
        margin-bottom: 18px;
    }

    .filter-panel {
        background:
            linear-gradient(135deg, rgba(184,138,46,0.16), rgba(244,239,227,0.92)),
            #f4efe3;
        border: 2px solid var(--ink);
        padding: 30px;
        margin-top: 30px;
        margin-bottom: 20px;
        box-shadow: 7px 7px 0px #171717;
    }

    .filter-eyebrow {
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: var(--brass);
        margin-bottom: 10px;
    }

    .filter-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(32px, 4vw, 44px);
        color: var(--ink);
        margin: 0;
        line-height: 1.05;
    }

    .filter-copy {
        max-width: 780px;
        margin-top: 12px;
        margin-bottom: 0;
        font-style: italic;
        color: rgba(23,23,23,0.74);
        font-size: 16px;
        line-height: 1.55;
    }

    .filter-mini-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 18px;
    }

    .filter-mini-tag {
        border: 1.5px solid #171717;
        padding: 6px 10px;
        font-family: 'Roboto Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        background-color: rgba(244,239,227,0.7);
        color: #171717;
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

    /* ============================================================
       PODIUM + MEDAL WALL
    ============================================================ */

    .emotional-section {
        margin-top: 34px;
        margin-bottom: 34px;
    }

    .podium-wrapper {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 18px;
        margin-top: 26px;
        margin-bottom: 32px;
    }

    .podium-place {
        border: 2px solid #171717;
        background: #f4efe3;
        text-align: center;
        min-width: 190px;
        box-shadow: 5px 5px 0px #171717;
        color: #171717;
        

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;

        box-sizing: border-box;
        padding: 14px 12px 18px 12px;
        overflow: hidden;
        }

    .podium-place.first {
        height: 245px;
        background: linear-gradient(180deg, rgba(184,138,46,0.26), #f4efe3);
    }

    .podium-place.second {
        height: 205px;
        background: linear-gradient(180deg, rgba(192,192,192,0.28), #f4efe3);
    }

    .podium-place.third {
        height: 175px;
        background: linear-gradient(180deg, rgba(184, 92, 36, 0.58), #f4efe3);
    }

    .podium-medal {
        font-size: 42px;
        margin-top: 18px;
    }

    .podium-rank {
        font-family: 'Playfair Display', serif;
        font-size: 44px;
        line-height: 1;
        color: #171717;
    }

    .podium-noc {
        font-family: 'Playfair Display', serif;
        font-size: 30px;
        margin-top: 10px;
        color: #171717;
    }

    .podium-count {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.22em;
        margin-top: 8px;
        color: #68645c;
    }

    .medal-wall {
        border: 2px solid #171717;
        background: rgba(255,255,255,0.16);
        padding: 24px;
        margin-top: 22px;
        margin-bottom: 26px;
        box-shadow: 6px 6px 0px #171717;
    }

    .medal-wall-title {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        text-align: center;
        margin-bottom: 8px;
        color: #171717;
    }

    .medal-wall-subtitle {
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.28em;
        color: #b88a2e;
        margin-bottom: 20px;
    }

    .medal-detail-card {
        border: 2px solid #171717;
        background: #f4efe3;
        padding: 20px;
        margin-top: 18px;
        margin-bottom: 22px;
        min-height: 150px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .medal-detail-title {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        margin-bottom: 8px;
        color: #171717;
    }

    .medal-detail-text {
        font-family: 'Roboto Mono', monospace;
        font-size: 12px;
        line-height: 1.7;
        color: rgba(23,23,23,0.75);
    }

    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: 1fr;
        }

        .stat-box:not(:first-child) {
            border-left: none;
            border-top: 2px solid var(--ink);
        }

        .podium-wrapper {
            flex-direction: column;
            align-items: center;
        }

        .podium-place.first,
        .podium-place.second,
        .podium-place.third {
            height: auto;
            min-height: 160px;
            width: 90%;
            padding-bottom: 20px;
        }
    }
    [data-testid="stSelectSlider"] label p,
    [data-testid="stSlider"] label p {
        font-size: 28px !important; /* Grandezza ridotta rispetto a prima */
        font-family: 'Playfair Display', serif !important;
        font-weight: normal !important; /* Rimuove il grassetto */
        color: var(--ink) !important;
        padding-bottom: 15px !important; 
    }

    /* Colora di nero il pallino (thumb) e il tooltip del valore */
    div[data-testid="stSelectSlider"] div[role="slider"] {
        background-color: #171717 !important;
        border: 2px solid #171717 !important;
    }
    div[data-testid="stSelectSlider"] div[data-testid="stThumbValue"] {
        background-color: #171717 !important;
        color: #f4efe3 !important;
        font-family: 'Roboto Mono', monospace !important;
    }
    
    /* ============================================================
        ATHLETE EXPLORER SEARCH BAR
    ============================================================ */

    /* ============================================================
    ATHLETE EXPLORER SEARCH BAR
============================================================ */

[data-testid="stTextInput"] {
    margin-top: 12px !important;
    margin-bottom: 18px !important;
}

[data-testid="stTextInput"] > div {
    background: transparent !important;
}

[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #171717 !important;
    border: 2px solid #171717 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] input {
    background-color: #171717 !important;
    color: #f4efe3 !important;
    caret-color: #f4efe3 !important;
    height: 48px !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 15px !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(244,239,227,0.65) !important;
}

/* Scritta a destra tipo "Press Enter to apply" */
[data-testid="stTextInput"] div[data-baseweb="input"] * {
    color: #f4efe3 !important;
}

    /* ============================================================
   BLACK SIDEBAR MENU
============================================================ */

    [data-testid="stSidebar"] {
        background-color: #171717 !important;
    }

    [data-testid="stSidebar"] > div {
        background-color: #171717 !important;
    }

    [data-testid="stSidebar"] * {
        color: #f4efe3 !important;
    }

    /* Titolo Menu */
    [data-testid="stSidebar"] h2 {
        color: #b88a2e !important;
    }

    /* Bottoni del menu laterale */
    [data-testid="stSidebar"] div.stButton {
        margin-bottom: 18px !important;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background-color: #171717 !important;
        color: #f4efe3 !important;
        border: 1.5px solid #f4efe3 !important;
        border-radius: 0px !important;
        font-family: 'Roboto Mono', monospace !important;
        font-size: 13px !important;
        padding: 18px 10px !important;
        min-height: 54px !important;
        box-shadow: none !important;
    }

    /* Testo dentro i bottoni */
    [data-testid="stSidebar"] div.stButton > button * {
        color: #f4efe3 !important;
    }

    /* Hover bottoni */
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #f4efe3 !important;
        color: #171717 !important;
        border-color: #b88a2e !important;
        box-shadow: 4px 4px 0px #b88a2e !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover * {
        color: #171717 !important;
    }

    /* Linea divisoria */
    [data-testid="stSidebar"] hr {
        border-color: rgba(244,239,227,0.35) !important;
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
        st.error(f"These columns are missing in the Excel file: {missing}")
        st.write("Columns present in the file:")
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


def safe_js(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
        .replace("\n", " ")
        .replace('"', '&quot;')
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

def noc_flag_html(noc, height=34):
    noc = str(noc).upper().strip()

    noc_to_country = {
        "USA": "us",
        "FRA": "fr",
        "GBR": "gb",
        "ITA": "it",
        "SWE": "se",
        "GER": "de",
        "FRG": "de",
        "GDR": "de",
        "GRE": "gr",
        "ESP": "es",
        "NED": "nl",
        "BEL": "be",
        "SUI": "ch",
        "CAN": "ca",
        "AUS": "au",
        "JPN": "jp",
        "CHN": "cn",
        "KOR": "kr",
        "BRA": "br",
        "RUS": "ru",
        "URS": "su",
        "HUN": "hu",
        "POL": "pl",
        "ROU": "ro",
        "DEN": "dk",
        "FIN": "fi",
        "NOR": "no",
        "AUT": "at",
        "MEX": "mx",
        "CUB": "cu",
        "JAM": "jm",
        "KEN": "ke",
        "ETH": "et",
        "RSA": "za",
    }

    if noc == "URS":
        flag_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/120px-Flag_of_the_Soviet_Union.svg.png"
        return f'<img src="{flag_url}" height="{height}" style="vertical-align:middle; border-radius:3px; margin-right:12px;">'

    country_code = noc_to_country.get(noc)

    if country_code:
        return f'<img src="https://flagcdn.com/h80/{country_code}.png" height="{height}" style="vertical-align:middle; border-radius:3px; margin-right:12px;">'

    return '<span style="margin-right:12px;">🏳️</span>'
@st.cache_data(show_spinner=False)
def noc_flag_url(noc):
    noc = str(noc).upper().strip()

    noc_to_country = {
        "USA": "us",
        "FRA": "fr",
        "GBR": "gb",
        "ITA": "it",
        "SWE": "se",
        "GER": "de",
        "FRG": "de",
        "GDR": "de",
        "GRE": "gr",
        "ESP": "es",
        "NED": "nl",
        "BEL": "be",
        "SUI": "ch",
        "CAN": "ca",
        "AUS": "au",
        "JPN": "jp",
        "CHN": "cn",
        "KOR": "kr",
        "BRA": "br",
        "RUS": "ru",
        "HUN": "hu",
        "POL": "pl",
        "ROU": "ro",
        "DEN": "dk",
        "FIN": "fi",
        "NOR": "no",
        "AUT": "at",
        "MEX": "mx",
        "CUB": "cu",
        "JAM": "jm",
        "KEN": "ke",
        "ETH": "et",
        "RSA": "za",
    }

    if noc == "URS":
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/120px-Flag_of_the_Soviet_Union.svg.png"

    country_code = noc_to_country.get(noc)

    if country_code:
        return f"https://flagcdn.com/h120/{country_code}.png"

    return None
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

    # --- CALCOLO DEL MIGLIOR ATLETA CON REGOLE TIE-BREAK ---
    if period_df[medals_mask].empty:
        best_athlete_table = pd.DataFrame(columns=["Sport", "best_athlete"])
    else:
        athlete_medals = (
            period_df[medals_mask]
            .groupby(['Sport', 'Name', 'Medal'])
            .size()
            .unstack(fill_value=0)
        )
        for m in ['Gold', 'Silver', 'Bronze']:
            if m not in athlete_medals.columns:
                athlete_medals[m] = 0
        athlete_medals = athlete_medals.reset_index()
        
        athlete_medals_sorted = athlete_medals.sort_values(
            by=['Sport', 'Gold', 'Silver', 'Bronze', 'Name'],
            ascending=[True, False, False, False, True]
        )
        best_athlete_table = (
            athlete_medals_sorted
            .drop_duplicates(subset=['Sport'])
            .rename(columns={"Name": "best_athlete"})
        )

    merged = (
        base_stats
        .merge(medal_stats, on="Sport", how="left")
        .merge(
            top_country_table[["Sport", "top_country"]],
            on="Sport",
            how="left"
        )
        .merge(
            best_athlete_table[["Sport", "best_athlete"]],
            on="Sport",
            how="left"
        )
    )
    merged["medals"] = merged["medals"].fillna(0).astype(int)
    merged["top_country"] = merged["top_country"].fillna("No medals")
    merged["best_athlete"] = merged["best_athlete"].fillna("Nessun atleta")
    merged = merged[merged["Sport"].isin(sports_to_show)]
    
    sport_stats = {}
    for _, row in merged.iterrows():
        sport = row["Sport"]
        noc_str = str(row["top_country"])
        
        # Se non ci sono medaglie mostriamo solo il testo, altrimenti aggiungiamo la bandiera
        if noc_str == "No medals":
            top_country_display = "No medals"
        else:
            # Impostiamo l'altezza della bandiera a 16px per farla stare bene nella riga del testo
            top_country_display = f"{noc_flag_html(noc_str, height=16)}{noc_str}"
            
        sport_stats[sport] = {
            "icon": sport_emoji(sport),
            "disciplines": int(row["disciplines"]),
            "athletes": int(row["athletes"]),
            "medals": int(row["medals"]),
            "top_country": top_country_display, # Salviamo il testo comprensivo di codice della bandiera
            "best_athlete": str(row["best_athlete"]),
        }

    return sports_to_show, sport_stats


def apply_plotly_theme(fig, height=460):
    fig.update_layout(
        height=height,
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        font=dict(
            family="Roboto Mono",
            color="#171717"
        ),
        title=dict(
            font=dict(
                family="Playfair Display",
                size=26,
                color="#171717"
            )
        ),
        xaxis=dict(
            title_font=dict(color="#171717"),
            tickfont=dict(color="#171717"),
            gridcolor="rgba(23,23,23,0.18)",
            linecolor="#171717",
            zerolinecolor="#171717"
        ),
        yaxis=dict(
            title_font=dict(color="#171717"),
            tickfont=dict(color="#171717"),
            gridcolor="rgba(23,23,23,0.18)",
            linecolor="#171717",
            zerolinecolor="#171717"
        ),
        legend=dict(
            font=dict(color="#171717")
        ),
        hoverlabel=dict(
            bgcolor="#f4efe3",
            bordercolor="#171717",
            font=dict(
                family="Roboto Mono",
                size=13,
                color="#171717"
            )
        ),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    fig.update_xaxes(
        title_font_color="#171717",
        tickfont_color="#171717"
    )

    fig.update_yaxes(
        title_font_color="#171717",
        tickfont_color="#171717"
    )

    return fig


# ============================================================
# MAIN COMPONENTS
# ============================================================

def masthead():
    st.html(
        """
        <style>
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
        """
    )


def intro():
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )


def era_controls():
    st.markdown('<div class="section-kicker">Select Era</div>', unsafe_allow_html=True)

    era_context = {
        "1896-1936": "Before World War II",
        "1937-1976": "Post-war expansion",
        "1977-2016": "Modern global Games",
        "ALL": "Full archive"
    }

    cols = st.columns(len(ERAS))

    for col, era in zip(cols, ERAS):
        with col:
            st.html(
                f"""
                <div style="
                    text-align: center;
                    min-height: 28px;
                    margin-bottom: 2px;
                ">
                    <div style="
                        font-family: 'Playfair Display', serif;
                        font-size: 23px;
                        color: #171717;
                        line-height: 1;
                    ">
                        {era_context[era]}
                    </div>
                </div>
                """
            )

            if st.session_state.era == era:
                st.markdown(
                    f'<div class="active-era">{era_label(era)}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(era_label(era), key=f"era_{era}", width="stretch"):
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

    if st.button("Open", key=f"open_{block_id}", width="stretch"):
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
# PODIUM + MEDAL WALL
# ============================================================

def olympic_podium_and_medal_wall(filtered_medals_df, selected_year):
    st.markdown(
        """
        <div class="emotional-section">
            <div class="paper-panel">
                <div class="panel-title-row">
                    <h2 class="panel-title">Olympic Podium & Medal Wall</h2>
                    <span class="stamp">Emotional Layer</span>
                </div>
                <p class="italic-desc">
                    Medal data becomes a physical Olympic object: a podium and a wall of memories.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if filtered_medals_df.empty:
        st.info("No medal data available for the selected filters.")
        return

    unique_medals = (
        filtered_medals_df
        .drop_duplicates(subset=["Year", "Sport", "Event", "Medal", "NOC"])
        .copy()
    )

    if unique_medals.empty:
        st.info("No unique medal data available for the selected filters.")
        return

    medal_ranking = (
        unique_medals
        .groupby("NOC")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Medals")
    )

    top3 = medal_ranking.head(3).copy()

    while len(top3) < 3:
        top3.loc[len(top3)] = ["—", 0]

    first = top3.iloc[0]
    second = top3.iloc[1]
    third = top3.iloc[2]

    st.html(
        f"""
        <style>
        body {{
            margin: 0;
            background: transparent;
        }}

        .podium-wrapper {{
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 18px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}

        .podium-place {{
            border: 2px solid #171717;
            text-align: center;
            min-width: 190px;
            box-shadow: 5px 5px 0px #171717;
            color: #171717;
            box-sizing: border-box;

            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;

            padding: 14px 10px 14px 10px;
            overflow: hidden;
        }}

        .podium-place.first {{
            height: 270px;
            background: linear-gradient(180deg, rgba(184,138,46,0.30), #f4efe3);
        }}

        .podium-place.second {{
            height: 235px;
            background: linear-gradient(180deg, rgba(192,192,192,0.34), #f4efe3);
        }}

        .podium-place.third {{
            height: 215px;
            background: linear-gradient(180deg, rgba(166, 78, 28, 0.72), #f4efe3);
        }}

        .podium-medal {{
            font-size: 40px;
            line-height: 1;
            margin-top: 2px;
        }}

        .podium-rank {{
            font-family: Georgia, serif;
            font-size: 42px;
            line-height: 1;
            color: #171717;
            margin: 0;
        }}

        .podium-noc {{
            font-family: Georgia, serif;
            font-size: 28px;
            line-height: 1.05;
            color: #171717;
            margin: 0;
        }}

        .podium-count {{
            font-family: monospace;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: #68645c;
            line-height: 1.1;
            margin: 0;
            padding-bottom: 2px;
        }}

        .podium-place.third .podium-medal,
        .podium-place.third .podium-rank,
        .podium-place.third .podium-noc {{
            color: #8f4a1f;
        }}
        </style>

        <div class="podium-wrapper">

                <div class="podium-place second">
                <div class="podium-medal">🥈</div>
                <div class="podium-rank">2</div>
                <div class="podium-noc">{html.escape(str(second["NOC"]))}</div>
                <div class="podium-count">{int(second["Medals"])} medals</div>
            </div>

                <div class="podium-place first">
                <div class="podium-medal">🥇</div>
                <div class="podium-rank">1</div>
                <div class="podium-noc">{html.escape(str(first["NOC"]))}</div>
                <div class="podium-count">{int(first["Medals"])} medals</div>
            </div>

            <div class="podium-place third">
                <div class="podium-medal">🥉</div>
                <div class="podium-rank">3</div>
                <div class="podium-noc">{html.escape(str(third["NOC"]))}</div>
                <div class="podium-count">{int(third["Medals"])} medals</div>
            </div>

        </div>
        """
    )

    st.markdown(
        """
        <div class="medal-wall">
            <div class="medal-wall-title">Medal Wall</div>
            <div class="medal-wall-subtitle">Click a medal to open the country memory</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    medal_wall_df = medal_ranking.head(18).copy()
    wall_cols = st.columns(6)

    for i, row in medal_wall_df.iterrows():
        noc = row["NOC"]
        medals = int(row["Medals"])

        with wall_cols[i % 6]:
            if st.button(
                f"🏅 {noc}\n{medals} medals",
                key=f"medal_wall_{selected_year}_{noc}_{i}",
                width="stretch"
            ):
                st.session_state.selected_medal_wall_noc = noc
                st.rerun()

    selected_noc = st.session_state.get("selected_medal_wall_noc", None)

    valid_nocs = medal_ranking["NOC"].tolist()

    if selected_noc is not None and selected_noc in valid_nocs:
        country_medals = unique_medals[unique_medals["NOC"] == selected_noc].copy()

        gold = int((country_medals["Medal"] == "Gold").sum())
        silver = int((country_medals["Medal"] == "Silver").sum())
        bronze = int((country_medals["Medal"] == "Bronze").sum())
        total = len(country_medals)

        top_sports = (
            country_medals
            .groupby("Sport")
            .size()
            .sort_values(ascending=False)
            .head(5)
            .reset_index(name="Medals")
        )

        top_sports_text = ", ".join(
            [
                f"{row['Sport']} ({int(row['Medals'])})"
                for _, row in top_sports.iterrows()
            ]
        )

        st.markdown(
            f"""
            <div class="medal-detail-card">
                <div class="medal-detail-title">🏅 {html.escape(str(selected_noc))} Olympic Memory</div>
                <div class="medal-detail-text">
                    <b>Total medals:</b> {total}<br>
                    <b>Gold:</b> {gold} · <b>Silver:</b> {silver} · <b>Bronze:</b> {bronze}<br>
                    <b>Strongest sports in this view:</b> {html.escape(top_sports_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def fixed_opening_image(image_path, size=(900, 430)):
    img = Image.open(image_path).convert("RGB")
    img = ImageOps.fit(
        img,
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )
    return img

# ============================================================
# OPENING CEREMONY COMPARISON
# ============================================================

def opening_ceremony_comparison():
    image_1896 = Path("images/opening_1896.jpg")
    image_2016 = Path("images/opening_2016.jpg")

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">How was the Opening Ceremony?</h2>
                <span class="stamp">1896 vs 2016</span>
            </div>
            <p class="italic-desc">
                A visual comparison between the first modern Olympic Opening Ceremony and a contemporary global show.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="section-box">
                <div class="medal-wall-title">Athens · 1896</div>
                <div class="medal-wall-subtitle">The first  Olympic opening ceremony</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if image_1896.exists():
            st.image(
                fixed_opening_image(image_1896),
                width="stretch"
            )
        else:
            st.warning("Missing image: images/opening_1896.jpg")

        st.markdown(
            """
            <div class="medal-detail-card">
                <div class="medal-detail-title">A solemn beginning</div>
                <div class="medal-detail-text">
                    The 1896 Opening Ceremony was formal, simple and symbolic.
                    It represented the rebirth of the Olympic Games and took place in Athens,
                    strongly connected to the ancient Greek tradition.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="section-box">
                <div class="medal-wall-title">Rio de Janeiro · 2016</div>
                <div class="medal-wall-subtitle">A global cultural spectacle</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if image_2016.exists():
            st.image(
                fixed_opening_image(image_2016),
                width="stretch"
            )
        else:
            st.warning("Missing image: images/opening_2016.jpg")

        st.markdown(
            """
            <div class="medal-detail-card">
                <div class="medal-detail-title">A modern Olympic show</div>
                <div class="medal-detail-text">
                    The 2016 Opening Ceremony was a large-scale performance with music,
                    choreography, lights and cultural references to Brazil, nature,
                    diversity and Olympic unity.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# OLYMPIC EVOLUTION CHART
# ============================================================

def olympic_evolution_chart(df):
    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">Olympic Data Stories</h2>
                <span class="stamp">Combined Insights</span>
            </div>
            <p class="italic-desc">
                These charts combine multiple dimensions of the Olympic dataset to reveal hidden patterns in Olympic history.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    chart_type = st.radio(
        "Choose a complex data story",
        [
            "Olympic Complexity Map",
            "Gender Balance by Sport Across Eras"
        ],
        horizontal=True
    )

    # ============================================================
    # 1. OLYMPIC COMPLEXITY MAP
    # ============================================================

    if chart_type == "Olympic Complexity Map":
        chart_df = (
            df.groupby(["Year", "City"])
            .agg(
                Athletes=("ID", "nunique"),
                Athlete_entries=("ID", "count"),
                Nations=("NOC", "nunique"),
                Sports=("Sport", "nunique"),
                Events=("Event", "nunique")
            )
            .reset_index()
            .sort_values("Year")
        )

        fig = px.scatter(
            chart_df,
            x="Year",
            y="Athletes",
            size="Nations",
            color="Events",
            hover_name="City",
            hover_data={
                "Year": True,
                "Athletes": True,
                "Athlete_entries": True,
                "Nations": True,
                "Sports": True,
                "Events": True
            },
            title="How did the Olympic Games become larger and more complex?"
        )

        fig.update_traces(
            marker=dict(
                opacity=0.82,
                line=dict(
                    color="#171717",
                    width=1.4
                )
            )
        )

        fig = apply_plotly_theme(fig, height=580)

        fig.update_layout(
            xaxis_title="Olympic Year",
            yaxis_title="Number of athletes",
            coloraxis_colorbar=dict(
                title="Events"
            )
        )

        st.plotly_chart(fig, width="stretch")

        st.markdown(
            """
            <div style="text-align: right; font-size: 14px; color: var(--muted); margin-top: -20px; padding-right: 15px; margin-bottom: 25px;">
                ◍ <i>The size of the bubble indicates the number of participating <b>Nations</b></i>
            </div>
            """,
            unsafe_allow_html=True
        )
    # ============================================================
    # 2. GENDER BALANCE BY SPORT ACROSS ERAS
    # ============================================================

    elif chart_type == "Gender Balance by Sport Across Eras":
        gender_df = df.copy()

        def assign_era(year):
            if year <= 1936:
                return "1896–1936"
            elif year <= 1976:
                return "1937–1976"
            else:
                return "1977–2016"

        gender_df["Era"] = gender_df["Year"].apply(assign_era)

        # Keep the most represented sports to avoid overcrowding
        top_sports = (
            gender_df.groupby("Sport")["ID"]
            .nunique()
            .sort_values(ascending=False)
            .head(16)
            .index
            .tolist()
        )

        gender_df = gender_df[gender_df["Sport"].isin(top_sports)].copy()

        total_df = (
            gender_df
            .groupby(["Era", "Sport"])
            .agg(
                Total_athletes=("ID", "nunique"),
                Events=("Event", "nunique"),
                Nations=("NOC", "nunique")
            )
            .reset_index()
        )

        women_df = (
            gender_df[gender_df["Sex"].astype(str).str.upper().isin(["F", "FEMALE"])]
            .groupby(["Era", "Sport"])["ID"]
            .nunique()
            .reset_index(name="Women_athletes")
        )

        chart_df = total_df.merge(
            women_df,
            on=["Era", "Sport"],
            how="left"
        )

        chart_df["Women_athletes"] = chart_df["Women_athletes"].fillna(0)

        era_order = ["1896–1936", "1937–1976", "1977–2016"]
        chart_df["Era"] = pd.Categorical(
            chart_df["Era"],
            categories=era_order,
            ordered=True
        )

        chart_df = chart_df.sort_values(["Sport", "Era"])

        # Elegant external title
        st.markdown(
            """
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 38px;
                line-height: 1.05;
                color: #171717;
                margin-top: 28px;
                margin-bottom: 8px;
            ">
                How did female participation change across Olympic sports?
            </div>
            """,
            unsafe_allow_html=True
        )

        fig = px.scatter(
            chart_df,
            x="Era",
            y="Sport",
            size="Women_athletes",
            color="Women_athletes",
            size_max=28,
            color_continuous_scale=[
                [0.0, "#f7c6d9"],
                [0.5, "#d17be3"],
                [1.0, "#6f2dbd"]
            ],
            custom_data=["Women_athletes"],
            title=None
        )

        fig.update_traces(
            marker=dict(
                opacity=0.82,
                line=dict(
                    color="#171717",
                    width=1.1
                )
            ),
            hovertemplate=
                "<b>Era:</b> %{x}<br>" +
                "<b>Sport:</b> %{y}<br>" +
                "<b>Women athletes:</b> %{marker.size}<extra></extra>"
        )
        fig = apply_plotly_theme(fig, height=680)

        fig.update_layout(
            title=None,
            xaxis_title="Olympic era",
            yaxis_title="Sport",
            margin=dict(l=90, r=155, t=55, b=70),
            showlegend=False,
            coloraxis_colorbar=dict(
                title="Women athletes",
                x=1.02,
                y=0.50,
                len=0.78,
                thickness=18
            )
        )

        st.plotly_chart(fig, width="stretch")

        st.markdown(
            """
            <div style="text-align: right; font-size: 14px; color: var(--muted); margin-top: -20px; padding-right: 15px; margin-bottom: 25px;">
                ◍ <i>The size of the bubble remarks the number of women athletes</i>
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
        if st.button("← Back to Olympic Archive", key="back_from_year", width="stretch"):
            st.session_state.page = "main"
            st.rerun()

    available_years = sorted(df["Year"].dropna().unique().astype(int).tolist())

    selected_year = st.select_slider(
        "Choose an Olympic year :",
        options=available_years,
        value=available_years[-1]
    )

    year_df = df[df["Year"] == selected_year].copy()
    year_medals_df = df_medals[df_medals["Year"] == selected_year].copy()

    if year_df.empty:
        st.info("No data available for this year.")
        return

    city = year_df["City"].dropna().iloc[0]
    games = year_df["Games"].dropna().iloc[0]

    athletes = year_df["Name"].nunique()
    athlete_entries = len(year_df)
    sports = year_df["Sport"].nunique()
    events = year_df["Event"].nunique()
    nations = year_df["NOC"].nunique()
    medal_entries = len(year_medals_df)

    city_to_country_code = {
        "Athina": "gr", "Athens": "gr", "Paris": "fr", "St. Louis": "us",
        "London": "gb", "Stockholm": "se", "Antwerpen": "be", "Antwerp": "be",
        "Amsterdam": "nl", "Los Angeles": "us", "Berlin": "de", "Helsinki": "fi",
        "Melbourne": "au", "Roma": "it", "Rome": "it", "Tokyo": "jp",
        "Mexico City": "mx", "Munich": "de", "Montreal": "ca",
        "Moskva": "su", "Moscow": "su",
        "Seoul": "kr", "Barcelona": "es", "Atlanta": "us",
        "Sydney": "au", "Beijing": "cn", "Rio de Janeiro": "br"
    }

    country_code = city_to_country_code.get(city, "")

    if city in ["Moskva", "Moscow"]:
        flag_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/120px-Flag_of_the_Soviet_Union.svg.png"
        flag_html = f'<img src="{flag_url}" height="55" style="vertical-align: middle; border-radius: 4px;">'
    elif country_code:
        flag_html = f'<img src="https://flagcdn.com/h120/{country_code}.png" height="55" style="vertical-align: middle; border-radius: 4px;">'
    else:
        flag_html = html.escape(str(games))

    st.markdown(
        f"""
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">{int(selected_year)} · {html.escape(str(city))}</h2>
                <span class="stamp" style="padding: 6px 14px;">{flag_html}</span>
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

    

    st.markdown(
        """
        <div class="filter-panel">
            <div class="filter-eyebrow">Interactive filter room</div>
            <h2 class="filter-title">Build Your Olympic View</h2>
            <p class="filter-copy">
                Choose one or more sports, select the nations you want to compare,
                and generate a focused Olympic view for this edition.
            </p>
            <div class="filter-mini-row">
                <span class="filter-mini-tag">Sport filter</span>
                <span class="filter-mini-tag">Nation filter</span>
                <span class="filter-mini-tag">Podium view</span>
                <span class="filter-mini-tag">Medal wall</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    available_sports = sorted(year_df["Sport"].dropna().unique().tolist())
    available_nocs = sorted(year_df["NOC"].dropna().unique().tolist())

    f1, f2 = st.columns(2)

    with f1:
        selected_sports = st.multiselect(
            "Choose sport(s)",
            options=available_sports,
            default=[],
            placeholder="All sports"
        )

    with f2:
        selected_nocs = st.multiselect(
            "Choose nation(s)",
            options=available_nocs,
            default=[],
            placeholder="All nations"
        )

    filtered_df = year_df.copy()
    filtered_medals_df = year_medals_df.copy()

    if selected_sports:
        filtered_df = filtered_df[filtered_df["Sport"].isin(selected_sports)]
        filtered_medals_df = filtered_medals_df[filtered_medals_df["Sport"].isin(selected_sports)]

    if selected_nocs:
        filtered_df = filtered_df[filtered_df["NOC"].isin(selected_nocs)]
        filtered_medals_df = filtered_medals_df[filtered_medals_df["NOC"].isin(selected_nocs)]

    st.markdown("#### Filtered summary")

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Athletes", f"{filtered_df['Name'].nunique():,}")
    m2.metric("Entries", f"{len(filtered_df):,}")
    m3.metric("Sports", filtered_df["Sport"].nunique())
    m4.metric("Nations", filtered_df["NOC"].nunique())
    m5.metric("Medal entries", f"{len(filtered_medals_df):,}")

    olympic_podium_and_medal_wall(
        filtered_medals_df,
        selected_year
    )

    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title" style="font-size: 30px;">Choose What to Compare</h2>
                <span class="stamp">Chart view</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    control_col1, control_col2 = st.columns([1.7, 0.8])

    with control_col1:
        chart_view = st.radio(
            "Choose visualization",
            [
                "Sport participation",
                "Nation medal ranking",
                "Events by sport",
                "Sport × nation medals",
                "Gender distribution"
            ],
            horizontal=True
        )

    with control_col2:
        if chart_view == "Sport participation":
            top_n = st.slider("How many results?", min_value=1, max_value=15, value=10)
        
        elif chart_view == "Nation medal ranking":
            top_n = st.slider("How many results?", min_value=1, max_value=15, value=10)
        
        elif chart_view == "Events by sport":
            top_n = st.slider("How many results?", min_value=1, max_value=20, value=10)
        
        elif chart_view == "Sport × nation medals":
            top_n = st.slider("How many results?", min_value=1, max_value=7, value=5)
        
        elif chart_view == "Gender distribution":
            top_n = None

    if chart_view == "Sport participation":
        if filtered_df.empty:
            st.info("No data available with the selected filters.")
        else:
            chart_df = (
                filtered_df
                .groupby("Sport")
                .size()
                .sort_values(ascending=False)
                .head(top_n)
                .reset_index(name="Athlete entries")
            )

            fig = px.bar(
                chart_df,
                x="Athlete entries",
                y="Sport",
                orientation="h",
                text="Athlete entries",
                title=f"Sport Participation · {selected_year}"
            )

            fig.update_traces(
                marker_color="#b88a2e",
                marker_line_color="#171717",
                marker_line_width=1.2,
                textposition="outside",
                textfont=dict(color="#171717")
            )

            fig = apply_plotly_theme(fig, height=520)
            fig.update_layout(yaxis=dict(autorange="reversed"))

            st.plotly_chart(fig, width="stretch")

    elif chart_view == "Nation medal ranking":
        if filtered_medals_df.empty:
            st.info("No medal data available with the selected filters.")
        else:
            chart_df = (
                filtered_medals_df
                .drop_duplicates(subset=["Year", "Sport", "Event", "Medal", "NOC"])
                .groupby("NOC")
                .size()
                .sort_values(ascending=False)
                .head(top_n)
                .reset_index(name="Medals")
            )

            fig = px.bar(
                chart_df,
                x="NOC",
                y="Medals",
                text="Medals",
                title=f"Nation Medal Ranking · {selected_year}"
            )

            fig.update_traces(
                marker_color="#b88a2e",
                marker_line_color="#171717",
                marker_line_width=1.2,
                textposition="outside",
                textfont=dict(color="#171717")
            )

            fig = apply_plotly_theme(fig, height=500)

            st.plotly_chart(fig, width="stretch")

    elif chart_view == "Events by sport":
        if filtered_df.empty:
            st.info("No data available with the selected filters.")
        else:
            chart_df = (
                filtered_df
                .groupby("Sport")["Event"]
                .nunique()
                .sort_values(ascending=False)
                .head(top_n)
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
                textposition="outside",
                textfont=dict(color="#171717")
            )

            fig = apply_plotly_theme(fig, height=520)
            fig.update_layout(xaxis_tickangle=-35)

            st.plotly_chart(fig, width="stretch")

    elif chart_view == "Sport × nation medals":
        if filtered_medals_df.empty:
            st.info("No medal data available with the selected filters.")
        else:
            chart_df = (
                filtered_medals_df
                .drop_duplicates(subset=["Year", "Sport", "Event", "Medal", "NOC"])
                .groupby(["Sport", "NOC"])
                .size()
                .reset_index(name="Medals")
            )

            top_sports = (
            chart_df
            .groupby("Sport")["Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .index
            .tolist()
        )
        
        chart_df = chart_df[chart_df["Sport"].isin(top_sports)]

        top_nations = (
            chart_df
            .groupby("NOC")["Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(7)
            .index
            .tolist()
        )
        
        chart_df = chart_df[chart_df["NOC"].isin(top_nations)]

        fig = px.bar(
                chart_df,
                x="Sport",
                y="Medals",
                color="NOC",
                text="Medals",
                barmode="group",
                title=f"Sport × Nation Medal Comparison · {selected_year}"
            )

        fig.update_traces(
                marker_line_color="#171717",
                marker_line_width=1.1,
                textposition="outside",
                textfont=dict(color="#171717")
            )

        fig = apply_plotly_theme(fig, height=560)

        fig.update_layout(
                xaxis_tickangle=-25,
                bargap=0.28,
                bargroupgap=0.08,
                legend_title_text="Nation"
            )

        st.plotly_chart(fig, width="stretch")

    elif chart_view == "Gender distribution":
        if filtered_df.empty:
            st.info("No data available with the selected filters.")
        else:
            chart_df = (
                filtered_df
                .groupby("Sex")
                .size()
                .reset_index(name="Athlete entries")
            )

            fig = px.pie(
                chart_df,
                names="Sex",
                values="Athlete entries",
                title=f"Gender Distribution · {selected_year}",
                hole=0.45,
                color="Sex",
                color_discrete_map={
                    "M": "#1f77b4",
                    "F": "#e377c2",
                    "Male": "#1f77b4",
                    "Female": "#e377c2"
             }
            )

            fig.update_traces(
                marker=dict(line=dict(color="#171717", width=1.5)),
                textfont=dict(color="#171717")
            )

            fig = apply_plotly_theme(fig, height=460)

            st.plotly_chart(fig, width="stretch")

# ============================================================
# OLYMPIC RINGS
# ============================================================

def olympic_rings(period_df, era):
    sports_to_show, sport_stats = build_sport_stats_for_rings(period_df)
    sports_number = len(sports_to_show)
    selected_period = era_label(era)
    safe_selected_period = html.escape(selected_period)
    
    def generate_positions(number_of_sports):
        import math
        
        # Centri esatti calcolati millimetricamente dal CSS
        ring_centers = [
            (247, 277),  # Blue
            (522, 277),  # Yellow
            (797, 277),  # Black
            (382, 447),  # Green
            (657, 447)   # Red
        ]
        
        R_stroke = 133.5 
        # Margine di sicurezza calcolato (raggio icona 23px + metà spessore anello 8.5px + margine visivo)
        clearance = 38  
        
        positions = [(0, 0)] * number_of_sports
        
        for ring_idx in range(5):
            # Filtra gli sport assegnati a questo anello specifico
            sport_indices = [i for i in range(number_of_sports) if i % 5 == ring_idx]
            n_sports = len(sport_indices)
            
            if n_sports == 0:
                continue
                
            valid_angles = []
            # Scansiona i 360 gradi in modo finissimo (passi da 0.25 gradi)
            for step in range(360 * 4):
                angle_deg = step / 4.0
                a = math.radians(angle_deg)
                px = ring_centers[ring_idx][0] + R_stroke * math.cos(a)
                py = ring_centers[ring_idx][1] + R_stroke * math.sin(a)
                
                # Verifica che questo punto dell'arco non attraversi un altro anello
                is_safe = True
                for o_idx, (ocx, ocy) in enumerate(ring_centers):
                    if o_idx == ring_idx:
                        continue
                    dist_to_other_center = math.hypot(px - ocx, py - ocy)
                    if abs(dist_to_other_center - R_stroke) < clearance:
                        is_safe = False
                        break
                        
                if is_safe:
                    valid_angles.append(angle_deg)
                    
            # Fallback (non dovrebbe mai attivarsi, ma previene errori software)
            if not valid_angles:
                valid_angles = [step / 4.0 for step in range(360 * 4)]
                
            # Distribuisci matematicamente le icone lungo gli angoli sicuri ricavati
            step_size = len(valid_angles) / n_sports
            for i, sport_idx in enumerate(sport_indices):
                # Piazza l'icona esattamente al centro dello slot a lei dedicato
                sample_idx = int(i * step_size + (step_size / 2))
                sample_idx = min(sample_idx, len(valid_angles) - 1)
                
                chosen_angle = valid_angles[sample_idx]
                a = math.radians(chosen_angle)
                px = ring_centers[ring_idx][0] + R_stroke * math.cos(a)
                py = ring_centers[ring_idx][1] + R_stroke * math.sin(a)
                
                positions[sport_idx] = (px, py)
                
        return positions

    positions = generate_positions(len(sports_to_show))
    
    rings_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
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
    .ring-blue {{ left: 105px; top: 135px; border: 17px solid #1d5f9f; }}
    .ring-yellow {{ left: 380px; top: 135px; border: 17px solid #e6b31e; }}
    .ring-black {{ left: 655px; top: 135px; border: 17px solid #1f2933; }}
    .ring-green {{ left: 240px; top: 305px; border: 17px solid #2e7d4f; }}
    .ring-red {{ left: 515px; top: 305px; border: 17px solid #c74639; }}
    
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
    .info-label {{ letter-spacing: 1px; }}
    .info-value {{ font-weight: bold; text-align: right; }}
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
    .close-info:hover {{ background: #a16207; }}
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
        px, py = position
        x = px - 23
        y = py - 23
        icon = sport_stats[sport]["icon"]
        safe_sport_html = html.escape(str(sport))
        safe_sport_js = safe_js(sport)
        disciplines_count = sport_stats[sport]["disciplines"]
        athletes_count = sport_stats[sport]["athletes"]
        medals_count = sport_stats[sport]["medals"]
        top_country = sport_stats[sport]["top_country"]
        best_athlete = sport_stats[sport]["best_athlete"]

        rings_html += f"""
        <button class="sport-badge"
        onclick="openSportInfo(
        `{safe_sport_js}`, `{safe_js(icon)}`, `{disciplines_count}`,
        `{athletes_count}`, `{medals_count}`, `{safe_js(top_country)}`,
        `{safe_js(best_athlete)}`
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
        <div class="info-row"><div class="info-label">PERIOD</div><div class="info-value">{safe_selected_period}</div></div>
        <div class="info-row"><div class="info-label">DISCIPLINES</div><div id="infoDisciplines" class="info-value">-</div></div>
        <div class="info-row"><div class="info-label">ATHLETES</div><div id="infoAthletes" class="info-value">-</div></div>
        <div class="info-row"><div class="info-label">TOTAL MEDAL ENTRIES</div><div id="infoMedals" class="info-value">-</div></div>
        <div class="info-row"><div class="info-label">BEST COUNTRY</div><div id="infoCountry" class="info-value">-</div></div>
  <div class="info-row"><div class="info-label">BEST ATHLETE</div><div id="infoBestAthlete" class="info-value">-</div></div>
        </div>
        <div class="instruction">HOVER A BADGE TO READ ITS SPORT · CLICK TO OPEN THE DISPATCH</div>
        </div>

        <script>
        function openSportInfo(sport, icon, disciplines, athletes, medals, country, bestAthlete) {{
            document.getElementById("infoPanel").classList.add("show");
            document.getElementById("infoTitle").innerHTML = icon + " " + sport;
            document.getElementById("infoDisciplines").innerHTML = disciplines;
            document.getElementById("infoAthletes").innerHTML = athletes;
            document.getElementById("infoMedals").innerHTML = medals;
            document.getElementById("infoCountry").innerHTML = country;
            document.getElementById("infoBestAthlete").innerHTML = bestAthlete;
        }}
        function closeSportInfo() {{
            document.getElementById("infoPanel").classList.remove("show");
        }}
        </script>
    """
    
    encoded_html = base64.b64encode(
        rings_html.encode("utf-8")
    ).decode("utf-8")

    st.iframe(
        src=f"data:text/html;charset=utf-8;base64,{encoded_html}",
        height=700,
        width="stretch"
    )

# ============================================================
# ATHLETE EXPLORER
# ============================================================

@st.cache_data(show_spinner=False)
def build_athlete_stats(df_medals):
    df_temp = df_medals.copy()
    df_temp["Edition_Label"] = df_temp["Year"].astype(str) + " · " + df_temp["City"].astype(str)

    athlete_stats = (
        df_temp
        .groupby(["Name", "NOC"])
        .agg(
            gold=("Medal", lambda x: (x == "Gold").sum()),
            silver=("Medal", lambda x: (x == "Silver").sum()),
            bronze=("Medal", lambda x: (x == "Bronze").sum()),
            total=("Medal", "count"),
            sports=("Sport", lambda x: sorted(x.dropna().unique())),
            editions=("Edition_Label", lambda x: sorted(set(x.dropna())))
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
        flag_html = noc_flag_html(picked["NOC"], height=34)

        st.html(
            f"""
            <div class="athlete-card">
                <div class="mono-small">{html.escape(str(picked["NOC"]))}</div>

                <h3 class="athlete-name" style="display:flex; align-items:center; gap:6px;">
                    {flag_html}
                    <span>{html.escape(str(picked["Name"]))}</span>
                </h3>
            </div>
            """
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

        st.markdown("#### Editions")
        editions_html = ""
        for ed in picked["editions"]:
            editions_html += f"""
            <span class="mini-tag mono-tag">
                {html.escape(str(ed))}
            </span>
            """
        st.markdown(
            f"""
            <div class="tag-wrapper">
                {editions_html}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ATHLETE RACE
# ============================================================

def athlete_race(df_medals):
    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">The Great Race · Athletes</h2>
                <span class="stamp">Athlete Profile Radar</span>
            </div>
            <p class="italic-desc">
                Compare two Olympic athletes through a multi-dimensional career profile.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    available_sports = sorted(df_medals["Sport"].dropna().unique().tolist())

    selected_sport = st.selectbox(
        "Filter by Sport",
        options=available_sports,
        index=available_sports.index("Tennis") if "Tennis" in available_sports else 0
    )

    filtered_medals = df_medals[df_medals["Sport"] == selected_sport].copy()

    athlete_stats = build_athlete_stats(filtered_medals)

    top_athletes = athlete_stats.head(40).copy()

    options = [
        f'{row["Name"]} · {row["NOC"]} · {int(row["total"])} medals'
        for _, row in top_athletes.iterrows()
    ]

    if len(options) < 2:
        st.info("Not enough athletes to compare in this sport.")
        return

    col1, col2 = st.columns(2)

    with col1:
        athlete_a_label = st.selectbox("Athlete A", options, index=0)

    with col2:
        athlete_b_label = st.selectbox("Athlete B", options, index=1)

    athlete_a_name = top_athletes.iloc[options.index(athlete_a_label)]["Name"]
    athlete_b_name = top_athletes.iloc[options.index(athlete_b_label)]["Name"]

    def get_radar_metrics(athlete_name):
        athlete_df = filtered_medals[
            filtered_medals["Name"] == athlete_name
        ].copy()

        athlete_df = athlete_df.drop_duplicates(
            subset=["Year", "Sport", "Event", "Medal", "Name"]
        )

        if athlete_df.empty:
            return {
                "Gold medals": 0,
                "Silver medals": 0,
                "Bronze medals": 0,
                "Total medals": 0,
                "Olympic editions": 0,
                "Events medalled": 0,
                "Career span": 0,
                "Medals per edition": 0
            }

        gold = int((athlete_df["Medal"] == "Gold").sum())
        silver = int((athlete_df["Medal"] == "Silver").sum())
        bronze = int((athlete_df["Medal"] == "Bronze").sum())
        total = int(len(athlete_df))

        editions = int(athlete_df["Year"].nunique())
        events_medalled = int(athlete_df["Event"].nunique())

        years = sorted(athlete_df["Year"].dropna().unique())

        if len(years) > 1:
            career_span = int(max(years) - min(years))
        else:
            career_span = 0

        medals_per_edition = round(total / editions, 2) if editions > 0 else 0

        return {
            "Gold medals": gold,
            "Silver medals": silver,
            "Bronze medals": bronze,
            "Total medals": total,
            "Olympic editions": editions,
            "Events medalled": events_medalled,
            "Career span": career_span,
            "Medals per edition": medals_per_edition
        }

    metrics_a = get_radar_metrics(athlete_a_name)
    metrics_b = get_radar_metrics(athlete_b_name)

    categories = list(metrics_a.keys())

    actual_a = [metrics_a[metric] for metric in categories]
    actual_b = [metrics_b[metric] for metric in categories]

    max_values = [
        max(value_a, value_b, 1)
        for value_a, value_b in zip(actual_a, actual_b)
    ]

    normalized_a = [
        (value / max_value) * 100
        for value, max_value in zip(actual_a, max_values)
    ]

    normalized_b = [
        (value / max_value) * 100
        for value, max_value in zip(actual_b, max_values)
    ]

    categories_closed = categories + [categories[0]]
    normalized_a_closed = normalized_a + [normalized_a[0]]
    normalized_b_closed = normalized_b + [normalized_b[0]]
    actual_a_closed = actual_a + [actual_a[0]]
    actual_b_closed = actual_b + [actual_b[0]]

    radar_fig = go.Figure()

    radar_fig.add_trace(
        go.Scatterpolar(
            r=normalized_a_closed,
            theta=categories_closed,
            mode="lines+markers",
            fill="toself",
            name=athlete_a_name,
            customdata=actual_a_closed,
            line=dict(
                color="#171717",
                width=3,
                dash="solid"
            ),
            marker=dict(
                color="#f4efe3",
                size=12,
                symbol="circle-open",
                line=dict(
                    color="#171717",
                    width=2.5
                )
            ),
            fillcolor="rgba(23, 23, 23, 0.08)",
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                "%{theta}<br>" +
                "Real value: %{customdata}<extra></extra>"
        )
    )

    radar_fig.add_trace(
        go.Scatterpolar(
            r=normalized_b_closed,
            theta=categories_closed,
            mode="lines+markers",
            fill="toself",
            name=athlete_b_name,
            customdata=actual_b_closed,
            line=dict(
                color="#b88a2e",
                width=3,
                dash="dash"
            ),
            marker=dict(
                color="#b88a2e",
                size=13,
                symbol="x",
                line=dict(
                    color="#b88a2e",
                    width=2.5
                )
            ),
            fillcolor="rgba(184, 138, 46, 0.08)",
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                "%{theta}<br>" +
                "Real value: %{customdata}<extra></extra>"
        )
    )

    radar_title = f"Athlete Profile Radar · {selected_sport}"

    radar_fig.update_layout(
        title=radar_title,
        height=650,
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        font=dict(
            family="Roboto Mono",
            color="#171717"
        ),
        polar=dict(
            bgcolor="#f4efe3",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[25, 50, 75, 100],
                ticktext=["25", "50", "75", "100"],
                gridcolor="rgba(23,23,23,0.25)",
                linecolor="#171717",
                tickfont=dict(color="#171717")
            ),
            angularaxis=dict(
                gridcolor="rgba(23,23,23,0.25)",
                linecolor="#171717",
                tickfont=dict(
                    color="#171717",
                    size=12
                )
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font=dict(color="#171717")
        ),
        margin=dict(l=80, r=80, t=110, b=60)
    )

    st.plotly_chart(radar_fig, width="stretch")

    comparison_df = pd.DataFrame(
        {
            "Metric": categories,
            athlete_a_name: actual_a,
            athlete_b_name: actual_b
        }
    )

    st.markdown(
        """
        <div class="medal-detail-card">
            <div class="medal-detail-title">How to read this radar</div>
            <div class="medal-detail-text">
                Each axis represents one Olympic career dimension. The radar values are normalized from 0 to 100
                between the two selected athletes. When both athletes have the same value, their points overlap;
                this is why one athlete is shown with an open circle and the other with a golden X.
                The table below reports the real values.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    table_rows = ""

    for _, row in comparison_df.iterrows():
        value_a = row[athlete_a_name]
        value_b = row[athlete_b_name]

        if isinstance(value_a, float) and value_a.is_integer():
            value_a = int(value_a)

        if isinstance(value_b, float) and value_b.is_integer():
            value_b = int(value_b)

        table_rows += f"""
         <tr>
            <td>{html.escape(str(row["Metric"]))}</td>
            <td>{html.escape(str(value_a))}</td>
            <td>{html.escape(str(value_b))}</td>
        </tr>
        """

    st.html(
        f"""
        <style>
            .radar-table-wrapper {{
                max-width: 900px;
                margin: 18px auto 34px auto;
                border: 1.5px solid #171717;
                background: #171717;
                box-shadow: 5px 5px 0px #b88a2e;
            }}

            .radar-table {{
                width: 100%;
                border-collapse: collapse;
                font-family: 'Roboto Mono', monospace;
                background: #171717;
                color: #f4efe3;
                font-size: 12px;
            }}

            .radar-table th {{
                color: #f4efe3 !important;
                background: #171717 !important;
                border-bottom: 1.5px solid #f4efe3;
                border-right: 1px solid rgba(244,239,227,0.35);
                padding: 10px 12px;
                text-align: left;
                font-weight: 600;
                letter-spacing: 0.04em;
            }}

            .radar-table td {{
                color: #f4efe3 !important;
                background: #171717 !important;
                border-bottom: 1px solid rgba(244,239,227,0.22);
                border-right: 1px solid rgba(244,239,227,0.22);
                padding: 9px 12px;
                text-align: left;
            }}

            .radar-table td:not(.radar-metric) {{
                text-align: center;
                font-weight: 600;
            }}

            .radar-table tr:last-child td {{
                border-bottom: none;
            }}

            .radar-table th:last-child,
            .radar-table td:last-child {{
                border-right: none;
            }}

            .radar-table-title {{
                font-family: 'Playfair Display', serif;
                font-size: 26px;
                color: #f4efe3;
                padding: 14px 16px 4px 16px;
            }}

            .radar-table-subtitle {{
                font-family: 'Roboto Mono', monospace;
                font-size: 10px;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                color: #b88a2e;
                padding: 0 16px 12px 16px;
            }}
        </style>

        <div class="radar-table-wrapper">
            <div class="radar-table-title">Real values</div>
            <div class="radar-table-subtitle">Radar metrics comparison</div>

            <table class="radar-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>{html.escape(str(athlete_a_name))}</th>
                        <th>{html.escape(str(athlete_b_name))}</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """
    )



# ============================================================
# NATION DUEL
# ============================================================
# ============================================================
# NATION DUEL
# ============================================================

def nation_duel(df_medals):
    st.markdown(
        """
        <div class="paper-panel">
            <div class="panel-title-row">
                <h2 class="panel-title">The Great Duel · Nations</h2>
                <span class="stamp">Beyond the Medal Table</span>
            </div>
            <p class="italic-desc">
                Compare two Olympic nations through edition rivalry, sport-by-sport dominance and national medal profiles.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    unique_medals = (
        df_medals
        .drop_duplicates(subset=["Year", "Sport", "Event", "Medal", "NOC"])
        .copy()
    )

    if unique_medals.empty:
        st.info("No medal data available.")
        return

    top_nocs = (
        unique_medals
        .groupby("NOC")
        .size()
        .sort_values(ascending=False)
        .head(35)
        .index
        .tolist()
    )

    if len(top_nocs) < 2:
        st.info("Not enough nations to compare.")
        return

    col1, col2 = st.columns(2)

    with col1:
        nation_a = st.selectbox(
            "Nation A",
            top_nocs,
            index=top_nocs.index("USA") if "USA" in top_nocs else 0,
            key="select_nation_a"
        )

    with col2:
        nation_b = st.selectbox(
            "Nation B",
            top_nocs,
            index=top_nocs.index("URS") if "URS" in top_nocs else min(1, len(top_nocs) - 1),
            key="select_nation_b"
        )

    if nation_a == nation_b:
        st.warning("Please select two different nations.")
        return

    duel_df = unique_medals[unique_medals["NOC"].isin([nation_a, nation_b])].copy()

    # ============================================================
    # SUMMARY FUNCTION
    # ============================================================

    def nation_summary(noc):
        sub = duel_df[duel_df["NOC"] == noc].copy()

        total = len(sub)
        gold = int((sub["Medal"] == "Gold").sum())
        silver = int((sub["Medal"] == "Silver").sum())
        bronze = int((sub["Medal"] == "Bronze").sum())
        sports = int(sub["Sport"].nunique())
        editions = int(sub["Year"].nunique())

        if not sub.empty:
            best_edition = int(sub.groupby("Year").size().max())
        else:
            best_edition = 0

        medals_per_edition = total / editions if editions > 0 else 0
        gold_efficiency = gold / total if total > 0 else 0

        top3_sports_medals = (
            sub.groupby("Sport")
            .size()
            .sort_values(ascending=False)
            .head(3)
            .sum()
        )

        specialization_index = top3_sports_medals / total if total > 0 else 0

        return {
            "total": total,
            "gold": gold,
            "silver": silver,
            "bronze": bronze,
            "sports": sports,
            "editions": editions,
            "best_edition": best_edition,
            "medals_per_edition": medals_per_edition,
            "gold_efficiency": gold_efficiency,
            "specialization_index": specialization_index
        }

    summary_a = nation_summary(nation_a)
    summary_b = nation_summary(nation_b)

    # ============================================================
    # SUMMARY METRICS
    # ============================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(f"{nation_a} medals", summary_a["total"])
    c2.metric(f"{nation_b} medals", summary_b["total"])

    if summary_a["total"] >= summary_b["total"]:
        ahead_nation = nation_a
    else:
        ahead_nation = nation_b

    c3.metric(
        "Medal gap",
        abs(summary_a["total"] - summary_b["total"]),
        delta=f"{ahead_nation} ahead"
    )

    if summary_a["sports"] >= summary_b["sports"]:
        broader_nation = nation_a
    else:
        broader_nation = nation_b

    flag_url = noc_flag_url(broader_nation)

    with c4:
        st.caption("Broader nation")

        if flag_url:
            st.image(flag_url, width=76)
        else:
            st.markdown(f"### {broader_nation}")

        st.success("↑ More medal-winning sports")
    chart_choice = st.radio(
        "Choose the nation comparison view",
        [
            "Edition-by-edition rivalry",
            "Sport-by-sport duel",
            "National profile radar"
        ],
        horizontal=True
    )

    # ============================================================
    # 1. EDITION-BY-EDITION RIVALRY
    # ============================================================

    if chart_choice == "Edition-by-edition rivalry":
        medals_by_year = (
            duel_df
            .groupby(["Year", "NOC"])
            .size()
            .reset_index(name="Medals")
        )

        pivot = medals_by_year.pivot(
            index="Year",
            columns="NOC",
            values="Medals"
        ).fillna(0)

        for noc in [nation_a, nation_b]:
            if noc not in pivot.columns:
                pivot[noc] = 0

        pivot = pivot.reset_index()
        pivot["Medal gap"] = pivot[nation_a] - pivot[nation_b]

        pivot["Winner"] = np.where(
            pivot["Medal gap"] > 0,
            nation_a,
            np.where(
                pivot["Medal gap"] < 0,
                nation_b,
                "Tie"
            )
        )

        pivot["Gap label"] = pivot["Medal gap"].apply(
            lambda x: f"{nation_a} +{int(x)}" if x > 0 else (
                f"{nation_b} +{abs(int(x))}" if x < 0 else "Tie"
            )
        )

        # Calcolo dinamico del colore in base al totale medaglie cumulative
        color_a = "#b88a2e" if summary_a["total"] >= summary_b["total"] else "#c0c0c0"
        color_b = "#b88a2e" if summary_b["total"] > summary_a["total"] else "#c0c0c0"

        fig = px.bar(
            pivot,
            x="Year",
            y="Medal gap",
            color="Winner",
            title=f"Who won each Olympic edition? · {nation_a} vs {nation_b}",
            color_discrete_map={
                nation_a: color_a,
                nation_b: color_b,
                "Tie": "#68645c"
            },
            hover_data={
                nation_a: True,
                nation_b: True,
                "Medal gap": True,
                "Winner": True
            }
        )

        fig.update_traces(
            marker_line_color="#171717",
            marker_line_width=1.2
            
        )

        fig.add_hline(
            y=0,
            line_width=2,
            line_color="#171717"
        )

        fig = apply_plotly_theme(fig, height=560)

        fig.update_layout(
            xaxis_title="Olympic year",
            yaxis_title=f"Medal gap ({nation_a} − {nation_b})",
            legend_title_text="Edition winner",
            bargap=0.25,
            margin=dict(l=60, r=80, t=80, b=60)
        )

        st.plotly_chart(fig, width="stretch")

        

  

        # ============================================================
    # 2. SPORT-BY-SPORT DUEL · DUMBBELL CHART
    # ============================================================

    elif chart_choice == "Sport-by-sport duel":
        sport_table = (
            duel_df
            .groupby(["Sport", "NOC"])
            .size()
            .reset_index(name="Medals")
        )

        pivot = sport_table.pivot(
            index="Sport",
            columns="NOC",
            values="Medals"
        ).fillna(0)

        for noc in [nation_a, nation_b]:
            if noc not in pivot.columns:
                pivot[noc] = 0

        pivot["Total medals"] = pivot[nation_a] + pivot[nation_b]
        pivot["Difference"] = pivot[nation_a] - pivot[nation_b]
        pivot["Abs difference"] = pivot["Difference"].abs()

        plot_df = (
            pivot
            .sort_values("Total medals", ascending=False)
            .head(18)
            .reset_index()
        )

        plot_df = plot_df.sort_values("Total medals", ascending=True)
        plot_df["Text A"] = plot_df[nation_a].astype(int).astype(str)
        plot_df["Text B"] = plot_df[nation_b].astype(int).astype(str)

        plot_df["Text position A"] = np.where(
            plot_df[nation_a] >= plot_df[nation_b],
            "middle right",
            "middle left"
        )

        plot_df["Text position B"] = np.where(
            plot_df[nation_b] >= plot_df[nation_a],
            "middle right",
            "middle left"
        )

        fig = go.Figure()

        # Calcolo dinamico dei colori per i punti del dumbbell chart
        color_a = "#b88a2e" if summary_a["total"] >= summary_b["total"] else "#c0c0c0"
        color_b = "#b88a2e" if summary_b["total"] > summary_a["total"] else "#c0c0c0"

        # Linee tra le due nazioni
        for _, row in plot_df.iterrows():
            fig.add_trace(
                go.Scatter(
                    x=[row[nation_a], row[nation_b]],
                    y=[row["Sport"], row["Sport"]],
                    mode="lines",
                    line=dict(
                        color="rgba(23,23,23,0.35)",
                        width=3
                    ),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

        # Punti Nation A
        fig.add_trace(
            go.Scatter(
                x=plot_df[nation_a],
                y=plot_df["Sport"],
                mode="markers+text",
                name=nation_a,
                text=plot_df["Text A"],
                textposition=plot_df["Text position A"],
                textfont=dict(
                    color=color_a,
                    size=11,
                    family="Arial"
                ),
                marker=dict(
                    size=16,
                    color=color_a,
                    line=dict(
                        color="#171717",
                        width=2
                    )
                ),
                hovertemplate=
                    "<b>%{y}</b><br>" +
                    "Nazione: %{fullData.name}<br>" +
                    "Medaglie: %{x}<extra></extra>"
            )
        )

        # Punti Nation B
        fig.add_trace(
            go.Scatter(
                x=plot_df[nation_b],
                y=plot_df["Sport"],
                mode="markers+text",
                name=nation_b,
                text=plot_df["Text B"],
                textposition=plot_df["Text position B"],
                textfont=dict(
                    color=color_b,
                    size=11,
                    family="Arial"
                ),
                marker=dict(
                    size=16,
                    color=color_b,
                    line=dict(
                        color="#171717",
                        width=2
                    )
                ),
                hovertemplate=
                    "<b>" + nation_b + "</b><br>" +
                    "Sport: %{y}<br>" +
                    "Medals: %{x}<extra></extra>"
            )
        )

        fig.update_layout(
            title=dict(
                text=f"Who dominates each Olympic sport? · {nation_a} vs {nation_b}",
                    font=dict(
                    family="Playfair Display",
                    size=26,
                    color="#171717"
                ),
                x=0,
                    xanchor="left"
            ),



            height=680,
            paper_bgcolor="#f4efe3",
            plot_bgcolor="#f4efe3",
            font=dict(
                family="Roboto Mono",
                color="#171717"
            ),
            xaxis=dict(
                title="Medals in each sport",
                gridcolor="rgba(23,23,23,0.18)",
                linecolor="#171717",
                zeroline=False,
                tickfont=dict(color="#171717"),
                title_font=dict(color="#171717")
            ),
            yaxis=dict(
                title="Sport",
                gridcolor="rgba(23,23,23,0.10)",
                linecolor="#171717",
                tickfont=dict(color="#171717"),
                title_font=dict(color="#171717")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.03,
                xanchor="center",
                x=0.5,
                font=dict(color="#171717")
            ),
            hoverlabel=dict(
                bgcolor="#f4efe3",
                bordercolor="#171717",
                font=dict(
                    family="Roboto Mono",
                    size=13,
                    color="#171717"
                )
            ),
            margin=dict(l=130, r=90, t=95, b=60)
        )

        st.plotly_chart(fig, width="stretch")

        
    # ============================================================
    # 3. NATIONAL PROFILE RADAR
    # ============================================================

    elif chart_choice == "National profile radar":
        radar_metrics = {
            "Total medals": (summary_a["total"], summary_b["total"]),
            "Gold medals": (summary_a["gold"], summary_b["gold"]),
            "Medal sports": (summary_a["sports"], summary_b["sports"]),
            "Medal editions": (summary_a["editions"], summary_b["editions"]),
            "Best edition": (summary_a["best_edition"], summary_b["best_edition"]),
            "Medals / edition": (summary_a["medals_per_edition"], summary_b["medals_per_edition"]),
            "Gold efficiency": (summary_a["gold_efficiency"], summary_b["gold_efficiency"]),
            "Specialization": (summary_a["specialization_index"], summary_b["specialization_index"])
        }

        categories = list(radar_metrics.keys())

        actual_a = [radar_metrics[m][0] for m in categories]
        actual_b = [radar_metrics[m][1] for m in categories]

        max_values = [
            max(a, b, 1)
            for a, b in zip(actual_a, actual_b)
        ]

        normalized_a = [
            (a / max_v) * 100
            for a, max_v in zip(actual_a, max_values)
        ]

        normalized_b = [
            (b / max_v) * 100
            for b, max_v in zip(actual_b, max_values)
        ]

        categories_closed = categories + [categories[0]]
        normalized_a_closed = normalized_a + [normalized_a[0]]
        normalized_b_closed = normalized_b + [normalized_b[0]]
        actual_a_closed = actual_a + [actual_a[0]]
        actual_b_closed = actual_b + [actual_b[0]]

        # Calcolo dinamico dei colori (linee e bordi)
        color_a = "#b88a2e" if summary_a["total"] >= summary_b["total"] else "#8A8D91"
        color_b = "#b88a2e" if summary_b["total"] > summary_a["total"] else "#8A8D91"

        # Calcolo dinamico dei colori per il riempimento (fill) con trasparenza al 15%
        fill_a = "rgba(184, 138, 46, 0.15)" if summary_a["total"] >= summary_b["total"] else "rgba(192, 192, 192, 0.15)"
        fill_b = "rgba(184, 138, 46, 0.15)" if summary_b["total"] > summary_a["total"] else "rgba(192, 192, 192, 0.15)"

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=normalized_a_closed,
                theta=categories_closed,
                mode="lines+markers",
                fill="toself",
                name=nation_a,
                customdata=actual_a_closed,
                line=dict(
                    color=color_a,
                    width=3
                ),
                marker=dict(
                    color=color_a,
                    size=11,
                    symbol="circle-open",
                    line=dict(
                        color=color_a,
                        width=2.5
                    )
                ),
                fillcolor=fill_a,
                hovertemplate=
                    "<b>%{fullData.name}</b><br>" +
                    "%{theta}<br>" +
                    "Real value: %{customdata:.2f}<extra></extra>"
            )
        )

        fig.add_trace(
            go.Scatterpolar(
                r=normalized_b_closed,
                theta=categories_closed,
                mode="lines+markers",
                fill="toself",
                name=nation_b,
                customdata=actual_b_closed,
                line=dict(
                    color=color_b,
                    width=3,
                    dash="dash"
                ),
                marker=dict(
                    color=color_b,
                    size=12,
                    symbol="x",
                    line=dict(
                        color=color_b,
                        width=2.5
                    )
                ),
                fillcolor=fill_b,
                hovertemplate=
                    "<b>%{fullData.name}</b><br>" +
                    "%{theta}<br>" +
                    "Real value: %{customdata:.2f}<extra></extra>"
            )
        )

        fig.update_layout(
            title=dict(
                text=f"Who has the stronger Olympic profile? · {nation_a} vs {nation_b}",
                font=dict(
                    family="Playfair Display",
                    size=26,
                    color="#171717"
                ),
                x=0,
                xanchor="left"
            ),
            height=650,
            paper_bgcolor="#f4efe3",
            plot_bgcolor="#f4efe3",
            font=dict(
                family="Roboto Mono",
                color="#171717"
            ),
            polar=dict(
                bgcolor="#f4efe3",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[25, 50, 75, 100],
                    ticktext=["25", "50", "75", "100"],
                    gridcolor="rgba(23,23,23,0.25)",
                    linecolor="#171717",
                    tickfont=dict(color="#171717")
                ),
                angularaxis=dict(
                    gridcolor="rgba(23,23,23,0.25)",
                    linecolor="#171717",
                    tickfont=dict(
                        color="#171717",
                        size=12
                    )
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="center",
                x=0.5,
                font=dict(color="#171717")
            ),
            margin=dict(l=80, r=80, t=110, b=60)
        )

        st.plotly_chart(fig, width="stretch")

        
# ============================================================
# TRIVIA
# ============================================================

def curiosity_cards():
    st.markdown('<div class="section-kicker">Lo sapevi che?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Olympic Trivia from the Archive</div>', unsafe_allow_html=True)

    questions = [
        {
            "q": "In which city were the first modern Olympic Games held in 1896?",
            "options": ["Paris", "London", "Rome", "Athens"],
            "answer": "Athens"
        },
        {
            "q": "Which nation has won the most gold medals in Summer Olympic history (1896-2016)?",
            "options": ["Soviet Union", "China", "United States", "Great Britain"],
            "answer": "United States"
        },
        {
            "q": "Who is the athlete that won 8 gold medals in a single edition (Beijing 2008)?",
            "options": ["Usain Bolt", "Mark Spitz", "Carl Lewis", "Michael Phelps"],
            "answer": "Michael Phelps"
        },
        {
            "q": "In what year were the Berlin Olympics, famous for Jesse Owens' victories, held?",
            "options": ["1928", "1932", "1936", "1948"],
            "answer": "1936"
        },
        {
            "q": "Which of these sports returned to the Olympics in 2016 after over 100 years of absence?",
            "options": ["Baseball", "Golf", "Karate", "Softball"],
            "answer": "Golf"
        },
        {
            "q": "Which gymnast scored the first historical 'perfect 10' at Montreal 1976?",
            "options": ["Olga Korbut", "Mary Lou Retton", "Larisa Latynina", "Nadia Comăneci"],
            "answer": "Nadia Comăneci"
        },
        {
            "q": "How many Olympic rings are there and what do they primarily represent?",
            "options": ["6 - The founding nations", "5 - The continents", "4 - The elements", "5 - The oceans"],
            "answer": "5 - The continents"
        },
        {
            "q": "Who is nicknamed 'The fastest man alive', dominating the 100m and 200m from 2008 to 2016?",
            "options": ["Tyson Gay", "Justin Gatlin", "Usain Bolt", "Asafa Powell"],
            "answer": "Usain Bolt"
        },
        {
            "q": "At what age did diver Marjorie Gestring become the youngest individual Olympic champion in 1936?",
            "options": ["11 years", "13 years", "15 years", "17 years"],
            "answer": "13 years"
        },
        {
            "q": "Which city was the first in history to host the Summer Olympics three times (1908, 1948, 2012)?",
            "options": ["Paris", "Los Angeles", "Athens", "London"],
            "answer": "London"
        },
        {
            "q": "In 1900, the Paris Olympics were held alongside what other major event?",
            "options": ["The World's Fair", "The World Cup", "The Diamond Jubilee", "The King's Coronation"],
            "answer": "The World's Fair"
        },
        {
            "q": "In which edition did the major US-led boycott occur?",
            "options": ["Montreal 1976", "Los Angeles 1984", "Seoul 1988", "Moscow 1980"],
            "answer": "Moscow 1980"
        },
        {
            "q": "What is the only nation to have won at least one gold medal in every Summer edition from 1896 to 2016?",
            "options": ["United States", "France", "Great Britain", "Greece"],
            "answer": "Great Britain"
        },
        {
            "q": "Which swimming stroke was the last to be introduced to the men's Olympic program (1956)?",
            "options": ["Backstroke", "Breaststroke", "Freestyle", "Butterfly"],
            "answer": "Butterfly"
        },
        {
            "q": "At Mexico City 1968, which athlete revolutionized the high jump by inventing a new technique?",
            "options": ["Valeriy Brumel", "Dick Fosbury", "Javier Sotomayor", "Patrik Sjöberg"],
            "answer": "Dick Fosbury"
        }
    ]

    # Inizializzazione delle variabili di stato per il quiz
    if "trivia_q_idx" not in st.session_state:
        st.session_state.trivia_q_idx = 0
    if "trivia_score" not in st.session_state:
        st.session_state.trivia_score = 0
    if "trivia_answered" not in st.session_state:
        st.session_state.trivia_answered = False
    if "trivia_selected" not in st.session_state:
        st.session_state.trivia_selected = None

    idx = st.session_state.trivia_q_idx

    col_title, col_reset = st.columns([4, 1])
    with col_reset:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Restart Quiz", use_container_width=True):
            st.session_state.trivia_q_idx = 0
            st.session_state.trivia_score = 0
            st.session_state.trivia_answered = False
            st.session_state.trivia_selected = None
            st.rerun()

    # Se il quiz è terminato
    if idx >= len(questions):
        st.success(f"🎉 Quiz Completed! You got {st.session_state.trivia_score} correct answers over {len(questions)}.")
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.trivia_q_idx = 0
            st.session_state.trivia_score = 0
            st.session_state.trivia_answered = False
            st.session_state.trivia_selected = None
            st.rerun()
        return

    q_data = questions[idx]

    # Grafica della carta della domanda
    st.markdown(
        f"""
        <div class="trivia-card" style="margin-bottom: 20px; padding: 20px; text-align: center;">
            <div class="trivia-head" style="justify-content: center; margin-bottom: 15px;">
                <span class="stamp">Question {idx + 1} of {len(questions)}</span>
            </div>
            <h3 style="color: var(--ink); font-family: 'Playfair Display', serif;">{html.escape(q_data["q"])}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Callback eseguita quando l'utente clicca una risposta
    def check_answer(selected_option):
        st.session_state.trivia_selected = selected_option
        st.session_state.trivia_answered = True
        if selected_option == q_data["answer"]:
            st.session_state.trivia_score += 1

    disabled = st.session_state.trivia_answered

    # Creazione della griglia 2x2 per i bottoni
    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    for i, option in enumerate(q_data["options"]):
        btn_label = option
        # Modifica l'estetica del bottone se l'utente ha già risposto
        if st.session_state.trivia_answered:
            if option == q_data["answer"]:
                btn_label = f"✅ {option}"
            elif option == st.session_state.trivia_selected:
                btn_label = f"❌ {option}"
        
        cols[i].button(
            btn_label, 
            key=f"btn_{idx}_{i}", 
            on_click=check_answer, 
            args=(option,),
            disabled=disabled,
            use_container_width=True
        )

    # Feedback dopo aver risposto
    if st.session_state.trivia_answered:
        st.markdown("<hr style='margin: 20px 0; border-color: var(--muted); opacity: 0.3;'>", unsafe_allow_html=True)
        if st.session_state.trivia_selected == q_data["answer"]:
            st.success("✨ Correct Answer!")
        else:
            st.error(f"❌ Uncorrect Answer! The Correct Answer was: **{q_data['answer']}**")
            
        if st.button("Next Question ➡️", type="primary", use_container_width=True):
            st.session_state.trivia_q_idx += 1
            st.session_state.trivia_answered = False
            st.session_state.trivia_selected = None
            st.rerun()

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
    
    back_col1, back_col2, back_col3 = st.columns([1.5, 1, 1.3])
    with back_col2:
        if st.button("← Back to Olympic Archive", width="stretch"):
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
    
    city_to_country_code = {
        "Athina": "gr", "Athens": "gr", "Paris": "fr", "St. Louis": "us",
        "London": "gb", "Stockholm": "se", "Antwerpen": "be", "Antwerp": "be",
        "Amsterdam": "nl", "Los Angeles": "us", "Berlin": "de", "Helsinki": "fi",
        "Melbourne": "au", "Roma": "it", "Rome": "it", "Tokyo": "jp",
        "Mexico City": "mx", "Munich": "de", "Montreal": "ca",
        "Moskva": "su", "Moscow": "su", 
        "Seoul": "kr", "Barcelona": "es", "Atlanta": "us", 
        "Sydney": "au", "Beijing": "cn", "Rio de Janeiro": "br"
    }

    host_df = (
        df[["Year", "City"]]
        .drop_duplicates()
        .sort_values("Year")
        .reset_index(drop=True)
    )
    
    map_agg_df = (
        df.groupby("City")
        .agg(
            Edizioni=("Year", lambda x: ", ".join(map(str, sorted(x.unique())))),
            Totale_Atleti=("ID", "nunique")
        )
        .reset_index()
    )
    
    map_agg_df["Latitude"] = map_agg_df["City"].map(
        lambda c: city_coordinates.get(c, (None, None))[0]
    )
    map_agg_df["Longitude"] = map_agg_df["City"].map(
        lambda c: city_coordinates.get(c, (None, None))[1]
    )
    host_map_df = map_agg_df.dropna(subset=["Latitude", "Longitude"])
    
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Map of Summer Olympic Host Cities</div>', unsafe_allow_html=True)
    
    fig_map = px.scatter_geo(
        host_map_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        custom_data=["Edizioni", "Totale_Atleti"],
        projection="natural earth",
    )
    fig_map.update_traces(
        marker=dict(
            size=13,
            color="#b88a2e",
            line=dict(width=1.5, color="#171717")
        ),
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "Editions: %{customdata[0]}<br>"
            "Total Athletes: %{customdata[1]}"
            "<extra></extra>"
        )
    )
    fig_map.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#f4efe3",
        plot_bgcolor="#f4efe3",
        hoverlabel=dict(
            bgcolor="#f4efe3",
            bordercolor="#171717",
            font=dict(
                family="Roboto Mono",
                size=13,
                color="#171717"
            )
         ),
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
    st.plotly_chart(fig_map, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Register of Host Cities</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    host_columns = [col1, col2, col3]
    
    for index, row in host_df[["Year", "City"]].iterrows():
        city = row["City"]
        country_code = city_to_country_code.get(city, "")
        
        # Generazione dell'HTML della bandiera (margine destro aggiunto per separarla dal nome)
        if city in ["Moskva", "Moscow"]:
            flag_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/120px-Flag_of_the_Soviet_Union.svg.png"
            flag_html = f'<img src="{flag_url}" height="14" style="vertical-align: middle; border-radius: 2px; margin-right: 6px;">'
        elif country_code:
            flag_html = f'<img src="https://flagcdn.com/h20/{country_code}.png" height="14" style="vertical-align: middle; border-radius: 2px; margin-right: 6px;">'
        else:
            flag_html = '<span style="color: #b88a2e; margin-right: 6px; font-style: normal;">✣</span>'
            
        selected_col = host_columns[index % 3]
        with selected_col:
            st.markdown(
                f"""
                <div class="host-row">
                    <span class="host-year">{int(row["Year"])}</span>
                    <span class="host-city">{flag_html}{html.escape(str(city))}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CURIOSITIES PAGE
# ============================================================

def show_curiosities_page(df):
    st.markdown('<div class="cartography-title">Olympic Curiosities</div>', unsafe_allow_html=True)
    st.markdown('<div class="cartography-subtitle">◆ Opening Ceremony · 1896 vs 2016 ◆</div>', unsafe_allow_html=True)

    back_col1, back_col2, back_col3 = st.columns([1.5, 1, 1.3])

    with back_col2:
        if st.button("← Back to Olympic Archive", key="back_to_main_from_curiosities", width="stretch"):
            st.session_state.page = "main"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    opening_ceremony_comparison()
    st.markdown("<br><br>", unsafe_allow_html=True)

    olympic_evolution_chart(df)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="medal-detail-card">
            <div class="medal-detail-title"> 🌍  The Incredible Anomaly of Melbourne-Stockholm 1956</div>
            <div class="medal-detail-text">
                Did you know that the 1956 edition was the only one in the history of the Summer Olympics to take place across two different nations and continents? <br><br>
                The official host city was Melbourne, Australia. However, the Australian government enforced a strict six-month quarantine law for all incoming animals, including horses. This made it absolutely impossible for international athletes to transport and compete with their own horses.<br><br>
                To avoid canceling the discipline, the IOC made an unprecedented decision: the <b>Equestrian</b> events were separated from the rest of the Games and moved to June in <b>Stockholm, Sweden</b> (reusing the 1912 Olympic Stadium). All other competitions took place regularly in Melbourne five months later, between November and December!
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# MAIN
# ============================================================

def main():
    if "active_block" not in st.session_state:
        st.session_state.active_block = None

    if "era" not in st.session_state:
        st.session_state.era = "1977-2016"

    if "page" not in st.session_state:
        st.session_state.page = "main"

    if "selected_medal_wall_noc" not in st.session_state:
        st.session_state.selected_medal_wall_noc = None

    default_path = Path("olympic_clean_summer.xlsx")

    with st.sidebar:
        # ---- Menu ----
        st.markdown("<h2 style='text-align: center; color: #b88a2e;'>🧭 Menu</h2>", unsafe_allow_html=True)
        
        if st.button("🏛️ The Olympic Archive (Home)", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

        if st.button("📅 Year-by-Year Explorer", use_container_width=True):
            st.session_state.page = "year_explorer"
            st.rerun()
            
        if st.button("🌍 Cartography of Host Cities", use_container_width=True):
            st.session_state.page = "hosts"
            st.rerun()
            
        if st.button("✨ Olympic Curiosities", use_container_width=True):
            st.session_state.page = "curiosities"
            st.rerun()
            
        st.markdown("---") 
        
    if default_path.exists():
        df, df_medals = load_excel_from_path(default_path)
    else:
        st.error("Default dataset not found! Please check your file path.")
        st.stop()


    masthead()

    if st.session_state.page == "hosts":
        show_host_city_cartography(df)
        footer()
        return

    if st.session_state.page == "curiosities":
        show_curiosities_page(df)
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
        c1, c2, c3 = st.columns([0.5, 4, 0.5])

        with c2:
            if st.button(
                "✦ Click to Explore a Single Olympic Year ✦",
                key="open_year_explorer",
                width="stretch",
                type="primary"
            ):
                st.session_state.page = "year_explorer"
                st.session_state.selected_medal_wall_noc = None
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
                "Search through indexed champions and read their full medal records.",
                "◎"
            )

        with row1_col2:
            dispatch_card(
                "race",
                "Compare",
                "The Great Race · Athletes",
                "Phelps vs Spitz and beyond: compare two athletes along a cumulative timeline.",
                "▶"
            )

        with row2_col1:
            dispatch_card(
                "duel",
                "Duel",
                "The Great Duel · Nations",
                "Two nations, one timeline. Compare the cumulative medal tables.",
                "⚔"
            )

        with row2_col2:
            dispatch_card(
                "trivia",
                "Trivia",
                "Olympic Trivia from the Archive",
                "Themed trivia: try to guess and then reveal the answer.",
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

        olympic_rings(df_era, era)

        c1, c2, c3 = st.columns([1, 2.2, 1])

        with c2:
            if st.button(
                "🌍 View the Cartography of Host Cities 🧭",
                key="open_hosts",
                width="stretch"
            ):
                st.session_state.page = "hosts"
                st.rerun()

        c1, c2, c3 = st.columns([1, 2.2, 1])

        with c2:
            if st.button(
                "💡 Explore Olympic Curiosities 🔍",
                key="open_curiosities_era",
                width="stretch"
            ):
                st.session_state.page = "curiosities"
                st.rerun()

    footer()

if __name__ == "__main__":
    main()
