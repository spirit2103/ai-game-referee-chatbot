import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from game_logic import game

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env")
    exit(1)

client = genai.Client(api_key=api_key)

# Define tools
tools_list = [game.validate, game.resolve, game.update]

def run_game():
    print("\n--- AI Referee Initialized ---")
    print("(Type 'quit' to exit)\n")

    print("Referee: Welcome! I will judge the match between You and the Bot.")
    print("Referee: Best of 3. Rock, Paper, Scissors, or Bomb (once).")

    while not game.game_over:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']: break
        
        # --- TRAFFIC CONTROL ---
        # Pauses to keep you safe from rate limits
        print("Referee is judging...", end="\r") 
        time.sleep(4) 
        
        # 2. Inject Context (Stateless Mode)
        current_state = f"""
        MATCH STATUS:
        - Current Round: {game.rounds_played + 1} of 3
        - Score: User {game.user_score} - Bot {game.bot_score}
        - Bomb Used: User={game.user_bomb_used}, Bot={game.bot_bomb_used}
        """

        # 3. Strict Referee Persona
        sys_instruct = f"""
        You are the NEUTRAL REFEREE for a game of Rock-Paper-Scissors-Plus.
        There are two players: the USER (human) and the BOT (computer).
        
        {current_state}
        
        YOUR JOB:
        1. Receive the User's move.
        2. CALL `validate` first. 
        3. CALL `resolve` to find out what the BOT played and who won.
        4. CALL `update` to record the score.
        5. ANNOUNCE the result. 
           - Say "The Bot played [move]". Do NOT say "I played".
           - Announce the winner clearly.
        """

        # 4. Create fresh chat
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct,
                tools=tools_list,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                )
            )
        )
        
        try:
            # 5. Send Message
            response = chat.send_message(user_input)
            
            # Clear the loading text
            print(" " * 30, end="\r") 
            print(f"Referee: {response.text}")

        except Exception as e:
            # Silent Error Handling
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("Referee: (Connection glitch... re-judging...)")
                time.sleep(10)
                try:
                    response = chat.send_message(user_input)
                    print(f"Referee: {response.text}")
                except:
                    print("Referee: System busy. Please state your move again.")
            else:
                print(f"Error: {e}")

    # Final Score
    print("\n--- FINAL RESULTS ---")
    print(f"User: {game.user_score} - Bot: {game.bot_score}")
    if game.user_score > game.bot_score: print("Winner: USER")
    elif game.bot_score > game.user_score: print("Winner: BOT")
    else: print("Result: DRAW")

if __name__ == "__main__":
    run_game()