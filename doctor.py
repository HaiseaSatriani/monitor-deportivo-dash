"""
layouts/doctor.py — Dashboard del medico.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
from config import HIGHLIGHT_COLOR, TEAL_COLOR, DARK_BACKGROUND

doctor_layout = html.Div(
    id="doctor-container",
    style={"backgroundColor":DARK_BACKGROUND,"minHeight":"100vh","color":"white","fontFamily":"Inter,sans-serif"},
    children=[
        # HEADER
        html.Div(style={"backgroundColor":"#1a1a1a","padding":"15px 40px","borderBottom":"1px solid rgba(0,212,255,0.1)",
                         "display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
            html.Div(style={"display":"flex","alignItems":"center"}, children=[
                html.Div(html.Span("A",style={"color":HIGHLIGHT_COLOR,"fontWeight":"bold","fontSize":"1.2rem"}),
                         style={"width":"40px","height":"40px","backgroundColor":"rgba(0,212,255,0.1)",
                                 "borderRadius":"10px","border":f"2px solid {HIGHLIGHT_COLOR}",
                                 "display":"flex","alignItems":"center","justifyContent":"center","marginRight":"15px"}),
                html.H1("ATHLETICA", style={"color":HIGHLIGHT_COLOR,"fontSize":"1.8rem","fontWeight":"900",
                                             "letterSpacing":"2px","margin":"0"}),
            ]),
            html.Div(style={"flex":"1","height":"1px","backgroundColor":"rgba(0,212,255,0.2)","margin":"0 30px"}),
            html.Div(style={"display":"flex","alignItems":"center","gap":"10px"}, children=[
                html.Div(id="doctor-profile-avatar",
                         style={"width":"45px","height":"45px","backgroundColor":TEAL_COLOR,"borderRadius":"50%",
                                 "display":"flex","alignItems":"center","justifyContent":"center",
                                 "color":"#0a0a0a","fontWeight":"bold","fontSize":"1.2rem"}),
                html.Div(children=[
                    html.Div(id="doctor-profile-name", style={"fontWeight":"600","color":"#fff"}),
                    html.Div("Medico", style={"fontSize":"0.8rem","color":TEAL_COLOR}),
                ]),
            ]),
        ]),

        # BODY: SIDEBAR + MAIN
        html.Div(style={"display":"flex"}, children=[
            # SIDEBAR
            html.Div(style={"width":"300px","padding":"30px","borderRight":"1px solid rgba(0,212,255,0.1)",
                             "backgroundColor":"#141414","minHeight":"calc(100vh - 70px)"}, children=[
                html.H4("Navegacion Medico", style={"color":TEAL_COLOR,"marginBottom":"20px","fontSize":"1.1rem"}),
                html.Button("Dashboard", id="nav-dashboard-doctor", n_clicks=0,
                            style={"width":"100%","padding":"12px","backgroundColor":"rgba(78,205,196,0.1)",
                                   "borderRadius":"10px","border":"none","color":TEAL_COLOR,
                                   "textAlign":"left","marginBottom":"10px","cursor":"pointer","transition":"all 0.3s"}),
                html.Button("Mis Pacientes", id="nav-pacientes-doctor", n_clicks=0,
                            style={"width":"100%","padding":"12px","backgroundColor":"transparent",
                                   "borderRadius":"10px","border":"none","color":"#ccc",
                                   "textAlign":"left","marginBottom":"10px","cursor":"pointer","transition":"all 0.3s"}),
                html.Hr(style={"borderColor":"#2b2b2b","margin":"20px 0"}),
                html.H4("Buscar Pacientes", style={"color":HIGHLIGHT_COLOR,"marginBottom":"12px"}),
                dcc.Input(id="doctor-search-input", type="text", placeholder="Nombre, usuario o email...",
                          debounce=True,
                          style={"width":"100%","padding":"12px","backgroundColor":"#2b2b2b","border":"1px solid #444",
                                 "borderRadius":"8px","color":"white","marginBottom":"12px"}),
                html.Button("Buscar", id="doctor-search-btn", n_clicks=0,
                            style={"width":"100%","padding":"10px","backgroundColor":HIGHLIGHT_COLOR,"border":"none",
                                   "borderRadius":"8px","fontWeight":"600","color":"#0a0a0a","cursor":"pointer","marginBottom":"15px"}),
                html.Div(id="doctor-search-results", style={"maxHeight":"350px","overflowY":"auto"}),
                html.Hr(style={"borderColor":"#2b2b2b","margin":"20px 0"}),
                html.Button([html.I(className="bi bi-box-arrow-left me-2"), "Cerrar Sesion"],
                            id="btn-logout-doctor", n_clicks=0,
                            style={"width":"100%","padding":"10px","backgroundColor":"transparent",
                                   "border":"1px solid rgba(255,100,100,0.3)","borderRadius":"8px",
                                   "color":"#ff6b6b","cursor":"pointer","fontSize":"0.9rem"}),
            ]),
            # MAIN
            html.Div(style={"flex":"1","padding":"40px","overflowY":"auto"}, children=[
                # Trigger de refresco
                dcc.Store(id="doctor-dashboard-refresh-trigger"),
                html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center","marginBottom":"20px"}, children=[
                    html.H2("Panel de Control Medico", style={"color":HIGHLIGHT_COLOR,"margin":"0","fontSize":"2.2rem"}),
                    html.Div(f"Ultima actualizacion: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                             style={"color":"#aaa","fontSize":"0.9rem"}),
                ]),
                html.P("Gestiona tus pacientes, visualiza sus datos de salud y monitoriza su progreso.",
                       style={"color":"#ccc","marginBottom":"30px"}),
                # Stats
                html.Div(style={"backgroundColor":"#1a1a1a","borderRadius":"12px","padding":"20px",
                                 "marginBottom":"25px","border":"1px solid rgba(0,212,255,0.1)"}, children=[
                    html.H4("📊 Estadisticas de Pacientes", style={"color":HIGHLIGHT_COLOR,"marginBottom":"15px"}),
                    html.Div(style={"display":"grid","gridTemplateColumns":"repeat(4,1fr)","gap":"15px"}, children=[
                        html.Div(style={"textAlign":"center"}, children=[
                            html.Div(id="doctor-patient-count",
                                     style={"fontSize":"2rem","fontWeight":"700","color":HIGHLIGHT_COLOR}),
                            html.Div("Total", style={"color":"#ccc","fontSize":"0.85rem"}),
                        ]),
                        html.Div(style={"textAlign":"center"}, children=[
                            html.Div(id="doctor-active-patients-count",
                                     style={"fontSize":"2rem","fontWeight":"700","color":TEAL_COLOR}),
                            html.Div("Activos", style={"color":"#ccc","fontSize":"0.85rem"}),
                        ]),
                        html.Div(style={"textAlign":"center"}, children=[
                            html.Div(id="doctor-avg-activity",
                                     style={"fontSize":"2rem","fontWeight":"700","color":"#ffd166"}),
                            html.Div("Actividad Prom.", style={"color":"#ccc","fontSize":"0.85rem"}),
                        ]),
                        html.Div(style={"textAlign":"center"}, children=[
                            html.Div(id="doctor-risk-patients",
                                     style={"fontSize":"2rem","fontWeight":"700","color":"#ff6b6b"}),
                            html.Div("En Riesgo", style={"color":"#ccc","fontSize":"0.85rem"}),
                        ]),
                    ]),
                ]),
                html.H4("Mis Pacientes", style={"color":HIGHLIGHT_COLOR,"marginBottom":"15px","fontSize":"1.5rem"}),
                html.Div(id="doctor-patients-grid",
                         style={"display":"grid","gridTemplateColumns":"repeat(auto-fill,minmax(340px,1fr))","gap":"20px"}),
            ]),
        ]),
    ]
)
