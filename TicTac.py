import copy

# Constantes para las puntuaciones
WIN_SCORE = 10
FUTURE_WIN_SCORE = 5
NEUTRAL_SCORE = 0
FUTURE_LOSE_SCORE = -5
LOSE_SCORE = -10

# Representación del tablero 3x3 como una lista de listas
EMPTY = 0
X = 1
O = 2

# Función para verificar si un jugador ha ganado
def check_win(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Función para evaluar una jugada en el árbol
def evaluate_move(board, player):
    if check_win(board, player):
        return WIN_SCORE
    elif check_win(board, 3 - player):
        return LOSE_SCORE
    else:
        future_moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    future_board = copy.deepcopy(board)
                    future_board[i][j] = player
                    future_score = evaluate_move(future_board, 3 - player)
                    future_moves.append(future_score)

        best_future_score = max(
            future_moves) if future_moves else NEUTRAL_SCORE

        if player == X and best_future_score == WIN_SCORE:
            return FUTURE_WIN_SCORE
        elif player == O and best_future_score == -LOSE_SCORE:
            return FUTURE_WIN_SCORE
        elif best_future_score == NEUTRAL_SCORE:
            return NEUTRAL_SCORE
        elif check_win(board, player):
            return WIN_SCORE
        elif check_win(board, 3 - player):
            return LOSE_SCORE
        else:
            return 0

# Función para generar el árbol de búsqueda
def generate_tree(board, player):
    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                future_board = copy.deepcopy(board)
                future_board[i][j] = player
                possible_moves.append(
                    (i, j, evaluate_move(future_board, 3 - player)))

    return possible_moves

# Función para imprimir el tablero con "X" y "O"
def print_board(board):
    for row in board:
        print(" | ".join(
            ["X" if cell == X else "O" if cell == O else " " for cell in row]))
        print("-" * 9)

def evaluate_and_print(board, player, winner_score):
    possible_moves = generate_tree(board, player)
    for move in possible_moves:
        i, j, score = move
        print(f"\nEvaluación para colocar {player} en ({i}, {j}):")

        future_board = copy.deepcopy(board)
        future_board[i][j] = player
        print_board(future_board)

        # Evaluar si el jugador gana en una jugada futura
        if check_win(future_board, player) and player == 1:
            winner_score = FUTURE_WIN_SCORE
            print(
                f"Puntuación: {winner_score} puntos: Ganaste en esta futura jugada\n")
            print(
                "----------------------------------------------------------------------")
        elif check_win(future_board, player) and player == 2:
            winner_score = FUTURE_LOSE_SCORE
            print(f"Puntuación: {winner_score} puntos: Perdiste en una futura jugada\n")
            print(
             "----------------------------------------------------------------------")
        else: 
            evaluate_and_print(future_board, 3 - player, winner_score)
            
            if move == possible_moves[-1] and winner_score == NEUTRAL_SCORE:
                print(f"Puntuación: {winner_score} puntos: Empate\n")
                print(
                    "----------------------------------------------------------------------")
                   

# Función principal para mostrar las evaluaciones
def show_evaluations():
    initial_board = [[O, EMPTY, O],
                     [O, EMPTY, X],
                     [X, EMPTY, X]]

    print("Tablero inicial:")
    print_board(initial_board)

    player = X

    # Evaluar si el jugador gana
    if check_win(initial_board, player):
        winner_score = WIN_SCORE
        print(f"Puntuación: {winner_score} puntos: Ganaste\n")
        return
    elif check_win(initial_board, 3 - player):
        winner_score = LOSE_SCORE
        print(f"Puntuación: {winner_score} puntos: Perdiste\n")
        return
    else:
        winner_score = NEUTRAL_SCORE
        print("-----------------------------------Posibles Movimientos-----------------------------------")
        evaluate_and_print(initial_board, player, winner_score)


if __name__ == "__main__":
    show_evaluations()
