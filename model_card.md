**Developer:** Rahul Punji

## Reliability and Evaluation: How I Tested and Improved the AI

To ensure this system was robust enough for production, I relied on **logging and error handling** combined with **human evaluation**. Because the core pipeline relies on an LLM outputting perfectly formatted JSON, my primary evaluation metric was whether the system could survive a bad LLM response without crashing.

**Testing Summary:**
the AI struggled when given highly contradictory context ("fast paced relaxing lullaby"). System reliability reached 100% after adding a try/except validation rule that logged JSON parsing failures and safely triggered a fallback default profile.

## 5. Reflection and Ethics: Thinking Critically About the AI

### Limitations and Biases

This system inherits inherent biases from both the LLM and the local dataset. The OpenAI model is heavily skewed towards Western music and popular genres. If a user inputs complex cultural requests, the LLM often forces them into generic buckets. Because the retrieval acts on a limited local dataset, the retriever cannot fulfill a perfect JSON request if the catalog lacks that specific genre.

### Potential Misuse and Prevention

A potential misuse of this system involves prompt injection or abuse. Someone could input a complex text payload or malicious instructions designed to bypass the JSON formatting, potentially crashing the application or racking up costs. To prevent this, I implemented strict enforcement using the OpenAI API and wrapped the parsing logic in a try/except guardrail. If the system detects such output, it silently catches the error and falls back to a default user profile.

### Testing Surprises

During reliability testing, I was surprised by how the LLM handled highly contradictory inputs. Instead of prioritizing one trait, the LLM often averaged the values out. This highlighted that LLMs tend to seek mathematical consensus.

### AI Collaboration Reflection

Building this pipeline required heavy collaboration with GitHub Copilot/Chat, which presented both massive time savings and subtle debugging challenges.

- **Helpful Suggestion:** Copilot was useful when implementing the data ingestion layer. It accurately anticipated my need to cast numerical CSV columns to floats and ints, writing a dictionary comprehension to handle the type casting.
- **Flawed Suggestion:** When writing the sorting logic for the recommendation engine, Copilot confidently suggested using list.sort(). This was somewhat flawed because it mutated my original catalog of songs in place. I had to manually intervene, debug, and switch the logic to use Python's sorted function to ensure the core dataset remained for subsequent searches.
