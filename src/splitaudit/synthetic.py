"""Grouped synthetic data with a controllable 'group effect share' rho.

label depends on (a) a real, group-INDEPENDENT signal in x and (b) a group-level
effect that is visible through group-specific feature fingerprints. A random split
lets the model memorise group fingerprints (leakage); a group-held-out split cannot.
rho = 0 -> no leakage possible; rho = 1 -> label is almost purely group-driven.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def make_grouped(n_groups=40, per_group=25, n_features=12, rho=0.5, signal=1.0, seed=0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    g_effect = rng.normal(0, 1, n_groups)                         # latent group propensity
    g_fingerprint = rng.normal(0, 1.5, (n_groups, n_features))    # group-specific feature offset
    rows = []
    w = rng.normal(0, 1, n_features); w /= np.linalg.norm(w)
    for g in range(n_groups):
        X = rng.normal(0, 1, (per_group, n_features)) + g_fingerprint[g]
        # real signal uses the within-group-centred part of x; fingerprint carries the group effect
        real = (X - g_fingerprint[g]) @ w * signal
        logit = (1 - rho) * real + rho * 2.0 * g_effect[g]
        y = (rng.random(per_group) < 1 / (1 + np.exp(-logit))).astype(int)
        df = pd.DataFrame(X, columns=[f"f{j}" for j in range(n_features)])
        df["y"], df["group"] = y, f"g{g:03d}"
        rows.append(df)
    out = pd.concat(rows, ignore_index=True)
    return out.sample(frac=1.0, random_state=seed).reset_index(drop=True)
