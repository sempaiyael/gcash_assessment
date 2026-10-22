"""Model training orchestrator (Day 2).

Models: Logistic Regression, XGBoost (priority baseline), FT-Transformer
(pytorch-tabular, D001). TabNet deliberately dropped — bundled in
pytorch-tabular if ever needed, and it duplicates the DL slot without adding
to the story.

# TIMING GAUGE — run `python -m src.train --sample-frac 0.2` FIRST.
#   Sample: 20% stratified of fit (~9.4K rows) + val. Full run ~= gauge x5.
#   OK: full all-models < 45 min. Red flag: > 75 min -> reduce FT-T max_epochs
#   to 30, drop n_estimators to 400, or run models separately via --models.

Usage:
    python -m src.train --sample-frac 0.2
    python -m src.train
    python -m src.train --models lr,xgb
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

from src import evaluation as ev
from src.models import baselines as bl
from src.models import ft_transformer_model as ftt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _split_xy(df: pd.DataFrame):
    meta = df[["tconst", "primaryTitle", "startYear", "hit_score"]].copy()
    X = df.drop(columns=bl.META_COLS)
    y = df["hit_label"].to_numpy()
    return X, y, meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Train hit-prediction models")
    parser.add_argument("--sample-frac", type=float, default=1.0,
                        help="stratified fraction of fit/val for timing gauges")
    parser.add_argument("--models", type=str, default="lr,xgb,ftt",
                        help="comma list: lr,xgb,ftt")
    parser.add_argument("--max-epochs", type=int, default=50)
    args = parser.parse_args()
    wanted = {m.strip() for m in args.models.split(",")}

    t_total = time.time()
    df = pd.read_parquet(DATA / "features.parquet")
    fit_df = df[df["split"] == "fit"].copy()
    val_df = df[df["split"] == "val"].copy()
    test_df = df[df["split"] == "test"].copy()

    if args.sample_frac < 1.0:
        frac = args.sample_frac
        fit_df = fit_df.groupby("hit_label", group_keys=False).sample(frac=frac, random_state=42)
        val_df = val_df.groupby("hit_label", group_keys=False).sample(frac=frac, random_state=42)
        print(f"[gauge] SAMPLE_FRAC={frac}: fit={len(fit_df):,}, val={len(val_df):,}, "
              f"test kept full={len(test_df):,} | extrapolate fit time x{1 / frac:.0f}")

    X_fit, y_fit, _ = _split_xy(fit_df)
    X_val, y_val, _ = _split_xy(val_df)
    X_test, y_test, test_meta = _split_xy(test_df)
    print(f"[data] fit={len(fit_df):,} ({y_fit.mean():.1%} pos) | "
          f"val={len(val_df):,} ({y_val.mean():.1%} pos) | "
          f"test={len(test_df):,} ({y_test.mean():.1%} pos)")

    nums, cats = bl.feature_columns(fit_df)
    evals: list[dict] = []
    results: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    importances: dict[str, pd.Series] = {}
    times: dict[str, float] = {}
    thresholds: dict[str, float] = {}

    if "lr" in wanted:
        pipe, dt = bl.fit_logistic_regression(X_fit, y_fit, X_val, y_val, nums, cats)
        times["Logistic Regression"] = dt
        val_p = pipe.predict_proba(X_val)[:, 1]
        test_p = pipe.predict_proba(X_test)[:, 1]
        e = ev.evaluate_model("Logistic Regression", y_val, val_p, y_test, test_p)
        evals.append(e)
        results["Logistic Regression"] = (y_test, test_p)
        thresholds["Logistic Regression"] = e["threshold_tuned"]
        importances["Logistic Regression (|coef|)"] = bl.lr_coefficient_importance(pipe)
        test_meta = test_meta.assign(**{"proba_lr": test_p})

    if "xgb" in wanted:
        fitted, dt = bl.fit_xgboost(X_fit, y_fit, X_val, y_val, nums, cats)
        times["XGBoost"] = dt
        val_p = bl.predict_proba_xgb(fitted, X_val)
        test_p = bl.predict_proba_xgb(fitted, X_test)
        e = ev.evaluate_model("XGBoost", y_val, val_p, y_test, test_p)
        evals.append(e)
        results["XGBoost"] = (y_test, test_p)
        thresholds["XGBoost"] = e["threshold_tuned"]
        importances["XGBoost (gain)"] = bl.xgb_gain_importance(fitted)
        test_meta = test_meta.assign(**{"proba_xgb": test_p})

    if "ftt" in wanted:
        model, dt = ftt.fit_ft_transformer(
            X_fit, y_fit, X_val, y_val, max_epochs=args.max_epochs,
        )
        times["FT-Transformer"] = dt
        val_p = ftt.predict_proba_ftt(model, X_val)
        att = ftt.ftt_attention_importance(model)  # before test predict: attn is last-forward
        test_p = ftt.predict_proba_ftt(model, X_test)
        e = ev.evaluate_model("FT-Transformer", y_val, val_p, y_test, test_p)
        evals.append(e)
        results["FT-Transformer"] = (y_test, test_p)
        thresholds["FT-Transformer"] = e["threshold_tuned"]
        if att is not None:
            importances["FT-Transformer (attn)"] = att
        test_meta = test_meta.assign(**{"proba_ftt": test_p})
        try:
            model.save_model(str(DATA / "ft_transformer_model"))
        except Exception as e_save:  # noqa: BLE001
            print(f"[ftt] model save failed (non-fatal): {e_save}")

    ev.FIGURES.mkdir(parents=True, exist_ok=True)
    ev.TABLES.mkdir(parents=True, exist_ok=True)
    comparison = ev.save_comparison(evals, ev.TABLES / "model_comparison.csv")
    ev.plot_roc_curves(results, ev.FIGURES / "model_roc_curves.png")
    ev.plot_pr_curves(results, ev.FIGURES / "model_pr_curves.png")
    ev.plot_metrics_bar(comparison, ev.FIGURES / "model_metrics_bar.png")
    ev.plot_confusion_matrices(results, thresholds, ev.FIGURES / "model_confusion_matrices.png")
    if importances:
        ev.plot_feature_importance(importances, ev.FIGURES / "model_feature_importance.png")

    test_meta = test_meta.assign(hit_label=y_test)
    test_meta.to_parquet(DATA / "test_predictions.parquet", index=False)

    print("\n=== TEST COMPARISON (tuned thresholds) ===")
    print(comparison.to_string(index=False))
    print("\n=== FIT TIMES ===")
    for k, v in times.items():
        print(f"  {k}: {v:.1f}s")
    print(f"[total] done in {(time.time() - t_total) / 60:.1f} min")
    if args.sample_frac < 1.0:
        est = {k: v / args.sample_frac for k, v in times.items()}
        print("[gauge] extrapolated full-run fit times:")
        for k, v in est.items():
            print(f"  {k}: ~{v:.0f}s")


if __name__ == "__main__":
    main()
