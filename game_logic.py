import random

class GameEngine:
    def __init__(self):
        self.user_score = 0
        self.bot_score = 0
        self.rounds_played = 0
        self.max_rounds = 3
        self.user_bomb_used = False
        self.bot_bomb_used = False
        self.game_over = False

    def validate(self, move: str) -> dict:
        """Checks if move is valid and bomb rules are respected."""
        move = move.lower().strip()
        if move not in ["rock", "paper", "scissors", "bomb"]:
            return {"valid": False, "reason": "Invalid move. Use Rock, Paper, Scissors, or Bomb."}
        if move == "bomb" and self.user_bomb_used:
            return {"valid": False, "reason": "Bomb already used once."}
        return {"valid": True, "reason": "Valid"}

    def resolve(self, user_move: str) -> dict:
        """Calculates round winner."""
        user_move = user_move.lower().strip()
        bot_choices = ["rock", "paper", "scissors"]
        if not self.bot_bomb_used: bot_choices.append("bomb")
        
        bot_move = random.choice(bot_choices)
        if bot_move == "bomb": self.bot_bomb_used = True
        
        if user_move == bot_move: winner = "draw"
        elif user_move == "bomb": winner = "user"
        elif bot_move == "bomb": winner = "bot"
        elif (user_move == "rock" and bot_move == "scissors") or \
             (user_move == "paper" and bot_move == "rock") or \
             (user_move == "scissors" and bot_move == "paper"):
            winner = "user"
        else: winner = "bot"

        return {"user_move": user_move, "bot_move": bot_move, "winner": winner}

    def update(self, winner: str, user_move: str) -> dict:
        """Updates score state."""
        if self.game_over: return {"game_over": True}
        
        self.rounds_played += 1
        if user_move == "bomb": self.user_bomb_used = True
        
        if winner == "user": self.user_score += 1
        elif winner == "bot": self.bot_score += 1
        
        if self.rounds_played >= self.max_rounds: self.game_over = True
        
        return {
            "round": self.rounds_played,
            "scores": f"User: {self.user_score} - Bot: {self.bot_score}",
            "game_over": self.game_over
        }

game = GameEngine()