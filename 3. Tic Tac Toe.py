import random

# ----------------------------
# Helper / Display functions
# ----------------------------
def display_board(board):
    """Print the board as three rows (positions 1..9 shown as X/O or blank)."""
    row1 = board[0:3]
    row2 = board[3:6]
    row3 = board[6:9]
    print()
    print(row_to_str(row1))
    print(row_to_str(row2))
    print(row_to_str(row3))
    print()

def row_to_str(row):
    return f"[ {row[0]} ] [ {row[1]} ] [ {row[2]} ]"

def available_moves(board):
    return [i for i, v in enumerate(board) if v == " "]

# ----------------------------
# Win / Draw checks
# ----------------------------
WIN_COMBOS = [
    (0,1,2), (3,4,5), (6,7,8),    # rows
    (0,3,6), (1,4,7), (2,5,8),    # cols
    (0,4,8), (2,4,6)              # diagonals
]

def check_winner(board, player):
    for a,b,c in WIN_COMBOS:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def is_draw(board):
    return " " not in board

def game_result(board):
    """Return 'X' or 'O' if winner, 'Draw' if draw, else None."""
    for p in ["X","O"]:
        if check_winner(board, p):
            return p
    if is_draw(board):
        return "Draw"
    return None

# ----------------------------
# Minimax (perfect AI)
# ----------------------------
def minimax(board, maximizing, ai_player, human_player):
    """
    Return tuple (score, move_index).
    Scores: +1 -> ai win, -1 -> human win, 0 -> draw
    """
    result = game_result(board)
    if result == ai_player:
        return 1, None
    if result == human_player:
        return -1, None
    if result == "Draw":
        return 0, None

    if maximizing:
        best_score = -2
        best_move = None
        for move in available_moves(board):
            board[move] = ai_player
            score, _ = minimax(board, False, ai_player, human_player)
            board[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
                # if we found winning score, break early
                if best_score == 1:
                    break
        return best_score, best_move
    else:
        best_score = 2
        best_move = None
        for move in available_moves(board):
            board[move] = human_player
            score, _ = minimax(board, True, ai_player, human_player)
            board[move] = " "
            if score < best_score:
                best_score = score
                best_move = move
                if best_score == -1:
                    break
        return best_score, best_move

# ----------------------------
# Bot move chooser
# ----------------------------
def get_bot_move(board, bot_mode, ai_player, human_player):
    moves = available_moves(board)
    if not moves:
        return None
    if bot_mode == "random":
        return random.choice(moves)
    elif bot_mode == "ai":
        _, move = minimax(board, True, ai_player, human_player)
        # fallback in rare case
        return move if move is not None else random.choice(moves)
    else:
        raise ValueError("Unknown bot mode")

# ----------------------------
# Input helpers
# ----------------------------
def ask_player_choice():
    while True:
        choice = input("Choose X or O (X plays first): ").strip().upper()
        if choice in ("X","O"):
            return choice
        print("Invalid. Enter X or O.")

def ask_game_mode():
    print("\nChoose mode:")
    print("1 - Player vs Player")
    print("2 - Player vs Bot (random moves)")
    print("3 - Player vs Bot (perfect AI)")
    while True:
        sel = input("Enter 1, 2, or 3: ").strip()
        if sel in ("1","2","3"):
            return {"1":"pvp","2":"random","3":"ai"}[sel]
        print("Invalid selection.")

def ask_move(board, player):
    while True:
        pos = input(f"Player {player}, enter position (1-9): ").strip()
        if not pos.isdigit():
            print("Please enter a number 1-9.")
            continue
        pos = int(pos)
        if pos < 1 or pos > 9:
            print("Choose a number from 1 to 9.")
            continue
        idx = pos - 1
        if board[idx] != " ":
            print("Position occupied. Choose another.")
            continue
        return idx

# ----------------------------
# Main game loop
# ----------------------------
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    mode = ask_game_mode()
    board = [" "] * 9
    player_choice = ask_player_choice()
    human_player = player_choice
    ai_player = "O" if human_player == "X" else "X"

    # Determine turn order: X always moves first
    current_player = "X"

    # For PvP, both are human; for bot modes, one is human, one bot
    if mode == "pvp":
        print("\nStarting Player vs Player")
    else:
        print(f"\nStarting Player vs Bot ({mode})")
        print(f"You are {human_player}, Bot is {ai_player}")

    display_board(board)

    while True:
        result = game_result(board)
        if result == "Draw":
            print("It's a draw!")
            break
        elif result in ("X","O"):
            print(f"Player {result} wins!")
            break

        if mode == "pvp":
            # human move for whichever player
            idx = ask_move(board, current_player)
            board[idx] = current_player
        else:
            # Player vs Bot
            if current_player == human_player:
                idx = ask_move(board, human_player)
                board[idx] = human_player
            else:
                print("Bot is thinking...")
                bot_idx = get_bot_move(board, mode, ai_player, human_player)
                print(f"Bot chooses position {bot_idx + 1}")
                board[bot_idx] = ai_player

        display_board(board)
        # switch player
        current_player = "O" if current_player == "X" else "X"

    # After match, ask replay
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again == "y":
            return True
        elif again == "n":
            return False
        else:
            print("Enter y or n.")

# ----------------------------
# Runner
# ----------------------------
if __name__ == "__main__":
    while True:
        replay = play_game()
        if not replay:
            print("Thanks for playing!")
            break
