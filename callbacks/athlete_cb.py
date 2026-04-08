"""
callbacks/athlete_cb.py — Callbacks del Dashboard del Atleta — Athletica Pro
"""
import base64
import io
import json
import random
from datetime import datetime, timedelta

import dash
from dash import Input, Output, State, callback_context, html, dcc, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from config import HIGHLIGHT_COLOR, TEAL_COLOR, rpe_color

# ─────────────────────────────────────────────────────────────
# PALETA Y CONSTANTES
# ─────────────────────────────────────────────────────────────
LIME   = "#E8FF47"
CYAN   = "#00F5FF"
ORANGE = "#FFB74D"
RED    = "#EF5350"
GREEN  = "#81C784"
PURPLE = "#9C88FF"
MUTED  = "#6B7280"
WHITE  = "#F9FAFB"
DARK2  = "#141414"
DARK3  = "#1C1C1C"

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9CA3AF", family="'Plus Jakarta Sans', sans-serif", size=11),
    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
               showline=False, tickfont=dict(color="#6B7280"), zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
               showline=False, tickfont=dict(color="#6B7280"), zeroline=False),
)
_MARGIN = dict(l=40, r=20, t=10, b=40)

WORKOUT_ICONS = {
    "carrera_facil": "🏃", "intervalos": "⚡", "tempo": "🎯",
    "trail": "⛰️", "ciclismo": "🚴", "fuerza": "💪", "hiit": "🔥",
    "yoga": "🧘", "natacion": "🏊", "recuperacion": "🔄",
    "cardio": "❤️", "otro": "🏅",
}

TRAINING_TIPS = [
    "La zona 2 mejora tu capacidad aeróbica base. El 80% de tus kilómetros deben ser fáciles.",
    "Duerme 8h antes de una sesión de calidad. El sueño es el mejor suplemento.",
    "El RPE ideal para entrenamientos fáciles es 3-4/10. Si puedes hablar cómodamente, vas bien.",
    "Hidratación: bebe 500ml antes de entrenar y 150ml cada 20min durante la sesión.",
    "La recuperación activa (caminar, yoga suave) acelera la regeneración muscular.",
    "El HRV bajo por la mañana = señal de fatiga acumulada. Considera un día de descanso.",
    "Los intervalos en Z4-Z5 solo deberían representar el 20% de tu volumen semanal.",
    "Come 60-90g de carbohidratos por hora en esfuerzos superiores a 75 minutos.",
    "La cadencia ideal en running oscila entre 170-180 pasos por minuto.",
    "Semanas de descarga cada 3-4 semanas: reduce el volumen al 60% pero mantén la intensidad.",
]


def _empty_fig(msg="Sin datos disponibles"):
    fig = go.Figure()
    fig.add_annotation(text=msg, x=0.5, y=0.5, xref="paper", yref="paper",
                       showarrow=False, font=dict(color="#4B5563", size=13))
    fig.update_layout(**_LAYOUT_BASE, margin=_MARGIN)
    return fig


def _rpe_text(rpe):
    labels = {1:"Recuperación",2:"Muy fácil",3:"Fácil",4:"Moderado fácil",5:"Moderado",
              6:"Moderado intenso",7:"Intenso",8:"Muy intenso",9:"Máximo",10:"Absoluto máximo"}
    return labels.get(int(rpe), "Moderado")


def _zone_label(avg_hr, max_hr=190):
    if max_hr <= 0: max_hr = 190
    pct = avg_hr / max_hr * 100
    if pct < 60:  return "Z1", "#4FC3F7"
    if pct < 70:  return "Z2", GREEN
    if pct < 80:  return "Z3", LIME
    if pct < 90:  return "Z4", ORANGE
    return "Z5", RED


def _pace_str(pace_decimal):
    if not pace_decimal or pace_decimal <= 0:
        return "—"
    mins = int(pace_decimal)
    secs = int((pace_decimal - mins) * 60)
    return f"{mins}:{secs:02d}/km"


def _estimate_vo2max(workouts):
    running = [w for w in workouts if w.get("workout_type") in
               ("carrera_facil","intervalos","tempo","trail") and
               w.get("avg_hr", 0) and w.get("pace_min_km", 0)]
    if not running:
        return 45.0
    avg_hr_vals = [w["avg_hr"] for w in running[-5:]]
    avg_hr = sum(avg_hr_vals) / len(avg_hr_vals)
    resting_hr = 55
    max_hr = 190
    vo2 = 15 * (max_hr / resting_hr)
    paces = [w["pace_min_km"] for w in running[-5:] if w.get("pace_min_km", 0) > 0]
    if paces:
        avg_pace = sum(paces) / len(paces)
        pace_bonus = max(0, (6.5 - avg_pace) * 2)
        vo2 += pace_bonus
    return round(min(85, max(30, vo2)), 1)


