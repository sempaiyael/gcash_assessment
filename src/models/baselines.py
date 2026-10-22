"""Baseline models: Logistic Regression (interpretable floor) and XGBoost
(prioritized tabular-GBDT benchmark, Day 2 decision).

Both consume the same feature frame from data/features.parquet. Categoricals
(certification, language) are one-hot encoded with handle_unknown='ignore';
numeric NaNs: median-imputed for LR, left native for XGBoost.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

CATEGORICAL_FEATURES = ["certification", "language"]
META_COLS = ["tconst", "primaryTitle", "startYear", "hit_score", "split", "hit_label"]


def feature_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    feats = [c for c in df.columns if c not in META_COLS]
    cats = [c for c in feats if c in CATEGORICAL_FEATURES]
    nums = [c for c in feats if c not in CATEGORICAL_FEATURES]
    return nums, cats


def _onehot(nums: list[str], cats: list[str], scale_numeric: bool) -> ColumnTransformer:
    num_steps = [("impute", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scale", StandardScaler()))
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(num_steps), nums),
            ("cat", Pipeline([
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), cats),
        ],
        sparse_threshold=0.3,
    )


def fit_logistic_regression(
    X_train: pd.DataFrame, y_train: np.ndarray,
    X_val: pd.DataFrame, y_val: np.ndarray,
    nums: list[str], cats: list[str],
) -> tuple[Pipeline, float]:
    """class_weight='balanced' handles the ~10% positive rate."""
    pipe = Pipeline([
        ("prep", _onehot(nums, cats, scale_numeric=True)),
        ("clf", LogisticRegression(
            class_weight="balanced", max_iter=2000, solver="lbfgs",
        )),
    ])
    t0 = time.time()
    pipe.fit(X_train, y_train)
    dt = time.time() - t0
    print(f"[lr] fit {len(X_train):,} rows in {dt:.1f}s")
    return pipe, dt


def fit_xgboost(
    X_train: pd.DataFrame, y_train: np.ndarray,
    X_val: pd.DataFrame, y_val: np.ndarray,
    nums: list[str], cats: list[str],
) -> tuple[XGBClassifier, float]:
    """scale_pos_weight = neg/pos on the fit split (class imbalance, D016)."""
    prep = _onehot(nums, cats, scale_numeric=False)
    Xtr = prep.fit_transform(X_train)
    Xva = prep.transform(X_val)
    pos = float(np.sum(y_train == 1))
    spw = float(np.sum(y_train == 0)) / max(pos, 1.0)
    clf = XGBClassifier(
        n_estimators=800,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=5,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0.1,
        scale_pos_weight=spw,
        tree_method="hist",
        eval_metric="auc",
        early_stopping_rounds=50,
        n_jobs=-1,
        random_state=42,
    )
    t0 = time.time()
    clf.fit(Xtr, y_train, eval_set=[(Xva, y_val)], verbose=False)
    dt = time.time() - t0
    best_it = clf.best_iteration
    print(f"[xgb] fit {Xtr.shape[0]:,}x{Xtr.shape[1]} in {dt:.1f}s | "
          f"scale_pos_weight={spw:.2f} | best_iteration={best_it}")
    fitted = (prep, clf)
    return fitted, dt


def predict_proba_xgb(fitted, X: pd.DataFrame) -> np.ndarray:
    prep, clf = fitted
    return clf.predict_proba(prep.transform(X))[:, 1]


def xgb_gain_importance(fitted, top_n: int = 20) -> pd.Series:
    prep, clf = fitted
    names = prep.get_feature_names_out()
    booster = clf.get_booster()
    gain = booster.get_score(importance_type="gain")
    mapped = pd.Series({names[int(k[1:]) if k.startswith("f") and k[1:].isdigit() else k]: v
                        for k, v in gain.items()})
    mapped.index = [i.replace("num__", "").replace("cat__", "") for i in mapped.index]
    return mapped.sort_values(ascending=False).head(top_n)


def lr_coefficient_importance(pipe: Pipeline, top_n: int = 20) -> pd.Series:
    names = pipe.named_steps["prep"].get_feature_names_out()
    coef = np.abs(pipe.named_steps["clf"].coef_.ravel())
    s = pd.Series(coef, index=[n.replace("num__", "").replace("cat__", "") for n in names])
    return s.sort_values(ascending=False).head(top_n)
