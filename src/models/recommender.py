"""MovieLens recommender (bonus deliverable) — KNN baseline + SVD++/SVD.

Protocol (consistent with the project's no-leakage stance, D017/D022):
  * Temporal split by rating timestamp: earliest 90% = train, latest 10% = test.
  * Item support filter (D010 philosophy): only items with >= MIN_ITEM_RATINGS
    train ratings are modeled/recommended — computed on train only.
  * Rating metrics: RMSE / MAE on predictable test rows (warm user + item in train).
  * Ranking metrics: Precision@K / Recall@K / NDCG@K under the standard
    sampled-candidate protocol — each test user's relevant items (test rating
    >= RELEVANT_THRESHOLD) ranked against N_CAND sampled distractors.

Scaling note (why SVD++ runs on a user cohort): surprise's SVD++ updates the
implicit y-factors for every item in a user's history on every rating —
training cost is O(sum_u |I_u|^2 * factors), quadratic in user history. On the
full 21.8M-rating train set that is hours per epoch budget. Plain SVD is
O(|R| * factors) and scales; SVD++ is benchmarked on a fixed COHORT_USERS
sample (all of each cohort user's train ratings retained — histories intact,
unlike a rating-sample which silently shortens them and distorts timing).

# TIMING GAUGE — run `python -m src.models.recommender gauge` FIRST.
#   Gauge: 5% rating sample + 500 cohort users, 3 epochs.
#   OK: full run < 50 min (SVD-full ~15 min, SVD++ cohort ~20 min, KNN ~3 min).
#   Red flag: > 75 min -> cut SVD++ epochs to 5 or COHORT_USERS to 2,500.

Usage:
    python -m src.models.recommender gauge
    python -m src.models.recommender full
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "source_data" / "ml-25m"
DATA = ROOT / "data"
TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "reports" / "figures"

MIN_ITEM_RATINGS = 200
RELEVANT_THRESHOLD = 4.0
N_CAND = 100
TOP_K = 10
RANK_USERS = 5_000
COHORT_USERS = 5_000
SEED = 42


def load_ratings() -> pd.DataFrame:
    t0 = time.time()
    df = pd.read_csv(
        SOURCE / "ratings.csv",
        dtype={"userId": "int32", "movieId": "int32", "rating": "float32", "timestamp": "int64"},
    )
    print(f"[load] {len(df):,} ratings in {time.time() - t0:.0f}s")
    return df


def prepare_splits(df: pd.DataFrame, min_item_ratings: int = MIN_ITEM_RATINGS):
    cutoff = df["timestamp"].quantile(0.90)
    train_all = df[df["timestamp"] <= cutoff].copy()
    test_all = df[df["timestamp"] > cutoff].copy()
    counts = train_all["movieId"].value_counts()
    support = set(counts[counts >= min_item_ratings].index.astype("int64"))
    train = train_all[train_all["movieId"].isin(support)]
    test = test_all[test_all["movieId"].isin(support)]
    train_users = set(train["userId"].unique())
    predictable = test[test["userId"].isin(train_users)]
    print(f"[split] temporal cutoff @ 90th pct timestamp | train={len(train):,} "
          f"test={len(test):,} | supported items={len(support):,} "
          f"({len(train) / len(train_all):.1%} of train ratings kept)")
    print(f"[split] predictable test rows={len(predictable):,} ({len(predictable) / max(len(test), 1):.1%} coverage)")
    return train, predictable, support, train_all, test_all


def _to_trainset(train: pd.DataFrame):
    from surprise import Dataset, Reader

    reader = Reader(rating_scale=(0.5, 5.0))
    ds = Dataset.load_from_df(train[["userId", "movieId", "rating"]], reader)
    return ds.build_full_trainset()


def fit_svdpp(train: pd.DataFrame, n_epochs: int, n_factors: int = 30):
    from surprise import SVDpp

    t0 = time.time()
    trainset = _to_trainset(train)
    t_build = time.time() - t0
    algo = SVDpp(n_factors=n_factors, n_epochs=n_epochs, lr_all=0.005, reg_all=0.02, random_state=SEED)
    t1 = time.time()
    algo.fit(trainset)
    t_fit = time.time() - t1
    print(f"[svd++] fit {len(train):,} ratings | {n_factors} factors x {n_epochs} epochs | "
          f"build {t_build:.0f}s + fit {t_fit:.0f}s ({t_fit / n_epochs:.1f}s/epoch)")
    return algo, t_build + t_fit


def fit_svd(train: pd.DataFrame, n_epochs: int, n_factors: int = 50):
    from surprise import SVD

    t0 = time.time()
    trainset = _to_trainset(train)
    algo = SVD(n_factors=n_factors, n_epochs=n_epochs, lr_all=0.005, reg_all=0.02, random_state=SEED)
    algo.fit(trainset)
    print(f"[svd] fit {len(train):,} ratings | {n_factors} factors x {n_epochs} epochs | "
          f"{time.time() - t0:.0f}s")
    return algo, time.time() - t0


def fit_knn(train: pd.DataFrame):
    from surprise import KNNWithMeans, Dataset, Reader

    t0 = time.time()
    reader = Reader(rating_scale=(0.5, 5.0))
    ds = Dataset.load_from_df(train[["userId", "movieId", "rating"]], reader)
    trainset = ds.build_full_trainset()
    algo = KNNWithMeans(
        k=40, min_k=5, sim_options={"name": "pearson_baseline", "user_based": False, "min_support": 5},
        random_state=SEED,
    )
    algo.fit(trainset)
    print(f"[knn] item-based KNNWithMeans fit on {trainset.n_items:,} items in {time.time() - t0:.0f}s")
    return algo, time.time() - t0


def eval_rating(algo, test: pd.DataFrame) -> dict:
    from surprise import accuracy

    t0 = time.time()
    preds = algo.test(list(zip(test["userId"].tolist(), test["movieId"].tolist(), test["rating"].tolist())))
    rmse = accuracy.rmse(preds, verbose=False)
    mae = accuracy.mae(preds, verbose=False)
    print(f"[rating] RMSE={rmse:.4f} MAE={mae:.4f} on {len(test):,} rows ({time.time() - t0:.0f}s)")
    return {"rmse": float(rmse), "mae": float(mae), "n_rating_rows": int(len(test))}


def eval_ranking(algo, train: pd.DataFrame, test: pd.DataFrame, support: set,
                 n_users: int = RANK_USERS, n_cand: int = N_CAND, k: int = TOP_K) -> dict:
    """Sampled-candidate protocol: relevant = test items rated >= 4; distractors
    sampled from supported items the user never rated."""
    rng = np.random.default_rng(SEED)
    support_arr = np.array(sorted(support), dtype="int64")
    train_rated = train.groupby("userId")["movieId"].agg(set).to_dict()
    test_rel = (
        test[test["rating"] >= RELEVANT_THRESHOLD]
        .groupby("userId")["movieId"].agg(set).to_dict()
    )
    test_rated = test.groupby("userId")["movieId"].agg(set).to_dict()
    users = [u for u in test_rel if u in train_rated][:n_users]

    precs, recs, ndcgs = [], [], []
    t0 = time.time()
    for u in users:
        relevant = test_rel[u] & support
        if not relevant:
            continue
        seen = train_rated[u] | test_rated.get(u, set())
        pool = np.setdiff1d(support_arr, np.fromiter(seen, dtype="int64", count=len(seen)),
                            assume_unique=False)
        if len(pool) == 0:
            continue
        distract = rng.choice(pool, size=min(n_cand, len(pool)), replace=False)
        candidates = list(set(distract.tolist()) | relevant)
        scores = {i: algo.predict(u, int(i), clip=False).est for i in candidates}
        top = sorted(scores, key=scores.get, reverse=True)[:k]
        hits = [1 if i in relevant else 0 for i in top]
        n_rel = min(len(relevant), k)
        precs.append(sum(hits) / k)
        recs.append(sum(hits) / min(len(relevant), k))
        dcg = sum(h / np.log2(idx + 2) for idx, h in enumerate(hits))
        idcg = sum(1.0 / np.log2(idx + 2) for idx in range(n_rel))
        ndcgs.append(dcg / idcg if idcg > 0 else 0.0)

    out = {
        "precision_at_k": float(np.mean(precs)),
        "recall_at_k": float(np.mean(recs)),
        "ndcg_at_k": float(np.mean(ndcgs)),
        "k": k, "n_users_eval": len(precs),
    }
    print(f"[ranking] P@{k}={out['precision_at_k']:.4f} R@{k}={out['recall_at_k']:.4f} "
          f"NDCG@{k}={out['ndcg_at_k']:.4f} over {len(precs)} users ({time.time() - t0:.0f}s)")
    return out


def qualitative(algo, train: pd.DataFrame, pool_items: set, n_users: int = 5, k: int = 10) -> pd.DataFrame:
    movies = pd.read_csv(SOURCE / "movies.csv", dtype={"movieId": "int32"})
    title = dict(zip(movies["movieId"], movies["title"]))
    rng = np.random.default_rng(SEED)
    rated = train.groupby("userId")["movieId"].agg(set).to_dict()
    pool = np.array(sorted(pool_items))
    rows = []
    for u in rng.choice(np.array(list(rated.keys())), size=n_users, replace=False):
        scores = {i: algo.predict(int(u), int(i), clip=False).est
                  for i in rng.choice(pool, size=min(300, len(pool)), replace=False) if i not in rated[u]}
        for rank, i in enumerate(sorted(scores, key=scores.get, reverse=True)[:k], 1):
            rows.append({"userId": int(u), "rank": rank, "movieId": int(i),
                         "title": title.get(int(i), "?"), "score": round(float(scores[i]), 3)})
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="MovieLens recommender")
    parser.add_argument("mode", choices=["gauge", "full"])
    args = parser.parse_args()
    t0 = time.time()

    df = load_ratings()
    train, test, support, _, _ = prepare_splits(df)
    del df

    rng = np.random.default_rng(SEED)
    # Cohort drawn from WARM users (in both train and test) so ranking metrics
    # have statistical size — a uniform train-user sample lands ~230 eval users.
    warm_users = np.intersect1d(train["userId"].unique(), test["userId"].unique())
    if args.mode == "gauge":
        train = train.sample(frac=0.05, random_state=SEED)
        test = test.sample(frac=0.05, random_state=SEED)
        cohort_users = set(rng.choice(warm_users, size=500, replace=False))
        epochs_svdpp, epochs_svd = 3, 3
        rank_users = 500
        print(f"[gauge] SAMPLE_FRAC=0.05 rating-sample + 500 cohort users, 3 epochs, 500 rank-users")
    else:
        cohort_users = set(rng.choice(warm_users, size=min(COHORT_USERS, len(warm_users)), replace=False))
        epochs_svdpp, epochs_svd = 10, 20
        rank_users = RANK_USERS

    train_cohort = train[train["userId"].isin(cohort_users)]
    test_common = test[test["userId"].isin(cohort_users)]
    print(f"[cohort] {len(cohort_users):,} users | cohort train={len(train_cohort):,} | "
          f"common test={len(test_common):,} | full train={len(train):,} | warm test={len(test):,}")

    rows = []

    def _run(name, algo, fit_s, scope):
        r = eval_rating(algo, test_common)
        rank = eval_ranking(algo, train, test_common, support, n_users=rank_users)
        rows.append({"model": name, "test_scope": scope, "fit_s": round(fit_s, 1), **r, **rank})
        return algo

    svdpp_algo, t = fit_svdpp(train_cohort, n_epochs=epochs_svdpp)
    _run("SVD++ (cohort)", svdpp_algo, t, "cohort users")

    svd_cohort_algo, t = fit_svd(train_cohort, n_epochs=epochs_svd)
    _run("SVD (cohort)", svd_cohort_algo, t, "cohort users")

    svd_full_algo, t = fit_svd(train, n_epochs=epochs_svd)
    _run("SVD (full)", svd_full_algo, t, "cohort users")
    r_ext = eval_rating(svd_full_algo, test)
    rows.append({"model": "SVD (full)", "test_scope": "all warm users", "fit_s": np.nan,
                 **r_ext,
                 "precision_at_k": np.nan, "recall_at_k": np.nan, "ndcg_at_k": np.nan,
                 "k": TOP_K, "n_users_eval": 0})

    knn_algo, t = fit_knn(train)
    _run("KNN (item-based)", knn_algo, t, "cohort users")

    examples = qualitative(svdpp_algo, train_cohort, support, n_users=5)

    TABLES.mkdir(parents=True, exist_ok=True)
    comp = pd.DataFrame(rows)
    comp.to_csv(TABLES / f"recommender_comparison_{args.mode}.csv", index=False)
    comp.to_markdown(TABLES / f"recommender_comparison_{args.mode}.md", index=False)
    examples.to_csv(TABLES / f"recommender_examples_{args.mode}.csv", index=False)
    print("\n=== RECOMMENDER COMPARISON ===")
    print(comp.to_string(index=False))
    print(f"\n[total] {args.mode} done in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
