"""
app.py — Punto de entrada de Athletica.
Arquitectura modular: config / db / sensors / layouts / callbacks
"""
# ═══════════════════════════════════════════════════════════
# PANDAS CIRCULAR IMPORT FIX - must run before ANY other import
# ═══════════════════════════════════════════════════════════
import sys as _sys
try:
    if 'pandas' in _sys.modules and not hasattr(_sys.modules['pandas'], 'Series'):
        for _k in list(_sys.modules.keys()):
            if _k == 'pandas' or _k.startswith('pandas.'):
                del _sys.modules[_k]
    import pandas as _pd_check
    _pd_check.Series  # confirm loaded
except Exception:
    import types as _t
    _fpd = _t.ModuleType('pandas')
    _fpd.Series = list; _fpd.Index = list; _fpd.DataFrame = dict
    _sys.modules['pandas'] = _fpd
    try:
        import _plotly_utils.basevalidators as _bv; _bv.pd = _fpd
    except: pass
    try:
        import _plotly_utils.utils as _pu; _pu.pd = _fpd
    except: pass
# ═══════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════
# PATH FIX — garantiza que el directorio raíz esté en sys.path
# ═══════════════════════════════════════════════════════════
import os as _os
_root = _os.path.dirname(_os.path.abspath(__file__))
if _root not in _sys.path:
    _sys.path.insert(0, _root)
# ═══════════════════════════════════════════════════════════

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

from config import HIGHLIGHT_COLOR, DARK_BACKGROUND
from layouts.styles import GLOBAL_CSS

# ─────────────────────────────────────────────────────────────
# INSTANCIA
# ─────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css",
    ],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
app.title = "Athletica — Monitor Deportivo"
server = app.server

