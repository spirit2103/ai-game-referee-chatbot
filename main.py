import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from game_state import game_state

# -------------------- Setup --------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -------------------- Tool functions --------------------
def validate_move(move: str) -> dict:
    valid, result = game_state.validate_move(move)
    return {"valid": valid, "result": result}

def resolve_round(user_move: str) -> dict:
    bot_move, winner = game_state.resolve_round(user_move)
    return {"bot_move": bot_move, "winner": winner}

def update_game_state(winner: str, user_move: str) -> dict:
    return game_state.update_state(winner, user_move)

tools = [validate_move, resolve_round, update_game_state]

# -------------------- Game Loop --------------------
def run_game():

    # Rules first (clean & short)
    print("\n AI Game Referee — Rock–Paper–Scissors–Bomb\n")
    print("Rules:")
    print("1. Best of 3 rounds.")
    print("2. Moves: rock, paper, scissors, bomb.")
    print("3. Bomb can be used only once.")
    print("4. Bomb beats all moves.")
    print("5. Invalid input wastes the round.\n")

    while game_state.round < game_state.max_rounds:
        user_input = input("You: ")

        system_prompt = f"""
You are a neutral referee for Rock–Paper–Scissors–Bomb.

Current state:
- Round: {game_state.round + 1} / 3
- Score: User {game_state.user_score}, Bot {game_state.bot_score}
- User bomb used: {game_state.user_bomb_used}
- Bot bomb used: {game_state.bot_bomb_used}

Steps:
1. Validate move
2. Resolve round
3. Update state
4. Clearly announce result
"""

        try:
            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False
                    )
                )
            )

            print("\nReferee:", response.text)

        except ClientError as e:
            if e.code == 429:
                print(
                    "\nReferee: The game cannot continue due to rate limits. "
                    "Please try again later.\n"
                )
                break
            else:
                raise

    # Final result
    print("\n--- FINAL RESULT ---")
    print(f"User: {game_state.user_score} | Bot: {game_state.bot_score}")

    if game_state.user_score > game_state.bot_score:
        print("Winner: USER ")
    elif game_state.bot_score > game_state.user_score:
        print("Winner: BOT ")
    else:
        print("Result: DRAW")

if __name__ == "__main__":
    run_game()
