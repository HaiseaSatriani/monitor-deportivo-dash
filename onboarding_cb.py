"""
callbacks/onboarding_cb.py — Navegacion del wizard de onboarding.
VERSION V4 — barra de progreso, botones pill marcables, calculadora FC/VO2max
"""
import dash
from dash import Input, Output, State, callback_context, html
from config import ONBOARDING_STEPS

N_STEPS = len(ONBOARDING_STEPS)

LIME = "#E8FF47"
CYAN = "#00D4FF"

# Titulos propios para el wizard de corredores
RUNNER_STEPS = [
    {"title": "Tu perfil",        "subtitle": "Cuentanos quien eres, atleta"},
    {"title": "Objetivos",        "subtitle": "Que quieres conseguir corriendo?"},
    {"title": "Rendimiento",      "subtitle": "Parametros para calibrar tus zonas de entrenamiento"},
    {"title": "Salud",            "subtitle": "Lesiones, equipamiento y superficie habitual"},
    {"title": "Estilo de vida",   "subtitle": "Sueno, nutricion y disponibilidad"},
]

# Grupos de botones: { store_id: [lista de valores posibles] }
# El prefijo del id del boton es "store_id" sin "input-" + "-btn-"
BTN_GROUPS = {
    "input-gender":      ["M", "F", "NB", "X"],
    "input-sport-type":  ["RUNNER", "TRIATHLON", "TRAIL", "BIKE_RUN", "MULTI"],
    "input-experience":  ["0", "1", "3", "5", "10", "10p"],
    "input-training-days": ["1", "2", "3", "4", "5", "6", "7"],
    "input-train-type":  ["Z2", "INTERVALS", "TEMPO", "TRAIL", "MIXED"],
    "input-device":      ["garmin", "polar", "coros", "apple", "suunto", "other", "none"],
    "input-surface":     ["road", "track", "trail", "treadmill", "mixed"],
    "input-sleep-quality": ["excellent", "good", "fair", "poor"],
    "input-diet-restrictions": ["NONE", "HIGH_CARB", "LOW_CARB", "KETO", "VEGGIE", "VEGAN", "GLUTEN_FREE"],
    "input-supp-exp":    ["none", "basic", "advanced"],
}

# Prefijos de id de boton para cada store
BTN_ID_PREFIXES = {
    "input-gender":        "gender-btn-",
    "input-sport-type":    "sport-type-btn-",
    "input-experience":    "exp-btn-",
    "input-training-days": "tdays-btn-",
    "input-train-type":    "traintype-btn-",
    "input-device":        "device-btn-",
    "input-surface":       "surface-btn-",
    "input-sleep-quality": "sleepq-btn-",
    "input-diet-restrictions": "diet-btn-",
    "input-supp-exp":      "suppexp-btn-",
}

