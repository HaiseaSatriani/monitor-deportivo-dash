"""
db.py — Capa de persistencia SQLite completa para Athletica Pro.
Versión enterprise con métricas avanzadas, training plans y analytics.
"""

import sqlite3
import os
import time
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join("data", "athletica.db")


# ─────────────────────────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────────────────────────
def _conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────
def init_db():
    conn = _conn()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            username        TEXT PRIMARY KEY,
            password_hash   TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            full_name       TEXT,
            user_type       TEXT DEFAULT 'athlete',
            activity_level  INTEGER DEFAULT 5,
            age             INTEGER DEFAULT 25,
            weight_kg       REAL DEFAULT 70,
            height_cm       REAL DEFAULT 170,
            max_hr          INTEGER DEFAULT 190,
            resting_hr      INTEGER DEFAULT 60,
            onboarding_done INTEGER DEFAULT 0,
            avatar_color    TEXT DEFAULT '#E8FF47',
            created_at      TEXT
        );

        CREATE TABLE IF NOT EXISTS doctors (
            username        TEXT PRIMARY KEY,
            password_hash   TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            full_name       TEXT,
            specialty       TEXT DEFAULT 'Medicina Deportiva',
            created_at      TEXT
        );

        CREATE TABLE IF NOT EXISTS doctor_patients (
            doctor_username  TEXT,
            patient_username TEXT,
            PRIMARY KEY (doctor_username, patient_username)
        );

        CREATE TABLE IF NOT EXISTS goals (
            id           TEXT PRIMARY KEY,
            username     TEXT NOT NULL,
            goal_type    TEXT NOT NULL,
            name         TEXT NOT NULL,
            description  TEXT,
            target       TEXT,
            current_val  REAL DEFAULT 0,
            target_val   REAL DEFAULT 100,
            unit         TEXT DEFAULT '%',
            deadline     TEXT,
            progress     INTEGER DEFAULT 0,
            status       TEXT DEFAULT 'active',
            emoji        TEXT DEFAULT '🎯',
            priority     TEXT DEFAULT 'medium',
            created_at   TEXT,
            completed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS meals (
            id          TEXT PRIMARY KEY,
            username    TEXT NOT NULL,
            meal_type   TEXT,
            description TEXT,
            meal_time   TEXT,
            calories    INTEGER DEFAULT 0,
            carbs       INTEGER DEFAULT 0,
            protein     INTEGER DEFAULT 0,
            fat         INTEGER DEFAULT 0,
            fiber       INTEGER DEFAULT 0,
            sugar       INTEGER DEFAULT 0,
            meal_date   TEXT,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS workout_history (
            id              TEXT PRIMARY KEY,
            username        TEXT NOT NULL,
            workout_type    TEXT,
            workout_date    TEXT,
            duration_min    INTEGER DEFAULT 0,
            distance_km     REAL DEFAULT 0,
            avg_hr          INTEGER DEFAULT 0,
            max_hr_workout  INTEGER DEFAULT 0,
            calories_burned INTEGER DEFAULT 0,
            pace_min_km     REAL DEFAULT 0,
            rpe             INTEGER DEFAULT 5,
            mood            TEXT DEFAULT 'neutral',
            energy          INTEGER DEFAULT 5,
            pain            INTEGER DEFAULT 0,
            notes           TEXT,
            training_zone   TEXT DEFAULT 'Z2',
            created_at      TEXT
        );

        CREATE TABLE IF NOT EXISTS hydration (
            username TEXT,
            date     TEXT,
            liters   REAL DEFAULT 0,
            goal_l   REAL DEFAULT 3.0,
            PRIMARY KEY (username, date)
        );

        CREATE TABLE IF NOT EXISTS biometrics (
            id          TEXT PRIMARY KEY,
            username    TEXT NOT NULL,
            weight_kg   REAL,
            body_fat    REAL,
            muscle_mass REAL,
            resting_hr  INTEGER,
            hrv         INTEGER,
            vo2max      REAL,
            recorded_at TEXT
        );

        CREATE TABLE IF NOT EXISTS personal_records (
            id          TEXT PRIMARY KEY,
            username    TEXT NOT NULL,
            record_type TEXT NOT NULL,
            value       REAL NOT NULL,
            unit        TEXT DEFAULT 'min',
            distance    TEXT,
            recorded_at TEXT
        );
    """)

    conn.commit()

    # Migraciones: columnas añadidas en versiones posteriores
    # Se ejecutan de forma segura — si ya existen, se ignoran
    migrations = [
        "ALTER TABLE hydration ADD COLUMN goal_l REAL DEFAULT 3.0",
        "ALTER TABLE workout_history ADD COLUMN duration_min INTEGER DEFAULT 0",
        "ALTER TABLE workout_history ADD COLUMN distance_km REAL DEFAULT 0",
        "ALTER TABLE workout_history ADD COLUMN avg_hr INTEGER DEFAULT 0",
        "ALTER TABLE workout_history ADD COLUMN calories_burned INTEGER DEFAULT 0",
        "ALTER TABLE workout_history ADD COLUMN rpe INTEGER DEFAULT 5",
        "ALTER TABLE workout_history ADD COLUMN mood TEXT DEFAULT 'neutral'",
        "ALTER TABLE workout_history ADD COLUMN energy INTEGER DEFAULT 5",
        "ALTER TABLE workout_history ADD COLUMN pain INTEGER DEFAULT 0",
        "ALTER TABLE workout_history ADD COLUMN training_zone TEXT DEFAULT 'Z2'",
        "ALTER TABLE goals ADD COLUMN current_val REAL DEFAULT 0",
        "ALTER TABLE goals ADD COLUMN target_val REAL DEFAULT 100",
        "ALTER TABLE goals ADD COLUMN unit TEXT DEFAULT '%'",
        "ALTER TABLE goals ADD COLUMN priority TEXT DEFAULT 'medium'",
        "ALTER TABLE goals ADD COLUMN completed_at TEXT",
    ]
    for sql in migrations:
        try:
            conn.execute(sql)
            conn.commit()
        except Exception:
            pass  # Columna ya existe, ignorar

    conn.close()
    _seed_demo()


def _seed_demo():
    conn = _conn()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        demo_athletes = [
            ("Haisea", "123",  "haisea@athletica.com",  "Haisea Satriani", 10, 1, 28, 68.5, 175, 195, 52),
            ("test",   "test", "test@test.com",          "Alex Runner",      5, 1, 32, 75.0, 180, 188, 58),
            ("maria",  "1234", "maria@athletica.com",    "Maria Lopez",      7, 1, 25, 58.0, 165, 200, 55),
        ]
        for u in demo_athletes:
            c.execute(
                "INSERT OR IGNORE INTO users VALUES (?,?,?,?,'athlete',?,?,?,?,?,?,?,?,?)",
                (u[0], generate_password_hash(u[1]), u[2], u[3], u[4], u[5],
                 u[6], u[7], u[8], u[9], u[10], 1, '#E8FF47', datetime.now().isoformat())
            )

    c.execute("SELECT COUNT(*) FROM doctors")
    if c.fetchone()[0] == 0:
        demo_doctors = [
            ("medico1",   "doctor123", "dr.smith@athletica.com",  "Dr. John Smith",       "Medicina Deportiva"),
            ("neuro_med", "neuro2024", "neuro@athletica.com",     "Dra. Ana Neuro",        "Fisioterapia"),
        ]
        for d in demo_doctors:
            c.execute(
                "INSERT OR IGNORE INTO doctors VALUES (?,?,?,?,?,?)",
                (d[0], generate_password_hash(d[1]), d[2], d[3], d[4], datetime.now().isoformat())
            )
        links = [("medico1","Haisea"), ("medico1","test"), ("medico1","maria"), ("neuro_med","Haisea")]
        c.executemany("INSERT OR IGNORE INTO doctor_patients VALUES (?,?)", links)

    # Seed workout history for Haisea
    c.execute("SELECT COUNT(*) FROM workout_history WHERE username='Haisea'")
    if c.fetchone()[0] == 0:
        types = ["carrera_facil","intervalos","trail","ciclismo","fuerza","carrera_facil","tempo"]
        moods = ["excelente","bien","bien","regular","excelente","bien","cansado"]
        zones = ["Z2","Z4","Z3","Z2","Z3","Z2","Z3"]
        for i in range(14):
            day = (datetime.now() - timedelta(days=i*2)).strftime("%Y-%m-%d")
            rpe_val = random.randint(4, 8)
            c.execute("""
                INSERT OR IGNORE INTO workout_history
                  (id,username,workout_type,workout_date,duration_min,distance_km,avg_hr,
                   calories_burned,pace_min_km,rpe,mood,energy,pain,training_zone,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                f"wo_{i}_{random.randint(1000,9999)}", "Haisea",
                types[i % len(types)], day,
                random.randint(35, 90),
                round(random.uniform(5, 18), 1),
                random.randint(140, 175),
                random.randint(350, 750),
                round(random.uniform(4.5, 6.5), 2),
                rpe_val, moods[i % len(moods)],
                random.randint(5, 9), 0,
                zones[i % len(zones)],
                day + "T08:00:00"
            ))

    # Seed personal records
    c.execute("SELECT COUNT(*) FROM personal_records WHERE username='Haisea'")
    if c.fetchone()[0] == 0:
        prs = [
            ("5K",    "21:34", "min", "5km"),
            ("10K",   "44:12", "min", "10km"),
            ("21K",   "1:38:05", "min", "21km"),
            ("42K",   "3:28:44", "min", "42km"),
            ("1mile", "5:52", "min",  "1mi"),
        ]
        for pr in prs:
            c.execute(
                "INSERT OR IGNORE INTO personal_records VALUES (?,?,?,?,?,?,?)",
                (f"pr_{pr[0]}", "Haisea", pr[0], 0, pr[1], pr[3], datetime.now().isoformat())
            )

    # Seed biometrics
    c.execute("SELECT COUNT(*) FROM biometrics WHERE username='Haisea'")
    if c.fetchone()[0] == 0:
        for i in range(8):
            day = (datetime.now() - timedelta(days=i*7)).isoformat()
            c.execute(
                "INSERT OR IGNORE INTO biometrics VALUES (?,?,?,?,?,?,?,?,?)",
                (f"bio_{i}", "Haisea",
                 round(68.5 - i*0.2, 1),
                 round(12.0 + i*0.1, 1),
                 round(58.0 + i*0.1, 1),
                 random.randint(50, 58),
                 random.randint(52, 75),
                 round(52.0 + i*0.3, 1),
                 day)
            )

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────────────────────
def verify_user(identifier, password):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM doctors WHERE username=? OR email=?", (identifier, identifier))
    row = c.fetchone()
    if row and check_password_hash(row["password_hash"], password):
        conn.close()
        return {"username": row["username"], "full_name": row["full_name"], "user_type": "doctor"}

    c.execute("SELECT * FROM users WHERE username=? OR email=?", (identifier, identifier))
    row = c.fetchone()
    conn.close()
    if row and check_password_hash(row["password_hash"], password):
        return {
            "username":        row["username"],
            "full_name":       row["full_name"],
            "user_type":       row["user_type"],
            "activity_level":  row["activity_level"],
            "onboarding_done": bool(row["onboarding_done"]),
        }
    return None


def save_user(username, email, password, full_name=None, user_type="athlete"):
    conn = _conn()
    try:
        if user_type == "doctor":
            conn.execute(
                "INSERT INTO doctors (username,password_hash,email,full_name,specialty,created_at) VALUES (?,?,?,?,?,?)",
                (username, generate_password_hash(password), email, full_name or username,
                 "Medicina Deportiva", datetime.now().isoformat())
            )
        else:
            conn.execute(
                "INSERT INTO users (username,password_hash,email,full_name,user_type,activity_level,onboarding_done,created_at) VALUES (?,?,?,?,'athlete',5,0,?)",
                (username, generate_password_hash(password), email, full_name or username, datetime.now().isoformat())
            )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def username_or_email_exists(username, email):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username=? OR email=?", (username, email))
    if c.fetchone():
        conn.close(); return True
    c.execute("SELECT 1 FROM doctors WHERE username=? OR email=?", (username, email))
    exists = c.fetchone() is not None
    conn.close()
    return exists


# ─────────────────────────────────────────────────────────────
# ATLETAS
# ─────────────────────────────────────────────────────────────
def get_user(username):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def get_doctor(username):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM doctors WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users():
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT username,email,full_name,activity_level,created_at FROM users ORDER BY username")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_activity_level(username):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT activity_level FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row["activity_level"] if row else 5


def get_doctor_patients(doctor_username):
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        SELECT u.username, u.full_name, u.email, u.activity_level, u.created_at,
               u.weight_kg, u.height_cm, u.age
        FROM users u
        JOIN doctor_patients dp ON u.username = dp.patient_username
        WHERE dp.doctor_username = ?
        ORDER BY u.full_name
    """, (doctor_username,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_doctor_patient(doctor_username, patient_username):
    conn = _conn()
    try:
        conn.execute("INSERT OR IGNORE INTO doctor_patients VALUES (?,?)", (doctor_username, patient_username))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def remove_doctor_patient(doctor_username, patient_username):
    conn = _conn()
    conn.execute("DELETE FROM doctor_patients WHERE doctor_username=? AND patient_username=?",
                 (doctor_username, patient_username))
    conn.commit(); conn.close()
    return True


def search_users_by_name(query):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT username,full_name,email,activity_level FROM users WHERE username LIKE ? OR full_name LIKE ?",
              (f"%{query}%", f"%{query}%"))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# OBJETIVOS
# ─────────────────────────────────────────────────────────────
def add_user_goal(username, goal_type, goal_data):
    gid = f"goal_{int(time.time())}_{random.randint(1000,9999)}"
    conn = _conn()
    conn.execute("""
        INSERT INTO goals
          (id,username,goal_type,name,description,target,current_val,target_val,unit,
           deadline,progress,status,emoji,priority,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,0,'active',?,?,?)
    """, (
        gid, username, goal_type,
        goal_data.get("name", "Sin nombre"),
        goal_data.get("description", ""),
        goal_data.get("target", ""),
        float(goal_data.get("current_val", 0)),
        float(goal_data.get("target_val", 100)),
        goal_data.get("unit", "%"),
        goal_data.get("deadline", "1_month"),
        _emoji_for_goal(goal_data.get("name", "")),
        goal_data.get("priority", "medium"),
        datetime.now().isoformat()
    ))
    conn.commit(); conn.close()
    return True


def get_user_goals_for_display(username):
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        SELECT id,goal_type,name,description,target,current_val,target_val,unit,
               deadline,progress,status,emoji,priority,created_at,completed_at
        FROM goals WHERE username=? ORDER BY created_at DESC
    """, (username,))
    rows = c.fetchall()
    conn.close()
    fitness, health = [], []
    for r in rows:
        obj = dict(r)
        (fitness if r["goal_type"] == "fitness" else health).append(obj)
    return {"fitness": fitness, "health": health}


