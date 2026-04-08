"""
layouts/athlete.py — Dashboard del Atleta — Athletica Pro
Sección Métricas completamente rediseñada:
  • KPIs avanzados (VO2max, HRV, pace, cadencia, potencia)
  • 8 gráficas profesionales con descarga CSV
  • Upload de datos externos (CSV personalizado)
  • Visualización de datos subidos
  • ACWR con barra visual
  • Tabs por disciplina (Carrera / Ciclismo / Natación / Global)
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from config import HIGHLIGHT_COLOR, TEAL_COLOR, DARK_BACKGROUND

# ─────────────────────────────────────────────────────────────
# PALETA
# ─────────────────────────────────────────────────────────────
LIME   = "#E8FF47"
CYAN   = "#00F5FF"
ORANGE = "#FFB74D"
RED    = "#EF5350"
GREEN  = "#81C784"
PURPLE = "#9C88FF"
DARK1  = "#0D0D0D"
DARK2  = "#141414"
DARK3  = "#1C1C1C"
DARK4  = "#242424"
MUTED  = "#6B7280"
WHITE  = "#F9FAFB"

def _rgb(h):
    h = h.lstrip('#')
    return f'{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}'

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def _kpi_card(vid, label, icon_cls, color, sub_id=None):
    return html.Div(style={
        'background': DARK2, 'borderRadius': '16px',
        'border': '1px solid rgba(255,255,255,0.06)',
        'padding': '22px 24px',
        'display': 'flex', 'alignItems': 'center', 'gap': '16px',
    }, children=[
        html.Div(style={
            'width':'50px','height':'50px','borderRadius':'14px','flexShrink':'0',
            'backgroundColor':f'rgba({_rgb(color)},0.1)',
            'display':'flex','alignItems':'center','justifyContent':'center',
        }, children=[html.I(className=icon_cls, style={'color':color,'fontSize':'1.3rem'})]),
        html.Div([
            html.Div('—', id=vid, style={'fontFamily':'var(--font-display)','fontSize':'2rem','fontWeight':'900','color':color,'lineHeight':'1'}),
            html.Div(label, style={'fontSize':'0.68rem','textTransform':'uppercase','letterSpacing':'0.8px','color':MUTED,'marginTop':'5px'}),
            html.Div(id=sub_id, style={'fontSize':'0.76rem','color':'#9CA3AF','marginTop':'3px'}) if sub_id else None,
        ]),
    ])

def _card(children, cls="pro-card", extra_style=None):
    style = extra_style or {}
    return html.Div(className=cls, style=style, children=children)

def _section_header(title, subtitle="", badge=None):
    return html.Div(className="section-header", children=[
        html.Div([
            html.H2(title, className="section-title"),
            html.P(subtitle, className="section-subtitle") if subtitle else None,
        ]),
        html.Span(badge, className="section-badge") if badge else None,
    ])

def _nav_item(label, btn_id, icon_cls, active=False):
    return html.Button(
        className=f"nav-item {'nav-item--active' if active else ''}",
        id=btn_id, n_clicks=0,
        children=[
            html.I(className=icon_cls, style={"marginRight": "10px", "fontSize": "1rem"}),
            html.Span(label),
        ]
    )

def _chart_card(title, graph_id, height="220px", download_id=None, extra_controls=None):
    """Tarjeta de gráfica con botón de descarga CSV opcional."""
    header_children = [
        html.Span(title, style={
            'fontWeight': '700', 'fontSize': '0.88rem',
            'color': WHITE, 'textTransform': 'uppercase', 'letterSpacing': '0.5px',
        }),
    ]
    if extra_controls:
        header_children.append(extra_controls)
    if download_id:
        header_children.append(
            html.Button(
                [html.I(className="bi bi-download me-1"), "CSV"],
                id=download_id, n_clicks=0,
                style={
                    'background': 'rgba(232,255,71,0.08)',
                    'border': '1px solid rgba(232,255,71,0.25)',
                    'borderRadius': '7px', 'color': LIME,
                    'fontSize': '0.73rem', 'padding': '4px 10px',
                    'cursor': 'pointer', 'fontWeight': '600',
                }
            )
        )
    return html.Div(style={
        'background': DARK2, 'borderRadius': '16px',
        'border': '1px solid rgba(255,255,255,0.06)', 'padding': '20px',
    }, children=[
        html.Div(style={
            'display': 'flex', 'justifyContent': 'space-between',
            'alignItems': 'center', 'marginBottom': '14px', 'gap': '8px',
        }, children=header_children),
        dcc.Graph(
            id=graph_id,
            config={"displayModeBar": False},
            style={"height": height},
        ),
    ])

def _mini_kpi(vid, label, color=LIME):
    return html.Div(style={
        'background': DARK3, 'borderRadius': '12px',
        'border': f'1px solid rgba({_rgb(color)},0.15)',
        'padding': '16px 18px', 'textAlign': 'center', 'flex': '1',
    }, children=[
        html.Div('—', id=vid, style={
            'fontFamily': 'var(--font-display)', 'fontSize': '1.6rem',
            'fontWeight': '900', 'color': color, 'lineHeight': '1',
        }),
        html.Div(label, style={
            'fontSize': '0.67rem', 'color': MUTED,
            'textTransform': 'uppercase', 'letterSpacing': '0.6px', 'marginTop': '5px',
        }),
    ])

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def _sidebar():
    return html.Aside(className="sidebar", children=[
        html.Div(className="sidebar-profile", children=[
            html.Div(id="sidebar-user-avatar", className="sidebar-avatar"),
            html.Div(className="sidebar-info", children=[
                html.Div(id="sidebar-user-fullname", className="sidebar-name"),
                html.Div(id="sidebar-user-level",    className="sidebar-level"),
            ]),
        ]),
        html.Div(className="sidebar-score-block", children=[
            html.Div("Forma física", className="sidebar-score-label"),
            html.Div(id="health-status-dots", className="score-dots"),
            html.Div(id="health-status-description", className="score-desc"),
        ]),
        html.Nav(className="sidebar-nav", children=[
            html.Div("MENÚ PRINCIPAL", className="nav-section-label"),
            _nav_item("Inicio",         "nav-inicio-inicio",         "bi bi-house-door",       active=True),
            _nav_item("Métricas",       "nav-metricas-inicio",       "bi bi-activity"),
            _nav_item("Objetivos",      "nav-objetivos-inicio",      "bi bi-bullseye"),
            _nav_item("Nutrición",      "nav-nutricion-inicio",      "bi bi-egg-fried"),
            _nav_item("Entrenamientos", "nav-entrenamientos-inicio", "bi bi-lightning-charge"),
            html.Div("HERRAMIENTAS", className="nav-section-label", style={"marginTop": "12px"}),
            _nav_item("Vista Médico",   "nav-dashboard-doctor",      "bi bi-heart-pulse"),
        ]),
        html.Div(className="sidebar-footer", children=[
            html.Button(
                [html.I(className="bi bi-box-arrow-left"), " Cerrar sesión"],
                id="btn-logout", n_clicks=0, className="btn-logout"
            ),
        ]),
    ])

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
def _header():
    return html.Header(className="top-header", children=[
        html.Div(className="header-brand", children=[
            html.Div(className="brand-mark", children=[html.Span("A", className="brand-letter")]),
            html.Div(className="brand-text", children=[
                html.Span("ATHLETICA", className="brand-name"),
                html.Span("PRO", className="brand-suffix"),
            ]),
        ]),
        html.Div(className="header-center", children=[
            html.Div(id="doctor-viewing-banner", className="doctor-banner", style={"display": "none"},
                     children=[
                         html.I(className="bi bi-eye me-1"),
                         html.Span("Modo Vista Médica", style={"fontSize": "0.8rem", "fontWeight": "600"}),
                     ]),
            html.Div(className="weekly-bar-wrap", children=[
                html.Div("Progreso semanal", className="weekly-bar-label"),
                html.Div(className="weekly-bar-track", children=[
                    html.Div(id="weekly-progress-bar", className="weekly-bar-fill", style={"width": "65%"}),
                ]),
            ]),
        ]),
        html.Div(className="header-profile", children=[
            html.Div(id="user-profile-avatar", className="header-avatar"),
            html.Div(className="header-user-info", children=[
                html.Div(id="user-profile-name", className="header-user-name"),
                html.Div(id="user-profile-type", className="header-user-type"),
            ]),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
# SECCIÓN INICIO
# ─────────────────────────────────────────────────────────────
def _section_inicio():
    placeholder_txt = (
        'Ej: Correr 10km en menos de 50 minutos el proximo mes.\n\n'
        'Ej: Esta semana quiero completar 3 sesiones de Z2.'
    )
    return html.Div(id='section-inicio', style={'display': 'block', 'padding': '28px 32px', 'width': '100%'}, children=[
        html.Div(id='inicio-greeting', style={'marginBottom': '22px'}),
        html.Div(style={
            'display': 'grid', 'gridTemplateColumns': 'repeat(4,1fr)',
            'gap': '16px', 'marginBottom': '22px',
        }, children=[
            _kpi_card('metric-activity',  'NIVEL ACTIVIDAD',   'bi bi-bar-chart-fill',   CYAN,     None),
            _kpi_card('metric-cals',      'CALORIAS SEMANA',   'bi bi-fire',             ORANGE,   'metric-cals-sub'),
            _kpi_card('metric-hydration', 'HIDRATACION HOY',   'bi bi-droplet-fill',     '#4FC3F7','metric-hydration-sub'),
            _kpi_card('metric-bpm',       'FC ULTIMO ENTRENO', 'bi bi-heart-pulse-fill', LIME,     'metric-bpm-zone'),
        ]),
        html.Div(style={
            'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
            'gap': '16px', 'marginBottom': '16px',
        }, children=[
            html.Div(style={
                'background': DARK2, 'borderRadius': '16px',
                'border': '1px solid rgba(232,255,71,0.18)', 'padding': '26px 28px',
            }, children=[
                html.Div(style={'display':'flex','alignItems':'center','gap':'12px','marginBottom':'16px'}, children=[
                    html.Div(style={
                        'width':'38px','height':'38px','borderRadius':'11px','flexShrink':'0',
                        'backgroundColor':'rgba(232,255,71,0.12)','border':'1px solid rgba(232,255,71,0.25)',
                        'display':'flex','alignItems':'center','justifyContent':'center',
                    }, children=[html.I(className='bi bi-flag-fill', style={'color':LIME,'fontSize':'1rem'})]),
                    html.Div([
                        html.Div('Mi Objetivo', style={'fontWeight':'800','fontSize':'1.05rem','color':WHITE}),
                        html.Div('Escribe tu meta del dia o a largo plazo', style={'color':MUTED,'fontSize':'0.78rem','marginTop':'2px'}),
                    ]),
                ]),
                dcc.Textarea(
                    id='input-objetivo-dia', placeholder=placeholder_txt,
                    style={
                        'width':'100%','minHeight':'150px',
                        'backgroundColor':'rgba(255,255,255,0.03)',
                        'border':'1px solid rgba(255,255,255,0.08)',
                        'borderRadius':'10px','color':'#ddd','fontSize':'0.9rem',
                        'padding':'14px 16px','resize':'vertical','fontFamily':'inherit',
                        'lineHeight':'1.7','outline':'none',
                    }
                ),
                html.Div(style={'display':'flex','justifyContent':'space-between','alignItems':'center','marginTop':'12px'}, children=[
                    html.Div(id='objetivo-saved-msg', style={'fontSize':'0.82rem'}),
                    html.Button(
                        [html.I(className='bi bi-check2 me-1'), 'Guardar'],
                        id='btn-save-objetivo', n_clicks=0,
                        style={
                            'backgroundColor':LIME,'color':'#080808','border':'none',
                            'borderRadius':'9px','padding':'9px 22px',
                            'fontWeight':'800','fontSize':'0.85rem','cursor':'pointer',
                        }
                    ),
                ]),
            ]),
            html.Div(style={
                'background': DARK2, 'borderRadius': '16px',
                'border': '1px solid rgba(255,255,255,0.06)', 'padding': '26px 28px',
            }, children=[
                html.Div(style={'display':'flex','alignItems':'center','gap':'12px','marginBottom':'18px'}, children=[
                    html.Div(style={
                        'width':'38px','height':'38px','borderRadius':'11px','flexShrink':'0',
                        'backgroundColor':'rgba(0,245,255,0.1)','border':'1px solid rgba(0,245,255,0.2)',
                        'display':'flex','alignItems':'center','justifyContent':'center',
                    }, children=[html.I(className='bi bi-calendar-week', style={'color':CYAN,'fontSize':'1rem'})]),
                    html.Div([
                        html.Div('Resumen de la Semana', style={'fontWeight':'800','fontSize':'1.05rem','color':WHITE}),
                        html.Div('Disciplinas completadas esta semana', style={'color':MUTED,'fontSize':'0.78rem','marginTop':'2px'}),
                    ]),
                ]),
                html.Div(id='inicio-week-summary'),
            ]),
        ]),
        html.Div(style={
            'background': DARK2, 'borderRadius': '16px',
            'border': '1px solid rgba(232,255,71,0.18)', 'padding': '26px 28px',
        }, children=[
            html.Div(style={'display':'flex','alignItems':'center','gap':'12px','marginBottom':'14px'}, children=[
                html.Div(style={
                    'width':'38px','height':'38px','borderRadius':'11px','flexShrink':'0',
                    'backgroundColor':'rgba(232,255,71,0.12)','border':'1px solid rgba(232,255,71,0.25)',
                    'display':'flex','alignItems':'center','justifyContent':'center',
                }, children=[html.I(className='bi bi-lightbulb-fill', style={'color':LIME,'fontSize':'1rem'})]),
                html.Div([
                    html.Div('Consejo del Dia', style={'fontWeight':'800','fontSize':'1.05rem','color':LIME}),
                    html.Div(id='training-tip-sport-label', style={'color':MUTED,'fontSize':'0.78rem','marginTop':'2px'}),
                ]),
            ]),
            html.Div(id='training-tip', style={'color':'#ddd','fontSize':'0.92rem','lineHeight':'1.8'}),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
# SECCIÓN MÉTRICAS — REDISEÑADA
# ─────────────────────────────────────────────────────────────
def _section_metricas():

    # ── Tabs de disciplina
    def _disc_tab(label, tid, active=False):
        return html.Button(
            label, id=tid, n_clicks=0,
            style={
                'background': 'rgba(232,255,71,0.12)' if active else 'transparent',
                'border': f'1px solid {"rgba(232,255,71,0.5)" if active else "rgba(255,255,255,0.1)"}',
                'borderRadius': '8px', 'color': LIME if active else MUTED,
                'padding': '7px 18px', 'fontWeight': '700',
                'fontSize': '0.8rem', 'cursor': 'pointer', 'letterSpacing': '0.4px',
            }
        )

    disc_tabs = html.Div(style={'display':'flex','gap':'8px','marginBottom':'24px','flexWrap':'wrap'}, children=[
        _disc_tab("🌐 Global",    "metrics-tab-global",   active=True),
        _disc_tab("🏃 Running",   "metrics-tab-running"),
        _disc_tab("🚴 Ciclismo",  "metrics-tab-cycling"),
        _disc_tab("🏊 Natación",  "metrics-tab-swimming"),
        dcc.Store(id="metrics-active-tab", data="global"),
    ])

    # ── Fila de KPIs avanzados (8 indicadores)
    advanced_kpis = html.Div(style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(4, 1fr)',
        'gap': '12px',
        'marginBottom': '24px',
    }, children=[
        _mini_kpi("adv-kpi-vo2",       "VO₂max (ml/kg/min)", LIME),
        _mini_kpi("adv-kpi-hrv",       "HRV (ms)",            CYAN),
        _mini_kpi("adv-kpi-pace",      "Pace medio",          GREEN),
        _mini_kpi("adv-kpi-cadence",   "Cadencia (ppm)",      ORANGE),
        _mini_kpi("adv-kpi-power",     "Potencia (W)",        PURPLE),
        _mini_kpi("adv-kpi-tss",       "TSS semana",          LIME),
        _mini_kpi("adv-kpi-efficiency","Eficiencia FC",       CYAN),
        _mini_kpi("adv-kpi-fatigue",   "Índice fatiga",       RED),
    ])

    # ── Fila mini-stats semana (los originales)
    week_stats = html.Div(style={
        'display': 'flex', 'gap': '12px', 'marginBottom': '24px', 'flexWrap': 'wrap',
    }, children=[
        html.Div(style={
            'background': DARK3, 'borderRadius': '12px',
            'border': '1px solid rgba(255,255,255,0.07)',
            'padding': '14px 20px', 'flex': '1', 'minWidth': '100px', 'textAlign': 'center',
        }, children=[
            html.Div(id=vid, style={'fontFamily':'var(--font-display)','fontSize':'1.5rem','fontWeight':'900','color':color}),
            html.Div(label, style={'fontSize':'0.67rem','color':MUTED,'textTransform':'uppercase','letterSpacing':'0.5px','marginTop':'4px'}),
        ])
        for vid, label, color in [
            ("stat-sessions",  "Sesiones",    LIME),
            ("stat-km",        "Km semana",   CYAN),
            ("stat-time",      "Horas",       GREEN),
            ("stat-cal-week",  "Kcal",        ORANGE),
            ("stat-avg-rpe",   "RPE medio",   PURPLE),
        ]
    ])

    # ── Fila 1 de gráficas (2 col)
    row1 = html.Div(style={
        'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
        'gap': '16px', 'marginBottom': '16px',
    }, children=[
        _chart_card(
            "Carga de Entrenamiento Semanal (TSS)",
            "chart-weekly-load", height="230px",
            download_id="btn-dl-weekly-load",
        ),
        _chart_card(
            "Distribución por Zona FC",
            "chart-hr-zones", height="230px",
            download_id="btn-dl-hr-zones",
        ),
    ])

    # ── Fila 2 de gráficas (2 col)
    row2 = html.Div(style={
        'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
        'gap': '16px', 'marginBottom': '16px',
    }, children=[
        _chart_card(
            "Evolución del Pace (últimas 20 sesiones)",
            "chart-pace-trend", height="230px",
            download_id="btn-dl-pace",
        ),
        _chart_card(
            "Evolución del RPE (30 días)",
            "chart-rpe-trend", height="230px",
            download_id="btn-dl-rpe",
        ),
    ])

    # ── Fila 3 de gráficas (3 col)
    row3 = html.Div(style={
        'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr',
        'gap': '16px', 'marginBottom': '16px',
    }, children=[
        _chart_card(
            "Estado de Ánimo",
            "chart-mood-trend", height="220px",
            download_id="btn-dl-mood",
        ),
        _chart_card(
            "Volumen km por disciplina",
            "chart-volume-discipline", height="220px",
            download_id="btn-dl-volume",
        ),
        _chart_card(
            "FC Reposo — tendencia",
            "chart-resting-hr", height="220px",
            download_id="btn-dl-resting-hr",
        ),
    ])

    # ── ACWR con barra visual
    acwr_card = html.Div(style={
        'background': DARK2, 'borderRadius': '16px',
        'border': '1px solid rgba(255,255,255,0.06)',
        'padding': '22px 24px', 'marginBottom': '16px',
    }, children=[
        html.Div(style={'display':'flex','justifyContent':'space-between','alignItems':'center','marginBottom':'16px'}, children=[
            html.Div([
                html.Div("Ratio Carga Aguda:Crónica (ACWR)", style={
                    'fontWeight':'700','fontSize':'0.88rem','color':WHITE,
                    'textTransform':'uppercase','letterSpacing':'0.5px',
                }),
                html.Div("1.0 = equilibrio ideal · < 0.8 = infraentrenamiento · > 1.3 = riesgo lesión", style={
                    'fontSize':'0.73rem','color':MUTED,'marginTop':'4px',
                }),
            ]),
            html.Div(style={'display':'flex','alignItems':'center','gap':'16px'}, children=[
                html.Div(id="acwr-ratio-display", style={
                    'fontFamily':'var(--font-display)','fontSize':'2.2rem',
                    'fontWeight':'900','color':LIME,
                }),
                html.Div(id="acwr-status-label", style={
                    'fontSize':'0.82rem','fontWeight':'700',
                    'background':'rgba(232,255,71,0.1)',
                    'border':'1px solid rgba(232,255,71,0.25)',
                    'borderRadius':'8px','padding':'5px 12px',
                }),
            ]),
        ]),
        # Barra ACWR con zonas coloreadas
        html.Div(style={'position':'relative','height':'36px','borderRadius':'10px','overflow':'hidden',
                        'background':f'linear-gradient(to right, #4FC3F7 0%, {GREEN} 20%, {LIME} 40%, {ORANGE} 70%, {RED} 100%)'}, children=[
            # Marcadores de zona
            html.Div(style={'position':'absolute','top':'0','left':'0','right':'0','bottom':'0',
                            'display':'flex','alignItems':'center','justifyContent':'space-around',
                            'padding':'0 8px'}, children=[
                html.Span(t, style={'fontSize':'0.7rem','fontWeight':'700','color':'rgba(0,0,0,0.7)'})
                for t in ["< 0.8", "0.8", "1.0", "1.3", "> 1.5"]
            ]),
            # Indicador de posición actual
            html.Div(id="acwr-bar-container", style={
                'position':'absolute','top':'0','bottom':'0','width':'4px',
                'background':'#fff','boxShadow':'0 0 8px rgba(255,255,255,0.8)',
                'left':'40%','transition':'left 0.6s ease',
            }),
        ]),
        html.Div(style={'display':'flex','justifyContent':'space-between','marginTop':'6px','fontSize':'0.68rem','color':MUTED}, children=[
            html.Span("Infraentrenamiento"),
            html.Span("Zona óptima"),
            html.Span("Riesgo sobrecarga"),
        ]),
    ])

    # ── Panel Upload de datos externos
    upload_panel = html.Div(style={
        'background': DARK2, 'borderRadius': '16px',
        'border': '1px solid rgba(0,245,255,0.2)',
        'padding': '24px', 'marginBottom': '16px',
    }, children=[
        html.Div(style={'display':'flex','alignItems':'center','gap':'12px','marginBottom':'20px'}, children=[
            html.Div(style={
                'width':'40px','height':'40px','borderRadius':'12px','flexShrink':'0',
                'backgroundColor':'rgba(0,245,255,0.1)','border':'1px solid rgba(0,245,255,0.25)',
                'display':'flex','alignItems':'center','justifyContent':'center',
            }, children=[html.I(className="bi bi-cloud-upload-fill", style={'color':CYAN,'fontSize':'1.1rem'})]),
            html.Div([
                html.Div("Importar datos externos", style={'fontWeight':'800','fontSize':'1rem','color':WHITE}),
                html.Div("Sube un CSV de Garmin, Polar, Strava, Wahoo o cualquier fuente", style={'color':MUTED,'fontSize':'0.78rem','marginTop':'2px'}),
            ]),
        ]),

        html.Div(style={'display':'grid','gridTemplateColumns':'1fr auto','gap':'16px','alignItems':'start'}, children=[
            # Upload + instrucciones
            html.Div([
                dcc.Upload(
                    id="upload-metrics-csv",
                    children=html.Div(style={
                        'border': '2px dashed rgba(0,245,255,0.3)',
                        'borderRadius': '12px', 'padding': '28px',
                        'textAlign': 'center', 'cursor': 'pointer',
                        'background': 'rgba(0,245,255,0.03)',
                        'transition': 'all 0.2s',
                    }, children=[
                        html.I(className="bi bi-file-earmark-spreadsheet", style={'fontSize':'2rem','color':CYAN,'display':'block','marginBottom':'10px'}),
                        html.Div("Arrastra un CSV aquí o haz clic para seleccionar", style={'color':WHITE,'fontWeight':'600','fontSize':'0.9rem'}),
                        html.Div("Columnas recomendadas: date, distance_km, duration_min, avg_hr, rpe, pace_min_km, power_w, cadence", style={'color':MUTED,'fontSize':'0.74rem','marginTop':'6px'}),
                    ]),
                    accept=".csv",
                    multiple=False,
                ),
                html.Div(id="upload-metrics-status", style={'marginTop':'10px','fontSize':'0.82rem'}),
            ]),

            # Selector de columna a visualizar
            html.Div(style={'minWidth':'200px'}, children=[
                html.Div("Visualizar columna:", style={'color':MUTED,'fontSize':'0.78rem','marginBottom':'8px','textTransform':'uppercase','letterSpacing':'0.5px'}),
                dcc.Dropdown(
                    id="metrics-csv-column-selector",
                    placeholder="Selecciona columna...",
                    options=[],
                    clearable=False,
                    style={'fontSize':'0.85rem'},
                    className="pro-dropdown",
                ),
                html.Div(style={'marginTop':'10px'}, children=[
                    html.Div("Tipo de gráfica:", style={'color':MUTED,'fontSize':'0.78rem','marginBottom':'8px','textTransform':'uppercase','letterSpacing':'0.5px'}),
                    dcc.Dropdown(
                        id="metrics-csv-chart-type",
                        value="line",
                        clearable=False,
                        className="pro-dropdown",
                        options=[
                            {"label":"📈 Línea", "value":"line"},
                            {"label":"📊 Barras", "value":"bar"},
                            {"label":"⬤  Dispersión","value":"scatter"},
                            {"label":"📉 Área",   "value":"area"},
                        ],
                    ),
                ]),
                html.Button(
                    [html.I(className="bi bi-download me-1"), "Descargar CSV procesado"],
                    id="btn-dl-custom-csv", n_clicks=0,
                    style={
                        'marginTop':'12px','width':'100%',
                        'background':'rgba(0,245,255,0.08)',
                        'border':'1px solid rgba(0,245,255,0.3)',
                        'borderRadius':'9px','color':CYAN,
                        'padding':'9px 0','fontWeight':'700',
                        'fontSize':'0.8rem','cursor':'pointer',
                    }
                ),
                dcc.Download(id="download-custom-csv"),
            ]),
        ]),

        # Gráfica del CSV subido
        html.Div(id="uploaded-csv-chart-wrap", style={'marginTop':'20px','display':'none'}, children=[
            html.Div(style={'display':'flex','justifyContent':'space-between','alignItems':'center','marginBottom':'10px'}, children=[
                html.Div(id="uploaded-csv-chart-title", style={'fontWeight':'700','fontSize':'0.88rem','color':WHITE}),
                html.Div(id="uploaded-csv-stats", style={'display':'flex','gap':'12px'}),
            ]),
            dcc.Graph(
                id="chart-custom-upload",
                config={"displayModeBar": True, "toImageButtonOptions":{"format":"png","filename":"athletica_export"}},
                style={"height": "280px"},
            ),
            # Tabla resumen de estadísticas del CSV
            html.Div(id="uploaded-csv-summary-table", style={'marginTop':'14px'}),
        ]),

        # Store para datos CSV subido
        dcc.Store(id="metrics-csv-store"),
    ])

    # ── Gráfica adicional: evolución FC reposo + VO2max estimado (ancho completo)
    row4 = html.Div(style={
        'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
        'gap': '16px', 'marginBottom': '16px',
    }, children=[
        _chart_card(
            "Eficiencia Cardiaca (FC/pace)",
            "chart-hr-efficiency", height="220px",
            download_id="btn-dl-efficiency",
        ),
        _chart_card(
            "Variabilidad Cardiaca (HRV) — Tendencia",
            "chart-hrv-trend", height="220px",
            download_id="btn-dl-hrv",
        ),
    ])

    # Downloads (dcc.Download para cada gráfica)
    downloads = html.Div([
        dcc.Download(id="dl-weekly-load"),
        dcc.Download(id="dl-hr-zones"),
        dcc.Download(id="dl-pace"),
        dcc.Download(id="dl-rpe"),
        dcc.Download(id="dl-mood"),
        dcc.Download(id="dl-volume"),
        dcc.Download(id="dl-resting-hr"),
        dcc.Download(id="dl-efficiency"),
        dcc.Download(id="dl-hrv"),
    ])

    return html.Div(
        id="section-metricas",
        style={"display": "none", "padding": "28px 32px", "width": "100%"},
        children=[
            _section_header(
                "Métricas & Análisis",
                "Panel de rendimiento avanzado · Running · Ciclismo · Natación · Triatlón",
            ),
            disc_tabs,
            advanced_kpis,
            week_stats,
            row1,
            row2,
            row3,
            acwr_card,
            row4,
            upload_panel,
            downloads,
        ]
    )


# ─────────────────────────────────────────────────────────────
# SECCIÓN OBJETIVOS
# ─────────────────────────────────────────────────────────────
def _section_objetivos():
    return html.Div(id="section-objetivos", style={"display": "none", "padding": "32px 36px", "width": "100%"}, children=[
        _section_header("Mis Objetivos", "Gestiona tus metas deportivas y de salud"),
        html.Div(className="objetivos-layout", children=[
            html.Div(className="objetivos-list-panel", children=[
                html.Div(className="panel-toolbar", children=[
                    html.Div(className="goal-tabs", children=[
                        html.Button("Todos",   id="tab-goals-all",     className="goal-tab goal-tab--active", n_clicks=0),
                        html.Button("Activos", id="tab-goals-active",  className="goal-tab", n_clicks=0),
                        html.Button("Fitness", id="tab-goals-fitness", className="goal-tab", n_clicks=0),
                        html.Button("Salud",   id="tab-goals-health",  className="goal-tab", n_clicks=0),
                    ]),
                    html.Button(
                        [html.I(className="bi bi-plus-lg me-1"), "Nuevo objetivo"],
                        id="btn-agregar-objetivo", n_clicks=0, className="btn-primary-sm"
                    ),
                ]),
                html.Div(id="goals-display-container", className="goals-grid"),
                dcc.Store(id="user-goals-store"),
            ]),
            html.Div(className="objetivos-stats-panel", children=[
                _card([
                    html.Div("Resumen", className="card-title", style={"marginBottom": "16px"}),
                    html.Div(id="goals-summary-stats", className="goals-stats-list"),
                ]),
                _card([
                    html.Div("Próximos vencimientos", className="card-title", style={"marginBottom": "16px"}),
                    html.Div(id="goals-upcoming-deadlines"),
                ]),
            ]),
        ]),
        dbc.Modal(id="modal-add-goal", is_open=False, size="md", centered=True, className="pro-modal", children=[
            dbc.ModalHeader(dbc.ModalTitle("Nuevo Objetivo"), close_button=True, className="pro-modal-header"),
            dbc.ModalBody(className="pro-modal-body", children=[
                html.Div(id="choose-goal-type", children=[
                    html.P("¿Qué tipo de objetivo?", className="modal-subtitle"),
                    html.Div(className="goal-type-picker", children=[
                        html.Button([
                            html.I(className="bi bi-lightning-charge-fill"),
                            html.Span("Fitness"),
                            html.Small("Rendimiento deportivo"),
                        ], id="btn-fitness-goal", n_clicks=0, className="goal-type-card"),
                        html.Button([
                            html.I(className="bi bi-heart-pulse-fill"),
                            html.Span("Salud"),
                            html.Small("Bienestar y salud"),
                        ], id="btn-health-goal", n_clicks=0, className="goal-type-card"),
                    ]),
                ]),
                html.Div(id="goal-form-container", style={"display": "none"}, children=[
                    html.Div(className="goal-form-type-badge", children=[
                        html.I(id="goal-type-icon", className="bi bi-lightning-charge-fill"),
                        html.Span(id="goal-type-text", children="Fitness"),
                        html.Button("← Cambiar", id="btn-back-to-choose", n_clicks=0, className="link-btn"),
                    ]),
                    html.Div(className="form-group", children=[
                        html.Label("Nombre del objetivo *"),
                        dcc.Input(id="input-goal-name", type="text", placeholder="Ej: Correr 10km en menos de 45min", className="pro-input"),
                    ]),
                    html.Div(className="form-group", children=[
                        html.Label("Descripción"),
                        dcc.Textarea(id="input-goal-description", placeholder="¿Por qué es importante para ti?", className="pro-textarea", style={"minHeight": "80px"}),
                    ]),
                    html.Div(className="form-row", children=[
                        html.Div(className="form-group", children=[
                            html.Label("Meta específica"),
                            dcc.Input(id="input-goal-target", type="text", placeholder="Ej: 45:00 min", className="pro-input"),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Plazo"),
                            dcc.Dropdown(id="input-goal-deadline", clearable=False, className="pro-dropdown", value="1_month", options=[
                                {"label": "2 semanas", "value": "2_weeks"},
                                {"label": "1 mes",     "value": "1_month"},
                                {"label": "3 meses",   "value": "3_months"},
                                {"label": "6 meses",   "value": "6_months"},
                                {"label": "1 año",     "value": "1_year"},
                            ]),
                        ]),
                    ]),
                    html.Div(id="goal-success-msg", className="success-msg"),
                ]),
            ]),
            dbc.ModalFooter(className="pro-modal-footer", children=[
                dbc.Button("Cancelar", id="btn-cancel-goal", className="btn-ghost", color="link"),
                dbc.Button([html.I(className="bi bi-check2-circle me-2"), "Guardar objetivo"],
                           id="btn-submit-goal", n_clicks=0, className="btn-primary"),
            ]),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
# SECCIÓN NUTRICIÓN
# ─────────────────────────────────────────────────────────────
def _section_nutricion():
    return html.Div(id="section-nutricion", style={"display": "none", "padding": "32px 36px", "width": "100%"}, children=[
        _section_header("Nutrición & Hidratación", "Seguimiento diario de macros, calorías e ingesta"),
        html.Div(className="nutricion-layout", children=[
            # Panel principal izquierdo
            html.Div(className="nutricion-main", children=[
                # Resumen macros
                _card([
                    html.Div(className="macros-header", children=[
                        html.Div(className="total-cal-display", children=[
                            html.Div(id="total-calories-display", className="total-cal-number"),
                            html.Div("kcal hoy", className="total-cal-label"),
                        ]),
                        dcc.Graph(id="macro-pie-chart", config={"displayModeBar": False}, style={"height": "120px", "width": "120px"}),
                    ]),
                    html.Div(className="macro-bars", children=[
                        html.Div(className="macro-bar-row", children=[
                            html.Span("🌾 Carbos",    className="macro-name"),
                            html.Div(className="macro-track", children=[html.Div(className="macro-fill macro-fill--carbs",    id="macro-carbs-bar")]),
                            html.Span(id="macro-carbs-val",    className="macro-val"),
                        ]),
                        html.Div(className="macro-bar-row", children=[
                            html.Span("🥩 Proteína",  className="macro-name"),
                            html.Div(className="macro-track", children=[html.Div(className="macro-fill macro-fill--protein",  id="macro-protein-bar")]),
                            html.Span(id="macro-protein-val",  className="macro-val"),
                        ]),
                        html.Div(className="macro-bar-row", children=[
                            html.Span("🥑 Grasa",     className="macro-name"),
                            html.Div(className="macro-track", children=[html.Div(className="macro-fill macro-fill--fat",      id="macro-fat-bar")]),
                            html.Span(id="macro-fat-val",      className="macro-val"),
                        ]),
                    ]),
                ]),
                # Hidratación
                _card([
                    html.Div(className="hydration-header", children=[
                        html.Div(className="hydration-main-display", children=[
                            html.Div(id="hydration-liters-text", className="hydration-big-number"),
                            html.Div(id="hydration-goal-text",   className="hydration-goal"),
                        ]),
                        html.Div(className="hydration-actions", children=[
                            html.Button([html.I(className="bi bi-plus-circle me-1"), "+250ml"],
                                        id="btn-add-water", n_clicks=0, className="btn-water"),
                            html.Button([html.I(className="bi bi-plus-circle me-1"), "+500ml"],
                                        id="btn-add-water-500", n_clicks=0, className="btn-water btn-water--lg"),
                        ]),
                    ]),
                    html.Div(className="hydration-progress-track", children=[
                        html.Div(id="hydration-progress-bar", className="hydration-progress-fill"),
                    ]),
                    html.Div(id="hydration-milestones", className="hydration-milestones"),
                ]),
                # Registro comida
                _card([
                    html.Div(className="meal-form-header", children=[
                        html.Div("Añadir comida", className="card-title"),
                        html.Div(className="meal-type-tabs", children=[
                            html.Button("☀️ Desayuno", id="meal-tab-desayuno", className="meal-tab meal-tab--active", n_clicks=0),
                            html.Button("🌤️ Almuerzo", id="meal-tab-almuerzo", className="meal-tab", n_clicks=0),
                            html.Button("🌙 Cena",     id="meal-tab-cena",     className="meal-tab", n_clicks=0),
                            html.Button("🍎 Snack",    id="meal-tab-snacks",   className="meal-tab", n_clicks=0),
                        ]),
                        dcc.Store(id="meal-type-store", data="desayuno"),
                    ]),
                    html.Div(className="meal-input-row", children=[
                        dcc.Input(id="input-meal-description", type="text",
                                  placeholder="Ej: 100g arroz cocido, 150g pollo a la plancha…",
                                  className="pro-input meal-input"),
                        html.Button([html.I(className="bi bi-plus-lg me-1"), "Añadir"],
                                    id="btn-add-meal", n_clicks=0, className="btn-primary-sm"),
                    ]),
                    html.Div(id="meal-success-msg", className="success-msg"),
                ]),
            ]),
            # Panel derecho: log comidas
            html.Div(className="nutricion-sidebar", children=[
                _card([
                    html.Div("Comidas del día", className="card-title", style={"marginBottom": "16px"}),
                    html.Div([
                        html.Div(className="meal-section", children=[
                            html.Div("☀️ Desayuno", className="meal-section-label"),
                            html.Div(id="meals-desayuno"),
                        ]),
                        html.Div(className="meal-section", children=[
                            html.Div("🌤️ Almuerzo", className="meal-section-label"),
                            html.Div(id="meals-almuerzo"),
                        ]),
                        html.Div(className="meal-section", children=[
                            html.Div("🌙 Cena", className="meal-section-label"),
                            html.Div(id="meals-cena"),
                        ]),
                        html.Div(className="meal-section", children=[
                            html.Div("🍎 Snacks", className="meal-section-label"),
                            html.Div(id="meals-snacks"),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
# SECCIÓN ENTRENAMIENTOS
# ─────────────────────────────────────────────────────────────
def _section_entrenamientos():
    return html.Div(id="section-entrenamientos", style={"display": "none", "padding": "32px 36px", "width": "100%"}, children=[
        _section_header("Entrenamientos", "Historial completo de tus sesiones"),
        html.Div(className="entrenamientos-layout", children=[
            html.Div(className="entrenamientos-main", children=[
                html.Div(className="workout-filters", children=[
                    html.Button([html.I(className="bi bi-plus-lg me-1"), "Nueva sesión"],
                                id="btn-open-workout-survey", n_clicks=0, className="btn-primary-sm"),
                ]),
                html.Div(id="workout-history-list", className="workout-history-list"),
            ]),
            html.Div(className="entrenamientos-sidebar", children=[
                _card([
                    html.Div("Este mes", className="card-title", style={"marginBottom": "16px"}),
                    html.Div(id="month-stats-panel"),
                ]),
                _card([
                    html.Div(className="tip-icon-wrap",  children=[html.I(className="bi bi-lightbulb-fill")]),
                    html.Div(id="training-tip", className="training-tip-text"),
                ]),
            ]),
        ]),
    ])


# ─────────────────────────────────────────────────────────────
# MODAL ENCUESTA POST-ENTRENAMIENTO
# ─────────────────────────────────────────────────────────────
def _modal_survey():
    return dbc.Modal(
        id="modal-workout-survey",
        is_open=False, size="lg", centered=True, className="pro-modal",
        children=[
            dbc.ModalHeader(
                dbc.ModalTitle([html.I(className="bi bi-clipboard2-pulse me-2"), "Registrar Sesión"]),
                close_button=True, className="pro-modal-header",
            ),
            dbc.ModalBody(className="pro-modal-body", children=[
                html.Div(className="survey-grid", children=[
                    html.Div(className="survey-col", children=[
                        html.Div(className="form-group", children=[
                            html.Label("Tipo de entrenamiento"),
                            dcc.Dropdown(
                                id="survey-workout-type", placeholder="Selecciona...",
                                clearable=False, className="pro-dropdown",
                                options=[
                                    {"label": "🏃 Carrera fácil",  "value": "carrera_facil"},
                                    {"label": "⚡ Intervalos",     "value": "intervalos"},
                                    {"label": "🎯 Tempo run",      "value": "tempo"},
                                    {"label": "⛰️ Trail running",  "value": "trail"},
                                    {"label": "🚴 Ciclismo",       "value": "ciclismo"},
                                    {"label": "💪 Fuerza",         "value": "fuerza"},
                                    {"label": "🔥 HIIT",           "value": "hiit"},
                                    {"label": "🧘 Yoga/Movilidad", "value": "yoga"},
                                    {"label": "🏊 Natación",       "value": "natacion"},
                                    {"label": "🔄 Recuperación",   "value": "recuperacion"},
                                ],
                            ),
                        ]),
                        html.Div(className="form-row", children=[
                            html.Div(className="form-group", children=[
                                html.Label("Duración (min)"),
                                dcc.Input(id="survey-duration", type="number", placeholder="45", min=1, max=600, className="pro-input"),
                            ]),
                            html.Div(className="form-group", children=[
                                html.Label("Distancia (km)"),
                                dcc.Input(id="survey-distance", type="number", placeholder="10.5", min=0, max=500, step=0.1, className="pro-input"),
                            ]),
                        ]),
                        html.Div(className="form-row", children=[
                            html.Div(className="form-group", children=[
                                html.Label("FC Media (bpm)"),
                                dcc.Input(id="survey-avg-hr", type="number", placeholder="155", min=50, max=220, className="pro-input"),
                            ]),
                            html.Div(className="form-group", children=[
                                html.Label("Calorías estimadas"),
                                dcc.Input(id="survey-calories", type="number", placeholder="450", min=0, max=5000, className="pro-input"),
                            ]),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Notas"),
                            dcc.Textarea(id="survey-notes", placeholder="¿Cómo te fue? ¿Algo destacable?",
                                         className="pro-textarea", style={"minHeight": "80px"}),
                        ]),
                    ]),
                    html.Div(className="survey-col", children=[
                        html.Div(className="form-group rpe-group", children=[
                            html.Div(className="rpe-header", children=[
                                html.Label("Esfuerzo percibido (RPE)"),
                                html.Span(id="survey-rpe-label", className="rpe-badge"),
                            ]),
                            dcc.Slider(id="survey-rpe", min=1, max=10, step=1, value=5,
                                       marks={i: str(i) for i in range(1, 11)},
                                       className="rpe-slider",
                                       tooltip={"placement": "top", "always_visible": False}),
                            html.Div(className="rpe-scale-labels", children=[
                                html.Span("Muy fácil"),
                                html.Span("Máximo esfuerzo"),
                            ]),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Estado de ánimo"),
                            html.Div(className="mood-picker", children=[
                                html.Button(
                                    [html.Span(e, className="mood-emoji"), html.Span(label, className="mood-label")],
                                    id=f"mood-btn-{val}", n_clicks=0, className="mood-btn"
                                )
                                for e, label, val in [
                                    ("😄","Genial","excelente"), ("😊","Bien","bien"),
                                    ("😐","Regular","regular"), ("😓","Cansado","cansado"),
                                    ("😩","Agotado","agotado"),
                                ]
                            ]),
                            dcc.Store(id="survey-mood-store", data="bien"),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Label("Nivel de energía"),
                            dcc.Slider(id="survey-energy", min=1, max=10, step=1, value=6,
                                       marks={1:"1",5:"5",10:"10"}, className="energy-slider",
                                       tooltip={"placement":"top","always_visible":False}),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Div(className="pain-header", children=[
                                html.Label("Dolor o molestia"),
                                html.Span("0 = ninguno", className="form-hint"),
                            ]),
                            dcc.Slider(id="survey-pain", min=0, max=10, step=1, value=0,
                                       marks={0:"0",5:"5",10:"10"}, className="pain-slider",
                                       tooltip={"placement":"top","always_visible":False}),
                        ]),
                        html.Div(id="survey-success-msg", className="success-msg"),
                    ]),
                ]),
            ]),
            dbc.ModalFooter(className="pro-modal-footer", children=[
                dbc.Button("Cancelar", id="btn-cancel-survey", className="btn-ghost", color="link"),
                dbc.Button([html.I(className="bi bi-check2-circle me-2"), "Guardar sesión"],
                           id="btn-submit-survey", n_clicks=0, className="btn-primary"),
            ]),
        ]
    )


# ─────────────────────────────────────────────────────────────
# LAYOUT COMPLETO
# ─────────────────────────────────────────────────────────────
athlete_layout = html.Div(
    id="athlete-container",
    className="athlete-root",
    children=[
        _header(),
        html.Div(className="app-body", children=[
            _sidebar(),
            html.Main(className="main-content", children=[
                _section_inicio(),
                _section_metricas(),
                _section_objetivos(),
                _section_nutricion(),
                _section_entrenamientos(),
            ]),
        ]),
        _modal_survey(),
        html.Button(id="btn-open-workout-survey-2", style={"display": "none"}, n_clicks=0),
    ]
)