"""Evaluation metrics and comparison charts (Phase 3).

Metrics: ROC-AUC, PR-AUC (average precision), F1/precision/recall at 0.5 and
at the F1-optimal threshold tuned on the validation split. Class imbalance
(~10% positives) makes PR-AUC the primary ranking metric alongside ROC-AUC.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "reports" / "figures"
TABLES = ROOT / "reports" / "tables"


def tune_f1_threshold(y_true: np.ndarray, y_proba: np.ndarray) -> float:
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    f1 = 2 * precision * recall / np.clip(precision + recall, 1e-12, None)
    if len(thresholds) == 0:
        return 0.5
    return float(thresholds[int(np.nanargmax(f1[:-1]))])


def compute_metrics(y_true: np.ndarray, y_proba: np.ndarray, threshold: float) -> dict:
    y_pred = (y_proba >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, y_proba)),
        "pr_auc": float(average_precision_score(y_true, y_proba)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "threshold": float(threshold),
    }


def evaluate_model(
    name: str,
    y_val: np.ndarray, val_proba: np.ndarray,
    y_test: np.ndarray, test_proba: np.ndarray,
) -> dict:
    thr = tune_f1_threshold(y_val, val_proba)
    val_m = compute_metrics(y_val, val_proba, thr)
    test_m = compute_metrics(y_test, test_proba, thr)
    test_m05 = compute_metrics(y_test, test_proba, 0.5)
    return {
        "model": name,
        "threshold_tuned": thr,
        "val": val_m,
        "test": test_m,
        "test_at_0.5": test_m05,
    }


def plot_roc_curves(results: dict[str, tuple[np.ndarray, np.ndarray]], out_path: Path) -> None:
    """results: name -> (y_true, y_proba) on the test split."""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for name, (y, p) in results.items():
        fpr, tpr, _ = roc_curve(y, p)
        auc = roc_auc_score(y, p)
        ax.plot(fpr, tpr, lw=2, label=f"{name} (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="chance")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("Test ROC curves (2019-2023)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_pr_curves(results: dict[str, tuple[np.ndarray, np.ndarray]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for name, (y, p) in results.items():
        precision, recall, _ = precision_recall_curve(y, p)
        ap = average_precision_score(y, p)
        ax.plot(recall, precision, lw=2, label=f"{name} (AP={ap:.3f})")
    base = results[next(iter(results))][0].mean()
    ax.axhline(base, color="k", ls="--", lw=1, label=f"baseline ({base:.1%})")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Test precision-recall curves (2019-2023)")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_metrics_bar(comparison: pd.DataFrame, out_path: Path) -> None:
    metrics = ["roc_auc", "pr_auc", "f1", "precision", "recall"]
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(metrics))
    width = 0.8 / len(comparison)
    for i, row in comparison.iterrows():
        ax.bar(x + i * width, [row[m] for m in metrics], width, label=row["model"])
    ax.set_xticks(x + width * (len(comparison) - 1) / 2)
    ax.set_xticklabels(metrics)
    ax.set_ylim(0, 1)
    ax.set_title("Test metrics at tuned threshold")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_confusion_matrices(
    results: dict[str, tuple[np.ndarray, np.ndarray]],
    thresholds: dict[str, float],
    out_path: Path,
) -> None:
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 3.5))
    if n == 1:
        axes = [axes]
    for ax, (name, (y, p)) in zip(axes, results.items()):
        cm = confusion_matrix(y, (p >= thresholds[name]).astype(int))
        ax.imshow(cm, cmap="Blues")
        for (i, j), v in np.ndenumerate(cm):
            ax.text(j, i, str(v), ha="center", va="center",
                    color="white" if v > cm.max() / 2 else "black")
        ax.set_title(name)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
    fig.suptitle("Test confusion matrices (tuned thresholds)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_feature_importance(importances: dict[str, pd.Series], out_path: Path, top_n: int = 20) -> None:
    n = len(importances)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 8))
    if n == 1:
        axes = [axes]
    for ax, (name, s) in zip(axes, importances.items()):
        s = s.head(top_n)[::-1]
        ax.barh(s.index, s.values)
        ax.set_title(f"{name} — top {min(top_n, len(s))}")
        ax.grid(alpha=0.3, axis="x")
    fig.suptitle("Feature importance (test-relevant drivers of hit prediction)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def save_comparison(evals: list[dict], out_csv: Path) -> pd.DataFrame:
    rows = []
    for e in evals:
        rows.append({
            "model": e["model"],
            "roc_auc": e["test"]["roc_auc"],
            "pr_auc": e["test"]["pr_auc"],
            "f1": e["test"]["f1"],
            "precision": e["test"]["precision"],
            "recall": e["test"]["recall"],
            "threshold": e["threshold_tuned"],
            "roc_auc_at_0.5": e["test_at_0.5"]["roc_auc"],
            "f1_at_0.5": e["test_at_0.5"]["f1"],
        })
    comparison = pd.DataFrame(rows).sort_values("roc_auc", ascending=False)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(out_csv, index=False)
    md = comparison.to_markdown(index=False, floatfmt=".3f")
    out_csv.with_suffix(".md").write_text(md, encoding="utf-8")
    return comparison


def precision_at_k(y_true: np.ndarray, y_proba: np.ndarray, ks: list[int]) -> dict[int, float]:
    """Precision among the top-K scored items — the greenlight-slate metric (D025).

    At an 8% base rate, P@K is the business-facing form of precision: 'of the
    films we endorse, how many are actually hits?'
    """
    order = np.argsort(-y_proba)
    return {k: float(y_true[order[:k]].mean()) for k in ks}


def plot_precision_at_k(
    results: dict[str, tuple[np.ndarray, np.ndarray]],
    out_fig: Path,
    out_csv: Path,
) -> pd.DataFrame:
    """Slate-precision curves + P@K table (D025: two-tier greenlight framing).

    results: name -> (y_true, y_proba) on the test split.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    rows = []
    ks_curve = np.unique(np.round(np.logspace(np.log10(10), np.log10(3000), 40)).astype(int))
    for name, (y, p) in results.items():
        order = np.argsort(-p)
        ax.plot(ks_curve, [y[order[:k]].mean() for k in ks_curve], lw=2.2, label=name)
        row = {"model": name}
        row.update({f"P@{k}": round(v, 3) for k, v in precision_at_k(y, p, [25, 50, 100, 250]).items()})
        rows.append(row)
    base = results[next(iter(results))][0].mean()
    ax.axhline(base, color="k", ls="--", lw=1, label=f"base rate ({base:.0%})")
    ax.set_xscale("log")
    ax.set_xlabel("Slate size (top-K picks by model score)")
    ax.set_ylabel("Precision@K  (share of picks that are hits)")
    ax.set_title("Greenlight slate precision — top-K picks, test 2019-2023")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")
    fig.tight_layout()
    out_fig.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_fig, dpi=150)
    plt.close(fig)
    table = pd.DataFrame(rows)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_csv, index=False)
    return table
