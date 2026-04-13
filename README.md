# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders combine behavior signals (plays, skips, repeats, saves) with content signals (audio features and metadata). This project focuses on a transparent content-based approach: each song is scored against a user taste profile, then the songs are ranked and the top K are returned.

### Features Used

**Song features (`Song`)**

- `genre`
- `mood`
- `energy`
- `tempo_bpm`
- `valence`
- `danceability`
- `acousticness`

**User profile features (`UserProfile` / preferences)**

- `favorite_genre` (or allowed genres)
- `favorite_mood` (or allowed moods)
- `target_energy` or `target_energy_range`
- `target_tempo_bpm_range`
- `target_valence_range`
- `target_danceability_range`
- `target_acousticness_range`
- `likes_acoustic`

### Finalized Algorithm Recipe

1. Load user profile and songs from `data/songs.csv`.
2. For each song, compute:
   - **Genre score**: `+2.0` if song genre matches user preferred genre(s), else `0`.
   - **Mood score**: `+1.0` if song mood matches user preferred mood(s), else `0`.
   - **Energy proximity score**: `+1.5 * proximity`, where `proximity = 1 - |song_energy - target_energy|` (or range-based score if using ranges).
   - **Tempo score**: `+1.0 * range_score(song_tempo, target_tempo_range)`.
   - **Valence score**: `+1.0 * range_score(song_valence, target_valence_range)`.
   - **Danceability score**: `+1.0 * range_score(song_danceability, target_danceability_range)`.
   - **Acousticness score**: `+0.5 * range_score(song_acousticness, target_acousticness_range)`.
3. Sum all parts to get `total_song_score`.
4. Sort songs by `total_song_score` in descending order.
5. Return Top K recommendations with short explanations.

Default weights used in this plan:

- `genre: 2.0`
- `mood: 1.0`
- `energy: 1.5`
- `tempo_bpm: 1.0`
- `valence: 1.0`
- `danceability: 1.0`
- `acousticness: 0.5`

### Potential Biases / Risks

- This system may over-prioritize `genre`, ignoring songs with excellent mood/energy fit in other genres.
- It may favor tracks near the center of chosen numeric ranges and down-rank creative outliers.
- Mood and genre labels are subjective, so inconsistent tags can skew rankings.
- With a small catalog, recommendations may repeat similar styles and reduce discovery diversity.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:

- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:

- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:

- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```

![Terminal Output showing ranked songs](output.png)
