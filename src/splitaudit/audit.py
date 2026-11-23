"""Core audit: how much does the validation scheme change the reported score?

Schemes
  random        : shuffled K-fold (the common default; ignores groups)
  stratified    : stratified K-fold on the label (still ignores groups)
  group         : GroupKFold - no group appears in both train and test
  (optional) blocked : contiguous folds in the given row order (time/space proxy)

Optimism = score(random) - score(group), per repeat, with bootstrap CI over repeats.
Leakage diagnostic = share of test rows whose nearest training row (standardised
features) belongs to the SAME group; ~0 under a clean group split.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import GroupKFold, KFold, StratifiedKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

MODELS = {
    "logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "rf": RandomForestClassifier(n_estimators=150, min_samples_leaf=1, n_jobs=-1, random_state=0),
}


def _splits(scheme, X, y, groups, k, seed):
    if scheme == "random":
        return KFold(k, shuffle=True, random_state=seed).split(X)
    if scheme == "stratified":
        return StratifiedKFold(k, shuffle=True, random_state=seed).split(X, y)
    if scheme == "group":
        # shuffle group order per seed so repeats differ
        rng = np.random.default_rng(seed)
        ug = np.unique(groups); perm = dict(zip(ug, rng.permutation(len(ug))))
        gid = np.array([perm[g] for g in groups])
        return GroupKFold(k).split(X, y, gid)
    if scheme == "blocked":
        return KFold(k, shuffle=False).split(X)
    raise ValueError(scheme)


def _score(y, p, metric):
    if len(np.unique(y)) < 2:
        return np.nan
    return roc_auc_score(y, p) if metric == "auc" else balanced_accuracy_score(y, (p >= 0.5).astype(int))


def same_group_nn_rate(Xtr, gtr, Xte, gte):
    nn = NearestNeighbors(n_neighbors=1).fit(Xtr)
    idx = nn.kneighbors(Xte, return_distance=False)[:, 0]
    return float((gtr[idx] == gte).mean())


def run_audit(df: pd.DataFrame, features, label="y", group="group", models=("logreg", "rf"),
              schemes=("random", "stratified", "group"), k=5, repeats=5, metric="auc") -> pd.DataFrame:
    """Return one row per (model, scheme, repeat, fold)."""
    X = df[list(features)].to_numpy(float); y = df[label].to_numpy(int); g = df[group].to_numpy(str)
    Xs = StandardScaler().fit_transform(X)
    rows = []
    for rep in range(repeats):
        for scheme in schemes:
            for fold, (tr, te) in enumerate(_splits(scheme, X, y, g, k, rep)):
                nn_rate = same_group_nn_rate(Xs[tr], g[tr], Xs[te], g[te])
                overlap = len(set(g[tr]) & set(g[te])) / max(len(set(g[te])), 1)
                for name in models:
                    m = clone(MODELS[name]).fit(X[tr], y[tr])
                    p = m.predict_proba(X[te])[:, 1]
                    rows.append(dict(model=name, scheme=scheme, repeat=rep, fold=fold,
                                     score=_score(y[te], p, metric), same_group_nn=nn_rate,
                                     test_groups_seen_in_train=overlap))
    return pd.DataFrame(rows)


def optimism(res: pd.DataFrame, ref="group", cmp="random", n_boot=2000, seed=0) -> pd.DataFrame:
    """Per model: mean score under each scheme and optimism = cmp - ref, bootstrap CI over repeats."""
    rng = np.random.default_rng(seed)
    out = []
    for model, d in res.groupby("model"):
        per = d.groupby(["scheme", "repeat"]).score.mean().unstack(0)      # repeat x scheme
        diff = (per[cmp] - per[ref]).to_numpy()
        boots = np.array([rng.choice(diff, len(diff)).mean() for _ in range(n_boot)])
        out.append(dict(model=model, **{f"score_{s}": per[s].mean() for s in per.columns},
                        optimism=diff.mean(), ci_lo=np.quantile(boots, .025), ci_hi=np.quantile(boots, .975),
                        nn_same_group_random=d[d.scheme == cmp].same_group_nn.mean(),
                        nn_same_group_group=d[d.scheme == ref].same_group_nn.mean()))
    return pd.DataFrame(out)


def label_permutation_null(df, features, label="y", group="group", model="logreg", n_perm=20, seed=0):
    """Sanity check: permuting labels WITHIN groups destroys the label-feature link; the
    group-split score must then sit at chance (0.5 AUC). A score above chance means a bug."""
    rng = np.random.default_rng(seed); scores = []
    for i in range(n_perm):
        d = df.copy()
        d[label] = d.groupby(group)[label].transform(lambda s: rng.permutation(s.to_numpy()))
        r = run_audit(d, features, label, group, models=(model,), schemes=("group",), k=5, repeats=1)
        scores.append(r.score.mean())
    return np.array(scores)
