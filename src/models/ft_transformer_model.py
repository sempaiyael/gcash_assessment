"""FT-Transformer wrapper (pytorch-tabular 1.2.0).

Theory: Gorishniy et al., NeurIPS 2021 — feature tokenization + CLS token +
Transformer encoder; attention learns feature interactions
(wiki/concepts/FT_Transformer.md).

Class imbalance (~10% positives): weighted CrossEntropyLoss with
w_pos = n_neg / n_pos on the fit split (same recipe as XGBoost's
scale_pos_weight). Early stopping + best-checkpoint restore on valid_auroc.
"""

from __future__ import annotations

import time
import warnings

import numpy as np
import pandas as pd
import torch
from torch import nn

warnings.filterwarnings("ignore", message=".*incompatible dtype.*", category=FutureWarning)

CATEGORICAL_FEATURES = ["certification", "language"]
META_COLS = ["tconst", "primaryTitle", "startYear", "hit_score", "split", "hit_label"]


class WeightedCrossEntropy(nn.Module):
    def __init__(self, pos_weight: float):
        super().__init__()
        self.register_buffer("weight", torch.tensor([1.0, pos_weight], dtype=torch.float32))

    def forward(self, logits, targets):
        w = self.weight.to(logits.device)
        return nn.functional.cross_entropy(logits, targets.long().flatten(), weight=w)


def _frames(X: pd.DataFrame, y: np.ndarray) -> pd.DataFrame:
    df = X.copy()
    df["hit_label"] = y
    return df


def _prep(X: pd.DataFrame, nums: list[str], medians: pd.Series | None = None):
    """Cast numeric to plain float64 and fill NaN (nullable Float64/int dtypes
    and residual NaNs leak through the datamodule scaler and NaN the loss)."""
    X = X.copy()
    for c in nums:
        X[c] = pd.to_numeric(X[c], errors="coerce").astype("float64")
    if medians is None:
        medians = X[nums].median()
    X[nums] = X[nums].fillna(medians)
    for c in CATEGORICAL_FEATURES:
        X[c] = X[c].astype(str).fillna("Unknown").replace({"nan": "Unknown", "<NA>": "Unknown"})
    return X, medians


def fit_ft_transformer(
    X_train: pd.DataFrame, y_train: np.ndarray,
    X_val: pd.DataFrame, y_val: np.ndarray,
    max_epochs: int = 50,
    batch_size: int = 512,
    learning_rate: float = 1e-3,
):
    """Returns (tabular_model, fit_seconds)."""
    from pytorch_tabular import TabularModel
    from pytorch_tabular.config import DataConfig, OptimizerConfig, TrainerConfig
    from pytorch_tabular.models import FTTransformerConfig

    nums = [c for c in X_train.columns if c not in CATEGORICAL_FEATURES and c not in META_COLS]
    cats = [c for c in X_train.columns if c in CATEGORICAL_FEATURES]

    data_config = DataConfig(
        target=["hit_label"],
        continuous_cols=nums,
        categorical_cols=cats,
        handle_missing_values=True,
        normalize_continuous_features=True,
    )
    trainer_config = TrainerConfig(
        batch_size=batch_size,
        max_epochs=max_epochs,
        accelerator="auto",
        devices=1,
        early_stopping="valid_loss",
        early_stopping_mode="min",
        early_stopping_patience=8,
        checkpoints="valid_loss",
        checkpoints_mode="min",
        checkpoints_save_top_k=1,
        load_best=True,
        seed=42,
    )
    pos = float(np.sum(y_train == 1))
    pos_weight = float(np.sum(y_train == 0)) / max(pos, 1.0)
    model_config = FTTransformerConfig(
        task="classification",
        learning_rate=learning_rate,
        attn_feature_importance=True,
        metrics=["accuracy"],
    )
    optimizer_config = OptimizerConfig()

    tabular_model = TabularModel(
        data_config=data_config,
        model_config=model_config,
        optimizer_config=optimizer_config,
        trainer_config=trainer_config,
    )
    t0 = time.time()
    X_fit_p, medians = _prep(X_train, nums)
    X_val_p, _ = _prep(X_val, nums, medians)
    tabular_model.fit(
        train=_frames(X_fit_p, y_train),
        validation=_frames(X_val_p, y_val),
        loss=WeightedCrossEntropy(pos_weight),
    )
    dt = time.time() - t0
    tabular_model._fe_medians = medians
    print(f"[ftt] fit {len(X_train):,} rows in {dt:.1f}s | pos_weight={pos_weight:.2f} | "
          f"device={'cuda' if torch.cuda.is_available() else 'cpu'}")
    return tabular_model, dt


def predict_proba_ftt(tabular_model, X: pd.DataFrame) -> np.ndarray:
    nums = [c for c in X.columns if c not in CATEGORICAL_FEATURES and c not in META_COLS]
    X_p, _ = _prep(X, nums, getattr(tabular_model, "_fe_medians", None))
    pred = tabular_model.predict(X_p)
    return pred["hit_label_1_probability"].to_numpy(dtype=np.float64)


def ftt_attention_importance(tabular_model) -> pd.Series | None:
    """Attention-based feature importance (attn_feature_importance=True).

    NOTE: reflects the most recent forward pass — call right after the
    validation predict and before any other predict calls.
    """
    try:
        imp = tabular_model.model.feature_importance()
        if imp is None:
            return None
        names = (list(tabular_model.config.continuous_cols)
                 + list(tabular_model.config.categorical_cols))
        return pd.Series(np.asarray(imp).ravel(), index=names).sort_values(ascending=False)
    except Exception as e:  # noqa: BLE001 - importance is best-effort
        print(f"[ftt] attention importance unavailable: {e}")
        return None
