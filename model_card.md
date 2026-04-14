# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

This recommender suggests songs from a small catalog.
It tries to match a user’s genre, mood, energy, and acoustic preference.
The goal is to return a top-5 list that feels close to the user profile.

---

## 3. Data Used

The dataset has 20 songs.
Each song includes genre, mood, energy, tempo, valence, danceability, and acousticness.
Genres are varied, but the catalog is still small.
Because the data is limited, many music styles and edge cases are missing.

---

## 4. Algorithm Summary

The system gives points for genre match and mood match.
It gives more points when the song energy is close to the target energy.
It also adds a bonus when acousticness matches the user’s acoustic preference.
In the experiment, energy weight was increased and genre weight was reduced.
That made energy similarity more important in ranking.

---

## 5. Observed Behavior / Biases

The model can create an energy filter bubble.
Songs with very similar energy can rank high even if genre is different.
This is stronger after the weight shift experiment.
So users may get less variety than expected.

---

## 6. Evaluation Process

I tested three profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock.
I compared the top-5 outputs and checked if reasons matched each profile.
I also ran a weight-shift experiment (higher energy weight, lower genre weight).
A surprise was that non-target genres moved up when their energy was very close to target.

---

## 7. Intended Use and Non-Intended Use

Intended use: classroom exploration of simple recommender behavior.
It is useful for learning how preference weights change outputs.
Non-intended use: real production music recommendations.
It should not be used for high-stakes decisions or personalized profiling.

---

## 8. Ideas for Improvement

1. Add diversity controls so top results are not all from one energy band.
2. Let users choose ranges (not single targets) for energy and mood.
3. Learn weights from feedback instead of fixed manual weights.
