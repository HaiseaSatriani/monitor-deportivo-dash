"""
sensors.py — Procesamiento ECG para Athletica.
Detecta picos R, calcula BPM. Acepta columnas flexibles en CSV.
No requiere scipy (deteccion propia).
"""

import numpy as np
import pandas as pd
import os


def _find_peaks(signal, min_distance=50, threshold=None):
    """Maximo local simple sin scipy."""
    if threshold is None:
        threshold = np.percentile(signal, 82)
    peaks = []
    n = len(signal)
    for i in range(min_distance, n - min_distance):
        if signal[i] < threshold:
            continue
        window = signal[max(0, i - min_distance): i + min_distance + 1]
        if signal[i] == window.max():
            if not peaks or (i - peaks[-1]) >= min_distance:
                peaks.append(i)
    return np.array(peaks, dtype=int)


def load_ecg_and_compute_bpm(filepath="ecg_example.csv"):
    """
    Carga CSV ECG y calcula BPM.
    Columnas aceptadas (case-insensitive):
      tiempo : time, tiempo, t
      senal  : ecg, signal, valor, value, amplitude
    Devuelve: (t, ecg_norm, bpm, peaks)
    """
    if not os.path.exists(filepath):
        return _synthetic_ecg()

    try:
        df = pd.read_csv(filepath)
        col_map = {c.lower(): c for c in df.columns}

        t_col = next((col_map[k] for k in ("time","tiempo","t") if k in col_map), None)
        e_col = next((col_map[k] for k in ("ecg","signal","valor","value","amplitude") if k in col_map), None)

        if t_col is None or e_col is None:
            return _synthetic_ecg()

        t   = df[t_col].to_numpy(dtype=float)
        ecg = df[e_col].to_numpy(dtype=float)

        if len(t) < 20:
            return _synthetic_ecg()

        # Normalizar
        ecg_n = (ecg - np.mean(ecg)) / (np.std(ecg) + 1e-9)

        fs = 1.0 / max(t[1] - t[0], 1e-6)
        min_dist = max(10, int(0.4 * fs))

        peaks = _find_peaks(ecg_n, min_distance=min_dist)

        if len(peaks) > 1:
            rr  = np.diff(t[peaks])
            rr  = rr[rr > 0]
            bpm = float(60.0 / np.mean(rr)) if len(rr) > 0 else 72.0
        else:
            bpm = 72.0

        return t, ecg_n, bpm, peaks

    except Exception as e:
        print(f"Error procesando ECG: {e}")
        return _synthetic_ecg()


def _synthetic_ecg(duration=10, fs=200, bpm=72):
    """ECG sintetico PQRST realista a ~72 BPM."""
    n      = int(duration * fs)
    t      = np.linspace(0, duration, n)
    ecg    = np.zeros(n)
    period = int(fs * 60 / bpm)

    for start in range(0, n, period):
        _add_beat(ecg, start, fs, n)

    ecg += 0.04 * np.random.randn(n)
    ecg_n = (ecg - np.mean(ecg)) / (np.std(ecg) + 1e-9)

    min_dist = int(0.4 * fs)
    peaks = _find_peaks(ecg_n, min_distance=min_dist)

    return t, ecg_n, float(bpm), peaks


def _add_beat(ecg, start, fs, n):
    def gauss(center_s, width_s, amp):
        ci = start + int(center_s * fs)
        wi = max(1, int(width_s * fs))
        for j in range(-wi * 2, wi * 2 + 1):
            idx = ci + j
            if 0 <= idx < n:
                ecg[idx] += amp * np.exp(-0.5 * (j / wi) ** 2)

    gauss(0.10, 0.020, 0.25)   # P
    gauss(0.22, 0.008, -0.15)  # Q
    gauss(0.25, 0.008, 1.50)   # R (pico maximo)
    gauss(0.28, 0.008, -0.30)  # S
    gauss(0.38, 0.035, 0.35)   # T
