# AI Powered Music Recommender (RAG Pipeline)

**Author:** Rahul Punji

## 📺 Demo Walkthrough

👉 ([YOUR_LOOM_LINK_HERE](https://www.loom.com/share/908477a49232453a9a75943fbe153e3f))\*\*

---

## 📌 Project Overview

**Original Base Project:** _Content Based Music Recommender Simulation_
Originally, this system was a deterministic recommendation engine. It parsed a local CSV database of songs and scored them against a hardcoded Python dictionary by calculating the continuous vector proximity and categorical matches of acoustic features.

**The AI Extension:** _RAG Pipeline_
This project extends the original simulation by implementing a Retrieval-Augmented Generation pipeline to bridge the gap between subjective human language and math. Instead of editing a Python dictionary, users type how they feel or what they are doing. The AI translates that vibe into parameters, retrieves the mathematically closest tracks from the database, and acts as a curator to explain why those specific songs fit the user's request.

---

## 🏗️ Architecture Overview

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


Translation: The user's text is sent to the OpenAI API, prompted to output a formatted JSON object representing the audio target variables.

Retrieval: The system validates the JSON. If valid, it passes the parameters to the original scoring engine to retrieve the top tracks from the dataset.

Synthesis: The retrieved track metadata and the original user prompt are sent back to the LLM to generate an explainable AI response.

To run this project locally, follow these steps:

Clone the repository

python -m venv venv
source venv/bin/activate
Install dependencies:

pip install openai python-dotenv
Configure your API Key:
Create a file named .env in the root directory and add your OpenAI API key:
OPENAI_API_KEY=sk-your_api_key_here

Run the application:

cd src
python main.py

Test Case:
Input: "I'm pulling an all nighter to finish a coding project. I need something with a steady driving beat to keep me awake, but no vocals to distract me."

System JSON Translation: {'favorite_genre': 'Electronic', 'favorite_mood': 'Focus', 'target_energy': 0.8, 'likes_acoustic': False}

AI Curator Output: > "Hey there! I totally get that you need something to keep your brain buzzing while you tackle that coding project. So, I’ve put together a 3-song setlist that’ll give you the steady driving beat you’re after, without any distracting vocals.

First up, we have **"Neon Bazaar" by Rhythm Cartel**. This track has a euphoric vibe with an energy level of 0.81 and a near-perfect energy proximity of 0.99. It’s got a great non-acoustic feel, which means it’ll keep you engaged without drawing your focus away from your code. Perfect for keeping that adrenaline flowing!

Next, I’m bringing in **"Sunrise City" by Neon Echo**. This one really hits that happy mood at an energy level of 0.82 and also has a high energy proximity of 0.98. The driving beat in this track will help you power through those late-night coding sessions while keeping your spirits up. It’s like a little burst of sunshine for your project!

Lastly, we wrap up with **"Rooftop Lights" by Indigo Parade**. This indie pop gem carries a happy energy, though slightly lower at 0.76, but still maintains a solid energy proximity of 0.96. It's a bit more chill but still has enough groove to keep you in the zone. This one will give you a nice balance as you navigate through the night.

So, with this mix of euphoric beats and happy vibes, you’ll be well-equipped to take on that all-nighter! Happy coding! 🎶"


Design Decisions:
RAG over Pure Generation: I chose RAG instead of just asking an LLM. By forcing the LLM to translate text into JSON, I maintain deterministic control over the database search. The AI cannot hallucinate a song that doesn't exist in my catalog.

LLMs are prone to formatting errors. I implemented a try/except block and the response_format parameter. Slightly higher latency, but it ensures the core logic never crashes due to a bad string.

Building this pipeline demonstrated my ability as a Software Engineer to bridge deterministic backend systems with generative models. By integrating an LLM to handle human input while relying on vector proximity for data retrieval, I learned how to build systems that are accessible to users while remaining controllable and reliable for developers.
```
