"""
callbacks/doctor_cb.py — Dashboard del medico: perfil, pacientes, busqueda.
"""
import dash
from dash import Input, Output, State, callback_context, html, ALL
import dash_bootstrap_components as dbc
from config import HIGHLIGHT_COLOR, TEAL_COLOR


def register(app):

    # ── PERFIL del medico ─────────────────────────────────────
    @app.callback(
        [Output("doctor-profile-avatar",        "children"),
         Output("doctor-profile-name",          "children"),
         Output("doctor-patient-count",         "children"),
         Output("doctor-active-patients-count", "children"),
         Output("doctor-avg-activity",          "children"),
         Output("doctor-risk-patients",         "children"),
         Output("doctor-patients-grid",         "children")],
        [Input("url", "pathname"),
         Input("doctor-dashboard-refresh-trigger", "data"),
         Input("current-user", "data")],
    )
    def update_doctor_dashboard(pathname, trigger, current_user):
        if pathname != "/doctor-dashboard" or not current_user:
            raise dash.exceptions.PreventUpdate
        from db import get_doctor, get_doctor_patients, get_user, get_user_activity_level

        doctor = get_doctor(current_user) or {}
        full   = doctor.get("full_name", current_user)
        letter = full[0].upper() if full else "M"

        patient_unames = get_doctor_patients(current_user)
        patients = []
        for u in patient_unames:
            user = get_user(u)
            if user:
                user["username"] = u
                user["activity_level"] = get_user_activity_level(u)
                patients.append(user)

        total   = len(patients)
        active  = len([p for p in patients if p.get("activity_level", 0) >= 4])
        avg_act = round(sum(p.get("activity_level",5) for p in patients) / total, 1) if total else 0
        at_risk = len([p for p in patients if p.get("activity_level", 5) <= 3])

        grid = [_patient_card(p, current_user) for p in patients]
        if not grid:
            grid = [html.P("Sin pacientes aun. Usa la busqueda para agregar.", style={"color":"#888"})]

        return letter, full, total, active, avg_act, at_risk, grid

    # ── BUSQUEDA de pacientes ─────────────────────────────────
    @app.callback(
        Output("doctor-search-results", "children"),
        Input("doctor-search-btn", "n_clicks"),
        [State("doctor-search-input", "value"),
         State("current-user",        "data"),
         State("url", "pathname")],
        prevent_initial_call=True
    )
    def search_patients(n, term, current_user, pathname):
        if pathname != "/doctor-dashboard" or not n or not term:
            raise dash.exceptions.PreventUpdate
        from db import search_users_by_name, get_doctor_patients
        results   = search_users_by_name(term)
        my_patients = get_doctor_patients(current_user)
        if not results:
            return html.P("Sin resultados.", style={"color":"#888","fontSize":"0.9rem"})
        cards = []
        for r in results:
            already = r["username"] in my_patients
            cards.append(html.Div(style={"backgroundColor":"#2b2b2b","borderRadius":"8px","padding":"12px",
                                          "marginBottom":"8px","border":f"1px solid {'rgba(78,205,196,0.4)' if already else 'rgba(0,212,255,0.2)'}"}, children=[
                html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
                    html.Div(children=[
                        html.Div(r.get("full_name", r["username"]),
                                 style={"color":"#fff","fontWeight":"600","fontSize":"0.95rem"}),
                        html.Div(f"@{r['username']} • Nivel {r.get('activity_level',5)}/10",
                                 style={"color":"#ccc","fontSize":"0.8rem"}),
                    ]),
                    html.Button(
                        "Ya es paciente" if already else "+ Agregar",
                        id={"type":"add-patient-btn","patient-username": r["username"]},
                        n_clicks=0, disabled=already,
                        style={"backgroundColor": TEAL_COLOR if already else HIGHLIGHT_COLOR,
                               "border":"none","borderRadius":"6px","padding":"6px 12px",
                               "color":"#0a0a0a","fontWeight":"600","cursor":"default" if already else "pointer",
                               "fontSize":"0.8rem","opacity":"0.7" if already else "1"}
                    ),
                ]),
            ]))
        return html.Div(cards)

    # ── AGREGAR PACIENTE (pattern-match) ──────────────────────
    @app.callback(
        [Output("doctor-dashboard-refresh-trigger", "data", allow_duplicate=True),
         Output("doctor-search-results",            "children", allow_duplicate=True)],
        Input({"type":"add-patient-btn","patient-username": ALL}, "n_clicks"),
        [State("current-user",        "data"),
         State("doctor-search-input", "value"),
         State("url", "pathname")],
        prevent_initial_call=True
    )
    def add_patient(n_clicks_list, current_user, search_term, pathname):
        if pathname != "/doctor-dashboard":
            raise dash.exceptions.PreventUpdate
        ctx = callback_context
        if not ctx.triggered or not any(n for n in n_clicks_list if n):
            raise dash.exceptions.PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json as _json
        prop_dict = _json.loads(triggered.split(".")[0])
        patient_username = prop_dict.get("patient-username")
        if not patient_username:
            raise dash.exceptions.PreventUpdate
        from db import add_patient_to_doctor, search_users_by_name, get_doctor_patients
        add_patient_to_doctor(current_user, patient_username)
        import time
        # Actualizar resultados
        results   = search_users_by_name(search_term or "") if search_term else []
        my_patients = get_doctor_patients(current_user)
        cards = []
        for r in results:
            already = r["username"] in my_patients
            cards.append(html.Div(style={"backgroundColor":"#2b2b2b","borderRadius":"8px","padding":"12px",
                                          "marginBottom":"8px"}, children=[
                html.Div([
                    html.Div(r.get("full_name", r["username"]), style={"color":"#fff","fontWeight":"600"}),
                    html.Div("Ya es tu paciente" if already else "+ Agregar",
                              style={"color": TEAL_COLOR if already else HIGHLIGHT_COLOR,"fontSize":"0.8rem"}),
                ]),
            ]))
        return time.time(), html.Div(cards) if cards else dash.no_update

    # ── ELIMINAR PACIENTE ─────────────────────────────────────
    @app.callback(
        Output("doctor-dashboard-refresh-trigger", "data", allow_duplicate=True),
        Input({"type":"remove-patient-btn","patient-username": ALL}, "n_clicks"),
        [State("current-user", "data"),
         State("url", "pathname")],
        prevent_initial_call=True
    )
    def remove_patient(n_clicks_list, current_user, pathname):
        if pathname != "/doctor-dashboard":
            raise dash.exceptions.PreventUpdate
        ctx = callback_context
        if not ctx.triggered or not any(n for n in n_clicks_list if n):
            raise dash.exceptions.PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json as _json, time
        prop_dict = _json.loads(triggered.split(".")[0])
        patient = prop_dict.get("patient-username")
        if patient:
            from db import remove_patient_from_doctor
            remove_patient_from_doctor(current_user, patient)
        return time.time()

    # ── NAVEGACION medico → inicio (para ver datos paciente) ──
    @app.callback(
        [Output("viewing-patient", "data"),
         Output("url", "pathname", allow_duplicate=True)],
        Input({"type":"view-patient-btn","patient-username": ALL}, "n_clicks"),
        [State("url", "pathname")],
        prevent_initial_call=True
    )
    def view_patient(n_clicks_list, pathname):
        ctx = callback_context
        if not ctx.triggered or not any(n for n in n_clicks_list if n):
            raise dash.exceptions.PreventUpdate
        triggered = ctx.triggered[0]["prop_id"]
        import json as _json
        prop_dict = _json.loads(triggered.split(".")[0])
        patient = prop_dict.get("patient-username")
        return patient, "/inicio"


