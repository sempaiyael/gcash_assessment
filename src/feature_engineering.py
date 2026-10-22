"""Greenlight-time feature engineering for hit-movie prediction (Day 2).

Builds data/features.parquet from the Day-1 artifacts plus two extractions
from raw sources (movie-cast map, TMDb release timing/language).

LEAKAGE GUARDRAILS (D002, D017) — read before editing:
  * Features may only use information available at greenlight time.
  * Banned as features (they ARE or FEED the label): averageRating, numVotes,
    revenue, popularity, weighted_rating, wr_*, reach_*, roi*, hit_score,
    hit_mode, and the full-history actor_popularity/director_stats parquets.
  * Historical track-record features (director/cast/company/franchise/genre
    momentum) are computed AS-OF: per (entity, year) aggregates cumulated with
    shift(1), so a movie only sees outcomes of strictly EARLIER releases.
  * Label threshold (D016): 90th percentile of hit_score over the <=2018
    training population (fit + val), applied unchanged to test.
  * Split (D017 + Day-2 clarification): fit <=2015, val 2016-2018,
    test 2019-2023. 2024+ rows are dropped (noisy, incomplete labels).

Usage:
    python -m src.feature_engineering extract-cast [--max-chunks N]
    python -m src.feature_engineering extract-tmdb [--max-chunks N]
    python -m src.feature_engineering build

data/movie_cast.parquet:     tconst, nconst, ordering          (actor/actress only)
data/release_dates.parquet:  tconst, release_date, original_language
data/features.parquet:       model-ready frame (see build() docstring)
"""

from __future__ import annotations

import argparse
import re
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCE = ROOT / "source_data"

CAST_CATEGORIES = {"actor", "actress"}
CHUNK_PRINCIPALS = 2_000_000
CHUNK_TMDB = 200_000
TOP_BILLING = 3
MIN_COMPANY_TOKENS = 20
N_TOP_KEYWORDS = 15
N_TOP_LANGUAGES = 10

BANNED_FEATURE_SOURCES = [
    "averageRating", "numVotes", "revenue", "popularity",
    "weighted_rating", "wr_normalized", "reach_log", "reach_normalized",
    "roi", "roi_capped", "roi_normalized", "hit_score", "hit_mode",
]


# ---------------------------------------------------------------------------
# Extractions from raw sources
# ---------------------------------------------------------------------------

def extract_movie_cast(
    valid_tconsts: set[str],
    out_path: Path,
    max_chunks: int | None = None,
    chunksize: int = CHUNK_PRINCIPALS,
) -> pd.DataFrame:
    """title.principals.tsv.gz -> movie-cast map (actor/actress, valid movies).

    TIMING GAUGE — sample: --max-chunks 2 (~4M of ~90M rows, ~4-5%)
    Run the gauge first; extrapolate: full ~= per-chunk-avg x ~45 chunks.
    OK: full run < 15 min. Red flag: > 30 min -> rerun with chunksize=4e6
    or drop ordering > 10 rows inside the chunk filter.
    """
    src = SOURCE / "title.principals.tsv.gz"
    frames: list[pd.DataFrame] = []
    t0 = time.time()
    reader = pd.read_csv(
        src, sep="\t", dtype=str,
        usecols=["tconst", "ordering", "nconst", "category"],
        chunksize=chunksize,
    )
    for i, chunk in enumerate(reader):
        tc = time.time()
        hit = chunk[chunk["tconst"].isin(valid_tconsts) & chunk["category"].isin(CAST_CATEGORIES)]
        hit = hit.assign(ordering=pd.to_numeric(hit["ordering"], errors="coerce").astype("Int16"))
        frames.append(hit[["tconst", "nconst", "ordering"]])
        print(f"[extract-cast] chunk {i + 1}: {len(chunk):,} rows -> {len(hit):,} kept "
              f"in {time.time() - tc:.1f}s (elapsed {time.time() - t0:.0f}s)")
        if max_chunks is not None and i + 1 >= max_chunks:
            out = pd.concat(frames, ignore_index=True)
            print(f"[extract-cast] GAUGE STOP after {i + 1} chunks; NOT writing partial data. "
                  f"per-chunk avg {(time.time() - t0) / (i + 1):.1f}s")
            return out

    out = pd.concat(frames, ignore_index=True)
    out.to_parquet(out_path, index=False)
    print(f"[extract-cast] wrote {out_path} | {len(out):,} rows in {time.time() - t0:.0f}s")
    return out