def update_goal_progress(username, goal_id, progress):
    conn = _conn()
    status = "completed" if progress >= 100 else "active"
    completed_at = datetime.now().isoformat() if progress >= 100 else None
    conn.execute("""
        UPDATE goals SET progress=?, status=?, completed_at=?
        WHERE id=? AND username=?
    """, (min(100, progress), status, completed_at, goal_id, username))
    conn.commit(); conn.close()
    return True


def mark_goal_completed(username, goal_id):
    conn = _conn()
    conn.execute("""
        UPDATE goals SET status='completed', progress=100, completed_at=?
        WHERE id=? AND username=?
    """, (datetime.now().isoformat(), goal_id, username))
    conn.commit(); conn.close()
    return True


def delete_user_goal(username, goal_id):
    conn = _conn()
    conn.execute("DELETE FROM goals WHERE id=? AND username=?", (goal_id, username))
    conn.commit(); conn.close()
    return True


def _emoji_for_goal(name):
    name = name.lower()
    mapping = {
        "peso": "📉", "correr": "🏃", "velocidad": "⚡",
        "resistencia": "🫀", "fuerza": "💪", "flexibilidad": "🧘",
        "cardio": "💓", "frecuencia": "❤️", "hrv": "📊",
        "recuperacion": "🔄", "nutricion": "🥗", "agua": "💧",
        "calorias": "🔥", "proteina": "🥩", "sueno": "😴",
        "maraton": "🏅", "10k": "🎽", "5k": "🎯", "trail": "⛰️",
        "vo2": "🫁", "bici": "🚴", "nadar": "🏊",
    }
    for k, v in mapping.items():
        if k in name:
            return v
    return "🎯"


