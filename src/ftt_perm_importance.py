"""Feature importance for the final report figure.

XGBoost gain + LR |coef| are refit (seconds); FT-Transformer uses permutation
importance on a validation subsample — the attention path in pytorch-tabular
1.2.0 returns 152 values for 76 features (known mismatch), and permutation is
model-agnostic and comparable across models.

# TIMING GAUGE — batched permutation: one predict of ~152K rows (76 permuted
# blocks x 2,000 val rows) + 2 baseline fits. OK: < 3 min. Red flag: > 5 min
# -> cut PERM_SAMPLE to 1,000.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from src import evaluation as ev
from src.models import baselines as bl
from src.models import ft_transformer_model as ftt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

PERM_SAMPLE = 2000


def main() -> None:
    t0 = time.time()
    df = pd.read_parquet(DATA / "features.parquet")
    fit_df = df[df["split"] == "fit"].copy()
    val_df = df[df["split"] == "val"].copy()

    X_fit, y_fit, _ = _split(fit_df)
    X_val, y_val, _ = _split(val_df)

    nums, cats = bl.feature_columns(fit_df)
    importances: dict[str, pd.Series] = {}

    pipe, _ = bl.fit_logistic_regression(X_fit, y_fit, X_val, y_val, nums, cats)
    importances["Logistic Regression (|coef|)"] = bl.lr_coefficient_importance(pipe)

    fitted, _ = bl.fit_xgboost(X_fit, y_fit, X_val, y_val, nums, cats)
    importances["XGBoost (gain)"] = bl.xgb_gain_importance(fitted)

    from pytorch_tabular import TabularModel
    model = TabularModel.load_model(str(DATA / "ft_transformer_model"))
    model._fe_medians = ftt._prep(X_fit, nums)[1]

    val_sample = val_df.sample(n=min(PERM_SAMPLE, len(val_df)), random_state=42)
    Xs = val_sample.drop(columns=bl.META_COLS)
    ys = val_sample["hit_label"].to_numpy()

    # One batched predict instead of per-feature calls: each block is Xs with a
    # single column permuted (sklearn's permutation_importance would rebuild the
    # pytorch-tabular dataloader 77+ times -> 15+ min).
    blocks = []
    for i, col in enumerate(Xs.columns):
        Xp = Xs.copy()
        Xp[col] = np.random.default_rng(i).permutation(Xp[col].to_numpy())
        blocks.append(Xp)
    X_all = pd.concat([Xs] + blocks, ignore_index=True)
    t_pred = time.time()
    proba_all = ftt.predict_proba_ftt(model, X_all)
    print(f"[perm] batched predict of {len(X_all):,} rows in {time.time() - t_pred:.1f}s")
    n = len(Xs)
    baseline = roc_auc_score(ys, proba_all[:n])
    drops = []
    for i, col in enumerate(Xs.columns):
        auc = roc_auc_score(ys, proba_all[(i + 1) * n:(i + 2) * n])
        drops.append(baseline - auc)
    s = pd.Series(drops, index=Xs.columns)
    importances["FT-Transformer (permutation AUC)"] = s.sort_values(ascending=False)
    print(f"[perm] baseline AUC={baseline:.4f}")
    print(s.sort_values(ascending=False).head(15).to_string())

    ev.FIGURES.mkdir(parents=True, exist_ok=True)
    ev.plot_feature_importance(importances, ev.FIGURES / "model_feature_importance.png")
    print(f"[done] wrote {ev.FIGURES / 'model_feature_importance.png'}")


def _split(df: pd.DataFrame):
    X = df.drop(columns=bl.META_COLS)
    y = df["hit_label"].to_numpy()
    meta = df[["tconst", "primaryTitle", "startYear", "hit_score"]].copy()
    return X, y, meta


if __name__ == "__main__":
    main()
