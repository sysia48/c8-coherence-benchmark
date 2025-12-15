# ============================================================
# C8 COHERENCE BENCHMARK — CORE MODULE
# Author: Sylwia Romana Miksztal (Sysia)
# Anchor: C8
# Purpose: Deterministic coherence measurement
# ============================================================

import numpy as np
import hashlib
import json
from datetime import datetime


# ---------------- CORE METRICS ----------------

def sigma(phases):
    """Global phase coherence (Σ)"""
    return float(np.abs(np.mean(np.exp(1j * phases))))


def plv(phases):
    """Phase Locking Value"""
    return sigma(phases)


def energy(signal):
    """Signal energy"""
    return float(np.trapz(signal ** 2))


def delta_entropy(a, b):
    """Shannon entropy delta"""
    def H(x):
        p = np.abs(x)
        p = p / np.sum(p)
        p = p[p > 0]
        return -np.sum(p * np.log(p))
    return float(H(b) - H(a))


def lyapunov(prev, nxt):
    """Simple Lyapunov proxy"""
    return float(np.linalg.norm(nxt) - np.linalg.norm(prev))


def memory_retention(a, b):
    """Memory Retention Index (MRI)"""
    num = np.dot(a, b)
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float(num / den) if den else 0.0


# ---------------- CONTEXT ----------------

def build_context(n=4096):
    t = np.linspace(0, 2 * np.pi, n)
    return {
        "t": t,
        "signal": np.sin(t),
        "phases": np.angle(np.exp(1j * t)),
        "state": np.cos(t),
    }


# ---------------- RUN ----------------

def run_core():
    ctx = build_context()

    results = {
        "Sigma": sigma(ctx["phases"]),
        "PLV": plv(ctx["phases"]),
        "Energy": energy(ctx["signal"]),
        "DeltaS": delta_entropy(ctx["signal"], -ctx["signal"]),
        "Lyapunov": lyapunov(ctx["signal"][:-1], ctx["signal"][1:]),
        "MRI": memory_retention(ctx["state"], ctx["state"]),
    }

    artefact = {
        "framework": "C8 Coherence Benchmark",
        "anchor": "C8",
        "results": results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    artefact["sha256"] = hashlib.sha256(
        json.dumps(artefact, sort_keys=True).encode()
    ).hexdigest()

    return artefact


if __name__ == "__main__":
    print(json.dumps(run_core(), indent=2))