def extract_tmdb_extras(
    out_path: Path,
    max_chunks: int | None = None,
    chunksize: int = CHUNK_TMDB,
) -> pd.DataFrame:
    """TMDb zip CSV -> release_date + original_language per imdb_id.

    TIMING GAUGE — sample: --max-chunks 2 (~400K of ~1.26M rows)
    Full scan is small: OK < 3 min. Red flag: > 10 min.
    """
    zip_path = SOURCE / "alanvourch-tmdb-movies-daily-updates.zip"
    frames: list[pd.DataFrame] = []
    t0 = time.time()
    with zipfile.ZipFile(zip_path) as z, z.open("TMDB_all_movies.csv") as f:
        reader = pd.read_csv(
            f,
            usecols=["imdb_id", "release_date", "original_language"],
            chunksize=chunksize,
        )
        for i, chunk in enumerate(reader):
            tc = time.time()
            hit = chunk[chunk["imdb_id"].astype("str").str.startswith("tt")]
            frames.append(hit)
            print(f"[extract-tmdb] chunk {i + 1}: {len(chunk):,} rows -> {len(hit):,} kept "
                  f"in {time.time() - tc:.1f}s")
            if max_chunks is not None and i + 1 >= max_chunks:
                out = pd.concat(frames, ignore_index=True)
                print(f"[extract-tmdb] GAUGE STOP after {i + 1} chunks; NOT writing partial data.")
                return out

    out = pd.concat(frames, ignore_index=True).rename(columns={"imdb_id": "tconst"})
    out["release_date"] = pd.to_datetime(out["release_date"], errors="coerce")
    out = out.drop_duplicates(subset="tconst")
    out.to_parquet(out_path, index=False)
    print(f"[extract-tmdb] wrote {out_path} | {len(out):,} rows in {time.time() - t0:.0f}s")
    return out


# ---------------------------------------------------------------------------
# As-of (leakage-safe) historical features
# ---------------------------------------------------------------------------

def _asof_prior(
    base: pd.DataFrame,
    specs: list[tuple[str, str, str]],
    prefix: str,
    year_col: str = "startYear",
) -> pd.DataFrame:
    """Per-(entity, year) aggregates -> cumulative PRIOR-year features.

    base must contain 'entity' and year_col. specs = (out_name, src_col, agg_fn).
    Rows are one per (entity, year); cumsum().groupby(entity).shift(1) makes a
    movie at year Y see only outcomes of years < Y (same-year releases are
    concurrent and correctly invisible to each other).
    """
    aggs = {out: (src, fn) for out, src, fn in specs}
    dy = base.groupby(["entity", year_col], dropna=True).agg(**aggs).reset_index()
    dy = dy.sort_values(["entity", year_col], kind="stable")
    grp = dy.groupby("entity", sort=False)
    for out, _, _ in specs:
        cum = grp[out].cumsum()
        dy[f"{prefix}_prior_{out}"] = cum.groupby(dy["entity"], sort=False).shift(1)
    dy[f"{prefix}_prior_last_year"] = grp[year_col].shift(1)
    dy[f"{prefix}_first_year"] = grp[year_col].transform("min")
    return dy


