# 🤖 AI Game Referee: Rock-Paper-Scissors-Plus

An AI-powered Game Referee built using the **Google GenAI SDK**. This agent acts as a neutral judge for a "Rock-Paper-Scissors-Plus" match between a human User and a Python-controlled Bot.

The project demonstrates **Tool-Use (Function Calling)**, **Stateless Architecture**, and **Deterministic Game State Management**.

## 🚀 Features

* **Google ADK / GenAI Integration:** Uses the official `google-genai` library with `gemini-1.5-flash`.
* **"Plus" Game Variant:** Includes standard rules plus a strategic **"Bomb"** move (single-use, beats everything).
* **Deterministic Logic:** The LLM understands natural language (e.g., "I throw a rock"), but the game rules and scoring are strictly enforced by Python logic to prevent hallucinations.
* **Stateless Architecture:** Implements a "Context Injection" pattern to maintain perfect memory of the game state while keeping token usage minimum.
* **Rate Limit Resilience:** Includes "Traffic Control" mechanisms to ensure smooth gameplay on the Google Gemini Free Tier.

## 🛠️ Architecture

The solution follows a **Tool-Augmented Agent** pattern:

1.  **The Referee (AI Agent):**
    * **Role:** Neutral Judge.
    * **Responsibility:** Parses user intent, calls tools, and announces results.
    * **Model:** `gemini-1.5-flash` (Optimized for speed/cost).
2.  **The Engine (`GameEngine` Class):**
    * **Role:** Source of Truth.
    * **Responsibility:** Manages `user_score`, `bot_score`, `bomb_used` flags, and calculates the winner.
    * **Design:** Pure Python class (`game_logic.py`).
3.  **The Tools:**
    * `validate(move)`: Checks if the move is legal.
    * `resolve(move)`: Calculates the winner (User vs. Bot).
    * `update(winner)`: Updates the official score.

## 📦 Installation

1.  **Clone the repository** (or unzip the folder).
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration (API Key Setup)

You need a Google API Key to run the AI Referee.

1.  **Get your Key:**
    * Go to [Google AI Studio](https://aistudio.google.com/).
    * Click "Get API key" -> "Create API key in new project".
    * Copy the key string (it starts with `AIza...`).

2.  **Create the Environment File:**
    * In the root folder of this project (where `main.py` is), create a new file named `.env`.
    * **Note:** The file name is just `.env` (no name before the dot).

3.  **Add the Key:**
    * Open the `.env` file in Notepad or VS Code.
    * Paste your key strictly in this format:
    ```text
    GOOGLE_API_KEY=AIzaSyPasteYourActualKeyHereCharacters
    ```
    * Save the file.

## 🎮 How to Run

Execute the main script:
```bash
python main.py