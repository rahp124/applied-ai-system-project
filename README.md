# Vibe-to-Vector: AI-Powered Music Recommender (RAG Pipeline)

**Author:** Rahul Punji

## 📌 Project Overview

**Original Project:** _Content-Based Music Recommender Simulation_
Originally, this system was a deterministic, math-based recommendation engine. It parsed a CSV database of songs and scored them against a rigid, hardcoded user profile dictionary (e.g., `target_energy: 0.8`) by calculating the continuous vector proximity and categorical matches of audio features.

**The AI Extension:** _Vibe-to-Vector RAG Pipeline_
This project extends the original simulation by implementing a Retrieval-Augmented Generation (RAG) pipeline to bridge the gap between subjective human language and rigid algorithmic math. Instead of editing a Python dictionary, users can simply type how they feel or what they are doing. The AI translates that semantic "vibe" into mathematical parameters, retrieves the mathematically closest tracks, and then acts as an AI curator to explain why those specific songs fit the user's request.

## 🏗️ Architecture & Data Flow

The system operates in three main phases: Translation, Retrieval, and Synthesis.

```mermaid
graph TD
    UserInput[User Input: Natural Language]
    Translator[Translator Agent: LLM JSON Output]
    JSONCheck[Automated Guardrails: JSON Check & Logging]
    Retriever[Song Search & Ranking: Python Scoring Engine]
    Database[Database: songs.csv]
    Synthesis[Synthesis Agent: LLM Curator]
    Output[Final Conversational Response]

    UserInput --> |Text Request| Translator
    Translator -. |Draft JSON Profile| JSONCheck
    JSONCheck -. |Logged Failure / Fallback| Translator
    JSONCheck --> |Validated JSON Profile| Retriever
    Retriever -. |Query| Database
    Database -. |Song Data| Retriever
    Retriever --> |Top Songs & Metadata| Synthesis
    UserInput --> |Original Context| Synthesis
    Synthesis --> |Approved Response| Output

Translation (Agent): The user's text is sent to the OpenAI API, heavily prompted to output a strictly formatted JSON object representing the audio target variables.

Retrieval (RAG): The system validates the JSON. If valid, it passes the parameters to the original scoring engine to rank and retrieve the top tracks from the dataset.

Synthesis (Curator): The retrieved track metadata and the original user prompt are sent back to the LLM to generate a conversational, explainable AI response.

🚀 Setup Instructions
To run this project locally, follow these steps:

Clone the repository:
git clone [YOUR_REPO_LINK]
cd [YOUR_REPO_FOLDER]

Set up a virtual environment (Recommended):
python -m venv venv
source venv/bin/activate  (Mac/Linux) OR venv\Scripts\activate (Windows)

Install dependencies:
pip install openai python-dotenv

Configure your API Key:
Create a file named .env in the root directory and add your OpenAI API key:
OPENAI_API_KEY=your_api_key_here

Run the application:
python -m src.main

💬 Sample Interactions
Test Case 1: The Standard Use Case
Input: "I'm pulling an all-nighter to finish a coding project. I need something with a steady driving beat to keep me awake, but no vocals to distract me."
System JSON Translation: {'favorite_genre': 'Electronic', 'favorite_mood': 'Focus', 'target_energy': 0.7, 'likes_acoustic': False}
Output: > "To keep you locked in for your coding session, I pulled 'Cyber Pulse' and 'Neon Drive'. Both have that steady, driving electronic energy (around 0.75) you need to stay awake, but they sit squarely in the 'Focus' mood without distracting acoustic elements or vocals."

Test Case 2: The Edge Case / Adversarial Profile
Input: "I want to go to sleep, give me the heaviest, loudest, most intense metal music possible."
System JSON Translation: {'favorite_genre': 'Metal', 'favorite_mood': 'Intense', 'target_energy': 0.95, 'likes_acoustic': False}
Output: > "While heavy metal isn't the typical choice for sleeping, I've queued up 'Stadium Roar' and 'Iron Thunder'. They match your request for maximum intensity and energy perfectly. Sweet dreams!"

🧠 Design Decisions & Trade-offs
RAG over Pure Generation: I chose a RAG architecture instead of just asking an LLM to "name 3 songs." By forcing the LLM to translate text into JSON, I maintain strict, deterministic control over the actual database search. The AI cannot hallucinate a song that doesn't exist in my songs.csv catalog.

JSON Guardrails: LLMs are prone to formatting errors. I implemented a try/except block and the response_format={ "type": "json_object" } parameter. The trade-off is slightly higher latency, but it ensures the core Python logic never crashes due to a bad string. If the LLM fails, it gracefully degrades to a default dictionary profile.

🧪 Testing Summary
Testing revealed that the system handles standard emotional requests (happy, sad, energetic) flawlessly. However, I discovered that highly contradictory inputs (e.g., "fast-paced relaxing acoustic") occasionally caused the LLM to average out the variables, resulting in a mediocre target_energy score of 0.5 rather than committing to an edge case. Implementing the JSON fallback dictionary successfully prevented any crashes during these adversarial tests.

💡 Reflection
[WRITE 1-2 PARAGRAPHS HERE. Mention what it was like bridging standard Python logic with generative AI. How did learning to write strict system prompts change how you view software engineering? Mention how this project helped you understand how real platforms handle massive amounts of subjective user data.]
```