# ─────────────────────────────────────────────────────────────
# helper: tarjeta de paciente
# ─────────────────────────────────────────────────────────────
def _patient_card(patient, doctor_username):
    username = patient.get("username", "")
    full     = patient.get("full_name", username)
    level    = patient.get("activity_level", 5)
    letter   = full[0].upper() if full else "P"
    risk     = level <= 3
    level_color = "#ff6b6b" if risk else ("#ffd166" if level <= 6 else TEAL_COLOR)

    return html.Div(style={"backgroundColor":"#1a1a1a","borderRadius":"15px","padding":"20px",
                             "border":f"1px solid {'rgba(255,107,107,0.3)' if risk else 'rgba(0,212,255,0.1)'}",
                             "boxShadow":"0 5px 20px rgba(0,0,0,0.3)"}, children=[
        html.Div(style={"display":"flex","alignItems":"center","marginBottom":"15px"}, children=[
            html.Div(letter, style={"width":"50px","height":"50px","backgroundColor":TEAL_COLOR,
                                     "borderRadius":"50%","display":"flex","alignItems":"center",
                                     "justifyContent":"center","color":"#0a0a0a","fontWeight":"bold",
                                     "fontSize":"1.3rem","marginRight":"15px"}),
            html.Div(children=[
                html.Div(full, style={"fontWeight":"700","color":"#fff","fontSize":"1.1rem"}),
                html.Div(f"@{username}", style={"color":"#888","fontSize":"0.85rem"}),
            ]),
            html.Div(f"Nivel {level}/10", style={"marginLeft":"auto","color":level_color,
                                                    "fontWeight":"700","fontSize":"0.95rem"}),
        ]),
        html.Div(style={"display":"flex","gap":"8px"}, children=[
            html.Button("Ver datos",
                id={"type":"view-patient-btn","patient-username":username}, n_clicks=0,
                style={"flex":"1","padding":"8px","backgroundColor":HIGHLIGHT_COLOR,"border":"none",
                       "borderRadius":"8px","color":"#0a0a0a","fontWeight":"600","cursor":"pointer","fontSize":"0.85rem"}),
            html.Button("Eliminar",
                id={"type":"remove-patient-btn","patient-username":username}, n_clicks=0,
                style={"padding":"8px 12px","backgroundColor":"transparent",
                       "border":"1px solid rgba(255,100,100,0.3)","borderRadius":"8px",
                       "color":"#ff6b6b","cursor":"pointer","fontSize":"0.85rem"}),
        ]),
    ])