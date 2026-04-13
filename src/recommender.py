import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of typed dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            raw_id = (row.get("id") or "").strip()

            # Skip blank/comment/non-data rows.
            if not raw_id or raw_id.startswith("#"):
                continue

            try:
                song = {
                    "id": int(raw_id),
                    "title": (row.get("title") or "").strip(),
                    "artist": (row.get("artist") or "").strip(),
                    "genre": (row.get("genre") or "").strip(),
                    "mood": (row.get("mood") or "").strip(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            except (KeyError, TypeError, ValueError):
                # Skip malformed rows safely.
                continue

            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a weighted match score and human-readable reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    # Weighted categorical matches
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match")

    # Weighted numerical proximity on energy
    target_energy = user_prefs.get("energy")
    song_energy = song.get("energy")
    if target_energy is not None and song_energy is not None:
        proximity = 1.0 - abs(float(song_energy) - float(target_energy))
        proximity = max(0.0, min(1.0, proximity))
        score += 1.5 * proximity
        reasons.append(f"energy proximity {proximity:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score, rank, and return the top-k song recommendations."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]

    return [
        (song, score, "; ".join(reasons) if reasons else "closest overall match")
        for song, score, reasons in ranked
    ]
