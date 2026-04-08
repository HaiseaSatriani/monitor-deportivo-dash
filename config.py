"""
config.py — Constantes globales de Athletica.
"""

HIGHLIGHT_COLOR  = "#00d4ff"
TEAL_COLOR       = "#4ecdc4"
DARK_BACKGROUND  = "#0a0a0a"

SPORTS_OPTIONS = [
    {"label": "Correr",           "icon": "bi bi-person-walking"},
    {"label": "Ciclismo",         "icon": "bi bi-bicycle"},
    {"label": "Natacion",         "icon": "bi bi-water"},
    {"label": "Gym (Pesas)",      "icon": "bi bi-fire"},
    {"label": "CrossFit (HIIT)",  "icon": "bi bi-lightning-fill"},
    {"label": "Yoga / Pilates",   "icon": "bi bi-peace"},
    {"label": "Futbol",           "icon": "bi bi-trophy"},
    {"label": "Baloncesto",       "icon": "bi bi-dribbble"},
    {"label": "Otro / Ninguno",   "icon": "bi bi-question-circle"},
]

HEALTH_CONDITIONS = [
    "Diabetes", "Hipertension", "Asma",
    "Problemas cardiacos", "Artritis", "Ninguna",
]

DIET_RESTRICTIONS = [
    "Vegetariano", "Vegano", "Sin gluten",
    "Sin lactosa", "Alergico a frutos secos", "Ninguna",
]

ONBOARDING_STEPS = [
    {"title": "Bienvenido/a!",        "subtitle": "Cuentanos un poco sobre ti"},
    {"title": "Datos Biometricos",    "subtitle": "Para personalizar tu experiencia"},
    {"title": "Deportes & Actividad", "subtitle": "Que te gusta hacer?"},
    {"title": "Salud & Condiciones",  "subtitle": "Para cuidar tu bienestar"},
    {"title": "Sueno & Nutricion",    "subtitle": "Ultimos detalles"},
]

RPE_COLORS = {
    (1, 3):  "#4ecdc4",
    (4, 6):  "#ffd166",
    (7, 8):  "#ff9a3c",
    (9, 10): "#ff6b6b",
}

def rpe_color(rpe):
    for (lo, hi), color in RPE_COLORS.items():
        if lo <= rpe <= hi:
            return color
    return "#ccc"
