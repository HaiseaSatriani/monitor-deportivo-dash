"""
callbacks/auth_cb.py — Login, registro, tipo de usuario.
"""
import dash
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from config import HIGHLIGHT_COLOR


def register(app):

    # ── TIPO DE USUARIO en registro ──────────────────────────
    @app.callback(
        [Output("reg-user-type", "data"),
         Output("btn-reg-type-athlete", "style"),
         Output("btn-reg-type-doctor", "style"),
         Output("user-type-indicator", "children")],
        [Input("btn-reg-type-athlete", "n_clicks"),
         Input("btn-reg-type-doctor", "n_clicks")],
        prevent_initial_call=True
    )
    def handle_user_type_selection(athlete_clicks, doctor_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        sel_style = {"background":"rgba(232,255,71,0.07)","border":"2px solid #E8FF47",
                     "borderRadius":"12px","padding":"18px 12px","cursor":"pointer","color":"white",
                     "textAlign":"center","flex":"1","transition":"all 0.25s"}
        unsel_style = {"background":"transparent","border":"1px solid #222",
                        "borderRadius":"12px","padding":"18px 12px","cursor":"pointer","color":"#aaa",
                        "textAlign":"center","flex":"1","transition":"all 0.25s"}

        if trigger == "btn-reg-type-athlete":
            return "athlete", sel_style, unsel_style, "✅ Tipo: Atleta"
        return "doctor", unsel_style, sel_style, "✅ Tipo: Entrenador/a"

    # ── CHECKBOX TERMINOS ─────────────────────────────────────
    @app.callback(
        [Output("accept-terms", "data"),
         Output("terms-checkbox-visual", "children"),
         Output("terms-checkbox-visual", "style")],
        Input("terms-checkbox-visual", "n_clicks"),
        State("accept-terms", "data"),
        prevent_initial_call=True
    )
    def toggle_terms(n, current):
        if not n:
            raise dash.exceptions.PreventUpdate
        new_val = not current
        symbol = "☑" if new_val else "☐"
        color = HIGHLIGHT_COLOR if new_val else "#ccc"
        return new_val, symbol, {"background":"transparent","border":"none","color":color,
                                   "fontSize":"1.4rem","cursor":"pointer","padding":"0"}

    # ── LOGIN ─────────────────────────────────────────────────
    @app.callback(
        [Output("current-user", "data"),
         Output("login-message", "children"),
         Output("onboarding-completed", "data"),
         Output("onboarding-user-name", "data"),
         Output("user-type-store", "data")],
        Input("login-btn", "n_clicks"),
        [State("login-username", "value"),
         State("login-password", "value")],
        prevent_initial_call=True
    )
    def handle_login(n_clicks, identifier, password):
        if not n_clicks:
            raise dash.exceptions.PreventUpdate
        if not identifier or not password:
            return None, "Por favor ingresa usuario y contrasena.", dash.no_update, dash.no_update, dash.no_update

        from db import verify_user
        user_data = verify_user(identifier, password)
        if user_data:
            username  = user_data["username"]
            user_type = user_data.get("user_type", "athlete")
            onboarding_done = user_data.get("onboarding_done", True) if user_type == "athlete" else True
            return username, "", onboarding_done, username, user_type
        return None, "❌ Usuario o contrasena incorrectos.", dash.no_update, dash.no_update, dash.no_update

    # ── REGISTRO ──────────────────────────────────────────────
    @app.callback(
        [Output("current-user",       "data",   allow_duplicate=True),
         Output("register-message",   "children"),
         Output("onboarding-completed","data",  allow_duplicate=True),
         Output("onboarding-user-name","data",  allow_duplicate=True),
         Output("user-type-store",    "data",   allow_duplicate=True)],
        Input("register-btn", "n_clicks"),
        [State("reg-username",  "value"),
         State("reg-email",     "value"),
         State("reg-password",  "value"),
         State("reg-password2", "value"),
         State("accept-terms",  "data"),
         State("reg-user-type", "data")],
        prevent_initial_call=True
    )
    def handle_registration(n_clicks, username, email, password, password2, terms, user_type):
        if not n_clicks:
            raise dash.exceptions.PreventUpdate
        err = lambda msg: (None, html.Span(msg, style={"color":"#ff6b6b"}),
                           dash.no_update, dash.no_update, dash.no_update)

        if not all([username, email, password]):
            return err("❌ Completa todos los campos.")
        if password != password2:
            return err("❌ Las contrasenas no coinciden.")
        if not terms:
            return err("❌ Acepta los terminos y condiciones.")

        from db import save_user, username_or_email_exists
        if username_or_email_exists(username, email):
            return err("❌ El usuario o email ya existe.")

        ok = save_user(username, email, password, full_name=username, user_type=user_type or "athlete")
        if ok:
            utype = user_type or "athlete"
            onboarding_done = (utype == "doctor")
            return (username,
                    html.Span("✅ Registro exitoso! Redirigiendo...", style={"color":"#4ecdc4"}),
                    onboarding_done, username, utype)
        return err("❌ Error al registrar. Intenta nuevamente.")

    # ── REDIRECCION DESPUES DE LOGIN / REGISTRO ───────────────
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("current-user",        "data"),
         Input("onboarding-completed","data"),
         Input("user-type-store",     "data")],
        State("url", "pathname"),
        prevent_initial_call=True
    )
    def redirect_after_auth(current_user, onboarding_done, user_type, pathname):
        if not current_user:
            raise dash.exceptions.PreventUpdate
        if pathname not in ("/login", "/register"):
            raise dash.exceptions.PreventUpdate
        if user_type == "doctor":
            return "/doctor-dashboard"
        if not onboarding_done:
            return "/onboarding"
        return "/inicio"