def _calculate_tss(workouts, week=True):
    if week:
        cutoff = datetime.now() - timedelta(days=7)
    else:
        cutoff = datetime.now() - timedelta(days=42)
    total_tss = 0
    for w in workouts:
        date_str = w.get("workout_date", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d")
            if d < cutoff:
                continue
        except Exception:
            continue
        dur_h  = (w.get("duration_min", 45) or 45) / 60
        rpe    = w.get("rpe", 5) or 5
        if_val = rpe / 10
        total_tss += dur_h * (if_val ** 2) * 100
    return round(total_tss, 0)


# ─────────────────────────────────────────────────────────────
# REGISTRO DE CALLBACKS
# ─────────────────────────────────────────────────────────────
def register(app):

    # ── NAVEGACIÓN ────────────────────────────────────────────
    SECTIONS = [
        "section-inicio", "section-metricas", "section-objetivos",
        "section-nutricion", "section-entrenamientos",
    ]
    NAV_MAP = {
        "nav-inicio-inicio":         "section-inicio",
        "nav-metricas-inicio":       "section-metricas",
        "nav-objetivos-inicio":      "section-objetivos",
        "nav-nutricion-inicio":      "section-nutricion",
        "nav-entrenamientos-inicio": "section-entrenamientos",
    }

    @app.callback(
        [Output(s, "style") for s in SECTIONS],
        [Input(btn, "n_clicks") for btn in NAV_MAP],
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def navigate_sections(*args):
        pathname = args[-1]
        if pathname != "/inicio":
            raise dash.exceptions.PreventUpdate
        ctx = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        active  = NAV_MAP.get(trigger, "section-inicio")
        show    = {"padding": "28px 32px"}
        hide    = {"padding": "28px 32px", "display": "none"}
        return [show if s == active else hide for s in SECTIONS]

    # ── PERFIL ────────────────────────────────────────────────
    @app.callback(
        [
            Output("sidebar-user-avatar",       "children"),
            Output("sidebar-user-fullname",     "children"),
            Output("sidebar-user-level",        "children"),
            Output("health-status-dots",        "children"),
            Output("health-status-description", "children"),
            Output("user-profile-avatar",       "children"),
            Output("user-profile-name",         "children"),
            Output("user-profile-type",         "children"),
            Output("metric-activity",           "children"),
            Output("personal-records-list",     "children"),
        ],
        [Input("url", "pathname"), Input("current-user", "data"), Input("user-type-store", "data")],
        prevent_initial_call=True,
    )
    def update_profile(pathname, current_user, user_type):
        if pathname not in ("/inicio",) or not current_user:
            raise dash.exceptions.PreventUpdate
        from db import (get_user, get_user_activity_level,
                        get_health_score_from_activity_level,
                        get_health_description, get_doctor, get_personal_records)
        is_doctor = (user_type == "doctor")
        if is_doctor:
            doctor = get_doctor(current_user) or {}
            full   = doctor.get("full_name", current_user)
            level  = 0; score = 0
        else:
            user  = get_user(current_user) or {}
            full  = user.get("full_name", current_user)
            level = get_user_activity_level(current_user)
            score = get_health_score_from_activity_level(level)
        desc   = get_health_description(score)
        letter = full[0].upper() if full else "U"
        dots   = [html.Div(className="score-dot" + (" score-dot--active" if i <= score else ""))
                  for i in range(1, 6)]
        prs    = get_personal_records(current_user) if not is_doctor else []
        if prs:
            pr_items = [html.Div(className="pr-item", children=[
                html.Span(pr.get("record_type", ""), className="pr-distance"),
                html.Span(pr.get("unit", ""),        className="pr-time"),
            ]) for pr in prs[:5]]
        else:
            pr_items = [html.P("Sin récords aún. ¡A entrenar!", className="empty-state-sm")]
        return (letter, full, f"Nivel {level}/10" if not is_doctor else "Médico",
                dots, desc, letter, full, "Médico" if is_doctor else "Atleta",
                f"{level}/10", pr_items)

    # ── ECG ───────────────────────────────────────────────────
    @app.callback(
        [Output("ecg-graph-inicio", "figure"),
         Output("ecg-bpm-display",  "children"),
         Output("ecg-data-store",   "data"),
         Output("ecg-status-label", "children")],
        [Input("upload-ecg-inicio", "contents"), Input("url", "pathname")],
        [State("upload-ecg-inicio", "filename"), State("current-user", "data")],
        prevent_initial_call=True,
    )
    def update_ecg(contents, pathname, filename, current_user):
        if pathname != "/inicio":
            raise dash.exceptions.PreventUpdate
        from sensors import load_ecg_and_compute_bpm
        import tempfile, os
        status = "Señal sintética"
        if contents:
            try:
                _, content_string = contents.split(",")
                decoded = base64.b64decode(content_string)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as f:
                    f.write(decoded); tmppath = f.name
                t, ecg, bpm, peaks = load_ecg_and_compute_bpm(tmppath)
                os.unlink(tmppath); status = f"Archivo: {filename}"
            except Exception:
                t, ecg, bpm, peaks = load_ecg_and_compute_bpm(); status = "Error al leer archivo"
        else:
            t, ecg, bpm, peaks = load_ecg_and_compute_bpm()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=ecg, mode="lines", line=dict(color=LIME, width=1.5),
                                 fill="tozeroy", fillcolor="rgba(232,255,71,0.06)"))
        if len(peaks):
            fig.add_trace(go.Scatter(x=t[peaks], y=ecg[peaks], mode="markers",
                                     marker=dict(color=RED, size=7, line=dict(color="#0D0D0D", width=1))))
        fig.update_layout(showlegend=False, margin=dict(l=30,r=10,t=5,b=25), **_LAYOUT_BASE)
        store = json.dumps({"t": t.tolist(), "ecg": ecg.tolist()})
        return fig, f"♥ {bpm:.0f} BPM", store, status

    @app.callback(
        Output("download-ecg-csv", "data"),
        Input("btn-download-ecg",  "n_clicks"),
        State("ecg-data-store",    "data"),
        prevent_initial_call=True,
    )
    def download_ecg(n, store_data):
        if not n or not store_data: raise dash.exceptions.PreventUpdate
        import pandas as pd
        data = json.loads(store_data)
        df   = pd.DataFrame({"Time": data["t"], "ECG": data["ecg"]})
        return dcc.send_data_frame(df.to_csv, "ecg_athletica.csv", index=False)

    # ── KPIs INICIO ───────────────────────────────────────────
    @app.callback(
        [Output("metric-bpm",          "children"),
         Output("metric-bpm-zone",     "children"),
         Output("metric-cals",         "children"),
         Output("metric-cals-sub",     "children"),
         Output("metric-hydration",    "children"),
         Output("metric-hydration-sub","children"),
         Output("recent-workouts-list","children")],
        [Input("url", "pathname"), Input("current-user", "data")],
        prevent_initial_call=True,
    )
    def update_inicio_metrics(pathname, current_user):
        if pathname != "/inicio" or not current_user:
            raise dash.exceptions.PreventUpdate
        from db import get_workout_history, get_hydration
        workouts  = get_workout_history(current_user, limit=7)
        hydration = get_hydration(current_user)
        liters    = hydration.get("liters", 0.0)
        goal      = hydration.get("goal",   3.0)
        last_bpm = 72; zone_label = "Reposo"; last_cal = 0
        if workouts:
            last_bpm    = workouts[0].get("avg_hr", 0) or 72
            zone_label, _ = _zone_label(last_bpm)
            last_cal    = workouts[0].get("calories_burned", 0) or 0
        week_cal = sum(w.get("calories_burned", 0) or 0 for w in workouts)
        if workouts:
            recent_items = []
            for w in workouts[:5]:
                icon  = WORKOUT_ICONS.get(w.get("workout_type",""), "🏅")
                rpe   = w.get("rpe", 5) or 5; color = rpe_color(rpe)
                dist  = w.get("distance_km", 0) or 0
                dur   = w.get("duration_min", 0) or 0
                date  = w.get("workout_date", "")
                recent_items.append(html.Div(className="recent-item", children=[
                    html.Span(icon, className="recent-icon"),
                    html.Div(className="recent-info", children=[
                        html.Span((w.get("workout_type") or "Entrenamiento").replace("_"," ").title(), className="recent-name"),
                        html.Span(f"{dist:.1f}km · {dur}min", className="recent-meta"),
                    ]),
                    html.Div(className="recent-right", children=[
                        html.Span(f"RPE {rpe}", className="rpe-chip", style={"borderColor":color,"color":color}),
                        html.Span(date[-5:] if date else "", className="recent-date"),
                    ]),
                ]))
        else:
            recent_items = [html.P("Sin actividad registrada aún.", className="empty-state-sm")]
        return (str(last_bpm), zone_label, str(last_cal), f"{week_cal} kcal semana",
                f"{liters:.1f}L", f"de {goal:.1f}L objetivo", recent_items)

    # ── INICIO: Resumen semana + Greeting ─────────────────────
    @app.callback(
        [Output("inicio-greeting",    "children"),
         Output("inicio-week-summary","children")],
        [Input("url", "pathname"), Input("current-user", "data")],
        prevent_initial_call=True,
    )
    def update_inicio_greeting(pathname, current_user):
        if pathname != "/inicio" or not current_user:
            raise dash.exceptions.PreventUpdate

        from db import get_workout_history, get_workout_stats

        hour = datetime.now().hour
        saludo = "¡Buenos días" if hour < 12 else ("¡Buenas tardes" if hour < 19 else "¡Buenas noches")
        greeting = html.Div([
            html.Div(f"{saludo}, {current_user}! 👋", style={
                "fontFamily": "var(--font-display)", "fontSize": "1.8rem",
                "fontWeight": "900", "color": WHITE, "lineHeight": "1.1",
            }),
            html.Div("Aquí tienes tu resumen del día.", style={
                "color": MUTED, "fontSize": "0.9rem", "marginTop": "4px",
            }),
        ])

        workouts = get_workout_history(current_user, limit=30)
        stats    = get_workout_stats(current_user)
        week     = stats.get("week", {})

        cutoff = datetime.now() - timedelta(days=7)
        week_workouts = []
        for w in workouts:
            try:
                d = datetime.strptime(w.get("workout_date",""), "%Y-%m-%d")
                if d >= cutoff:
                    week_workouts.append(w)
            except Exception:
                pass

        disc_map = {
            "carrera_facil":"🏃 Running","intervalos":"🏃 Running","tempo":"🏃 Running","trail":"🏃 Running",
            "ciclismo":"🚴 Ciclismo","natacion":"🏊 Natación","fuerza":"💪 Fuerza",
            "hiit":"🔥 HIIT","yoga":"🧘 Yoga","recuperacion":"🔄 Recuperación",
            "cardio":"❤️ Cardio","otro":"🏅 Otro",
        }
        disc_stats = {}
        for w in week_workouts:
            disc = disc_map.get(w.get("workout_type","otro"), "🏅 Otro")
            if disc not in disc_stats:
                disc_stats[disc] = {"sessions": 0, "km": 0, "min": 0, "cal": 0}
            disc_stats[disc]["sessions"] += 1
            disc_stats[disc]["km"]       += w.get("distance_km", 0) or 0
            disc_stats[disc]["min"]      += w.get("duration_min", 0) or 0
            disc_stats[disc]["cal"]      += w.get("calories_burned", 0) or 0

        if not disc_stats:
            week_summary = html.Div(
                "Sin entrenamientos esta semana. ¡A moverse! 💪",
                style={"color": MUTED, "fontSize": "0.88rem", "padding": "8px 0"},
            )
        else:
            rows = []
            for disc, s in disc_stats.items():
                rows.append(html.Div(style={
                    "display": "flex", "alignItems": "center", "gap": "12px",
                    "padding": "10px 0",
                    "borderBottom": "1px solid rgba(255,255,255,0.05)",
                }, children=[
                    html.Span(disc, style={"flex":"1","fontWeight":"700","color":WHITE,"fontSize":"0.9rem"}),
                    html.Span(f"{s['sessions']} ses.", style={"color":LIME,"fontSize":"0.82rem","fontWeight":"700","minWidth":"48px","textAlign":"right"}),
                    html.Span(f"{s['km']:.1f} km" if s["km"] > 0 else f"{s['min']} min",
                              style={"color":CYAN,"fontSize":"0.82rem","minWidth":"60px","textAlign":"right"}),
                    html.Span(f"{s['cal']} kcal", style={"color":ORANGE,"fontSize":"0.82rem","minWidth":"60px","textAlign":"right"}),
                ]))
            total_ses = sum(s["sessions"] for s in disc_stats.values())
            total_km  = sum(s["km"]       for s in disc_stats.values())
            total_cal = sum(s["cal"]      for s in disc_stats.values())
            rows.append(html.Div(style={
                "display":"flex","alignItems":"center","gap":"12px",
                "padding":"10px 0","borderTop":"2px solid rgba(232,255,71,0.2)","marginTop":"4px",
            }, children=[
                html.Span("TOTAL SEMANA", style={"flex":"1","fontWeight":"900","color":LIME,"fontSize":"0.8rem","letterSpacing":"0.5px"}),
                html.Span(f"{total_ses} ses.", style={"color":LIME,"fontSize":"0.82rem","fontWeight":"700","minWidth":"48px","textAlign":"right"}),
                html.Span(f"{total_km:.1f} km", style={"color":CYAN,"fontSize":"0.82rem","minWidth":"60px","textAlign":"right"}),
                html.Span(f"{total_cal} kcal", style={"color":ORANGE,"fontSize":"0.82rem","minWidth":"60px","textAlign":"right"}),
            ]))
            week_summary = html.Div(rows)

        return greeting, week_summary

    # ══════════════════════════════════════════════════════════
    # SECCIÓN MÉTRICAS
    # ══════════════════════════════════════════════════════════

    @app.callback(
        [Output("metrics-tab-global",  "style"),
         Output("metrics-tab-running", "style"),
         Output("metrics-tab-cycling", "style"),
         Output("metrics-tab-swimming","style"),
         Output("metrics-active-tab",  "data")],
        [Input("metrics-tab-global",   "n_clicks"),
         Input("metrics-tab-running",  "n_clicks"),
         Input("metrics-tab-cycling",  "n_clicks"),
         Input("metrics-tab-swimming", "n_clicks")],
        prevent_initial_call=True,
    )
    def switch_metrics_tab(g, r, c, s):
        ctx     = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "metrics-tab-global"
        tab_map = {
            "metrics-tab-global":   "global",
            "metrics-tab-running":  "running",
            "metrics-tab-cycling":  "cycling",
            "metrics-tab-swimming": "swimming",
        }
        active = tab_map.get(trigger, "global")
        def _style(key):
            on  = {'background':'rgba(232,255,71,0.12)','border':'1px solid rgba(232,255,71,0.5)',
                   'borderRadius':'8px','color':LIME,'padding':'7px 18px','fontWeight':'700',
                   'fontSize':'0.8rem','cursor':'pointer','letterSpacing':'0.4px'}
            off = {'background':'transparent','border':'1px solid rgba(255,255,255,0.1)',
                   'borderRadius':'8px','color':MUTED,'padding':'7px 18px','fontWeight':'700',
                   'fontSize':'0.8rem','cursor':'pointer','letterSpacing':'0.4px'}
            return on if tab_map[key] == active else off
        return (_style("metrics-tab-global"), _style("metrics-tab-running"),
                _style("metrics-tab-cycling"), _style("metrics-tab-swimming"), active)

    @app.callback(
        [
            Output("adv-kpi-vo2",        "children"),
            Output("adv-kpi-hrv",        "children"),
            Output("adv-kpi-pace",       "children"),
            Output("adv-kpi-cadence",    "children"),
            Output("adv-kpi-power",      "children"),
            Output("adv-kpi-tss",        "children"),
            Output("adv-kpi-efficiency", "children"),
            Output("adv-kpi-fatigue",    "children"),
            Output("stat-sessions",      "children"),
            Output("stat-km",            "children"),
            Output("stat-time",          "children"),
            Output("stat-cal-week",      "children"),
            Output("stat-avg-rpe",       "children"),
            Output("chart-weekly-load",      "figure"),
            Output("chart-hr-zones",         "figure"),
            Output("chart-pace-trend",       "figure"),
            Output("chart-rpe-trend",        "figure"),
            Output("chart-mood-trend",       "figure"),
            Output("chart-volume-discipline","figure"),
            Output("chart-resting-hr",       "figure"),
            Output("chart-hr-efficiency",    "figure"),
            Output("chart-hrv-trend",        "figure"),
            Output("acwr-ratio-display", "children"),
            Output("acwr-status-label",  "children"),
            Output("acwr-bar-container", "style"),
        ],
        [Input("url", "pathname"),
         Input("current-user", "data"),
         Input("metrics-active-tab", "data")],
        prevent_initial_call=True,
    )
    def load_metrics(pathname, current_user, active_tab):
        if pathname != "/inicio" or not current_user:
            raise dash.exceptions.PreventUpdate
        if active_tab is None:
            active_tab = "global"

        from db import get_workout_history, get_workout_stats, calculate_training_load

        all_workouts = get_workout_history(current_user, limit=60)

        DISC_FILTER = {
            "running":  ("carrera_facil","intervalos","tempo","trail"),
            "cycling":  ("ciclismo",),
            "swimming": ("natacion",),
        }
        if active_tab and active_tab != "global":
            workouts = [w for w in all_workouts
                        if w.get("workout_type","") in DISC_FILTER.get(active_tab, ())]
        else:
            workouts = all_workouts

        stats = get_workout_stats(current_user)
        week  = stats.get("week", {})

        s_sessions = str(week.get("total_sessions") or 0)
        s_km       = f"{(week.get('total_km') or 0):.1f}"
        total_min  = week.get("total_min") or 0
        s_time     = f"{int(total_min // 60)}h {int(total_min % 60)}m"
        s_cal      = str(int(week.get("total_cal") or 0))
        s_rpe      = f"{(week.get('avg_rpe') or 0):.1f}"

        vo2     = _estimate_vo2max(workouts)
        tss     = _calculate_tss(workouts, week=True)

        running_w = [w for w in workouts if w.get("workout_type") in
                     ("carrera_facil","intervalos","tempo","trail") and
                     w.get("pace_min_km", 0)]
        avg_pace = (sum(w["pace_min_km"] for w in running_w[-10:]) / len(running_w[-10:])
                    if running_w else 0)

        cadence_workouts = [w for w in workouts if w.get("cadence", 0)]
        avg_cadence = (sum(w["cadence"] for w in cadence_workouts) / len(cadence_workouts)
                       if cadence_workouts else random.randint(168, 178))

        power_workouts = [w for w in workouts if w.get("power_w", 0)]
        avg_power = (sum(w["power_w"] for w in power_workouts) / len(power_workouts)
                     if power_workouts else "—")

        recent_rpe = [w.get("rpe", 5) for w in workouts[:5]] if workouts else [5]
        avg_recent_rpe = sum(recent_rpe) / len(recent_rpe)
        hrv_sim = round(max(20, 85 - avg_recent_rpe * 5 + random.uniform(-3, 3)), 1)

        eff_workouts = [w for w in running_w if w.get("avg_hr", 0)]
        if eff_workouts:
            eff_vals = [w.get("pace_min_km", 6) / (w.get("avg_hr", 160) / 100)
                        for w in eff_workouts[-5:]]
            eff = round(sum(eff_vals) / len(eff_vals), 2)
        else:
            eff = "—"

        load   = calculate_training_load(all_workouts)
        ratio  = load.get("ratio", 1.0)
        fatigue_idx = round(max(0, min(10, (ratio - 0.8) * 12.5)), 1)

        status = load.get("status", "optimal")
        status_map = {
            "optimal":       ("Óptimo ✓",       LIME),
            "undertraining": ("Poco volumen ↓",  CYAN),
            "overload_risk": ("Riesgo fatiga ⚠", RED),
        }
        status_text, status_color = status_map.get(status, ("Óptimo", LIME))
        acwr_pct = min(98, max(2, (ratio - 0.5) * 100))
        acwr_bar_style = {
            'position':'absolute','top':'0','bottom':'0','width':'4px',
            'background':'#fff','boxShadow':'0 0 8px rgba(255,255,255,0.8)',
            'left':f'{acwr_pct:.0f}%','transition':'left 0.6s ease',
        }

        # ── Gráfica 1: Carga semanal
        weeks_data = {}
        for w in workouts:
            date = w.get("workout_date", "")
            if not date: continue
            try:
                d        = datetime.strptime(date, "%Y-%m-%d")
                wk       = d.strftime("W%V '%y")
                if wk not in weeks_data:
                    weeks_data[wk] = {"tss": 0, "km": 0}
                dur_h    = (w.get("duration_min", 45) or 45) / 60
                rpe_w    = (w.get("rpe", 5) or 5)
                weeks_data[wk]["tss"] += dur_h * (rpe_w / 10) ** 2 * 100
                weeks_data[wk]["km"]  += w.get("distance_km", 0) or 0
            except Exception:
                pass
        wk_labels = sorted(weeks_data.keys())[-10:]
        wk_tss    = [weeks_data[k]["tss"] for k in wk_labels]
        wk_km     = [weeks_data[k]["km"]  for k in wk_labels]

        fig_load = go.Figure()
        fig_load.add_trace(go.Bar(x=wk_labels, y=wk_tss, name="TSS",
                                  marker=dict(color=LIME, opacity=0.85), yaxis="y"))
        fig_load.add_trace(go.Scatter(x=wk_labels, y=wk_km, mode="lines+markers",
                                      name="km", line=dict(color=CYAN, width=2),
                                      marker=dict(size=5), yaxis="y2"))
        fig_load.update_layout(
            **_LAYOUT_BASE, margin=_MARGIN, showlegend=True, bargap=0.3,
            legend=dict(font=dict(color="#9CA3AF",size=9), orientation="h", x=0, y=1.1),
            yaxis2=dict(overlaying="y", side="right", showgrid=False,
                        tickfont=dict(color=CYAN, size=9), zeroline=False),
        )

        # ── Gráfica 2: Zonas FC
        zone_counts  = {"Z1":0,"Z2":0,"Z3":0,"Z4":0,"Z5":0}
        zone_colors  = {"Z1":"#4FC3F7","Z2":GREEN,"Z3":LIME,"Z4":ORANGE,"Z5":RED}
        for w in workouts:
            ah  = w.get("avg_hr", 0) or 0
            dur = w.get("duration_min", 0) or 1
            if ah > 0:
                zone, _ = _zone_label(ah)
                zone_counts[zone] = zone_counts.get(zone, 0) + dur
        fig_zones = go.Figure(data=[go.Pie(
            labels=list(zone_counts.keys()), values=list(zone_counts.values()),
            hole=0.62, marker=dict(colors=[zone_colors[z] for z in zone_counts]),
            textfont=dict(size=10, color="#fff"),
        )])
        fig_zones.update_layout(showlegend=True,
                                legend=dict(font=dict(color="#9CA3AF",size=10),
                                            orientation="v", x=1.02, y=0.5),
                                margin=dict(l=0,r=60,t=10,b=10), **_LAYOUT_BASE)

        # ── Gráfica 3: Pace trend
        pace_data = [(w.get("workout_date",""), w.get("pace_min_km",0))
                     for w in reversed(workouts)
                     if w.get("workout_date") and w.get("pace_min_km", 0) > 0][-20:]
        if pace_data:
            p_dates  = [d for d, _ in pace_data]
            p_values = [v for _, v in pace_data]
            p_labels = [_pace_str(v) for v in p_values]
        else:
            p_dates = ["Sin datos"]; p_values = [0]; p_labels = ["—"]

        fig_pace = go.Figure()
        fig_pace.add_trace(go.Scatter(
            x=p_dates, y=p_values, mode="lines+markers",
            text=p_labels, hovertemplate="%{text}<extra></extra>",
            line=dict(color=GREEN, width=2), marker=dict(color=GREEN, size=6),
            fill="tozeroy", fillcolor="rgba(129,199,132,0.05)",
        ))
        fig_pace.update_layout(**_LAYOUT_BASE, margin=_MARGIN,
                               yaxis=dict(autorange="reversed", tickformat=".1f",
                                          gridcolor="rgba(255,255,255,0.04)",
                                          tickfont=dict(color="#6B7280"),
                                          showline=False, zeroline=False))

        # ── Gráfica 4: RPE trend
        rpe_data = [(w.get("workout_date",""), w.get("rpe",5))
                    for w in reversed(workouts) if w.get("workout_date")][-20:]
        rpe_dates  = [d for d,_ in rpe_data] if rpe_data else ["Sin datos"]
        rpe_values = [r for _,r in rpe_data] if rpe_data else [5]
        fig_rpe = go.Figure()
        fig_rpe.add_trace(go.Scatter(
            x=rpe_dates, y=rpe_values, mode="lines+markers",
            line=dict(color=CYAN, width=2), marker=dict(color=CYAN, size=6),
            fill="tozeroy", fillcolor="rgba(0,245,255,0.05)",
        ))
        fig_rpe.update_layout(**_LAYOUT_BASE, margin=_MARGIN)

        # ── Gráfica 5: Mood
        mood_map  = {"excelente":5,"bien":4,"regular":3,"cansado":2,"agotado":1}
        mood_data = [(w.get("workout_date",""), mood_map.get(w.get("mood","regular"),3))
                     for w in reversed(workouts) if w.get("workout_date")][-15:]
        m_dates  = [d[-5:] for d,_ in mood_data] if mood_data else ["Sin datos"]
        m_values = [v for _,v in mood_data] if mood_data else [3]
        m_colors = [GREEN if v>=4 else (LIME if v==3 else RED) for v in m_values]
        fig_mood = go.Figure()
        fig_mood.add_trace(go.Bar(x=m_dates, y=m_values, marker=dict(color=m_colors)))
        fig_mood.update_layout(**_LAYOUT_BASE, showlegend=False, margin=_MARGIN,
                               yaxis=dict(range=[0,5.5], tickvals=[1,2,3,4,5],
                                          ticktext=["Agotado","Cansado","Regular","Bien","Genial"],
                                          tickfont=dict(color="#6B7280",size=9),
                                          gridcolor="rgba(255,255,255,0.04)"))

        # ── Gráfica 6: Volumen por disciplina
        disc_map = {"carrera_facil":"Running","intervalos":"Running","tempo":"Running","trail":"Running",
                    "ciclismo":"Ciclismo","natacion":"Natación","fuerza":"Fuerza","hiit":"HIIT",
                    "yoga":"Yoga","recuperacion":"Recuperación","cardio":"Cardio","otro":"Otro"}
        disc_km  = {}
        for w in workouts:
            disc = disc_map.get(w.get("workout_type","otro"), "Otro")
            disc_km[disc] = disc_km.get(disc, 0) + (w.get("distance_km", 0) or 0)
        disc_color_m = {"Running":LIME,"Ciclismo":CYAN,"Natación":"#4FC3F7","Fuerza":ORANGE,
                        "HIIT":RED,"Yoga":GREEN,"Recuperación":PURPLE}
        fig_vol = go.Figure()
        for disc, km_val in disc_km.items():
            if km_val > 0:
                fig_vol.add_trace(go.Bar(
                    name=disc, x=[disc], y=[km_val],
                    marker=dict(color=disc_color_m.get(disc, MUTED)),
                ))
        fig_vol.update_layout(**_LAYOUT_BASE, showlegend=False, bargap=0.35, margin=_MARGIN)

        # ── Gráfica 7: FC Reposo
        rhr_dates  = []
        rhr_values = []
        for w in sorted(workouts, key=lambda x: x.get("workout_date",""))[-20:]:
            date = w.get("workout_date", "")
            if not date: continue
            rhr_sim = 55 + (w.get("rpe",5) or 5) * 0.8 + random.gauss(0, 1.5)
            rhr_dates.append(date[-5:])
            rhr_values.append(round(rhr_sim, 1))
        if not rhr_dates:
            rhr_dates = ["Sin datos"]; rhr_values = [60]
        fig_rhr = go.Figure()
        fig_rhr.add_trace(go.Scatter(
            x=rhr_dates, y=rhr_values, mode="lines+markers",
            line=dict(color="#4FC3F7", width=2), marker=dict(color="#4FC3F7", size=5),
            fill="tozeroy", fillcolor="rgba(79,195,247,0.05)",
        ))
        fig_rhr.update_layout(**_LAYOUT_BASE, margin=_MARGIN)

        # ── Gráfica 8: Eficiencia FC
        eff_dates  = []
        eff_values = []
        for w in sorted(running_w, key=lambda x: x.get("workout_date",""))[-20:]:
            date = w.get("workout_date","")
            if not date or not w.get("avg_hr",0): continue
            eff_val = round((w.get("pace_min_km",6) / (w.get("avg_hr",160) / 100)), 2)
            eff_dates.append(date[-5:])
            eff_values.append(eff_val)
        if not eff_dates:
            eff_dates = ["Sin datos"]; eff_values = [3.5]
        fig_eff = go.Figure()
        fig_eff.add_trace(go.Scatter(
            x=eff_dates, y=eff_values, mode="lines+markers",
            line=dict(color=ORANGE, width=2), marker=dict(color=ORANGE, size=6),
        ))
        fig_eff.add_hline(y=3.5, line_dash="dot", line_color="rgba(255,255,255,0.2)",
                          annotation_text="óptimo", annotation_font_color="#6B7280",
                          annotation_font_size=10)
        fig_eff.update_layout(**_LAYOUT_BASE, margin=_MARGIN)

        # ── Gráfica 9: HRV
        hrv_dates  = []
        hrv_values = []
        baseline_hrv = 70
        for w in sorted(workouts, key=lambda x: x.get("workout_date",""))[-30:]:
            date = w.get("workout_date","")
            if not date: continue
            rpe_w    = w.get("rpe",5) or 5
            hrv_val  = baseline_hrv - rpe_w * 4 + random.gauss(0, 4)
            hrv_dates.append(date[-5:])
            hrv_values.append(round(max(15, hrv_val), 1))
        if not hrv_dates:
            hrv_dates = ["Sin datos"]; hrv_values = [65]
        fig_hrv = go.Figure()
        fig_hrv.add_trace(go.Scatter(
            x=hrv_dates, y=hrv_values, mode="lines+markers",
            line=dict(color=PURPLE, width=2), marker=dict(color=PURPLE, size=5),
            fill="tozeroy", fillcolor="rgba(156,136,255,0.05)",
        ))
        fig_hrv.add_hline(y=50, line_dash="dot", line_color="rgba(255,255,255,0.15)",
                          annotation_text="umbral alerta", annotation_font_color="#6B7280",
                          annotation_font_size=9)
        fig_hrv.update_layout(**_LAYOUT_BASE, margin=_MARGIN)

        return (
            f"{vo2}", f"{hrv_sim} ms", _pace_str(avg_pace),
            f"{avg_cadence}", f"{avg_power}W" if isinstance(avg_power, float) else "—",
            f"{tss:.0f}", f"{eff:.2f}" if isinstance(eff, float) else "—", f"{fatigue_idx}/10",
            s_sessions, s_km, s_time, s_cal, s_rpe,
            fig_load, fig_zones, fig_pace, fig_rpe,
            fig_mood, fig_vol, fig_rhr, fig_eff, fig_hrv,
            html.Span(f"{ratio:.2f}", style={"color": status_color}),
            html.Span(status_text,    style={"color": status_color}),
            acwr_bar_style,
        )

    # ── CSV Upload ────────────────────────────────────────────
    @app.callback(
        [Output("metrics-csv-store",           "data"),
         Output("metrics-csv-column-selector", "options"),
         Output("metrics-csv-column-selector", "value"),
         Output("upload-metrics-status",       "children")],
        Input("upload-metrics-csv", "contents"),
        State("upload-metrics-csv", "filename"),
        prevent_initial_call=True,
    )
    def process_uploaded_csv(contents, filename):
        if not contents:
            raise dash.exceptions.PreventUpdate
        try:
            import pandas as pd
            _, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            df      = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            if df.empty:
                return (dash.no_update, [], None,
                        html.Span("❌ CSV vacío.", style={"color": RED}))
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            options = [{"label": c, "value": c} for c in numeric_cols]
            default = numeric_cols[0] if numeric_cols else None
            store   = df.to_json(date_format="iso", orient="split")
            status  = html.Span(
                f"✅ {filename} — {len(df)} filas · {len(df.columns)} columnas",
                style={"color": LIME}
            )
            return store, options, default, status
        except Exception as e:
            return (dash.no_update, [], None,
                    html.Span(f"❌ Error: {str(e)[:60]}", style={"color": RED}))

    @app.callback(
        [Output("uploaded-csv-chart-wrap",    "style"),
         Output("chart-custom-upload",        "figure"),
         Output("uploaded-csv-chart-title",   "children"),
         Output("uploaded-csv-stats",         "children"),
         Output("uploaded-csv-summary-table", "children")],
        [Input("metrics-csv-store",       "data"),
         Input("metrics-csv-column-selector", "value"),
         Input("metrics-csv-chart-type",      "value")],
        prevent_initial_call=True,
    )
    def render_csv_chart(store_data, column, chart_type):
        if not store_data or not column:
            return {"display": "none"}, _empty_fig(), "", [], []
        try:
            import pandas as pd
            df  = pd.read_json(io.StringIO(store_data), orient="split")
            col = df[column].dropna()
            if col.empty:
                return {"display":"none"}, _empty_fig("Sin datos en esta columna"), "", [], []

            date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower() or "fecha" in c.lower()]
            x_vals = df[date_cols[0]].values if date_cols else df.index.values

            fig = go.Figure()
            color = LIME
            if chart_type == "bar":
                fig.add_trace(go.Bar(x=x_vals, y=col.values, marker=dict(color=LIME, opacity=0.85)))
            elif chart_type == "scatter":
                fig.add_trace(go.Scatter(x=x_vals, y=col.values, mode="markers",
                                         marker=dict(color=CYAN, size=7, opacity=0.8)))
                color = CYAN
            elif chart_type == "area":
                fig.add_trace(go.Scatter(x=x_vals, y=col.values, mode="lines",
                                         fill="tozeroy", line=dict(color=PURPLE, width=2),
                                         fillcolor="rgba(156,136,255,0.07)"))
                color = PURPLE
            else:
                fig.add_trace(go.Scatter(x=x_vals, y=col.values, mode="lines+markers",
                                         line=dict(color=GREEN, width=2), marker=dict(color=GREEN, size=5)))
                color = GREEN

            if len(col) >= 7:
                ma = pd.Series(col.values).rolling(7, min_periods=1).mean()
                fig.add_trace(go.Scatter(
                    x=x_vals, y=ma.values, mode="lines", name="Media 7 sesiones",
                    line=dict(color="rgba(255,255,255,0.3)", width=1.5, dash="dot"),
                ))

            fig.update_layout(**_LAYOUT_BASE, margin=_MARGIN, showlegend=len(col) >= 7)

            stats_items = [
                html.Div(style={'background':DARK3,'borderRadius':'8px','padding':'8px 14px','textAlign':'center'}, children=[
                    html.Div(f"{v:.2f}" if isinstance(v, float) else str(v),
                             style={'fontFamily':'var(--font-display)','fontSize':'1.1rem','fontWeight':'900','color':color}),
                    html.Div(label, style={'fontSize':'0.65rem','color':MUTED,'textTransform':'uppercase'}),
                ])
                for label, v in [
                    ("Mín",    float(col.min())),
                    ("Máx",    float(col.max())),
                    ("Media",  float(col.mean())),
                    ("Mediana",float(col.median())),
                    ("σ",      float(col.std())),
                ]
            ]
            stats_row = html.Div(stats_items, style={'display':'flex','gap':'8px','flexWrap':'wrap'})

            preview_cols = df.select_dtypes(include="number").columns.tolist()[:6]
            header = html.Tr([html.Th(c, style={'color':MUTED,'fontSize':'0.72rem','padding':'6px 10px',
                                                 'textTransform':'uppercase','fontWeight':'600'})
                              for c in preview_cols])
            rows   = [
                html.Tr([
                    html.Td(f"{df.iloc[i][c]:.2f}" if isinstance(df.iloc[i][c], float) else str(df.iloc[i][c]),
                            style={'color':'#ddd','fontSize':'0.8rem','padding':'5px 10px',
                                   'borderTop':'1px solid rgba(255,255,255,0.05)'})
                    for c in preview_cols
                ])
                for i in range(min(8, len(df)))
            ]
            table = html.Div(style={'overflowX':'auto','marginTop':'8px'}, children=[
                html.Table(style={'width':'100%','borderCollapse':'collapse'},
                           children=[html.Thead(header), html.Tbody(rows)])
            ])

            title = f"📊 {column} — {len(col)} registros"
            return {"display":"block"}, fig, title, stats_row, table

        except Exception as e:
            return {"display":"none"}, _empty_fig(f"Error: {str(e)[:50]}"), "", [], []

    @app.callback(
        Output("download-custom-csv", "data"),
        Input("btn-dl-custom-csv",    "n_clicks"),
        State("metrics-csv-store",    "data"),
        prevent_initial_call=True,
    )
    def download_custom_csv(n, store_data):
        if not n or not store_data: raise dash.exceptions.PreventUpdate
        import pandas as pd
        df = pd.read_json(io.StringIO(store_data), orient="split")
        return dcc.send_data_frame(df.to_csv, "athletica_datos.csv", index=False)

    # ── Descargas gráficas ────────────────────────────────────
    _CHART_DOWNLOADS = [
        ("btn-dl-weekly-load", "dl-weekly-load",  "carga_semanal.csv"),
        ("btn-dl-hr-zones",    "dl-hr-zones",      "zonas_fc.csv"),
        ("btn-dl-pace",        "dl-pace",          "tendencia_pace.csv"),
        ("btn-dl-rpe",         "dl-rpe",           "tendencia_rpe.csv"),
        ("btn-dl-mood",        "dl-mood",          "animo.csv"),
        ("btn-dl-volume",      "dl-volume",        "volumen_disciplina.csv"),
        ("btn-dl-resting-hr",  "dl-resting-hr",    "fc_reposo.csv"),
        ("btn-dl-efficiency",  "dl-efficiency",    "eficiencia_fc.csv"),
        ("btn-dl-hrv",         "dl-hrv",           "hrv.csv"),
    ]

    def _make_chart_download_callback(btn_id, dl_id, filename):
        @app.callback(
            Output(dl_id, "data"),
            Input(btn_id, "n_clicks"),
            [State("current-user", "data")],
            prevent_initial_call=True,
        )
        def _dl(n, current_user):
            if not n or not current_user:
                raise dash.exceptions.PreventUpdate
            import pandas as pd
            from db import get_workout_history
            workouts = get_workout_history(current_user, limit=60)
            df = pd.DataFrame(workouts)
            cols = [c for c in ["workout_date","workout_type","distance_km","duration_min",
                                 "avg_hr","rpe","pace_min_km","calories_burned","mood","training_zone"]
                    if c in df.columns]
            return dcc.send_data_frame(df[cols].to_csv, filename, index=False)

    for btn_id, dl_id, fn in _CHART_DOWNLOADS:
        _make_chart_download_callback(btn_id, dl_id, fn)

    # ══════════════════════════════════════════════════════════
    # ENCUESTA POST-ENTRENAMIENTO
    # ══════════════════════════════════════════════════════════
    @app.callback(
        Output("modal-workout-survey", "is_open"),
        [Input("btn-open-workout-survey",   "n_clicks"),
         Input("btn-open-workout-survey-2", "n_clicks"),
         Input("btn-cancel-survey",         "n_clicks"),
         Input("btn-submit-survey",         "n_clicks")],
        State("modal-workout-survey", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_survey_modal(n1, n2, n_cancel, n_submit, is_open):
        ctx = callback_context
        if not ctx.triggered: raise dash.exceptions.PreventUpdate
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger in ("btn-open-workout-survey", "btn-open-workout-survey-2"):
            return True
        return False

    @app.callback(
        Output("survey-rpe-label", "children"),
        Input("survey-rpe", "value"),
        prevent_initial_call=True,
    )
    def update_rpe_label(val):
        if val is None: return "5 — Moderado"
        color = rpe_color(val)
        return html.Span(f"{val} — {_rpe_text(val)}", style={"color": color})

    @app.callback(
        [Output("mood-btn-excelente","className"),
         Output("mood-btn-bien",     "className"),
         Output("mood-btn-regular",  "className"),
         Output("mood-btn-cansado",  "className"),
         Output("mood-btn-agotado",  "className"),
         Output("survey-mood-store", "data")],
        [Input("mood-btn-excelente","n_clicks"),
         Input("mood-btn-bien",     "n_clicks"),
         Input("mood-btn-regular",  "n_clicks"),
         Input("mood-btn-cansado",  "n_clicks"),
         Input("mood-btn-agotado",  "n_clicks")],
        State("survey-mood-store", "data"),
        prevent_initial_call=True,
    )
    def select_mood(*args):
        vals     = ["excelente","bien","regular","cansado","agotado"]
        current  = args[-1] or "bien"
        ctx      = callback_context
        selected = current
        if ctx.triggered:
            trigger  = ctx.triggered[0]["prop_id"].split(".")[0]
            selected = trigger.replace("mood-btn-","")
        classes = ["mood-btn mood-btn--selected" if v == selected else "mood-btn" for v in vals]
        return (*classes, selected)

    @app.callback(
        [Output("survey-success-msg",   "children"),
         Output("workout-history-list", "children"),
         Output("modal-workout-survey", "is_open", allow_duplicate=True)],
        Input("btn-submit-survey", "n_clicks"),
        [State("survey-workout-type","value"), State("survey-rpe","value"),
         State("survey-mood-store",  "data"),  State("survey-energy","value"),
         State("survey-pain",        "value"), State("survey-notes","value"),
         State("survey-duration",    "value"), State("survey-distance","value"),
         State("survey-avg-hr",      "value"), State("survey-calories","value"),
         State("current-user",       "data")],
        prevent_initial_call=True,
    )
    def submit_survey(n, wtype, rpe, mood, energy, pain, notes,
                      duration, distance, avg_hr, calories, current_user):
        if not n or not current_user or not wtype:
            raise dash.exceptions.PreventUpdate
        from db import save_workout, get_workout_history
        zone_label = "Z2"
        if avg_hr and avg_hr > 0:
            zone_label, _ = _zone_label(avg_hr)
        save_workout(current_user, wtype,
                     duration_min=duration or 0, distance_km=distance or 0,
                     avg_hr=avg_hr or 0, calories_burned=calories or 0,
                     rpe=rpe or 5, mood=mood or "bien", energy=energy or 5,
                     pain=pain or 0, notes=notes or "", training_zone=zone_label)
        workouts = get_workout_history(current_user)
        return (html.Span("✅ ¡Sesión registrada!", style={"color": LIME}),
                _render_workout_history(workouts), False)

    @app.callback(
        [Output("workout-history-list","children", allow_duplicate=True),
         Output("month-stats-panel",  "children"),
         Output("training-tip",       "children")],
        [Input("url", "pathname"), Input("current-user", "data")],
        prevent_initial_call=True,
    )
    def load_workouts(pathname, current_user):
        if pathname != "/inicio" or not current_user:
            raise dash.exceptions.PreventUpdate
        from db import get_workout_history, get_workout_stats
        workouts = get_workout_history(current_user, limit=30)
        stats    = get_workout_stats(current_user)
        month    = stats.get("month", {})
        month_panel = html.Div(className="month-stats-grid", children=[
            html.Div(className="month-stat", children=[
                html.Div(str(month.get("sessions") or 0), className="month-stat-val"),
                html.Div("Sesiones",   className="month-stat-label"),
            ]),
            html.Div(className="month-stat", children=[
                html.Div(f"{(month.get('km') or 0):.0f}", className="month-stat-val"),
                html.Div("Kilómetros", className="month-stat-label"),
            ]),
            html.Div(className="month-stat", children=[
                html.Div(f"{(month.get('cal') or 0):.0f}", className="month-stat-val"),
                html.Div("Kcal",       className="month-stat-label"),
            ]),
        ])
        return _render_workout_history(workouts), month_panel, random.choice(TRAINING_TIPS)

    # ── NUTRICIÓN ─────────────────────────────────────────────
    @app.callback(
        [Output("meal-success-msg",       "children"),
         Output("meals-desayuno",         "children"),
         Output("meals-almuerzo",         "children"),
         Output("meals-cena",             "children"),
         Output("meals-snacks",           "children"),
         Output("total-calories-display", "children"),
         Output("macro-carbs-val",        "children"),
         Output("macro-protein-val",      "children"),
         Output("macro-fat-val",          "children"),
         Output("macro-carbs-bar",        "style"),
         Output("macro-protein-bar",      "style"),
         Output("macro-fat-bar",          "style"),
         Output("macro-pie-chart",        "figure")],
        [Input("btn-add-meal","n_clicks"), Input("url","pathname")],
        [State("input-meal-description","value"),
         State("meal-type-store","data"), State("current-user","data")],
        prevent_initial_call=True,
    )
    def handle_meal(n_add, pathname, description, meal_type, current_user):
        if not current_user: raise dash.exceptions.PreventUpdate
        from db import (save_user_meal, load_user_meals,
                        calculate_daily_totals, estimate_nutrients_from_description)
        ctx     = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        if trigger == "btn-add-meal":
            if not n_add or not description: raise dash.exceptions.PreventUpdate
            nutrients = estimate_nutrients_from_description(description)
            save_user_meal(current_user, {"type": meal_type or "snacks",
                                          "description": description,
                                          "time": datetime.now().strftime("%H:%M"), **nutrients})
        meals  = load_user_meals(current_user)
        totals = calculate_daily_totals(meals)
        today  = datetime.now().strftime("%Y-%m-%d")
        def render_meal_list(filter_type):
            entries = [m for m in meals if m.get("meal_type")==filter_type and m.get("meal_date")==today]
            if not entries: return [html.P("—", className="empty-meal")]
            return [html.Div(className="meal-entry", children=[
                html.Span(m.get("description",""), className="meal-desc"),
                html.Span(f"{m.get('calories',0)} kcal", className="meal-cal"),
            ]) for m in entries]
        carbs_pct   = min(100, totals["carbs"]   / 3.0)
        protein_pct = min(100, totals["protein"] / 1.5)
        fat_pct     = min(100, totals["fat"]     / 0.7)
        fig = go.Figure(data=[go.Pie(
            labels=["Carbos","Proteína","Grasa"],
            values=[max(1,totals["carbs"]),max(1,totals["protein"]),max(1,totals["fat"])],
            hole=0.65, marker=dict(colors=[LIME,CYAN,ORANGE]), textinfo="none",
        )])
        fig.update_layout(showlegend=False, margin=dict(l=0,r=0,t=0,b=0), **_LAYOUT_BASE)
        return (
            html.Span("✅ Comida añadida", style={"color": LIME}) if trigger=="btn-add-meal" else "",
            render_meal_list("desayuno"), render_meal_list("almuerzo"),
            render_meal_list("cena"),     render_meal_list("snacks"),
            str(totals["calories"]), f"{totals['carbs']}g", f"{totals['protein']}g", f"{totals['fat']}g",
            {"width":f"{carbs_pct:.0f}%"}, {"width":f"{protein_pct:.0f}%"}, {"width":f"{fat_pct:.0f}%"},
            fig,
        )

    @app.callback(
        [Output("meal-tab-desayuno","className"), Output("meal-tab-almuerzo","className"),
         Output("meal-tab-cena","className"),     Output("meal-tab-snacks","className"),
         Output("meal-type-store","data")],
        [Input("meal-tab-desayuno","n_clicks"), Input("meal-tab-almuerzo","n_clicks"),
         Input("meal-tab-cena","n_clicks"),     Input("meal-tab-snacks","n_clicks")],
        State("meal-type-store","data"),
        prevent_initial_call=True,
    )
    def select_meal_type(n1,n2,n3,n4,current_type):
        tabs = ["desayuno","almuerzo","cena","snacks"]
        ctx  = callback_context
        if ctx.triggered:
            trigger  = ctx.triggered[0]["prop_id"].split(".")[0]
            selected = trigger.replace("meal-tab-","")
        else:
            selected = current_type or "desayuno"
        return (*["meal-tab meal-tab--active" if t==selected else "meal-tab" for t in tabs], selected)

    # ── HIDRATACIÓN ───────────────────────────────────────────
    @app.callback(
        [Output("hydration-liters-text",  "children"),
         Output("hydration-goal-text",    "children"),
         Output("hydration-progress-bar", "style"),
         Output("hydration-milestones",   "children"),
         Output("metric-hydration",       "children", allow_duplicate=True),
         Output("metric-hydration-sub",   "children", allow_duplicate=True)],
        [Input("btn-add-water","n_clicks"), Input("btn-add-water-500","n_clicks"),
         Input("url","pathname")],
        State("current-user","data"),
        prevent_initial_call=True,
    )
    def update_hydration(n1, n2, pathname, current_user):
        if not current_user: raise dash.exceptions.PreventUpdate
        from db import add_hydration, get_hydration
        ctx     = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        if trigger == "btn-add-water":
            hydration = add_hydration(current_user, 0.25)
        elif trigger == "btn-add-water-500":
            hydration = add_hydration(current_user, 0.50)
        else:
            hydration = get_hydration(current_user)
        liters = hydration.get("liters", 0.0)
        goal   = hydration.get("goal",   3.0)
        pct    = min(100, liters / goal * 100) if goal > 0 else 0
        milestones = []
        for mark in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            reached = liters >= mark
            milestones.append(html.Div(
                className="h-milestone" + (" h-milestone--reached" if reached else ""),
                children=[html.Div(className="h-milestone-dot"),
                          html.Div(f"{mark:.1f}L", className="h-milestone-label")],
            ))
        return (f"{liters:.2f} L", f"Objetivo: {goal:.1f} L",
                {"width": f"{pct:.0f}%"}, milestones,
                f"{liters:.1f}L", f"de {goal:.1f}L objetivo")

    # ── OBJETIVOS ─────────────────────────────────────────────
    @app.callback(
        Output("modal-add-goal","is_open"),
        [Input("btn-agregar-objetivo","n_clicks"),
         Input("btn-cancel-goal","n_clicks"),
         Input("btn-submit-goal","n_clicks")],
        State("modal-add-goal","is_open"),
        prevent_initial_call=True,
    )
    def toggle_goal_modal(*args):
        ctx     = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        return trigger == "btn-agregar-objetivo"

    @app.callback(
        [Output("choose-goal-type",   "style"),
         Output("goal-form-container","style"),
         Output("goal-type-icon",     "className"),
         Output("goal-type-text",     "children")],
        [Input("btn-health-goal","n_clicks"),
         Input("btn-fitness-goal","n_clicks"),
         Input("btn-back-to-choose","n_clicks")],
        prevent_initial_call=True,
    )
    def toggle_goal_form(h, f, back):
        ctx     = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        if trigger == "btn-back-to-choose":
            return {"display":"block"}, {"display":"none"}, "bi bi-lightning-charge-fill", "Fitness"
        if trigger == "btn-health-goal":
            return {"display":"none"}, {"display":"block"}, "bi bi-heart-pulse-fill",      "Salud"
        if trigger == "btn-fitness-goal":
            return {"display":"none"}, {"display":"block"}, "bi bi-lightning-charge-fill", "Fitness"
        raise dash.exceptions.PreventUpdate

    @app.callback(
        [Output("goal-success-msg",        "children"),
         Output("goals-display-container", "children"),
         Output("user-goals-store",        "data"),
         Output("goals-summary-stats",     "children")],
        Input("btn-submit-goal","n_clicks"),
        [State("input-goal-name","value"),    State("input-goal-description","value"),
         State("input-goal-target","value"),  State("input-goal-deadline","value"),
         State("goal-type-text","children"),  State("current-user","data")],
        prevent_initial_call=True,
    )
    def submit_goal(n, name, desc, target, deadline, goal_type_text, current_user):
        if not n or not current_user or not name: raise dash.exceptions.PreventUpdate
        from db import add_user_goal, get_user_goals_for_display
        gtype = "health" if goal_type_text == "Salud" else "fitness"
        add_user_goal(current_user, gtype, {"name":name,"description":desc or "",
                                             "target":target or "","deadline":deadline or "1_month"})
        goals = get_user_goals_for_display(current_user)
        return (html.Span("✅ Objetivo guardado", style={"color": LIME}),
                _render_goals(goals), goals, _render_goals_summary(goals))

    @app.callback(
        [Output("goals-display-container",  "children", allow_duplicate=True),
         Output("user-goals-store",         "data",     allow_duplicate=True),
         Output("goals-summary-stats",      "children", allow_duplicate=True),
         Output("goals-upcoming-deadlines", "children")],
        Input("url","pathname"),
        State("current-user","data"),
        prevent_initial_call=True,
    )
    def load_goals(pathname, current_user):
        if pathname != "/inicio" or not current_user: raise dash.exceptions.PreventUpdate
        from db import get_user_goals_for_display
        goals     = get_user_goals_for_display(current_user)
        all_goals = goals.get("fitness",[]) + goals.get("health",[])
        days_map  = {"2_weeks":14,"1_month":30,"3_months":90,"6_months":180,"1_year":365}
        upcoming  = sorted(
            [(days_map.get(g.get("deadline","1_month"),30), g)
             for g in all_goals if g.get("status")!="completed"],
            key=lambda x: x[0]
        )
        deadline_items = [
            html.Div(className="deadline-item", children=[
                html.Span(g.get("emoji","🎯"), className="deadline-emoji"),
                html.Div(className="deadline-info", children=[
                    html.Div(g.get("name",""),        className="deadline-name"),
                    html.Div(f"Vence en ~{days} días", className="deadline-when"),
                ]),
            ])
            for days, g in upcoming[:4]
        ] or [html.P("Sin vencimientos próximos.", className="empty-state-sm")]
        return _render_goals(goals), goals, _render_goals_summary(goals), deadline_items

    # ── LOGOUT ─────────────────────────────────────────────────
    @app.callback(
        [Output("current-user",        "data",     allow_duplicate=True),
         Output("onboarding-completed","data",     allow_duplicate=True),
         Output("user-type-store",     "data",     allow_duplicate=True),
         Output("url",                 "pathname", allow_duplicate=True)],
        [Input("btn-logout","n_clicks"), Input("btn-logout-doctor","n_clicks")],
        prevent_initial_call=True,
    )
    def logout(*args):
        ctx = callback_context
        if not ctx.triggered or not any(n for n in args if n):
            raise dash.exceptions.PreventUpdate
        return None, False, None, "/"


# ─────────────────────────────────────────────────────────────
# HELPERS DE RENDERIZADO
# ─────────────────────────────────────────────────────────────
def _render_workout_history(workouts):
    if not workouts:
        return html.Div(className="empty-state", children=[
            html.I(className="bi bi-calendar-x", style={"fontSize":"2rem","color":MUTED}),
            html.P("Sin sesiones registradas aún.", style={"color":MUTED,"marginTop":"8px"}),
            html.P("Pulsa 'Nueva sesión' para empezar.", style={"color":"#4B5563","fontSize":"0.85rem"}),
        ])
    items = []
    for w in workouts:
        wtype  = w.get("workout_type","otro") or "otro"
        icon   = WORKOUT_ICONS.get(wtype,"🏅")
        rpe    = w.get("rpe",5) or 5; color = rpe_color(rpe)
        dist   = w.get("distance_km",0) or 0
        dur    = w.get("duration_min",0) or 0
        cal    = w.get("calories_burned",0) or 0
        avg_hr = w.get("avg_hr",0) or 0
        zone, zcolor = _zone_label(avg_hr) if avg_hr>0 else ("—",MUTED)
        date   = w.get("workout_date","")
        notes  = w.get("notes","") or ""
        meta   = " · ".join(filter(None,[
            f"{dist:.1f} km" if dist>0 else None,
            f"{dur} min" if dur>0 else None,
            f"{cal} kcal" if cal>0 else None,
            f"{avg_hr} bpm" if avg_hr>0 else None,
        ]))
        items.append(html.Div(className="workout-card", children=[
            html.Div(className="workout-card-icon", children=[html.Span(icon)]),
            html.Div(className="workout-card-body", children=[
                html.Div(className="workout-card-top", children=[
                    html.Span(wtype.replace("_"," ").title(), className="workout-type-label"),
                    html.Span(date, className="workout-date"),
                ]),
                html.Div(meta, className="workout-meta") if meta else None,
                html.Div(notes[:80]+"…" if len(notes)>80 else notes, className="workout-notes") if notes else None,
            ]),
            html.Div(className="workout-card-right", children=[
                html.Span(f"RPE {rpe}", className="rpe-badge-sm", style={"borderColor":color,"color":color}),
                html.Span(zone, className="zone-badge", style={"color":zcolor}) if zone!="—" else None,
            ]),
        ]))
    return items


def _render_goals(goals):
    all_items = []
    dl_map = {"2_weeks":"2 sem","1_month":"1 mes","3_months":"3 meses","6_months":"6 meses","1_year":"1 año"}
    for gtype, label, accent in [("fitness","Fitness",LIME),("health","Salud",CYAN)]:
        for g in goals.get(gtype,[]):
            is_done = g.get("status")=="completed"
            prog    = g.get("progress",0) or 0
            all_items.append(html.Div(
                className="goal-card"+(" goal-card--done" if is_done else ""),
                children=[
                    html.Div(className="goal-card-header", children=[
                        html.Span(g.get("emoji","🎯"), className="goal-emoji"),
                        html.Div(className="goal-card-info", children=[
                            html.Div(g.get("name",""), className="goal-name"),
                            html.Div(g.get("description",""), className="goal-desc") if g.get("description") else None,
                        ]),
                        html.Span("✓ Completado" if is_done else label, className="goal-type-tag",
                                  style={"color":accent,"borderColor":f"{accent}33"}),
                    ]),
                    html.Div(className="goal-meta-row", children=[
                        html.Span(f"Meta: {g.get('target','')}", className="goal-target") if g.get("target") else None,
                        html.Span(f"Plazo: {dl_map.get(g.get('deadline','1_month'),'1 mes')}", className="goal-deadline"),
                    ]),
                    html.Div(className="goal-progress-wrap", children=[
                        html.Div(className="goal-progress-track", children=[
                            html.Div(className="goal-progress-fill",
                                     style={"width":f"{prog}%","backgroundColor":accent}),
                        ]),
                        html.Span(f"{prog}%", className="goal-progress-label", style={"color":accent}),
                    ]),
                ],
            ))
    return all_items or [html.Div(className="empty-state", children=[
        html.P("Sin objetivos todavía. ¡Crea el primero!", className="empty-state-text"),
    ])]


def _render_goals_summary(goals):
    all_goals = goals.get("fitness",[]) + goals.get("health",[])
    total     = len(all_goals)
    completed = sum(1 for g in all_goals if g.get("status")=="completed")
    active    = total - completed
    return [
        html.Div(className="goals-stat-item", children=[
            html.Span(str(total),     className="goals-stat-num"),
            html.Span("Total",        className="goals-stat-label"),
        ]),
        html.Div(className="goals-stat-item", children=[
            html.Span(str(active),    className="goals-stat-num", style={"color":LIME}),
            html.Span("Activos",      className="goals-stat-label"),
        ]),
        html.Div(className="goals-stat-item", children=[
            html.Span(str(completed), className="goals-stat-num", style={"color":CYAN}),
            html.Span("Completados",  className="goals-stat-label"),
        ]),
    ]