# ─────────────────────────────────────────────────────────────
# NUTRICIÓN
# ─────────────────────────────────────────────────────────────
def save_user_meal(username, meal_data):
    mid = f"meal_{int(time.time())}_{random.randint(100,999)}"
    today = datetime.now().strftime("%Y-%m-%d")
    conn = _conn()
    conn.execute("""
        INSERT INTO meals (id,username,meal_type,description,meal_time,calories,carbs,protein,fat,fiber,sugar,meal_date,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        mid, username,
        meal_data.get("type", "snacks"),
        meal_data.get("description", ""),
        meal_data.get("time", datetime.now().strftime("%H:%M")),
        meal_data.get("calories", 0),
        meal_data.get("carbs", 0),
        meal_data.get("protein", 0),
        meal_data.get("fat", 0),
        meal_data.get("fiber", 0),
        meal_data.get("sugar", 0),
        today,
        datetime.now().isoformat()
    ))
    conn.commit(); conn.close()
    return True


def load_user_meals(username, date=None):
    conn = _conn()
    c = conn.cursor()
    if date:
        c.execute("SELECT * FROM meals WHERE username=? AND meal_date=? ORDER BY meal_time", (username, date))
    else:
        c.execute("SELECT * FROM meals WHERE username=? ORDER BY created_at DESC", (username,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def calculate_daily_totals(meals):
    today = datetime.now().strftime("%Y-%m-%d")
    totals = {"calories": 0, "carbs": 0, "protein": 0, "fat": 0, "fiber": 0}
    for m in meals:
        if m.get("meal_date") == today or m.get("date") == today:
            for k in totals:
                totals[k] += m.get(k, 0)
    return totals


def get_hydration(username):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT liters, goal_l FROM hydration WHERE username=? AND date=?", (username, today))
    row = c.fetchone()
    conn.close()
    if row:
        return {"liters": row["liters"], "goal": row["goal_l"]}
    return {"liters": 0.0, "goal": 3.0}


def add_hydration(username, amount=0.25):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = _conn()
    conn.execute("""
        INSERT INTO hydration (username, date, liters, goal_l) VALUES (?,?,?,3.0)
        ON CONFLICT(username,date) DO UPDATE SET liters=liters+?
    """, (username, today, amount, amount))
    conn.commit(); conn.close()
    return get_hydration(username)


# ─────────────────────────────────────────────────────────────
# HISTORIAL ENTRENAMIENTOS
# ─────────────────────────────────────────────────────────────
def save_workout(username, workout_type, duration_min=0, distance_km=0, avg_hr=0,
                 calories_burned=0, rpe=5, mood="neutral", energy=5, pain=0,
                 notes="", training_zone="Z2"):
    wid = f"wo_{int(time.time())}_{random.randint(100,999)}"
    conn = _conn()
    conn.execute("""
        INSERT INTO workout_history
          (id,username,workout_type,workout_date,duration_min,distance_km,avg_hr,
           calories_burned,rpe,mood,energy,pain,notes,training_zone,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        wid, username, workout_type,
        datetime.now().strftime("%Y-%m-%d"),
        duration_min, distance_km, avg_hr, calories_burned,
        rpe, mood, energy, pain, notes, training_zone,
        datetime.now().isoformat()
    ))
    conn.commit(); conn.close()
    return True