def _btn_style(active):
    return {
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


def register(app):

    # ── NAVEGACION + barra de progreso + indicador de pasos ──
    @app.callback(
        [Output("onboarding-content",              "children"),
         Output("onboarding-current-step-title",   "children"),
         Output("onboarding-current-step-subtitle","children"),
         Output("onboarding-progress-bar",         "style"),
         Output("onboarding-step-counter",         "children"),
         Output("onboarding-next-btn-visual",       "children"),
         Output("onboarding-prev-btn-visual",       "style"),
         Output("onboarding-step-store",            "data"),
         Output("store-birthdate",                  "data"),
         Output("store-weight",                     "data"),
         Output("store-pr-5k",                      "data")],
        [Input("onboarding-next-btn-visual", "n_clicks"),
         Input("onboarding-prev-btn-visual", "n_clicks")],
        [State("onboarding-step-store", "data"),
         State("url", "pathname"),
         State("store-birthdate", "data"),
         State("store-weight",    "data"),
         State("store-pr-5k",     "data")],
        prevent_initial_call=True,
    )
    def navigate_step(next_n, prev_n, step, pathname, stored_bd, stored_w, stored_5k):
        if pathname != "/onboarding":
            raise dash.exceptions.PreventUpdate

        ctx = callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""
        step = step or 0

        if trigger == "onboarding-next-btn-visual":
            step = min(step + 1, N_STEPS - 1)
        elif trigger == "onboarding-prev-btn-visual":
            step = max(step - 1, 0)

        from layouts.onboarding import STEP_BUILDERS
        content      = STEP_BUILDERS[step]()
        meta         = RUNNER_STEPS[step]
        progress_pct = int((step + 1) / N_STEPS * 100)

        next_children = [
            "Finalizar",
            html.I(className="bi bi-check2 ms-2")
        ] if step == N_STEPS - 1 else [
            "Siguiente",
            html.I(className="bi bi-arrow-right ms-2")
        ]

        prev_style = {
            "backgroundColor": "transparent", "border": "1px solid #2a2a2a",
            "color": "#333", "borderRadius": "10px", "padding": "11px 24px",
            "fontWeight": "600", "fontSize": "0.9rem",
            "cursor": "default", "pointerEvents": "none",
        } if step == 0 else {
            "backgroundColor": "transparent", "border": "1px solid #2a2a2a",
            "color": "#555", "borderRadius": "10px", "padding": "11px 24px",
            "fontWeight": "600", "fontSize": "0.9rem",
        }

        progress_style = {
            "height": "100%",
            "width": f"{progress_pct}%",
            "background": f"linear-gradient(90deg, {LIME}, {CYAN})",
            "transition": "width 0.5s ease",
            "borderRadius": "4px",
        }

        # When leaving step 1 (step was 0, now going to 1), capture its inputs via State
        # But inputs are in the DOM only when step==0. We save them from previous stored values
        # or from the content render — we pass stored values through unchanged unless step was 0
        # NOTE: We can't read input-birthdate here directly (it's inside onboarding-content which
        # hasn't re-rendered yet). So we keep stored values; step1 inputs are saved by a separate
        # lightweight callback below that fires on input change.
        return (
            content,
            meta["title"],
            meta["subtitle"],
            progress_style,
            f"Paso {step + 1} de {N_STEPS}",
            next_children,
            prev_style,
            step,
            stored_bd,
            stored_w,
            stored_5k,
        )

    # ── FINALIZAR onboarding ──────────────────────────────────
    @app.callback(
        [Output("onboarding-completed", "data",    allow_duplicate=True),
         Output("url",                  "pathname", allow_duplicate=True)],
        Input("onboarding-next-btn-visual", "n_clicks"),
        [State("onboarding-step-store", "data"),
         State("current-user",          "data"),
         State("url",                   "pathname")],
        prevent_initial_call=True,
    )
    def finish_onboarding(n_clicks, step, current_user, pathname):
        if pathname != "/onboarding":
            raise dash.exceptions.PreventUpdate
        if not n_clicks or (step or 0) < N_STEPS - 1:
            raise dash.exceptions.PreventUpdate
        if current_user:
            from db import mark_onboarding_completed
            mark_onboarding_completed(current_user)
        return True, "/inicio"

    # ── INDICADOR DE VOLUMEN SEMANAL ──────────────────────────
    @app.callback(
        Output("activity-level-indicator", "children"),
        Input("input-activity-level", "value"),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def update_activity_indicator(level, pathname):
        if pathname != "/onboarding" or not level:
            raise dash.exceptions.PreventUpdate
        if level <= 10:   label, color = "Principiante",   "#81C784"
        elif level <= 30: label, color = "Amateur",        LIME
        elif level <= 60: label, color = "Intermedio",     "#FFB74D"
        elif level <= 90: label, color = "Avanzado",       "#FF8A65"
        else:             label, color = "Elite / Ultra",  "#EF5350"
        return html.Span(
            f"{level} km/semana — {label}",
            style={"color": color, "fontSize": "0.88rem", "fontWeight": "600"}
        )

    # ── BOTONES PILL: un callback por grupo ──────────────────
    # Patron: al pulsar cualquier boton del grupo, se actualiza el Store
    # y se devuelven los estilos de todos los botones del grupo.

    def _make_pill_callback(store_id, values, prefix):
        btn_ids = [prefix + v for v in values]
        outputs = [Output(bid, "style") for bid in btn_ids] + [Output(store_id, "data")]
        inputs  = [Input(bid, "n_clicks") for bid in btn_ids]
        states  = [State(store_id, "data")]

        @app.callback(outputs, inputs, states, prevent_initial_call=True)
        def _pill_cb(*args):
            n_list   = args[:len(values)]
            current  = args[-1]
            ctx = callback_context
            if not ctx.triggered:
                raise dash.exceptions.PreventUpdate
            trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
            # Extraer el valor seleccionado del id del boton
            selected = trigger_id.replace(prefix, "")
            styles = [_btn_style(v == selected) for v in values]
            return styles + [selected]

        return _pill_cb

    # Registrar un callback por cada grupo de botones
    _callbacks = {}
    for store_id, values in BTN_GROUPS.items():
        prefix = BTN_ID_PREFIXES[store_id]
        _callbacks[store_id] = _make_pill_callback(store_id, values, prefix)

    # ── CALCULADORA AUTOMATICA FC / VO2MAX ───────────────────
    # ── Guardar campos del paso 1 en Stores mientras se editan ──
    @app.callback(
        [Output("store-birthdate", "data", allow_duplicate=True),
         Output("store-weight",    "data", allow_duplicate=True)],
        [Input("input-birthdate",  "value"),
         Input("input-weight",     "value")],
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def save_step1_fields(birthdate, weight, pathname):
        if pathname != "/onboarding":
            raise dash.exceptions.PreventUpdate
        return birthdate, weight

    @app.callback(
        Output("store-pr-5k", "data", allow_duplicate=True),
        Input("input-pr-5k",  "value"),
        State("url", "pathname"),
        prevent_initial_call=True,
    )
    def save_pr5k(pr_5k, pathname):
        if pathname != "/onboarding":
            raise dash.exceptions.PreventUpdate
        return pr_5k

    @app.callback(
        [Output("calc-hr-result", "children"),
         Output("input-max-hr",   "value"),
         Output("input-vo2max",   "value")],
        Input("btn-calc-hr", "n_clicks"),
        [State("store-birthdate", "data"),
         State("store-weight",    "data"),
         State("store-pr-5k",     "data"),
         State("input-max-hr",    "value"),
         State("input-vo2max",    "value"),
         State("url",             "pathname")],
        prevent_initial_call=True,
    )
    def calc_hr(n_clicks, birthdate, weight, pr_5k, current_max_hr, current_vo2, pathname):
        if pathname != "/onboarding" or not n_clicks:
            raise dash.exceptions.PreventUpdate

        results = []
        new_max_hr = current_max_hr
        new_vo2    = current_vo2

        # ── Calcular edad desde DD/MM/AAAA
        age = None
        if birthdate:
            try:
                from datetime import datetime
                parts = birthdate.strip().split("/")
                if len(parts) == 3:
                    birth = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                    age   = (datetime.now() - birth).days // 365
            except Exception:
                pass

        # ── FC maxima (formula Tanaka: 208 - 0.7 * edad)
        if not current_max_hr and age:
            new_max_hr = round(208 - 0.7 * age)
            results.append(html.Div(style={"marginBottom": "8px"}, children=[
                html.Span("FC maxima estimada: ", style={"color": "#666", "fontSize": "0.88rem"}),
                html.Span(f"{new_max_hr} lpm", style={"color": LIME, "fontWeight": "700"}),
                html.Span(f"  (formula Tanaka, edad {age} anos)", style={"color": "#444", "fontSize": "0.8rem"}),
            ]))
        elif not age:
            results.append(html.Div(
                "Rellena tu fecha de nacimiento en el paso 1 para calcular la FC maxima.",
                style={"color": "#EF5350", "fontSize": "0.85rem", "marginBottom": "8px"}
            ))

        # ── VO2max desde ritmo de 5K (formula de Cooper aproximada)
        # VO2max = 483 / (tiempo_5k_min) + 3.5   (Cooper inverso simplificado)
        if not current_vo2 and pr_5k:
            try:
                parts = str(pr_5k).strip().split(":")
                t_min = float(parts[0]) + (float(parts[1]) / 60 if len(parts) > 1 else 0)
                # Pace en min/km -> VO2max estimado (Daniels & Gilbert)
                # VO2max = (-4.60 + 0.182258 * speed + 0.000104 * speed^2) / (0.8 + 0.1894393 * e^(-0.012778*t) + 0.2989558 * e^(-0.1932605*t))
                # Simplificado: usamos velocidad media en m/min
                speed_m_min = 5000 / (t_min * 60) * 60  # m/min
                vo2_raw     = -4.60 + 0.182258 * speed_m_min + 0.000104 * (speed_m_min ** 2)
                new_vo2     = round(max(20, min(90, vo2_raw)))
                results.append(html.Div(style={"marginBottom": "8px"}, children=[
                    html.Span("VO2max estimado: ", style={"color": "#666", "fontSize": "0.88rem"}),
                    html.Span(f"{new_vo2} ml/kg/min", style={"color": CYAN, "fontWeight": "700"}),
                    html.Span("  (estimado por ritmo de 5K)", style={"color": "#444", "fontSize": "0.8rem"}),
                ]))
            except Exception:
                results.append(html.Div(
                    "Formato de marca 5K invalido. Usa MM:SS (ej: 22:30).",
                    style={"color": "#EF5350", "fontSize": "0.85rem", "marginBottom": "8px"}
                ))
        elif not current_vo2 and not pr_5k:
            results.append(html.Div(
                "Introduce tu marca de 5K en el apartado de marcas personales para estimar el VO2max.",
                style={"color": "#666", "fontSize": "0.85rem", "marginBottom": "8px"}
            ))

        # Zonas de FC si tenemos max_hr
        hr = new_max_hr or current_max_hr
        if hr:
            z1 = round(hr * 0.50), round(hr * 0.60)
            z2 = round(hr * 0.60), round(hr * 0.70)
            z3 = round(hr * 0.70), round(hr * 0.80)
            z4 = round(hr * 0.80), round(hr * 0.90)
            z5 = round(hr * 0.90), hr
            zone_colors = ["#4FC3F7","#81C784", LIME, "#FFB74D","#EF5350"]
            zones_data  = [("Z1 Recuperacion",z1),("Z2 Aerobico",z2),("Z3 Tempo",z3),("Z4 Umbral",z4),("Z5 Maximo",z5)]
            results.append(html.Div(style={"marginTop": "12px", "marginBottom": "4px"}, children=[
                html.Span("Zonas de FC calculadas:", style={"color": "#aaa", "fontSize": "0.85rem", "fontWeight": "600"}),
            ]))
            results.append(html.Div(
                style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginTop": "8px"},
                children=[
                    html.Div(style={
                        "padding": "8px 12px", "borderRadius": "8px",
                        "border": f"1px solid {zone_colors[i]}33",
                        "backgroundColor": f"{zone_colors[i]}11",
                    }, children=[
                        html.Div(name, style={"color": zone_colors[i], "fontSize": "0.75rem", "fontWeight": "700"}),
                        html.Div(f"{lo}-{hi} lpm", style={"color": "white", "fontSize": "0.85rem"}),
                    ])
                    for i, (name, (lo, hi)) in enumerate(zones_data)
                ]
            ))

        if not results:
            results = [html.Span("Rellena fecha de nacimiento y/o marca de 5K para calcular.",
                                 style={"color": "#666", "fontSize": "0.85rem"})]

        return results, new_max_hr, new_vo2