def _director_features(movies: pd.DataFrame) -> pd.DataFrame:
    base = (
        movies[["primary_director_nconst", "startYear", "hit_score", "numVotes"]]
        .rename(columns={"primary_director_nconst": "entity"})
        .dropna(subset=["entity", "startYear"])
    )
    dy = _asof_prior(
        base,
        specs=[
            ("films", "hit_score", "size"),
            ("hit_sum", "hit_score", "sum"),
            ("votes_sum", "numVotes", "sum"),
        ],
        prefix="director",
    )
    dy["director_prior_avg_hit"] = (
        dy["director_prior_hit_sum"] / dy["director_prior_films"].replace(0, np.nan)
    )
    dy["director_prior_avg_votes"] = (
        dy["director_prior_votes_sum"] / dy["director_prior_films"].replace(0, np.nan)
    )
    dy["director_years_since_debut"] = dy["startYear"] - dy["director_first_year"]
    dy["director_years_since_last"] = dy["startYear"] - dy["director_prior_last_year"]
    keep = dy[[
        "entity", "startYear", "director_prior_films", "director_prior_avg_hit",
        "director_prior_avg_votes", "director_years_since_debut",
        "director_years_since_last",
    ]].rename(columns={"entity": "primary_director_nconst"})
    out = movies[["tconst", "primary_director_nconst", "startYear"]].merge(
        keep, on=["primary_director_nconst", "startYear"], how="left"
    )
    out["director_is_debut"] = (out["director_prior_films"].fillna(0) == 0).astype("int8")
    out["director_prior_films"] = out["director_prior_films"].fillna(0)
    out["director_years_since_last"] = out["director_years_since_last"].fillna(-1)
    return out.drop(columns=["primary_director_nconst", "startYear"])


def _cast_features(movies: pd.DataFrame, movie_cast: pd.DataFrame) -> pd.DataFrame:
    mc = movie_cast.merge(
        movies[["tconst", "startYear", "averageRating", "numVotes", "hit_score",
                "primary_director_nconst"]],
        on="tconst", how="inner",
    )
    # D008/D009: billing-weighted star power of each past credit
    mc["pair_score"] = (
        1.0 / np.log(mc["ordering"].astype(float) + 1.0)
        * mc["numVotes"] * mc["averageRating"]
    )
    base = mc.rename(columns={"nconst": "entity"})
    dy = _asof_prior(
        base,
        specs=[
            ("pop", "pair_score", "sum"),
            ("films", "hit_score", "size"),
            ("hit_sum", "hit_score", "sum"),
        ],
        prefix="cast",
    )
    m2 = mc.merge(dy, left_on=["nconst", "startYear"], right_on=["entity", "startYear"], how="left")
    m2 = m2.drop(columns=["entity"])
    top = m2[m2["ordering"] <= TOP_BILLING]

    agg = top.groupby("tconst").agg(
        cast_pop_sum=("cast_prior_pop", "sum"),
        cast_pop_mean=("cast_prior_pop", "mean"),
        cast_pop_max=("cast_prior_pop", "max"),
        cast_prior_films=("cast_prior_films", "sum"),
        cast_prior_hit_sum=("cast_prior_hit_sum", "sum"),
    ).reset_index()
    agg["cast_prior_avg_hit"] = (
        agg["cast_prior_hit_sum"] / agg["cast_prior_films"].replace(0, np.nan)
    )
    agg = agg.drop(columns=["cast_prior_hit_sum"])

    # actor-director collaboration history (top-billing only)
    pairs = top[["tconst", "nconst", "primary_director_nconst", "startYear"]].dropna()
    pairs = pairs.assign(entity=pairs["nconst"] + "|" + pairs["primary_director_nconst"])
    pdy = _asof_prior(
        pairs,
        specs=[("collab", "tconst", "size")],
        prefix="collab",
    )
    pairs = pairs.merge(pdy, on=["entity", "startYear"], how="left")
    collab = pairs.groupby("tconst")["collab_prior_collab"].sum().rename(
        "actor_director_prior_collabs"
    ).reset_index()

    out = agg.merge(collab, on="tconst", how="left")
    out["actor_director_prior_collabs"] = out["actor_director_prior_collabs"].fillna(0)
    return out


