"""
layouts/auth.py — Welcome, Login, Register layouts.
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HIGHLIGHT_COLOR

LIME = "#E8FF47"
CYAN = "#00D4FF"

# ─────────────────────────────────────────────────────────────
# WELCOME
# ─────────────────────────────────────────────────────────────
welcome_layout = html.Div(
    className="welcome-container",
    children=[
        html.Div(className="header-content", children=[
            html.Div(
                html.Span("A", style={"color": HIGHLIGHT_COLOR, "fontWeight": "bold", "fontSize": "2.5rem"}),
                className="logo-placeholder"
            ),
            html.H1("ATHLETICA", className="main-title"),
            html.H4("Tu guia definitiva para la salud y el bienestar.", className="subtitle"),
        ]),
        html.Div(className="features-grid", children=[
            html.Div(className="feature-card", children=[
                html.I(className="bi bi-calendar-check icon"),
                html.P("Seguimiento Inteligente de Habitos", className="card-title"),
                html.P("Registra actividad, sueno y nutricion.", className="card-text"),
            ]),
            html.Div(className="feature-card", children=[
                html.I(className="bi bi-activity icon"),
                html.P("Monitoreo de Bienestar", className="card-title"),
                html.P("Analiza rendimiento y niveles de fatiga.", className="card-text"),
            ]),
            html.Div(className="feature-card", children=[
                html.I(className="bi bi-bar-chart-line icon"),
                html.P("Reportes de Progreso", className="card-title"),
                html.P("Visualiza tu evolucion con graficos claros.", className="card-text"),
            ]),
        ]),
        html.Div(className="button-section", children=[
            dcc.Link(dbc.Button("Comenzar", className="auth-btn btn-primary-action"), href="/login", className="mx-3"),
            dcc.Link(dbc.Button("Crear cuenta", outline=True, className="mx-3", style={"color": HIGHLIGHT_COLOR, "borderColor": HIGHLIGHT_COLOR, "padding": "14px 40px", "borderRadius": "50px"}), href="/register"),
        ]),
        html.P("Datos cifrados de extremo a extremo", style={"color": "#888", "marginTop": "20px", "fontSize": "1.05rem"}),
    ]
)

# ─────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────
login_layout = html.Div(
    style={
        "minHeight": "100vh",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "backgroundColor": "#080808",
        "fontFamily": "'Inter', sans-serif",
        "padding": "20px",
    },
    children=[
        html.Div(
            style={
                "display": "flex",
                "width": "100%",
                "maxWidth": "1100px",
                "minHeight": "600px",
                "borderRadius": "24px",
                "overflow": "hidden",
                "boxShadow": "0 30px 80px rgba(0,0,0,0.8)",
                "border": "1px solid rgba(255,255,255,0.06)",
            },
            children=[
                # ── Panel izquierdo decorativo ──────────────
                html.Div(
                    style={
                        "flex": "1",
                        "background": "linear-gradient(160deg, #0f0f0f 0%, #111 40%, #0a150a 100%)",
                        "padding": "60px 50px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "space-between",
                        "position": "relative",
                        "overflow": "hidden",
                        "borderRight": "1px solid rgba(232,255,71,0.08)",
                    },
                    children=[
                        # Círculo decorativo de fondo
                        html.Div(style={
                            "position": "absolute", "width": "400px", "height": "400px",
                            "borderRadius": "50%", "top": "-100px", "right": "-150px",
                            "background": "radial-gradient(circle, rgba(232,255,71,0.06) 0%, transparent 70%)",
                            "pointerEvents": "none",
                        }),
                        html.Div(style={
                            "position": "absolute", "width": "300px", "height": "300px",
                            "borderRadius": "50%", "bottom": "-80px", "left": "-100px",
                            "background": "radial-gradient(circle, rgba(0,212,255,0.05) 0%, transparent 70%)",
                            "pointerEvents": "none",
                        }),
                        # Logo
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "gap": "14px"},
                            children=[
                                html.Div(
                                    "A",
                                    style={
                                        "width": "44px", "height": "44px",
                                        "backgroundColor": LIME,
                                        "borderRadius": "12px",
                                        "display": "flex", "alignItems": "center", "justifyContent": "center",
                                        "fontWeight": "900", "fontSize": "1.4rem", "color": "#080808",
                                    }
                                ),
                                html.Span("ATHLETICA", style={
                                    "color": "white", "fontWeight": "800",
                                    "fontSize": "1.5rem", "letterSpacing": "3px",
                                }),
                            ]
                        ),
                        # Texto central
                        html.Div(children=[
                            html.Div(style={
                                "display": "inline-block", "padding": "6px 14px",
                                "backgroundColor": "rgba(232,255,71,0.1)",
                                "borderRadius": "50px", "marginBottom": "24px",
                                "border": "1px solid rgba(232,255,71,0.2)",
                            }, children=[
                                html.Span("Tu rendimiento, en datos", style={
                                    "color": LIME, "fontSize": "1.1rem", "fontWeight": "600", "letterSpacing": "1px",
                                }),
                            ]),
                            html.H2("Bienvenido de nuevo.", style={
                                "color": "white", "fontSize": "2.7rem", "fontWeight": "800",
                                "lineHeight": "1.2", "margin": "0 0 16px 0",
                            }),
                            html.P("Accede a tu panel de rendimiento, historial de entrenamientos y métricas de salud personalizadas.", style={
                                "color": "#666", "fontSize": "1.05rem", "lineHeight": "1.7", "margin": "0 0 36px 0",
                            }),
                            # Stats decorativos
                            html.Div(style={"display": "flex", "gap": "30px"}, children=[
                                html.Div(children=[
                                    html.Div("98%", style={"color": LIME, "fontSize": "2rem", "fontWeight": "800"}),
                                    html.Div("Satisfacción", style={"color": "#555", "fontSize": "1.1rem"}),
                                ]),
                                html.Div(style={"width": "1px", "backgroundColor": "#222"}),
                                html.Div(children=[
                                    html.Div("12K+", style={"color": CYAN, "fontSize": "2rem", "fontWeight": "800"}),
                                    html.Div("Atletas activos", style={"color": "#555", "fontSize": "1.1rem"}),
                                ]),
                                html.Div(style={"width": "1px", "backgroundColor": "#222"}),
                                html.Div(children=[
                                    html.Div("4.9★", style={"color": "white", "fontSize": "2rem", "fontWeight": "800"}),
                                    html.Div("Valoración", style={"color": "#555", "fontSize": "1.1rem"}),
                                ]),
                            ]),
                        ]),
                        # Footer
                        html.P("© 2025 Athletica · Datos cifrados end-to-end", style={
                            "color": "#333", "fontSize": "1.08rem",
                        }),
                    ]
                ),
                # ── Panel derecho: formulario ────────────────
                html.Div(
                    style={
                        "width": "460px",
                        "flexShrink": "0",
                        "backgroundColor": "#0f0f0f",
                        "padding": "60px 50px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                    },
                    children=[
                        html.H2("Iniciar sesión", style={
                            "color": "white", "fontSize": "2.2rem", "fontWeight": "800",
                            "marginBottom": "8px", "marginTop": "0",
                        }),
                        html.P("Introduce tus credenciales para continuar.", style={
                            "color": "#555", "marginBottom": "40px", "fontSize": "1.1rem",
                        }),

                        # Campo usuario
                        html.Div(style={"marginBottom": "18px"}, children=[
                            html.Label("Usuario o Email", style={
                                "color": "#888", "fontSize": "1.1rem", "fontWeight": "600",
                                "letterSpacing": "0.5px", "display": "block", "marginBottom": "8px",
                            }),
                            html.Div(style={"position": "relative"}, children=[
                                html.I(className="bi bi-person", style={
                                    "position": "absolute", "left": "16px", "top": "50%",
                                    "transform": "translateY(-50%)", "color": "#444", "fontSize": "1.1rem",
                                    "zIndex": "1", "pointerEvents": "none",
                                }),
                                dcc.Input(
                                    id="login-username", type="text",
                                    placeholder="tu_usuario o email@ejemplo.com",
                                    debounce=False,
                                    style={
                                        "width": "100%", "padding": "14px 16px 14px 44px",
                                        "backgroundColor": "#161616",
                                        "border": "1px solid #222",
                                        "borderRadius": "12px", "color": "white",
                                        "fontSize": "1.05rem", "boxSizing": "border-box",
                                        "outline": "none", "transition": "border-color 0.2s",
                                    }
                                ),
                            ]),
                        ]),

                        # Campo contraseña
                        html.Div(style={"marginBottom": "28px"}, children=[
                            html.Label("Contraseña", style={
                                "color": "#888", "fontSize": "1.1rem", "fontWeight": "600",
                                "letterSpacing": "0.5px", "display": "block", "marginBottom": "8px",
                            }),
                            html.Div(style={"position": "relative"}, children=[
                                html.I(className="bi bi-lock", style={
                                    "position": "absolute", "left": "16px", "top": "50%",
                                    "transform": "translateY(-50%)", "color": "#444", "fontSize": "1.1rem",
                                    "zIndex": "1", "pointerEvents": "none",
                                }),
                                dcc.Input(
                                    id="login-password", type="password",
                                    placeholder="••••••••••",
                                    debounce=False,
                                    style={
                                        "width": "100%", "padding": "14px 16px 14px 44px",
                                        "backgroundColor": "#161616",
                                        "border": "1px solid #222",
                                        "borderRadius": "12px", "color": "white",
                                        "fontSize": "1.05rem", "boxSizing": "border-box",
                                        "outline": "none", "transition": "border-color 0.2s",
                                    }
                                ),
                            ]),
                        ]),

                        # Botón login
                        dbc.Button(
                            [html.Span("Entrar a Athletica"), html.I(className="bi bi-arrow-right ms-2")],
                            id="login-btn",
                            style={
                                "width": "100%", "padding": "15px",
                                "backgroundColor": LIME, "border": "none",
                                "borderRadius": "12px", "color": "#080808",
                                "fontWeight": "800", "fontSize": "1.1rem",
                                "cursor": "pointer", "letterSpacing": "0.3px",
                                "transition": "all 0.2s",
                            }
                        ),
                        html.Div(id="login-message", style={"marginTop": "12px", "fontSize": "1.08rem", "textAlign": "center"}),

                        # Separador
                        html.Div(style={
                            "display": "flex", "alignItems": "center", "gap": "16px",
                            "margin": "32px 0",
                        }, children=[
                            html.Div(style={"flex": "1", "height": "1px", "backgroundColor": "#1e1e1e"}),
                            html.Span("¿No tienes cuenta?", style={"color": "#444", "fontSize": "0.92rem", "whiteSpace": "nowrap"}),
                            html.Div(style={"flex": "1", "height": "1px", "backgroundColor": "#1e1e1e"}),
                        ]),

                        # Link a registro
                        dcc.Link(
                            dbc.Button(
                                "Crear cuenta gratis",
                                style={
                                    "width": "100%", "padding": "13px",
                                    "backgroundColor": "transparent",
                                    "border": "1px solid #2a2a2a",
                                    "borderRadius": "12px", "color": "#aaa",
                                    "fontWeight": "600", "fontSize": "1.05rem",
                                    "cursor": "pointer", "transition": "all 0.2s",
                                }
                            ),
                            href="/register"
                        ),
                    ]
                ),
            ]
        )
    ]
)

# ─────────────────────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────────────────────
def _type_btn(btn_id, emoji, title, subtitle, selected=False):
    border = f"2px solid {LIME}" if selected else "1px solid #222"
    bg = "rgba(232,255,71,0.07)" if selected else "transparent"
    return html.Button(
        [
            html.Div(emoji, style={"fontSize": "2.2rem", "marginBottom": "8px"}),
            html.H4(title, style={
                "color": LIME if selected else "#aaa",
                "marginBottom": "4px", "fontSize": "1.05rem", "fontWeight": "700", "margin": "6px 0 4px 0",
            }),
            html.P(subtitle, style={"color": "#555", "fontSize": "1.08rem", "margin": "0"}),
        ],
        id=btn_id, n_clicks=0,
        style={
            "background": bg, "border": border, "borderRadius": "12px",
            "padding": "18px 12px", "cursor": "pointer", "color": "white",
            "textAlign": "center", "flex": "1", "transition": "all 0.25s",
        }
    )

register_layout = html.Div(
    style={
        "minHeight": "100vh",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "backgroundColor": "#080808",
        "fontFamily": "'Inter', sans-serif",
        "padding": "20px",
    },
    children=[
        html.Div(
            style={
                "display": "flex",
                "width": "100%",
                "maxWidth": "1100px",
                "minHeight": "640px",
                "borderRadius": "24px",
                "overflow": "hidden",
                "boxShadow": "0 30px 80px rgba(0,0,0,0.8)",
                "border": "1px solid rgba(255,255,255,0.06)",
            },
            children=[
                # ── Panel izquierdo decorativo ──────────────
                html.Div(
                    style={
                        "flex": "1",
                        "background": "linear-gradient(160deg, #0f0f0f 0%, #0a150a 60%, #0d1a0d 100%)",
                        "padding": "60px 50px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "space-between",
                        "position": "relative",
                        "overflow": "hidden",
                        "borderRight": "1px solid rgba(232,255,71,0.08)",
                    },
                    children=[
                        html.Div(style={
                            "position": "absolute", "width": "350px", "height": "350px",
                            "borderRadius": "50%", "top": "-80px", "right": "-120px",
                            "background": "radial-gradient(circle, rgba(232,255,71,0.07) 0%, transparent 70%)",
                            "pointerEvents": "none",
                        }),
                        # Logo
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "gap": "14px"},
                            children=[
                                html.Div("A", style={
                                    "width": "44px", "height": "44px",
                                    "backgroundColor": LIME, "borderRadius": "12px",
                                    "display": "flex", "alignItems": "center", "justifyContent": "center",
                                    "fontWeight": "900", "fontSize": "1.4rem", "color": "#080808",
                                }),
                                html.Span("ATHLETICA", style={
                                    "color": "white", "fontWeight": "800",
                                    "fontSize": "1.5rem", "letterSpacing": "3px",
                                }),
                            ]
                        ),
                        # Texto central
                        html.Div(children=[
                            html.Div(style={
                                "display": "inline-block", "padding": "6px 14px",
                                "backgroundColor": "rgba(232,255,71,0.1)",
                                "borderRadius": "50px", "marginBottom": "24px",
                                "border": "1px solid rgba(232,255,71,0.2)",
                            }, children=[
                                html.Span("Empieza hoy, gratis", style={
                                    "color": LIME, "fontSize": "1.1rem", "fontWeight": "600", "letterSpacing": "1px",
                                }),
                            ]),
                            html.H2("Únete a la comunidad.", style={
                                "color": "white", "fontSize": "2.7rem", "fontWeight": "800",
                                "lineHeight": "1.2", "margin": "0 0 16px 0",
                            }),
                            html.P("Crea tu perfil en menos de 2 minutos y empieza a monitorizar tu rendimiento desde el primer día.", style={
                                "color": "#555", "fontSize": "1.05rem", "lineHeight": "1.7", "margin": "0 0 36px 0",
                            }),
                            # Bullets de beneficios
                            *[html.Div(style={"display": "flex", "alignItems": "center", "gap": "12px", "marginBottom": "14px"}, children=[
                                html.Div(style={
                                    "width": "28px", "height": "28px", "borderRadius": "8px",
                                    "backgroundColor": "rgba(232,255,71,0.1)",
                                    "display": "flex", "alignItems": "center", "justifyContent": "center",
                                    "flexShrink": "0",
                                }, children=[html.I(className=f"bi {icon}", style={"color": LIME, "fontSize": "1.05rem"})]),
                                html.Span(text, style={"color": "#666", "fontSize": "1.08rem"}),
                            ]) for icon, text in [
                                ("bi-activity", "ECG y métricas cardíacas en tiempo real"),
                                ("bi-bar-chart-line", "Historial de entrenamientos y tendencias"),
                                ("bi-shield-check", "Datos cifrados y privacidad garantizada"),
                            ]],
                        ]),
                        # Footer / link login
                        html.Div(style={"display": "flex", "alignItems": "center", "gap": "12px"}, children=[
                            html.Span("¿Ya tienes cuenta?", style={"color": "#444", "fontSize": "1.05rem"}),
                            dcc.Link("Iniciar sesión →", href="/login", style={
                                "color": LIME, "fontSize": "1.05rem", "fontWeight": "600",
                                "textDecoration": "none",
                            }),
                        ]),
                    ]
                ),
                # ── Panel derecho: formulario ────────────────
                html.Div(
                    style={
                        "width": "480px",
                        "flexShrink": "0",
                        "backgroundColor": "#0f0f0f",
                        "padding": "50px 48px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "overflowY": "auto",
                    },
                    children=[
                        html.H2("Crear cuenta", style={
                            "color": "white", "fontSize": "2.1rem", "fontWeight": "800",
                            "marginBottom": "6px", "marginTop": "0",
                        }),
                        html.P("Elige tu perfil y completa el formulario.", style={
                            "color": "#555", "marginBottom": "30px", "fontSize": "1.08rem",
                        }),

                        # Selector tipo usuario
                        html.Div(style={"marginBottom": "24px"}, children=[
                            html.Label("Soy...", style={
                                "color": "#888", "fontSize": "1.08rem", "fontWeight": "600",
                                "letterSpacing": "0.5px", "display": "block", "marginBottom": "10px",
                            }),
                            html.Div(style={"display": "flex", "gap": "12px"}, children=[
                                _type_btn("btn-reg-type-athlete", "🏃", "Atleta", "Monitoriza tu rendimiento", selected=True),
                                _type_btn("btn-reg-type-doctor",  "💪", "Entrenador/a", "Gestiona a tus deportistas"),
                            ]),
                            dcc.Store(id="reg-user-type", data="athlete"),
                            html.Div(id="user-type-indicator", style={
                                "marginTop": "8px", "textAlign": "center",
                                "fontSize": "1.08rem", "color": "#555",
                            }),
                        ]),

                        # Campos
                        *[html.Div(style={"marginBottom": "14px"}, children=[
                            html.Label(label, style={
                                "color": "#888", "fontSize": "1.08rem", "fontWeight": "600",
                                "letterSpacing": "0.5px", "display": "block", "marginBottom": "7px",
                            }),
                            html.Div(style={"position": "relative"}, children=[
                                html.I(className=f"bi {icon}", style={
                                    "position": "absolute", "left": "14px", "top": "50%",
                                    "transform": "translateY(-50%)", "color": "#333",
                                    "fontSize": "1.1rem", "pointerEvents": "none",
                                }),
                                dcc.Input(
                                    id=input_id, type=input_type,
                                    placeholder=placeholder,
                                    style={
                                        "width": "100%", "padding": "13px 14px 13px 38px",
                                        "backgroundColor": "#161616", "border": "1px solid #222",
                                        "borderRadius": "10px", "color": "white",
                                        "fontSize": "1.1rem", "boxSizing": "border-box", "outline": "none",
                                    }
                                ),
                            ]),
                        ]) for label, input_id, input_type, placeholder, icon in [
                            ("Nombre de usuario", "reg-username", "text",     "@username",              "bi-person"),
                            ("Correo electrónico","reg-email",    "email",    "correo@ejemplo.com",     "bi-envelope"),
                            ("Contraseña",        "reg-password", "password", "Mínimo 8 caracteres",    "bi-lock"),
                            ("Confirmar contraseña","reg-password2","password","Repite tu contraseña",  "bi-lock-fill"),
                        ]],

                        # Términos
                        html.Div(style={
                            "display": "flex", "alignItems": "center", "gap": "10px",
                            "margin": "8px 0 20px 0",
                            "padding": "12px 14px",
                            "backgroundColor": "#111",
                            "borderRadius": "10px",
                            "border": "1px solid #1e1e1e",
                        }, children=[
                            html.Button("☐", id="terms-checkbox-visual", n_clicks=0,
                                        style={
                                            "background": "transparent", "border": "none",
                                            "color": LIME, "fontSize": "1.5rem",
                                            "cursor": "pointer", "padding": "0", "lineHeight": "1",
                                        }),
                            html.Span("Acepto los términos y condiciones de uso", style={
                                "color": "#666", "fontSize": "0.93rem",
                            }),
                            dcc.Store(id="accept-terms", data=False),
                        ]),

                        # Botón crear cuenta
                        dbc.Button(
                            [html.Span("Crear cuenta"), html.I(className="bi bi-arrow-right ms-2")],
                            id="register-btn",
                            style={
                                "width": "100%", "padding": "14px",
                                "backgroundColor": LIME, "border": "none",
                                "borderRadius": "12px", "color": "#080808",
                                "fontWeight": "800", "fontSize": "1.08rem",
                                "cursor": "pointer", "letterSpacing": "0.3px",
                            }
                        ),
                        html.Div(id="register-message", style={"marginTop": "10px", "fontSize": "1.05rem", "textAlign": "center"}),
                    ]
                ),
            ]
        )
    ]
)