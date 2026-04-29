"""
Command line runner for the Music Recommender RAG Pipeline.

This file implements a full Retrieval-Augmented Generation (RAG) pipeline:
1. Load the song database from CSV
2. Get user vibe description via terminal input
3. Parse vibe to structured preferences using OpenAI
4. Recommend top songs based on preferences
5. Generate curated response from music curator using OpenAI
"""

import os
from dotenv import load_dotenv

from recommender import load_songs, recommend_songs, parse_vibe_to_dict, generate_curator_response


def main() -> None:
    # Load environment variables and get OpenAI API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment.")
        print("Please set it in your .env file or as an environment variable.")
        return
    
    # Load the song database
    songs = load_songs("../data/songs.csv") 
    print(f"✓ Loaded {len(songs)} songs from database")
    
    # Get user vibe description
    print("\n" + "="*60)
    user_input = input("What kind of vibe are you looking for? ").strip()
    print("="*60)
    
    if not user_input:
        print("No vibe provided. Exiting.")
        return
    
    # Parse user vibe to structured preferences
    print("\n🎧 Analyzing your vibe...")
    user_prefs = parse_vibe_to_dict(user_input, api_key)
    print(f"✓ Parsed preferences: {user_prefs}")
    
    # Get top 3 song recommendations
    print("\n🎵 Finding the perfect tracks...")
    recommendations = recommend_songs(user_prefs, songs, k=3)
    
    # Extract just the songs for curator response
    top_songs = [rec[0] for rec in recommendations]
    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        top_songs[idx - 1]['reasons'] = explanation
    
    # Generate curator response
    print("\n🎤 Crafting your curator response...")
    curator_response = generate_curator_response(user_input, top_songs, api_key)
    
    # Display results
    print("\n" + "="*60)
    print("🎵 YOUR PERSONALIZED MUSIC CURATOR RESPONSE")
    print("="*60)
    print(curator_response)
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
