---
title: Data Sources
type: concept
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [data, api, sources, augmentation]
---

# Data Sources

External APIs and data sources for augmenting IMDb data. Priority order for our 3-day timeline.

## Source Overview

| Source | Key Data | Cost | Priority |
|--------|---------|------|----------|
| **IMDb Datasets** | Title basics, ratings, crew, principals | Free (bulk) | Primary — Day 1 |
| **TMDb (Kaggle)** | Budget, revenue, cast, director, genres | Free (Kaggle) | Primary — Day 1 (D007) |
| **MovieLens** | Ratings, links to IMDb | Free | Bonus — Day 3 |
| **OMDb API** | IMDb ratings, Metascore, RT | Free (1K req/day) | Medium — if needed |
| **Box Office Mojo** | Box office, opening weekend, theater counts | Free (scraping) | Low — Day 2 if weak |
| **The Numbers** | Production budgets, profit/loss | Free (scraping) | Low — if TMDb insufficient |
| **YouTube Data API** | Trailer views, comments | Free (quota-limited) | Not for this project |

## TMDb Data (Kaggle — D007)

- **Source**: alanvourch's "Ultimate 1M Movies Dataset (TMDB + IMDb)"
- **URL**: https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates
- **File**: `TMDB_all_movies.csv` (760 MB uncompressed, 341 MB zip)
- **Rows**: 1,261,171
- **Columns (30)**: id, title, vote_average, vote_count, status, release_date, revenue, runtime, budget, imdb_id, original_language, original_title, overview, popularity, tagline, genres, production_companies, production_countries, spoken_languages, cast, director, director_of_photography, writers, producers, music_composer, imdb_rating, imdb_votes, poster_path, keywords, certification_us
- **Coverage**: 55% have imdb_id, 6.8% have budget > 0, 2.3% have revenue > 0, 1.2% have both, 38% have IMDb votes
- **Join key**: `imdb_id` → IMDb `tconst`
- **Resolution**: Used instead of TMDb API (D007) — no rate limits, no API key needed
- **Quality verified**: 2026-10-20 (see F002 for rejected alternative)

## OMDb API

- **URL**: https://www.omdbapi.com/
- **Provides**: IMDb ratings, Metascore, Rotten Tomatoes, runtime, genre, awards
- **Rate limits**: 1,000 requests/day (free tier)
- **Use case**: Cross-reference ratings, add critic scores

## Box Office Mojo

- **URL**: https://www.boxofficemojo.com/
- **Provides**: Domestic/worldwide box office, opening weekend, theater counts
- **Access**: Web scraping (owned by IMDb/Amazon)
- **Use case**: Revenue data if TMDb insufficient

## The Numbers

- **URL**: https://www.the-numbers.com/
- **Provides**: Production budgets, profit/loss estimates, DVD/streaming revenue
- **Access**: Web scraping
- **Use case**: Best publicly available budget data

## IMDb Datasets

See [[entities/IMDb_Datasets]] for file details.

## MovieLens

See [[entities/MovieLens_Dataset]] for file details.

## Data Augmentation Priority

1. IMDb datasets (primary — always)
2. TMDb Kaggle dataset (budget data — D007, already resolved)
3. OMDb API (critic scores — if time permits)
4. Box Office Mojo / The Numbers (unlikely needed)

## Related

- [[concepts/Movie_Feature_Engineering]] — what features to extract
- [[concepts/Deferred_Items]] — when to revisit each source
- [[entities/IMDb_Datasets]] — primary data
- [[entities/MovieLens_Dataset]] — bonus data