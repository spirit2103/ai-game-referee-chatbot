# 🤖 AI Game Referee: Rock–Paper–Scissors–Plus

An AI-powered Game Referee built using the **Google GenAI SDK**.  
The agent acts as a neutral judge for a *Rock–Paper–Scissors–Plus* match between a human User and a Python-controlled Bot.

The project demonstrates **Tool Use (Function Calling)**, **Deterministic Game Logic**, and **Clean Agent Design**.

---

## 🚀 Features

- **Google GenAI Integration:** Uses the official `google-genai` SDK with the free-tier model `gemini-flash-latest`.
- **"Plus" Game Variant:** Includes standard rules plus a strategic **Bomb** move (single-use, beats all moves).
- **Deterministic Logic:** All rules, validation, and scoring are enforced in Python to prevent LLM hallucinations.
- **Stateless LLM Calls:** Game state is managed deterministically in Python and injected into the prompt each round.
- **Graceful Rate-Limit Handling:** The game exits cleanly if free-tier API limits are reached.

---

## 🛠️ Architecture

The solution follows a **Tool-Augmented Agent** pattern:

### 1️⃣ AI Referee (LLM)
- **Role:** Neutral judge and narrator.
- **Responsibility:** Interprets user intent, invokes tools, and explains outcomes.
- **Model:** `models/gemini-flash-latest` (free-tier, low-latency).

### 2️⃣ Game Engine (`GameState`)
- **Role:** Source of truth.
- **Responsibility:** Maintains rounds, scores, bomb usage, and resolves winners.
- **Design:** Pure Python (`game_state.py`).

### 3️⃣ Tools (Python Functions)
- `validate_move(move)` – Validates user input.
- `resolve_round(move)` – Determines the winner.
- `update_game_state(winner, move)` – Updates game state.

The LLM **cannot modify game state directly**, ensuring deterministic behavior.

---

## 📦 Installation

1. Clone or extract the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
