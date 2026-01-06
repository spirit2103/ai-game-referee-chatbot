import random

class GameState:
    def __init__(self):
        self.round = 0
        self.max_rounds = 3
        self.user_score = 0
        self.bot_score = 0
        self.user_bomb_used = False
        self.bot_bomb_used = False

    def validate_move(self, move: str):
        move = move.lower().strip()
        if move not in ["rock", "paper", "scissors", "bomb"]:
            return False, "Invalid input"
        if move == "bomb" and self.user_bomb_used:
            return False, "Bomb already used"
        return True, move

    def resolve_round(self, user_move: str):
        choices = ["rock", "paper", "scissors"]
        if not self.bot_bomb_used:
            choices.append("bomb")

        bot_move = random.choice(choices)
        if bot_move == "bomb":
            self.bot_bomb_used = True

        if user_move == bot_move:
            winner = "draw"
        elif user_move == "bomb":
            winner = "user"
        elif bot_move == "bomb":
            winner = "bot"
        elif (
            (user_move == "rock" and bot_move == "scissors") or
            (user_move == "paper" and bot_move == "rock") or
            (user_move == "scissors" and bot_move == "paper")
        ):
            winner = "user"
        else:
            winner = "bot"

        return bot_move, winner

    def update_state(self, winner: str, user_move: str):
        self.round += 1

        if user_move == "bomb":
            self.user_bomb_used = True

        if winner == "user":
            self.user_score += 1
        elif winner == "bot":
            self.bot_score += 1

        return {
            "round": self.round,
            "user_score": self.user_score,
            "bot_score": self.bot_score,
            "game_over": self.round >= self.max_rounds
        }

game_state = GameState()