def _franchise_features(movies: pd.DataFrame) -> pd.DataFrame:
    title = movies["primaryTitle"].fillna("").str.lower()
    title = title.str.replace(r"[^a-z0-9 ]", " ", regex=True)
    title = title.str.replace(r"\b(part|episode|vol|volume|chapter|remake)\b\s*(\d+|[ivxlcdm]+)?", " ", regex=True)
    title = title.str.replace(r"\s+([ivxlcdm]{1,6}|\d{1,3})\s*$", " ", regex=True)
    movies = movies.assign(title_group=title.str.replace(r"\s+", " ", regex=True).str.strip())

    base = (
        movies[["title_group", "startYear", "hit_score"]]
        .rename(columns={"title_group": "entity"})
        .dropna(subset=["entity", "startYear"])
    )
    base = base[base["entity"] != ""]
    dy = _asof_prior(
        base,
        specs=[("releases", "hit_score", "size"), ("hit_sum", "hit_score", "sum")],
        prefix="franchise",
    )
    dy["franchise_prior_avg_hit"] = (
        dy["franchise_prior_hit_sum"] / dy["franchise_prior_releases"].replace(0, np.nan)
    )
    keep = dy[["entity", "startYear", "franchise_prior_releases", "franchise_prior_avg_hit"]]
    out = movies[["tconst", "title_group", "startYear"]].rename(
        columns={"title_group": "entity"}
    ).merge(keep, on=["entity", "startYear"], how="left")
    out["franchise_prior_releases"] = out["franchise_prior_releases"].fillna(0)
    marker = movies["primaryTitle"].fillna("").str.contains(
        r"\b(?:ii|iii|iv|v|vi|vii|viii|ix|x)\b|\bpart\s+\d+|\b\d+\b",
        case=False, regex=True,
    )
    out["is_sequel"] = ((out["franchise_prior_releases"] > 0) | marker.values).astype("int8")
    return out[["tconst", "franchise_prior_releases", "franchise_prior_avg_hit", "is_sequel"]]


def _genre_momentum(movies: pd.DataFrame) -> pd.DataFrame:
    g = (
        movies[["tconst", "startYear", "genres", "hit_score"]]
        .dropna(subset=["genres", "startYear"])
        .assign(genre=lambda d: d["genres"].str.split(","))
        .explode("genre")
    )
    g["genre"] = g["genre"].str.strip()
    gy = g.groupby(["genre", "startYear"])["hit_score"].mean().rename("genre_year_hit").reset_index()
    gy = gy.sort_values(["genre", "startYear"], kind="stable")
    gy["genre_prior_hit"] = gy.groupby("genre")["genre_year_hit"].transform(
        lambda s: s.shift(1).expanding().mean()
    )
    gg = g.merge(gy[["genre", "startYear", "genre_prior_hit"]], on=["genre", "startYear"], how="left")
    out = gg.groupby("tconst")["genre_prior_hit"].mean().rename("genre_momentum").reset_index()
    return out


def _company_features(movies: pd.DataFrame) -> pd.DataFrame:
    """Company track record (as-of). NOTE: TMDb company names can contain
    commas ('Johnson and Gibson, J. & N. Tait') so comma-splitting is
    approximate — tokens kept only if they appear >= MIN_COMPANY_TOKENS times.
    """
    c = (
        movies[["tconst", "startYear", "production_companies", "hit_score"]]
        .dropna(subset=["production_companies", "startYear"])
        .assign(company=lambda d: d["production_companies"].str.split(","))
        .explode("company")
    )
    c["company"] = c["company"].str.strip()
    c = c[c["company"] != ""]
    counts = c["company"].value_counts()
    keep_tokens = counts[counts >= MIN_COMPANY_TOKENS].index
    c = c[c["company"].isin(keep_tokens)]
    base = c.rename(columns={"company": "entity"})
    dy = _asof_prior(
        base,
        specs=[("films", "hit_score", "size"), ("hit_sum", "hit_score", "sum")],
        prefix="company",
    )
    dy["company_prior_hit_rate"] = (
        dy["company_prior_hit_sum"] / dy["company_prior_films"].replace(0, np.nan)
    )
    cc = c.merge(dy, left_on=["company", "startYear"], right_on=["entity", "startYear"], how="left")
    agg = cc.groupby("tconst").agg(
        company_prior_hit_max=("company_prior_hit_rate", "max"),
        company_prior_hit_mean=("company_prior_hit_rate", "mean"),
        company_known=("company_prior_hit_rate", "count"),
    ).reset_index()
    return agg


