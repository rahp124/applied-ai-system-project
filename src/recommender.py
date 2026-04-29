import csv
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from openai import OpenAI

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

    # Support both naming styles:
    # new: favorite_genre/favorite_mood/target_energy/likes_acoustic
    # old: genre/mood/energy
    preferred_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    preferred_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    song_genre = song.get("genre")
    song_mood = song.get("mood")
    song_energy = song.get("energy")
    song_acousticness = song.get("acousticness")

    # Weighted categorical matches (experiment: genre weight halved)
    if isinstance(preferred_genre, str) and isinstance(song_genre, str) and song_genre.lower() == preferred_genre.lower():
        score += 1.0
        reasons.append("genre match")

    if isinstance(preferred_mood, str) and isinstance(song_mood, str) and song_mood.lower() == preferred_mood.lower():
        score += 1.0
        reasons.append("mood match")

    # Weighted numerical proximity on energy (experiment: energy weight doubled)
    if target_energy is not None and song_energy is not None:
        proximity = 1.0 - abs(float(song_energy) - float(target_energy))
        proximity = max(0.0, min(1.0, proximity))
        score += 3.0 * proximity
        reasons.append(f"energy proximity {proximity:.2f}")

    # Acoustic preference bonus
    if isinstance(likes_acoustic, bool) and song_acousticness is not None:
        acousticness = float(song_acousticness)
        if likes_acoustic and acousticness >= 0.6:
            score += 1.0
            reasons.append("acoustic-friendly")
        elif not likes_acoustic and acousticness <= 0.4:
            score += 1.0
            reasons.append("non-acoustic vibe")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score, rank, and return the top-k song recommendations."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]

    return [
        (song, score, "; ".join(reasons) if reasons else "closest overall match")
        for song, score, reasons in ranked
    ]

def parse_vibe_to_dict(user_text: str, api_key: str) -> Dict:
    """
    Parse user's text description of their music vibe into a structured dictionary
    using OpenAI's API with JSON-formatted response.
    
    Args:
        user_text: The user's natural language description of their music preferences
        api_key: OpenAI API key for authentication
    
    Returns:
        A dictionary with keys: favorite_genre, favorite_mood, target_energy, likes_acoustic.
        Falls back to sensible defaults if API call fails.
    """
    # Initialize OpenAI client with provided API key
    client = OpenAI(api_key=api_key)
    
    # System prompt for music data analyst
    system_prompt = """You are a music data analyst. Analyze the user's text description of their music preferences 
and output a JSON object with exactly these four keys:
- 'favorite_genre': a string representing the music genre (e.g., "Electronic", "Jazz", "Pop")
- 'favorite_mood': a string representing the mood (e.g., "Energetic", "Relaxing", "Focus")
- 'target_energy': a float between 0.0 and 1.0 representing desired energy level
- 'likes_acoustic': a boolean indicating whether the user prefers acoustic elements

Respond ONLY with valid JSON, no additional text."""
    
    try:
        # Make API call with JSON response format enforcement
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            response_format={"type": "json_object"}
        )
        
        # Extract and parse the JSON response
        response_text = response.choices[0].message.content
        parsed_dict = json.loads(response_text)
        
        return parsed_dict
        
    except Exception as e:
        print(f"Warning: Failed to parse vibe with OpenAI API: {e}")
        
        # Return default fallback dictionary
        return {
            "favorite_genre": "Electronic",
            "favorite_mood": "Focus",
            "target_energy": 0.75,
            "likes_acoustic": False
        }

def generate_curator_response(user_text: str, recommended_songs: List[Dict], api_key: str) -> str:
    """
    Generate a conversational curator response explaining the recommended song setlist.
    
    Args:
        user_text: The user's original description of their music vibe
        recommended_songs: List of dictionaries containing song metadata and matching reasons
        api_key: OpenAI API key for authentication
    
    Returns:
        A conversational string response from the music curator
    """
    # Initialize OpenAI client with provided API key
    client = OpenAI(api_key=api_key)
    
    # System prompt for music curator persona
    system_prompt = """You are a cool, knowledgeable music curator with great taste. 
Your job is to explain why you've curated a specific 3-song setlist based on a listener's requested vibe. 
Write in a short, conversational, friendly tone. 
Naturally weave in the song titles and some of the numeric reasons (like energy levels, mood matches, or acoustic preferences) 
to show why each song was chosen. 
Make it feel like a personal recommendation from someone who really gets music."""
    
    # Format recommended songs for the user prompt
    songs_description = ""
    for i, song_info in enumerate(recommended_songs, 1):
        title = song_info.get('title', 'Unknown')
        artist = song_info.get('artist', 'Unknown')
        genre = song_info.get('genre', 'Unknown')
        mood = song_info.get('mood', 'Unknown')
        energy = song_info.get('energy', 'N/A')
        reasons = song_info.get('reasons', 'great match')
        
        songs_description += f"\n{i}. \"{title}\" by {artist} - Genre: {genre}, Mood: {mood}, Energy: {energy}, Why picked: {reasons}"
    
    user_prompt = f"""The listener requested: "{user_text}"

Here's the 3-song setlist I've curated for them:{songs_description}

Please write a short, conversational response explaining why I chose this setlist based on their requested vibe. Naturally incorporate the song titles and weave in the energy levels and other reasons."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Warning: Failed to generate curator response: {e}")
        return "I had trouble putting together my curator thoughts, but these songs should really match your vibe!"
