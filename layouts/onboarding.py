# -*- coding: utf-8 -*-
"""
layouts/onboarding.py - Wizard 5 pasos. Athletica Pro.
VERSION: CORREDORES-V4
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import HIGHLIGHT_COLOR

LIME = "#E8FF47"
CYAN = "#00D4FF"
BG   = "#0a0a0a"

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def _label(text, required=False):
    return html.Div(
        style={"marginBottom": "8px", "display": "flex", "alignItems": "center", "gap": "6px"},
        children=[
            html.Span(text, style={"color": "#aaa", "fontSize": "0.88rem", "fontWeight": "600", "letterSpacing": "0.3px"}),
            html.Span("*", style={"color": LIME, "fontSize": "0.88rem"}) if required else None,
        ]
    )

def _hint(text):
    return html.Span(text, style={"color": "#444", "fontSize": "0.8rem", "marginTop": "5px", "display": "block"})

def _input(id_, type_="text", placeholder="", min_=None, max_=None, step=None, value=None):
    props = {
        "id": id_,
        "type": type_,
        "placeholder": placeholder,
        "style": {
            "width": "100%", "padding": "13px 16px",
            "backgroundColor": "#161616", "border": "1px solid #222",
            "borderRadius": "10px", "color": "white", "fontSize": "0.95rem",
            "boxSizing": "border-box", "outline": "none", "fontFamily": "inherit",
        }
    }
    if min_ is not None: props["min"] = min_
    if max_ is not None: props["max"] = max_
    if step is not None: props["step"] = step
    if value is not None: props["value"] = value
    return dcc.Input(**props)

def _field(label_text, input_component, required=False, hint=None):
    children = [_label(label_text, required), input_component]
    if hint:
        children.append(_hint(hint))
    return html.Div(style={"marginBottom": "22px"}, children=children)

def _section_title(icon, text):
    return html.Div(
        style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "24px"},
        children=[
            html.Div(
                style={
                    "width": "36px", "height": "36px", "borderRadius": "10px",
                    "backgroundColor": "rgba(232,255,71,0.1)", "border": "1px solid rgba(232,255,71,0.2)",
                    "display": "flex", "alignItems": "center", "justifyContent": "center",
                },
                children=[html.I(className="bi " + icon, style={"color": LIME, "fontSize": "1rem"})]
            ),
            html.Span(text, style={"color": "white", "fontWeight": "700", "fontSize": "1.1rem"}),
        ]
    )

def _info_box(icon, title, text):
    return html.Div(
        style={
            "padding": "14px 16px", "backgroundColor": "rgba(0,212,255,0.05)",
            "borderRadius": "10px", "border": "1px solid rgba(0,212,255,0.15)",
            "marginBottom": "20px",
        },
        children=[
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "8px", "marginBottom": "6px"},
                children=[
                    html.I(className="bi " + icon, style={"color": CYAN, "fontSize": "1rem"}),
                    html.Span(title, style={"color": CYAN, "fontWeight": "700", "fontSize": "0.9rem"}),
                ]
            ),
            html.P(text, style={"color": "#555", "fontSize": "0.82rem", "margin": "0", "lineHeight": "1.6"}),
        ]
    )

def _pill_btn(btn_id, label, active=False):
    """Boton pill con estado visual. El callback en onboarding_cb actualiza el Store
    y devuelve el paso re-renderizado para reflejar el nuevo estado activo."""
    return html.Button(
        children=label,
        id=btn_id,
        n_clicks=0,
        style={
            "padding": "9px 18px",
            "borderRadius": "50px",
            "border": "1px solid " + (LIME if active else "#2a2a2a"),
            "backgroundColor": "rgba(232,255,71,0.1)" if active else "#111",
            "color": LIME if active else "#888",
            "cursor": "pointer",
            "fontSize": "0.85rem",
            "fontWeight": "600" if active else "400",
            "transition": "all 0.18s",
            "marginBottom": "6px",
        }
    )


# ─────────────────────────────────────────────────────────────
# PASO 1 — Perfil personal + tipo de deportista
# ─────────────────────────────────────────────────────────────
def onboarding_step_1():
    return html.Div(style={"padding": "8px 4px"}, children=[
        _section_title("bi-person-badge", "Tu perfil personal"),

        dbc.Row([
            dbc.Col(
                _field("Nombre completo", _input("input-full-name", placeholder="Ej: Ana Garcia"), required=True),
                md=7
            ),
            dbc.Col(
                _field(
                    "Fecha de nacimiento",
                    _input("input-birthdate", type_="text", placeholder="DD/MM/AAAA"),
                    required=True,
                    hint="Usada para calcular tu FC maxima estimada"
                ),
                md=5
            ),
        ]),

        dbc.Row([
            dbc.Col(_field("Altura (cm)", _input("input-height", type_="number", placeholder="170", min_=140, max_=220)), md=4),
            dbc.Col(_field("Peso (kg)",   _input("input-weight", type_="number", placeholder="65",  min_=40,  max_=150)), md=4),
            dbc.Col(_field("Ciudad",      _input("input-location", placeholder="Madrid")), md=4),
        ]),

        _label("Genero"),
        html.Div(
            id="gender-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("gender-btn-M",  "Hombre",            active=True),
                _pill_btn("gender-btn-F",  "Mujer",             active=False),
                _pill_btn("gender-btn-NB", "No binario",        active=False),
                _pill_btn("gender-btn-X",  "Prefiero no decir", active=False),
            ]
        ),
        dcc.Store(id="input-gender", data="M"),

        html.Hr(style={"borderColor": "#1a1a1a", "margin": "20px 0"}),

        _label("Que tipo de deportista eres?", required=True),
        _hint("Define que modulos activaremos para ti"),
        html.Div(style={"height": "10px"}),
        html.Div(
            id="sport-type-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("sport-type-btn-RUNNER",    "Solo running",            active=True),
                _pill_btn("sport-type-btn-TRIATHLON", "Triatlon (swim+bike+run)", active=False),
                _pill_btn("sport-type-btn-TRAIL",     "Trail / Montanya",        active=False),
                _pill_btn("sport-type-btn-BIKE_RUN",  "Ciclismo + running",      active=False),
                _pill_btn("sport-type-btn-MULTI",     "Multideporte",            active=False),
            ]
        ),
        dcc.Store(id="input-sport-type", data="RUNNER"),
        html.Div(id="sport-type-note", style={"marginTop": "4px"}),
    ])


# ─────────────────────────────────────────────────────────────
# PASO 2 — Experiencia y objetivos
# ─────────────────────────────────────────────────────────────
def onboarding_step_2():
    return html.Div(style={"padding": "8px 4px"}, children=[
        _section_title("bi-trophy", "Experiencia y objetivos"),

        _label("Anos corriendo"),
        html.Div(
            id="exp-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("exp-btn-0",   "Empiezo ahora",  active=False),
                _pill_btn("exp-btn-1",   "Menos de 1 ano", active=True),
                _pill_btn("exp-btn-3",   "1 a 3 anos",     active=False),
                _pill_btn("exp-btn-5",   "3 a 5 anos",     active=False),
                _pill_btn("exp-btn-10",  "5 a 10 anos",    active=False),
                _pill_btn("exp-btn-10p", "Mas de 10",      active=False),
            ]
        ),
        dcc.Store(id="input-experience", data="1"),
        html.Div(style={"height": "16px"}),

        _field(
            "Objetivo principal",
            dcc.Dropdown(
                id="input-main-goal",
                clearable=False,
                options=[
                    {"label": "Terminar mi primera carrera (5K/10K)", "value": "FIRST_RACE"},
                    {"label": "Bajar tiempo en una distancia",        "value": "IMPROVE_TIME"},
                    {"label": "Completar media maraton (21K)",        "value": "HALF_MARATHON"},
                    {"label": "Completar maraton (42K)",              "value": "MARATHON"},
                    {"label": "Completar ultrafondo (50K+)",          "value": "ULTRA"},
                    {"label": "Correr trail / montana",               "value": "TRAIL"},
                    {"label": "Completar un triatlon",                "value": "TRIATHLON_GOAL"},
                    {"label": "Mejorar salud cardiovascular",         "value": "WELLNESS"},
                    {"label": "Perder peso corriendo",                "value": "WEIGHT_LOSS"},
                    {"label": "Mantener forma fisica",                "value": "MAINTAIN"},
                ],
                value="IMPROVE_TIME",
                style={"backgroundColor": "#161616", "color": "#ccc", "border": "1px solid #222", "borderRadius": "10px"},
            ),
            required=True,
        ),

        dbc.Row([
            dbc.Col(
                _field(
                    "Distancia objetivo (km)",
                    _input("input-target-distance", type_="number", placeholder="42.2", min_=1, max_=250, step=0.1),
                    hint="Tu proxima carrera o meta"
                ),
                md=6
            ),
            dbc.Col(
                _field(
                    "Ritmo objetivo (min/km)",
                    _input("input-target-pace", type_="text", placeholder="Ej: 5:30"),
                    hint="Formato MM:SS"
                ),
                md=6
            ),
        ]),

        dbc.Row([
            dbc.Col(
                _field(
                    "Fecha de la carrera objetivo",
                    _input("input-race-date", type_="text", placeholder="DD/MM/AAAA"),
                    hint="Para calcular semanas disponibles"
                ),
                md=6
            ),
            dbc.Col(
                _field(
                    "Nombre de la carrera",
                    _input("input-race-name", type_="text", placeholder="Ej: Maraton de Madrid"),
                    hint="Opcional"
                ),
                md=6
            ),
        ]),

        _field(
            "Volumen semanal actual (km/semana)",
            dcc.Slider(
                id="input-activity-level",
                min=0, max=120, step=5, value=25,
                marks={0: "0", 20: "20", 40: "40", 60: "60", 80: "80", 100: "100", 120: "120+"},
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            hint="Media de los ultimos 3 meses",
        ),
        html.Div(id="activity-level-indicator", style={"textAlign": "center", "marginTop": "-8px", "marginBottom": "20px"}),

        _label("Dias disponibles para entrenar / semana"),
        html.Div(
            id="tdays-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("tdays-btn-1", "1", active=False),
                _pill_btn("tdays-btn-2", "2", active=False),
                _pill_btn("tdays-btn-3", "3", active=False),
                _pill_btn("tdays-btn-4", "4", active=True),
                _pill_btn("tdays-btn-5", "5", active=False),
                _pill_btn("tdays-btn-6", "6", active=False),
                _pill_btn("tdays-btn-7", "7", active=False),
            ]
        ),
        dcc.Store(id="input-training-days", data=4),
    ])


# ─────────────────────────────────────────────────────────────
# PASO 3 — Rendimiento con calculadora automatica
# ─────────────────────────────────────────────────────────────
def onboarding_step_3():
    return html.Div(style={"padding": "8px 4px"}, children=[
        _section_title("bi-activity", "Parametros de rendimiento"),

        _info_box(
            "bi-calculator",
            "Calculo automatico disponible",
            "Si no conoces tu FC maxima o VO2max exactos, deja esos campos vacios y pulsa "
            "Calcular estimacion. Usamos la formula de Tanaka (208 - 0.7 x edad) para FC max "
            "y la ecuacion de Cooper para VO2max estimado a partir de tu ritmo de 5K."
        ),

        dbc.Row([
            dbc.Col(
                _field(
                    "FC maxima (lpm)",
                    _input("input-max-hr", type_="number", placeholder="Vacio = calculo auto", min_=120, max_=220),
                    hint="Deja vacio para estimacion automatica"
                ),
                md=4
            ),
            dbc.Col(
                _field(
                    "FC en reposo (lpm)",
                    _input("input-resting-hr", type_="number", placeholder="55", min_=35, max_=100),
                    hint="Al despertar, antes de levantarte"
                ),
                md=4
            ),
            dbc.Col(
                _field(
                    "VO2max (ml/kg/min)",
                    _input("input-vo2max", type_="number", placeholder="Vacio = calculo auto", min_=20, max_=90),
                    hint="Deja vacio para estimar por ritmo de 5K"
                ),
                md=4
            ),
        ]),

        html.Button(
            children=[html.I(className="bi bi-magic me-2"), "Calcular estimacion automatica"],
            id="btn-calc-hr",
            n_clicks=0,
            style={
                "padding": "10px 22px", "borderRadius": "10px",
                "border": "1px solid rgba(0,212,255,0.35)",
                "backgroundColor": "rgba(0,212,255,0.07)",
                "color": CYAN, "cursor": "pointer", "fontSize": "0.88rem",
                "fontWeight": "600", "marginBottom": "20px", "transition": "all 0.2s",
            }
        ),
        html.Div(id="calc-hr-result", style={"marginBottom": "16px"}),

        _field(
            "Mejores marcas personales",
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"},
                children=[
                    html.Div(children=[
                        html.Span("5K",  style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                        _input("input-pr-5k", placeholder="22:30"),
                    ]),
                    html.Div(children=[
                        html.Span("10K", style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                        _input("input-pr-10k", placeholder="48:00"),
                    ]),
                    html.Div(children=[
                        html.Span("21K", style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                        _input("input-pr-half", placeholder="1:48:00"),
                    ]),
                    html.Div(children=[
                        html.Span("42K", style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                        _input("input-pr-marathon", placeholder="3:55:00"),
                    ]),
                ]
            ),
            hint="Opcional - usadas para predecir ritmos en otras distancias",
        ),

        _label("Tipo de entrenamiento preferido"),
        html.Div(
            id="traintype-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("traintype-btn-Z2",        "Zona 2 / Aerobico",   active=False),
                _pill_btn("traintype-btn-INTERVALS",  "Intervalos / Series", active=False),
                _pill_btn("traintype-btn-TEMPO",      "Tempo / Umbral",      active=False),
                _pill_btn("traintype-btn-TRAIL",      "Trail / Montana",     active=False),
                _pill_btn("traintype-btn-MIXED",      "Mixto",               active=True),
            ]
        ),
        dcc.Store(id="input-train-type", data="MIXED"),
    ])


# ─────────────────────────────────────────────────────────────
# PASO 4 — Salud, lesiones y equipamiento
# ─────────────────────────────────────────────────────────────
def onboarding_step_4():
    return html.Div(style={"padding": "8px 4px"}, children=[
        _section_title("bi-heart-pulse", "Salud y equipamiento"),

        _label("Condiciones de salud relevantes"),
        dbc.Checklist(
            id="input-health-conditions",
            options=[
                {"label": "Diabetes",            "value": "Diabetes"},
                {"label": "Hipertension",         "value": "Hipertension"},
                {"label": "Asma",                "value": "Asma"},
                {"label": "Problemas cardiacos",  "value": "Cardiaco"},
                {"label": "Artritis / artrosis", "value": "Artritis"},
                {"label": "Anemia",              "value": "Anemia"},
                {"label": "Ninguna",             "value": "Ninguna"},
            ],
            value=["Ninguna"],
            inline=True,
            className="mb-4",
            inputStyle={"marginRight": "6px"},
            labelStyle={"color": "#aaa", "marginRight": "18px", "marginBottom": "10px", "fontSize": "0.9rem", "cursor": "pointer"},
        ),

        _label("Lesion actual o reciente"),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px", "marginBottom": "22px"},
            children=[
                html.Div(children=[
                    html.Span("Zona afectada", style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="input-injury-location",
                        options=[
                            {"label": "Sin lesion activa",     "value": "Ninguna"},
                            {"label": "Rodilla",               "value": "Rodilla"},
                            {"label": "Tobillo / pie",         "value": "Tobillo"},
                            {"label": "Cadera / gluteo",       "value": "Cadera"},
                            {"label": "Pantorrilla / gemelo",  "value": "Pantorrilla"},
                            {"label": "Fascia plantar",        "value": "Fascia"},
                            {"label": "Tendon de Aquiles",     "value": "Aquiles"},
                            {"label": "Espalda baja / lumbar", "value": "Lumbar"},
                            {"label": "IT Band (rodilla)",     "value": "ITBand"},
                            {"label": "Periostitis tibial",    "value": "Periostitis"},
                            {"label": "Otra",                  "value": "Otra"},
                        ],
                        value="Ninguna", clearable=False,
                        style={"backgroundColor": "#161616", "border": "1px solid #222", "borderRadius": "10px"},
                    ),
                ]),
                html.Div(children=[
                    html.Span("Severidad", style={"color": "#555", "fontSize": "0.8rem", "display": "block", "marginBottom": "6px"}),
                    dcc.Dropdown(
                        id="input-injury-severity",
                        options=[
                            {"label": "Sin lesion",              "value": "Ninguna"},
                            {"label": "Leve - entreno normal",   "value": "Leve"},
                            {"label": "Moderada - me limita",    "value": "Moderada"},
                            {"label": "Alta - sin poder correr", "value": "Alta"},
                        ],
                        value="Ninguna", clearable=False,
                        style={"backgroundColor": "#161616", "border": "1px solid #222", "borderRadius": "10px"},
                    ),
                ]),
            ]
        ),

        _field(
            "Suplementacion / medicacion (opcional)",
            _input("input-medication", placeholder="Ej: Hierro, magnesio, vitamina D..."),
            hint="Ayuda a personalizar recomendaciones nutricionales",
        ),

        _label("Dispositivo GPS / reloj deportivo"),
        html.Div(
            id="device-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("device-btn-garmin", "Garmin",      active=False),
                _pill_btn("device-btn-polar",  "Polar",       active=False),
                _pill_btn("device-btn-coros",  "COROS",       active=False),
                _pill_btn("device-btn-apple",  "Apple Watch", active=False),
                _pill_btn("device-btn-suunto", "Suunto",      active=False),
                _pill_btn("device-btn-other",  "Otro",        active=False),
                _pill_btn("device-btn-none",   "Sin reloj",   active=True),
            ]
        ),
        dcc.Store(id="input-device", data="none"),
        html.Div(style={"height": "16px"}),

        _label("Superficie habitual de entrenamiento"),
        html.Div(
            id="surface-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("surface-btn-road",      "Asfalto",         active=True),
                _pill_btn("surface-btn-track",     "Pista atletismo", active=False),
                _pill_btn("surface-btn-trail",     "Trail / tierra",  active=False),
                _pill_btn("surface-btn-treadmill", "Cinta",           active=False),
                _pill_btn("surface-btn-mixed",     "Mixto",           active=False),
            ]
        ),
        dcc.Store(id="input-surface", data="road"),
        html.Div(style={"height": "16px"}),

        _field(
            "Zapatillas actuales (opcional)",
            _input("input-shoes", placeholder="Ej: Nike Vaporfly, Hoka Clifton..."),
            hint="Relevante para prevencion de lesiones",
        ),
    ])


# ─────────────────────────────────────────────────────────────
# PASO 5 — Sueno, nutricion y estilo de vida
# ─────────────────────────────────────────────────────────────
def onboarding_step_5():
    return html.Div(style={"padding": "8px 4px"}, children=[
        _section_title("bi-moon-stars", "Sueno, nutricion y estilo de vida"),

        dbc.Row([
            dbc.Col(
                _field(
                    "Horas de sueno por noche",
                    dcc.Slider(
                        id="input-sleep-hours",
                        min=4, max=10, step=0.5, value=7.5,
                        marks={4: "4h", 5: "5h", 6: "6h", 7: "7h", 8: "8h", 9: "9h", 10: "10h"},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    hint="La recuperacion empieza por el sueno",
                ),
                md=12
            ),
        ]),

        _label("Calidad de sueno habitual"),
        html.Div(
            id="sleepq-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("sleepq-btn-excellent", "Muy buena",       active=False),
                _pill_btn("sleepq-btn-good",      "Buena",           active=True),
                _pill_btn("sleepq-btn-fair",      "Regular",         active=False),
                _pill_btn("sleepq-btn-poor",      "Mala / insomnio", active=False),
            ]
        ),
        dcc.Store(id="input-sleep-quality", data="good"),
        html.Div(style={"height": "16px"}),

        _label("Estrategia nutricional"),
        html.Div(
            id="diet-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("diet-btn-NONE",        "Sin restricciones",  active=True),
                _pill_btn("diet-btn-HIGH_CARB",   "Alto en carbos",     active=False),
                _pill_btn("diet-btn-LOW_CARB",    "Bajo en carbos",     active=False),
                _pill_btn("diet-btn-KETO",        "Cetogenica",         active=False),
                _pill_btn("diet-btn-VEGGIE",      "Vegetariana",        active=False),
                _pill_btn("diet-btn-VEGAN",       "Vegana",             active=False),
                _pill_btn("diet-btn-GLUTEN_FREE", "Sin gluten",         active=False),
            ]
        ),
        dcc.Store(id="input-diet-restrictions", data=["NONE"]),
        html.Div(style={"height": "16px"}),

        _label("Experiencia con nutricion deportiva"),
        html.Div(
            id="suppexp-btn-group",
            style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "6px"},
            children=[
                _pill_btn("suppexp-btn-none",     "Ninguna - me lo explicas tu",      active=True),
                _pill_btn("suppexp-btn-basic",    "Basica (proteina, hidratos)",       active=False),
                _pill_btn("suppexp-btn-advanced", "Avanzada (geles, electrolitos...)", active=False),
            ]
        ),
        dcc.Store(id="input-supp-exp", data="none"),
        html.Div(style={"height": "16px"}),

        dbc.Row([
            dbc.Col(
                _field(
                    "Peso objetivo (kg) - opcional",
                    _input("input-target-weight", type_="number", placeholder="62", min_=40, max_=150),
                    hint="Solo si el control de peso es un objetivo",
                ),
                md=6
            ),
            dbc.Col(
                _field(
                    "Estilo de vida / trabajo",
                    dcc.Dropdown(
                        id="input-lifestyle",
                        options=[
                            {"label": "Sedentario (oficina / remoto)", "value": "sedentary"},
                            {"label": "Moderado (camino, de pie)",     "value": "moderate"},
                            {"label": "Activo (trabajo fisico)",       "value": "active"},
                        ],
                        value="sedentary",
                        clearable=False,
                        style={"backgroundColor": "#161616", "border": "1px solid #222", "borderRadius": "10px"},
                    ),
                    hint="Afecta al calculo de calorias totales diarias",
                ),
                md=6
            ),
        ]),

        html.Div(
            style={
                "padding": "16px 20px", "backgroundColor": "rgba(232,255,71,0.05)",
                "borderRadius": "12px", "border": "1px solid rgba(232,255,71,0.15)",
                "marginTop": "8px",
            },
            children=[
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        html.I(className="bi bi-check2-circle", style={"color": LIME, "fontSize": "1.2rem"}),
                        html.Span("Perfil completo!", style={"color": LIME, "fontWeight": "700", "fontSize": "1rem"}),
                    ]
                ),
                html.P(
                    "Calibraremos tus zonas Z1-Z5, carga semanal optima, predicciones de ritmo "
                    "por distancia y recomendaciones nutricionales personalizadas.",
                    style={"color": "#555", "fontSize": "0.83rem", "margin": "8px 0 0 0", "lineHeight": "1.6"}
                ),
            ]
        ),
    ])


STEP_BUILDERS = [onboarding_step_1, onboarding_step_2, onboarding_step_3, onboarding_step_4, onboarding_step_5]

# ─────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────────────────────
onboarding_layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": BG,
        "display": "flex",
        "alignItems": "flex-start",
        "justifyContent": "center",
        "padding": "40px 20px",
        "fontFamily": "'Inter', sans-serif",
    },
    children=[
        # Stores persistentes entre pasos (siempre en el DOM)
        dcc.Store(id="store-birthdate", data=None),
        dcc.Store(id="store-weight",    data=None),
        dcc.Store(id="store-pr-5k",     data=None),

        html.Div(
            style={
                "width": "100%", "maxWidth": "860px",
                "backgroundColor": "#0f0f0f",
                "borderRadius": "20px",
                "border": "1px solid #1a1a1a",
                "boxShadow": "0 20px 60px rgba(0,0,0,0.7)",
                "overflow": "hidden",
            },
            children=[
                # Header
                html.Div(
                    style={"padding": "28px 40px 0 40px", "borderBottom": "1px solid #141414"},
                    children=[
                        html.Div(
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px"},
                            children=[
                                html.Div(
                                    style={"display": "flex", "alignItems": "center", "gap": "12px"},
                                    children=[
                                        html.Div("A", style={
                                            "width": "36px", "height": "36px", "backgroundColor": LIME,
                                            "borderRadius": "9px", "display": "flex", "alignItems": "center",
                                            "justifyContent": "center", "fontWeight": "900", "color": "#080808",
                                        }),
                                        html.Span("ATHLETICA", style={"color": "white", "fontWeight": "800", "letterSpacing": "2px", "fontSize": "1rem"}),
                                    ]
                                ),
                                html.Div(id="onboarding-step-counter", style={"color": "#444", "fontSize": "0.85rem"}, children="Paso 1 de 5"),
                            ]
                        ),
                        html.H3(
                            id="onboarding-current-step-title",
                            style={"color": LIME, "fontSize": "1.9rem", "fontWeight": "800", "margin": "0 0 4px 0"},
                            children="Tu perfil"
                        ),
                        html.P(
                            id="onboarding-current-step-subtitle",
                            style={"color": "#555", "fontSize": "0.92rem", "margin": "0 0 16px 0"},
                            children="Cuentanos quien eres, atleta"
                        ),
                        # Barra de progreso — actualizada por onboarding_cb.py
                        html.Div(
                            style={"height": "4px", "backgroundColor": "#1a1a1a", "borderRadius": "4px", "overflow": "hidden"},
                            children=[
                                html.Div(
                                    id="onboarding-progress-bar",
                                    style={
                                        "height": "100%", "width": "20%",
                                        "background": "linear-gradient(90deg, " + LIME + ", " + CYAN + ")",
                                        "transition": "width 0.5s ease", "borderRadius": "4px",
                                    }
                                ),
                            ]
                        ),
                        # Indicador de pasos (barras)
                        html.Div(
                            style={"display": "flex", "gap": "6px", "paddingTop": "12px", "paddingBottom": "18px"},
                            children=[
                                html.Div(style={
                                    "flex": "1", "height": "4px", "borderRadius": "2px",
                                    "backgroundColor": LIME if i == 0 else "#222",
                                    "transition": "background-color 0.3s",
                                }) for i in range(5)
                            ]
                        ),
                    ]
                ),
                # Contenido del paso — pre-poblado con paso 1
                html.Div(id="onboarding-content", style={"padding": "28px 40px 20px 40px"}, children=onboarding_step_1()),
                # Navegacion
                html.Div(
                    style={
                        "padding": "20px 40px 32px 40px",
                        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                        "borderTop": "1px solid #141414",
                    },
                    id="onboarding-nav-container",
                    children=[
                        dbc.Button(
                            [html.I(className="bi bi-arrow-left me-2"), "Anterior"],
                            id="onboarding-prev-btn-visual",
                            style={
                                "backgroundColor": "transparent", "border": "1px solid #2a2a2a",
                                "color": "#555", "borderRadius": "10px", "padding": "11px 24px",
                                "fontWeight": "600", "fontSize": "0.9rem",
                            }
                        ),
                        dbc.Button(
                            ["Siguiente", html.I(className="bi bi-arrow-right ms-2")],
                            id="onboarding-next-btn-visual",
                            style={
                                "backgroundColor": LIME, "border": "none",
                                "color": "#080808", "borderRadius": "10px",
                                "padding": "11px 32px", "fontWeight": "800",
                                "fontSize": "0.95rem",
                            }
                        ),
                    ]
                ),
            ]
        )
    ]
)