# ─────────────────────────────────────────────────────────────
# INDEX STRING
# ─────────────────────────────────────────────────────────────
app.index_string = f"""
<!DOCTYPE html>
<html>
<head>
    {{%metas%}}
    <title>{{%title%}}</title>
    {{%favicon%}}
    {{%css%}}
    <style>{GLOBAL_CSS}</style>
</head>
<body>
    {{%app_entry%}}
    <footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────
# ROOT LAYOUT (stores + router)
# ─────────────────────────────────────────────────────────────
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # Stores globales de sesión
    dcc.Store(id="current-user",         storage_type="session"),
    dcc.Store(id="onboarding-completed", storage_type="session"),
    dcc.Store(id="onboarding-user-name", storage_type="session"),
    dcc.Store(id="user-type-store",      storage_type="session"),
    dcc.Store(id="viewing-patient",      storage_type="session"),

    # Stores de página
    dcc.Store(id="onboarding-step-store", data=0),
    dcc.Store(id="ecg-data-store"),

    html.Div(id="page-content"),

    # ── Ghost components: IDs usados en State/Output de callbacks ─
    html.Div(id="_ghost", style={"display": "none"}, children=[
        # ── Athlete dashboard ──
        dcc.Upload(id="upload-ecg-inicio"),        dcc.Store(id="download-ecg-csv"),
        html.Button(id="btn-open-workout-survey", n_clicks=0),  html.Button(id="btn-open-workout-survey-2", n_clicks=0),
        html.Button(id="btn-cancel-survey", n_clicks=0),        html.Button(id="btn-submit-survey", n_clicks=0),
        html.Button(id="btn-download-ecg", n_clicks=0),
        dcc.Slider(id="survey-rpe", min=1, max=10, value=5),               html.Div(id="survey-rpe-label"),
        html.Div(id="survey-success-msg"),       dcc.Store(id="survey-mood-store"),
        dcc.Dropdown(id="survey-workout-type"),      dcc.Input(id="survey-duration"),
        dcc.Input(id="survey-distance"),          dcc.Input(id="survey-avg-hr"),
        dcc.Input(id="survey-calories"),          dcc.Textarea(id="survey-notes"),
        dcc.Slider(id="survey-energy", min=1, max=10, value=5),            dcc.Slider(id="survey-pain", min=0, max=10, value=0),
        html.Button(id="mood-btn-excelente", n_clicks=0),       html.Button(id="mood-btn-bien", n_clicks=0),
        html.Button(id="mood-btn-regular", n_clicks=0),         html.Button(id="mood-btn-cansado", n_clicks=0),
        html.Button(id="mood-btn-agotado", n_clicks=0),
        html.Button(id="btn-add-meal", n_clicks=0),             dcc.Input(id="input-meal-description"),
        html.Button(id="meal-tab-desayuno", n_clicks=0),        html.Button(id="meal-tab-almuerzo", n_clicks=0),
        html.Button(id="meal-tab-cena", n_clicks=0),            html.Button(id="meal-tab-snacks", n_clicks=0),
        dcc.Store(id="meal-type-store"),          html.Div(id="meal-success-msg"),
        html.Div(id="meals-desayuno"),           html.Div(id="meals-almuerzo"),
        html.Div(id="meals-cena"),               html.Div(id="meals-snacks"),
        html.Button(id="btn-add-water", n_clicks=0),            html.Button(id="btn-add-water-500", n_clicks=0),
        html.Button(id="btn-agregar-objetivo", n_clicks=0),     html.Button(id="btn-cancel-goal", n_clicks=0),
        html.Button(id="btn-submit-goal", n_clicks=0),          html.Button(id="btn-health-goal", n_clicks=0),
        html.Button(id="btn-fitness-goal", n_clicks=0),         html.Button(id="btn-back-to-choose", n_clicks=0),
        html.Button(id="btn-logout", n_clicks=0),               html.Button(id="btn-logout-doctor", n_clicks=0),
        dcc.Input(id="input-goal-name"),          dcc.Textarea(id="input-goal-description"),
        dcc.Input(id="input-goal-target"),        dcc.Dropdown(id="input-goal-deadline"),
        html.Div(id="goal-type-text"),           html.Div(id="goal-type-icon"),
        html.Div(id="goal-success-msg"),         html.Div(id="goal-form-container"),
        html.Div(id="choose-goal-type"),         dbc.Modal(id="modal-add-goal"),
        html.Div(id="goals-display-container"),  html.Div(id="goals-summary-stats"),
        html.Div(id="goals-upcoming-deadlines"), dcc.Store(id="user-goals-store"),
        dbc.Modal(id="modal-workout-survey"),
        dcc.Graph(id="ecg-graph-inicio"),         html.Div(id="ecg-bpm-display"),
        html.Div(id="ecg-status-label"),
        dcc.Graph(id="chart-weekly-load"),        dcc.Graph(id="chart-hr-zones"),
        dcc.Graph(id="chart-rpe-trend"),          dcc.Graph(id="chart-mood-trend"),
        dcc.Graph(id="macro-pie-chart"),
        html.Div(id="sidebar-user-avatar"),      html.Div(id="sidebar-user-fullname"),
        html.Div(id="sidebar-user-level"),       html.Div(id="health-status-dots"),
        html.Div(id="health-status-description"),
        html.Div(id="user-profile-avatar"),      html.Div(id="user-profile-name"),
        html.Div(id="user-profile-type"),        html.Div(id="personal-records-list"),
        html.Div(id="metric-activity"),          html.Div(id="metric-bpm"),
        html.Div(id="metric-bpm-zone"),          html.Div(id="metric-cals"),
        html.Div(id="metric-cals-sub"),          html.Div(id="metric-hydration"),
        html.Div(id="metric-hydration-sub"),     html.Div(id="recent-workouts-list"),
        html.Div(id="workout-history-list"),     html.Div(id="month-stats-panel"),
        html.Div(id="training-tip"),
        html.Div(id="stat-sessions"),            html.Div(id="stat-km"),
        html.Div(id="stat-time"),                html.Div(id="stat-cal-week"),
        html.Div(id="stat-avg-rpe"),
        html.Div(id="acwr-ratio-display"),       html.Div(id="acwr-status-label"),
        html.Div(id="acwr-bar-container"),       # ← AÑADIDO: Output en load_metrics
        html.Div(id="total-calories-display"),   html.Div(id="macro-carbs-val"),
        html.Div(id="macro-protein-val"),        html.Div(id="macro-fat-val"),
        html.Div(id="macro-carbs-bar"),          html.Div(id="macro-protein-bar"),
        html.Div(id="macro-fat-bar"),
        html.Div(id="hydration-liters-text"),    html.Div(id="hydration-goal-text"),
        html.Div(id="hydration-progress-bar"),   html.Div(id="hydration-milestones"),
        html.Div(id="sidebar-sport-badge"),      html.Div(id="sidebar-next-race-label"),
        html.Div(id="sidebar-week-km"),          html.Div(id="sidebar-week-bar"),
        # ── Métricas avanzadas ──
        html.Div(id="adv-kpi-vo2"),              html.Div(id="adv-kpi-hrv"),
        html.Div(id="adv-kpi-pace"),             html.Div(id="adv-kpi-cadence"),
        html.Div(id="adv-kpi-power"),            html.Div(id="adv-kpi-tss"),
        html.Div(id="adv-kpi-efficiency"),       html.Div(id="adv-kpi-fatigue"),
        dcc.Store(id="metrics-active-tab", data="global"),
        html.Button(id="metrics-tab-global",  n_clicks=0),
        html.Button(id="metrics-tab-running", n_clicks=0),
        html.Button(id="metrics-tab-cycling", n_clicks=0),
        html.Button(id="metrics-tab-swimming",n_clicks=0),
        dcc.Graph(id="chart-pace-trend"),        dcc.Graph(id="chart-volume-discipline"),
        dcc.Graph(id="chart-resting-hr"),        dcc.Graph(id="chart-hr-efficiency"),
        dcc.Graph(id="chart-hrv-trend"),
        # Botones descarga gráficas
        html.Button(id="btn-dl-weekly-load", n_clicks=0), html.Button(id="btn-dl-hr-zones",   n_clicks=0),
        html.Button(id="btn-dl-pace",        n_clicks=0), html.Button(id="btn-dl-rpe",        n_clicks=0),
        html.Button(id="btn-dl-mood",        n_clicks=0), html.Button(id="btn-dl-volume",     n_clicks=0),
        html.Button(id="btn-dl-resting-hr",  n_clicks=0), html.Button(id="btn-dl-efficiency", n_clicks=0),
        html.Button(id="btn-dl-hrv",         n_clicks=0),
        dcc.Download(id="dl-weekly-load"),    dcc.Download(id="dl-hr-zones"),
        dcc.Download(id="dl-pace"),           dcc.Download(id="dl-rpe"),
        dcc.Download(id="dl-mood"),           dcc.Download(id="dl-volume"),
        dcc.Download(id="dl-resting-hr"),     dcc.Download(id="dl-efficiency"),
        dcc.Download(id="dl-hrv"),
        # Upload CSV externo
        dcc.Upload(id="upload-metrics-csv"),
        dcc.Store(id="metrics-csv-store"),
        html.Div(id="upload-metrics-status"),
        dcc.Dropdown(id="metrics-csv-column-selector"),
        dcc.Dropdown(id="metrics-csv-chart-type"),
        html.Button(id="btn-dl-custom-csv", n_clicks=0),
        dcc.Download(id="download-custom-csv"),
        dcc.Graph(id="chart-custom-upload"),
        html.Div(id="uploaded-csv-chart-wrap"),
        html.Div(id="uploaded-csv-chart-title"),
        html.Div(id="uploaded-csv-stats"),
        html.Div(id="uploaded-csv-summary-table"),
        # ── Onboarding ──
        html.Div(id="onboarding-content"),
        html.Div(id="onboarding-current-step-title"),
        html.Div(id="onboarding-current-step-subtitle"),
        html.Div(id="onboarding-progress-bar"),
        html.Div(id="onboarding-step-counter"),  # ← AÑADIDO: Output en navigate_step
        html.Button(id="onboarding-next-btn-visual", n_clicks=0),
        html.Button(id="onboarding-prev-btn-visual", n_clicks=0),
        html.Div(id="activity-level-indicator"),
        # ── Auth ──
        html.Div(id="login-message"),            html.Div(id="register-message"),
        dcc.Store(id="accept-terms"),             dcc.Store(id="reg-user-type"),
        html.Button(id="btn-reg-type-athlete", n_clicks=0),     html.Button(id="btn-reg-type-doctor", n_clicks=0),
        html.Button(id="terms-checkbox-visual", n_clicks=0),    html.Div(id="user-type-indicator"),
        # ── Doctor ──
        html.Button(id="doctor-search-btn", n_clicks=0),        dcc.Input(id="doctor-search-input"),
        html.Div(id="doctor-patients-grid"),     html.Div(id="doctor-search-results"),
        html.Div(id="doctor-profile-name"),      html.Div(id="doctor-profile-avatar"),
        html.Div(id="doctor-patient-count"),     html.Div(id="doctor-active-patients-count"),
        html.Div(id="doctor-avg-activity"),      html.Div(id="doctor-risk-patients"),
        dcc.Store(id="doctor-dashboard-refresh-trigger"),
        # ── Inicio seccion nueva ──
        html.Div(id="inicio-greeting"),
        html.Div(id="training-tip-sport-label"),
        html.Div(id="training-tip-entrena"),
        html.Div(id="inicio-week-summary"),
        html.Div(id="inicio-next-workout"),
        dcc.Textarea(id="input-objetivo-dia"),
        html.Button(id="btn-save-objetivo", n_clicks=0),
        html.Div(id="objetivo-saved-msg"),
    ]),

])

# ─────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    [
        State("current-user",         "data"),
        State("onboarding-completed", "data"),
        State("user-type-store",      "data"),
        State("viewing-patient",      "data"),
    ],
)
def render_page(pathname, current_user, onboarding_done, user_type, viewing_patient):
    from layouts.auth       import welcome_layout, login_layout, register_layout
    from layouts.onboarding import onboarding_layout
    from layouts.athlete    import athlete_layout
    from layouts.doctor     import doctor_layout

    # Rutas públicas
    if pathname in (None, "/", ""):
        return welcome_layout
    if pathname == "/login":
        return login_layout
    if pathname == "/register":
        return register_layout

    # Rutas protegidas
    if not current_user:
        return login_layout

    if pathname == "/onboarding":
        return onboarding_layout

    if pathname == "/doctor-dashboard":
        return doctor_layout if user_type == "doctor" else athlete_layout

    if pathname == "/inicio":
        return athlete_layout

    # Fallback
    return welcome_layout


# ─────────────────────────────────────────────────────────────
# REGISTRAR CALLBACKS
# ─────────────────────────────────────────────────────────────
from callbacks.auth_cb       import register as reg_auth
from callbacks.onboarding_cb import register as reg_onboarding
from callbacks.athlete_cb    import register as reg_athlete
from callbacks.doctor_cb     import register as reg_doctor

reg_auth(app)
reg_onboarding(app)
reg_athlete(app)
reg_doctor(app)

# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