def get_workout_history(username, limit=30):
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM workout_history WHERE username=?
        ORDER BY created_at DESC LIMIT ?
    """, (username, limit))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_workout_stats(username):
    """Estadísticas agregadas de entrenamientos."""
    conn = _conn()
    c = conn.cursor()
    # Última semana
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    c.execute("""
        SELECT
            COUNT(*) as total_sessions,
            SUM(duration_min) as total_min,
            SUM(distance_km) as total_km,
            SUM(calories_burned) as total_cal,
            AVG(rpe) as avg_rpe,
            AVG(avg_hr) as avg_hr
        FROM workout_history
        WHERE username=? AND workout_date >= ?
    """, (username, week_ago))
    week = dict(c.fetchone())

    # Mes
    month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    c.execute("""
        SELECT COUNT(*) as sessions, SUM(distance_km) as km, SUM(calories_burned) as cal
        FROM workout_history WHERE username=? AND workout_date >= ?
    """, (username, month_ago))
    month = dict(c.fetchone())

    conn.close()
    return {"week": week, "month": month}


# ─────────────────────────────────────────────────────────────
# BIOMETRÍA
# ─────────────────────────────────────────────────────────────
def get_biometrics_history(username, limit=12):
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM biometrics WHERE username=?
        ORDER BY recorded_at DESC LIMIT ?
    """, (username, limit))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_biometric(username, data):
    bid = f"bio_{int(time.time())}"
    conn = _conn()
    conn.execute("""
        INSERT INTO biometrics (id,username,weight_kg,body_fat,muscle_mass,resting_hr,hrv,vo2max,recorded_at)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        bid, username,
        data.get("weight_kg"), data.get("body_fat"),
        data.get("muscle_mass"), data.get("resting_hr"),
        data.get("hrv"), data.get("vo2max"),
        datetime.now().isoformat()
    ))
    conn.commit(); conn.close()
    return True


# ─────────────────────────────────────────────────────────────
# RECORDS PERSONALES
# ─────────────────────────────────────────────────────────────
def get_personal_records(username):
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM personal_records WHERE username=? ORDER BY distance", (username,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# HELPERS NUTRICIÓN
# ─────────────────────────────────────────────────────────────
def estimate_nutrients_from_description(description):
    d = description.lower()
    food_db = {
        "avena":     {"carbs": 25, "protein": 5,  "fat": 3,  "calories": 150, "fiber": 4},
        "pollo":     {"carbs": 0,  "protein": 25, "fat": 5,  "calories": 165, "fiber": 0},
        "salmon":    {"carbs": 0,  "protein": 22, "fat": 13, "calories": 206, "fiber": 0},
        "atun":      {"carbs": 0,  "protein": 26, "fat": 1,  "calories": 120, "fiber": 0},
        "arroz":     {"carbs": 45, "protein": 4,  "fat": 1,  "calories": 205, "fiber": 1},
        "pasta":     {"carbs": 40, "protein": 8,  "fat": 2,  "calories": 210, "fiber": 2},
        "huevo":     {"carbs": 1,  "protein": 6,  "fat": 5,  "calories": 78,  "fiber": 0},
        "aguacate":  {"carbs": 9,  "protein": 2,  "fat": 15, "calories": 160, "fiber": 7},
        "platano":   {"carbs": 27, "protein": 1,  "fat": 0,  "calories": 105, "fiber": 3},
        "yogur":     {"carbs": 6,  "protein": 10, "fat": 5,  "calories": 120, "fiber": 0},
        "almendra":  {"carbs": 6,  "protein": 6,  "fat": 14, "calories": 160, "fiber": 4},
        "lentejas":  {"carbs": 20, "protein": 9,  "fat": 0,  "calories": 116, "fiber": 8},
        "ensalada":  {"carbs": 10, "protein": 3,  "fat": 2,  "calories": 70,  "fiber": 3},
        "pan":       {"carbs": 15, "protein": 3,  "fat": 1,  "calories": 80,  "fiber": 1},
        "pavo":      {"carbs": 0,  "protein": 29, "fat": 7,  "calories": 189, "fiber": 0},
        "batido":    {"carbs": 30, "protein": 20, "fat": 3,  "calories": 220, "fiber": 2},
        "fruta":     {"carbs": 20, "protein": 1,  "fat": 0,  "calories": 80,  "fiber": 3},
        "verdura":   {"carbs": 8,  "protein": 2,  "fat": 0,  "calories": 40,  "fiber": 3},
        "quinoa":    {"carbs": 39, "protein": 8,  "fat": 4,  "calories": 220, "fiber": 5},
    }
    totals = {"carbs": 0, "protein": 0, "fat": 0, "calories": 0, "fiber": 0}
    matched = False
    for food, vals in food_db.items():
        if food in d:
            for k in totals:
                totals[k] += vals[k]
            matched = True
    if not matched:
        totals = {"carbs": 40, "protein": 15, "fat": 10, "calories": 300, "fiber": 3}
    return totals


# ─────────────────────────────────────────────────────────────
# HELPERS SALUD
# ─────────────────────────────────────────────────────────────
def get_health_score_from_activity_level(level):
    if level <= 2:  return 1
    if level <= 4:  return 2
    if level <= 6:  return 3
    if level <= 8:  return 4
    return 5


def get_health_description(score):
    return {
        1: "Actividad baja • Aumenta el ejercicio gradualmente",
        2: "Actividad media-baja • Buen comienzo, sigue progresando",
        3: "Actividad intermedia • Buen ritmo de ejercicio",
        4: "Actividad alta • Excelente condición física",
        5: "Actividad muy alta • Nivel atlético excepcional",
    }.get(score, "Estado normal • Manteniendo ritmo")


def calculate_training_load(workouts):
    """Calcula carga de entrenamiento (ACWR) de las últimas semanas."""
    if not workouts:
        return {"acute": 0, "chronic": 0, "ratio": 1.0, "status": "optimal"}
    acute_rpe = sum(w.get("rpe", 5) * w.get("duration_min", 45) for w in workouts[:7])
    chronic_rpe = sum(w.get("rpe", 5) * w.get("duration_min", 45) for w in workouts[:28]) / 4
    ratio = acute_rpe / chronic_rpe if chronic_rpe > 0 else 1.0
    if ratio < 0.8:   status = "undertraining"
    elif ratio > 1.5: status = "overload_risk"
    else:             status = "optimal"
    return {"acute": round(acute_rpe), "chronic": round(chronic_rpe), "ratio": round(ratio, 2), "status": status}


# Inicializar al importar
init_db()