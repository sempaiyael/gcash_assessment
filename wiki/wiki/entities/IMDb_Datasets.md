---
title: IMDb Datasets
type: entity
entity_type: tool
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [data, imdb, dataset]
---

# IMDb Datasets

Official IMDb non-commercial datasets. Updated daily. TSV.gz format.

## Download

https://datasets.imdbws.com/

## Key Files

| File | Fields | Use |
|------|--------|-----|
| title.basics.tsv.gz | tconst, titleType, primaryTitle, startYear, genres | Movie metadata |
| title.ratings.tsv.gz | tconst, averageRating, numVotes | Ratings |
| title.principals.tsv.gz | tconst, nconst, category | Cast/crew per title |
| name.basics.tsv.gz | nconst, primaryName, knownForTitles | Person metadata |
| title.crew.tsv.gz | tconst, directors, writers | Director/writer IDs |
| title.akas.tsv.gz | titleId, ordering, title, region | Alternative titles |

## Key Notes

- `\N` = null (not NaN)
- tconst = "tt" + number (title ID)
- nconst = "nm" + number (person ID)
- titleType: "movie", "short", "tvMovie", etc. — filter to "movie"
- startYear unreliable for future releases

## Related

- [[concepts/IMDb_Datasets]]
- [[concepts/Movie_Feature_Engineering]]