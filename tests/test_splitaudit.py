import numpy as np
from splitaudit.synthetic import make_grouped
from splitaudit.audit import run_audit, optimism, label_permutation_null, _splits

F = lambda df: [c for c in df if c.startswith("f")]


def test_group_split_never_shares_groups():
    df = make_grouped(seed=1); g = df.group.to_numpy()
    for seed in range(3):
        for tr, te in _splits("group", df[F(df)].to_numpy(), df.y.to_numpy(), g, 5, seed):
            assert not (set(g[tr]) & set(g[te]))
        # and the random split DOES share groups (that is the whole point)
    tr, te = next(_splits("random", df[F(df)].to_numpy(), df.y.to_numpy(), g, 5, 0))
    assert set(g[tr]) & set(g[te])


def test_no_leakage_without_group_effect_and_large_optimism_with_it():
    lo = optimism(run_audit(make_grouped(rho=0.0, seed=2), F(make_grouped(rho=0.0, seed=2)), models=("rf",), repeats=4))
    hi_df = make_grouped(rho=1.0, seed=2)
    hi = optimism(run_audit(hi_df, F(hi_df), models=("rf",), repeats=4))
    assert abs(lo.optimism.iloc[0]) < 0.05
    assert hi.optimism.iloc[0] > 0.15 and hi.ci_lo.iloc[0] > 0.1          # CI excludes zero


def test_optimism_increases_with_rho():
    vals = []
    for rho in (0.0, 0.5, 1.0):
        d = make_grouped(rho=rho, seed=3)
        vals.append(optimism(run_audit(d, F(d), models=("rf",), repeats=3)).optimism.iloc[0])
    assert vals[0] < vals[1] < vals[2]


def test_nn_same_group_diagnostic_flags_random_split():
    d = make_grouped(rho=0.5, seed=4)
    r = optimism(run_audit(d, F(d), models=("logreg",), repeats=2))
    assert r.nn_same_group_random.iloc[0] > 0.5 > r.nn_same_group_group.iloc[0]
    assert r.nn_same_group_group.iloc[0] == 0.0


def test_label_permutation_null_is_at_chance():
    d = make_grouped(rho=0.5, seed=5)
    s = label_permutation_null(d, F(d), n_perm=10)
    assert 0.45 < s.mean() < 0.55


def test_true_no_leakage_control_has_zero_optimism():
    """rho = 0 AND fingerprint_sd = 0: nothing group-specific exists, so optimism must be ~0."""
    d = make_grouped(rho=0.0, fingerprint_sd=0.0, seed=6)
    r = optimism(run_audit(d, F(d), models=("rf",), repeats=4))
    assert r.ci_lo.iloc[0] <= 0.0 <= r.ci_hi.iloc[0] or abs(r.optimism.iloc[0]) < 0.015


def test_covariate_leakage_alone_gives_positive_optimism_for_rf():
    """rho = 0 but large fingerprint: random forest memorises group offsets -> optimism > 0."""
    d = make_grouped(rho=0.0, fingerprint_sd=1.5, seed=6)
    r = optimism(run_audit(d, F(d), models=("rf",), repeats=4))
    assert r.ci_lo.iloc[0] > 0.0
