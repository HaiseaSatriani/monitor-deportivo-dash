# Athletica — Monitor Deportivo

Aplicacion Dash modular para atletas y medicos.

## Estructura

```
athletica/
├── app.py                  # Punto de entrada + router
├── config.py               # Constantes, colores, opciones
├── db.py                   # Capa de persistencia SQLite
├── sensors.py              # Procesamiento ECG
├── questionnaires.txt      # Preguntas de encuestas
├── requirements.txt
├── README.md
├── data/                   # Base de datos SQLite (auto-creada)
├── layouts/
│   ├── styles.py           # CSS global
│   ├── auth.py             # Welcome / Login / Register
│   ├── onboarding.py       # Wizard 5 pasos
│   ├── athlete.py          # Dashboard atleta (5 secciones + modales)
│   └── doctor.py           # Dashboard medico
└── callbacks/
    ├── auth_cb.py          # Login, registro, tipo usuario
    ├── onboarding_cb.py    # Navegacion wizard
    ├── athlete_cb.py       # ECG, encuesta, objetivos, nutricion
    └── doctor_cb.py        # Pacientes, busqueda, estadisticas
```

## Instalacion

```bash
pip install -r requirements.txt
python app.py
```

Abrir http://localhost:8050

## Credenciales demo

| Usuario    | Contrasena  | Tipo   |
|------------|-------------|--------|
| Haisea     | 123         | Atleta |
| test       | test        | Atleta |
| medico1    | doctor123   | Medico |
| neuro_med  | neuro2024   | Medico |

## Base de datos

SQLite en `data/athletica.db`. Se crea automaticamente al iniciar.

Tablas: `users`, `doctors`, `doctor_patients`, `goals`, `meals`, `workout_history`, `hydration`.

## ECG

Sube un CSV con columnas `Time` y `ECG` (o `time`/`ecg`, `t`/`signal`, etc.).
La app detecta picos R, calcula BPM y permite descargar el CSV procesado.

## Funcionalidades

- Autenticacion segura con hash de contrasenas (werkzeug)
- Onboarding de 5 pasos para atletas nuevos
- ECG: subida de CSV, deteccion de picos R, calculo BPM, descarga
- Encuesta post-entrenamiento (RPE, animo, energia, dolor, notas)
- Historial de entrenamientos con visualizacion
- Objetivos fitness/salud con seguimiento de progreso
- Nutricion: registro de comidas, macros, hidratacion
- Dashboard medico: lista de pacientes, busqueda, estadisticas, vista de paciente
