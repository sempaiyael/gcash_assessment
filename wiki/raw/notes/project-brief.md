# Project Brief — Original Email

> Source: GCash hiring team email (2026-10-19)
> This is the single source of truth for project requirements.

---

## Instructions

This test is designed to simulate an end-to-end data science project flow in GCash, from data engineering, analysis, modeling, and storytelling. We encourage creativity and technical rigor in approaching our business problems.

You are free to use any tools of your choice.

Please email all the relevant slides, code (or Git repository), and files to the hiring team.

---

## Project: Give Me The Next AAA Title

The Internet Movie Database, imdb.com, is a website devoted to collecting movie data supplied by studios and fans. It claims to be the biggest movie database on the web and is run by Amazon. IMDb makes its data available publicly, with more information on the fields listed here.

You can use other data sources such as the MovieLens data set. Feel free to augment your data as well through web scraping or finding other relevant data sets.

---

## REQUIRED

Prepare a presentation to convince the hypothetical management team of a movie studio (and their data scientists) deciding how to make the next AAA title.

### EDA Questions

Perform an exploratory analysis looking into the following questions:

1. What is the highest rated movie in 2023? How do we balance ratings and number of votes?
2. Who was the most popular actor in 2023?
3. What are the trends in user-movie preferences over the years?

### Hit Movie Metric

4. Define a metric that captures the notion of a 'hit movie'; justify your metric in the context of a movie studio director looking to invest in building the next AAA title.

### Prediction Model

- Build a model to predict the next AAA title using the given data plus other data you may think would be predictive.
- Be as creative as possible and incorporate other data sets, features, and algorithms beyond your typical supervised ML models (such as logistic regression or XGBoost).
- Motivate your choice of a novel algorithm and be prepared to discuss its theoretical underpinnings from the source paper or material. Cite your sources.

---

## BONUS (Optional: working on this will help improve your chances)

### Recommender System

Using the MovieLens ratings data set, build a recommender system applying an algorithm of your choice:

1. Implement a naive benchmark model (e.g. KNN, popular strategy)
2. Implement another model of your choice (e.g. matrix factorization models with collaborative filtering, content-based filtering, etc.)
3. Prepare a discussion on the theoretical underpinnings of the model, supported by academic literature (please cite your references properly)
4. Identify a metric to optimize your model; justify the metric
5. Compare the benchmark model and model of your choice against this metric
6. Give a qualitative assessment of the model's predictions - do these recommendations make sense?

### Bonus Presentation

Prepare a presentation that achieves the following:
- Details your model development process and results
- Convince the hypothetical management team of a movie streaming service (and their data scientists) to adopt your recommender system

---

## Deliverables

| Item | Type | Required |
|------|------|----------|
| Presentation slides (studio exec) | Slides | Yes |
| EDA analysis | Code + slides | Yes |
| Hit movie metric | Analysis + slides | Yes |
| Prediction model | Code + slides | Yes |
| Novel algorithm citations | Slides | Yes |
| Code / Git repository | Code | Yes |
| Recommender system | Code + slides | Bonus |
| Second presentation (streaming exec) | Slides | Bonus |