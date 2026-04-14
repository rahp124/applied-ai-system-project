"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    # Test user profiles (use any one profile for recommendation runs)
    high_energy_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
    }

    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "calm",
        "target_energy": 0.30,
        "likes_acoustic": True,
    }

    deep_intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    }

    # Pick the profile you want to test
    user_prefs = chill_lofi

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "="*60)
    if user_prefs == high_energy_pop:
        print("🎵 TOP MUSIC RECOMMENDATIONS: High Energy Pop")
    elif user_prefs == chill_lofi:
        print("🎵 TOP MUSIC RECOMMENDATIONS: Chill Lofi")
    elif user_prefs == deep_intense_rock:
        print("🎵 TOP MUSIC RECOMMENDATIONS: Deep Intense Rock")
    print("="*60 + "\n")
    
    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{idx}. {song['title']}")
        print(f"   Artist: {song.get('artist', 'Unknown')}")
        print(f"   Score: {score:.2f}/10")
        print(f"   ✓ {explanation}")
        print()
    
    print("="*60)


if __name__ == "__main__":
    main()