# ---------------------------------------------------------------------------
# Frame assembly
# ---------------------------------------------------------------------------

def build_features(
    movies: pd.DataFrame,
    movie_cast: pd.DataFrame,
    tmdb_extras: pd.DataFrame,
) -> tuple[pd.DataFrame, float]:
    """Returns (feature_frame, label_threshold).

    feature_frame columns: ids/meta (tconst, primaryTitle, startYear, hit_score),
    split, hit_label, then greenlight-time features only.
    """
    df = movies.copy()
    df = df[df["startYear"].notna() & (df["startYear"] <= 2023)].copy()
    df["startYear"] = df["startYear"].astype(int)

    # --- as-of historical blocks ---
    df = df.merge(_director_features(df), on="tconst", how="left")
    df = df.merge(_cast_features(df, movie_cast), on="tconst", how="left")
    df = df.merge(_franchise_features(df), on="tconst", how="left")
    df = df.merge(_genre_momentum(df), on="tconst", how="left")
    df = df.merge(_company_features(df), on="tconst", how="left")

    # --- static greenlight block ---
    df["runtime"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce")
    df["runtime_missing"] = df["runtime"].isna().astype("int8")
    df["runtime"] = df["runtime"].fillna(df["runtime"].median())

    df["log_budget"] = np.log1p(df["budget"].fillna(0))
    df["has_budget"] = (df["budget"].fillna(0) > 0).astype("int8")

    genre_dummies = (
        df["genres"].fillna("").str.get_dummies(sep=",")
    )
    genre_dummies.columns = ["genre_" + g.strip() for g in genre_dummies.columns]
    df = pd.concat([df, genre_dummies], axis=1)
    df["genre_count"] = (df["genres"].fillna("").str.count(",") + 1).where(df["genres"].notna(), 0)

    df["is_usa"] = df["production_countries"].fillna("").str.contains("United States").astype("int8")
    df["n_countries"] = (df["production_countries"].fillna("").str.count(",") + 1).where(
        df["production_countries"].notna(), 0
    )

    df["certification"] = df["certification_us"].fillna("Unknown").replace("", "Unknown")
    df["n_writers"] = (df["writers"].fillna("").str.count(",") + 1).where(df["writers"].notna(), 0)

    kw = df["keywords"].fillna("")
    df["keyword_count"] = (kw.str.count(r"\|") + 1).where(df["keywords"].notna(), 0)
    top_kw = kw.str.split("|").explode().str.strip().value_counts().head(N_TOP_KEYWORDS).index
    kw_dummies = pd.DataFrame(
        {f"kw_{k}": kw.str.split("|").apply(lambda xs, k=k: int(k in [x.strip() for x in xs]))
         for k in top_kw},
        index=df.index,
    )
    df = pd.concat([df, kw_dummies], axis=1)

    # --- release timing + language (TMDb extraction) ---
    df = df.merge(tmdb_extras, on="tconst", how="left")
    month = df["release_date"].dt.month
    df["release_month"] = month.astype("Float64")
    df["month_sin"] = np.sin(2 * np.pi * month.fillna(6) / 12)
    df["month_cos"] = np.cos(2 * np.pi * month.fillna(6) / 12)
    df["is_summer"] = month.between(5, 8).fillna(False).astype("int8")
    df["is_holiday"] = month.between(11, 12).fillna(False).astype("int8")
    df["release_date_missing"] = df["release_date"].isna().astype("int8")

    top_langs = df["original_language"].fillna("unknown").value_counts().head(N_TOP_LANGUAGES).index
    df["language"] = df["original_language"].fillna("unknown").where(
        df["original_language"].fillna("unknown").isin(top_langs), "other"
    )

    # --- label + split (D016 / D017) ---
    df["split"] = np.where(
        df["startYear"] <= 2015, "fit",
        np.where(df["startYear"] <= 2018, "val", "test"),
    )
    train_mask = df["split"].isin(["fit", "val"])
    thr = float(df.loc[train_mask, "hit_score"].quantile(0.90))
    df["hit_label"] = (df["hit_score"] >= thr).astype("int8")

    raw_cols = [
        "titleType", "originalTitle", "isAdult", "endYear", "runtimeMinutes",
        "genres", "directors", "writers", "primary_director_nconst", "director_name",
        "budget", "revenue", "popularity", "production_companies", "production_countries",
        "certification_us", "keywords", "decade", "weighted_rating", "wr_normalized",
        "reach_log", "reach_normalized", "roi", "roi_capped", "roi_normalized",
        "hit_mode", "release_date", "original_language", "title_group",
        "averageRating", "numVotes",
    ]
    df = df.drop(columns=[c for c in raw_cols if c in df.columns])
    return df, thr


def leakage_audit(df: pd.DataFrame, feature_cols: list[str]) -> None:
    offenders = [c for c in feature_cols if c in BANNED_FEATURE_SOURCES]
    if offenders:
        raise AssertionError(f"Banned columns used as features: {offenders}")
    print(f"[audit] {len(feature_cols)} feature cols, 0 banned-source columns")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hit-movie feature engineering")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("extract-cast", help="title.principals -> movie_cast.parquet")
    p1.add_argument("--max-chunks", type=int, default=None, help="timing gauge: stop after N chunks")

    p2 = sub.add_parser("extract-tmdb", help="TMDb zip -> release_dates.parquet")
    p2.add_argument("--max-chunks", type=int, default=None, help="timing gauge: stop after N chunks")

    sub.add_parser("build", help="build data/features.parquet")

    args = parser.parse_args()
    if args.cmd == "extract-cast":
        valid = set(pd.read_parquet(DATA / "valid_tconst_set.parquet")["tconst"])
        extract_movie_cast(valid, DATA / "movie_cast.parquet", max_chunks=args.max_chunks)
    elif args.cmd == "extract-tmdb":
        extract_tmdb_extras(DATA / "release_dates.parquet", max_chunks=args.max_chunks)
    elif args.cmd == "build":
        t0 = time.time()
        movies = pd.read_parquet(DATA / "movies_with_hit_score.parquet")
        movie_cast = pd.read_parquet(DATA / "movie_cast.parquet")
        tmdb_extras = pd.read_parquet(DATA / "release_dates.parquet")
        df, thr = build_features(movies, movie_cast, tmdb_extras)
        feature_cols = [c for c in df.columns if c not in
                        ["tconst", "primaryTitle", "startYear", "hit_score", "split", "hit_label"]]
        leakage_audit(df, feature_cols)
        df.to_parquet(DATA / "features.parquet", index=False)
        print(f"[build] wrote {DATA / 'features.parquet'} | {len(df):,} rows, "
              f"{len(feature_cols)} features | P90 threshold = {thr:.4f}")
        for s in ["fit", "val", "test"]:
            part = df[df["split"] == s]
            print(f"  {s}: n={len(part):,} | positives={int(part.hit_label.sum()):,} "
                  f"({part.hit_label.mean():.1%})")
        print(f"[build] done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
