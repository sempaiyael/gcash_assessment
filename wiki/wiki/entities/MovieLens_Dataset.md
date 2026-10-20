---
title: MovieLens Dataset
type: entity
entity_type: tool
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [data, movielens, dataset, recommender]
---

# MovieLens Dataset

Movie rating dataset from GroupLens Research. Used for recommender system.

## Download

https://grouplens.org/datasets/movielens/

## Versions

| Version | Size | Use |
|---------|------|-----|
| ml-latest-small | 100K ratings | Quick prototyping |
| ml-25M | 25M ratings | Full analysis |

## Key Files

| File | Fields | Use |
|------|--------|-----|
| ratings.csv | userId, movieId, rating, timestamp | User ratings |
| movies.csv | movieId, title, genres | Movie metadata |
| links.csv | movieId, imdbId, tmdbId | Mapping to IMDb |

## Key Notes

- movieId is MovieLens-specific, NOT the same as IMDb tconst
- Use links.csv to map movieId → imdbId → tconst
- Timestamps are Unix epoch
- Ratings are 0.5 to 5.0

## Related

- [[concepts/Recommender_Systems]]
- [[concepts/MovieLens_Dataset]]