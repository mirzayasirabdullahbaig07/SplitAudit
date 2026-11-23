import argparse
from pathlib import Path


def main(argv=None):
    p = argparse.ArgumentParser(prog="splitaudit")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("simulate", help="Sweep group-effect share rho on synthetic data (pipeline check)")
    s.add_argument("--out", default="results/simulate"); s.add_argument("--repeats", type=int, default=5)
    a = sub.add_parser("audit", help="Audit YOUR csv")
    a.add_argument("--csv", required=True); a.add_argument("--label", required=True); a.add_argument("--group", required=True)
    a.add_argument("--features", nargs="*", help="default: all numeric columns except label/group")
    a.add_argument("--metric", choices=["auc", "bacc"], default="auc")
    a.add_argument("--repeats", type=int, default=10); a.add_argument("--out", default="results/audit")
    args = p.parse_args(argv)
    import pandas as pd
    from .audit import optimism, run_audit
    pd.set_option("display.width", 200)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    if args.cmd == "simulate":
        from .synthetic import make_grouped
        allr = []
        for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
            df = make_grouped(rho=rho, seed=1)
            r = optimism(run_audit(df, [c for c in df if c.startswith("f")], repeats=args.repeats))
            r.insert(0, "rho", rho); allr.append(r)
        t = pd.concat(allr); print("SYNTHETIC sweep - pipeline check only\n", t.round(3).to_string(index=False))
        t.round(4).to_csv(out / "rho_sweep.csv", index=False)
    else:
        df = pd.read_csv(args.csv)
        feats = args.features or [c for c in df.select_dtypes("number").columns if c not in (args.label, args.group)]
        print(f"{len(df)} rows, {df[args.group].nunique()} groups, {len(feats)} features, positive rate {df[args.label].mean():.3f}")
        r = optimism(run_audit(df, feats, args.label, args.group, repeats=args.repeats, metric=args.metric))
        print(r.round(3).to_string(index=False)); r.round(4).to_csv(out / "optimism.csv", index=False)


if __name__ == "__main__":
    main()
