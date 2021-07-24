def validation(board, players):
		if board[1][1] == board[0][1] and board[1][1] == board[2][1] and board[1][1] != 0:
			return players['1'] if board[1][1] == players['1'] else players['2']
		elif board[1][1] == board[0][0] and board[1][1] == board[2][2] and board[1][1] != 0:
			return players['1'] if board[1][1] == players['1'] else players['2']
		elif board[1][1] == board[1][0] and board[1][1] == board[1][2] and board[1][1] != 0:
			return players['1'] if board[1][1] == players['1'] else players['2']
		elif board[1][1] == board[0][2] and board[1][1] == board[2][0] and board[1][1] != 0:
			return players['1'] if board[1][1] == players['1'] else players['2']
		elif board[0][1] == board[0][0] and board[0][1] == board[0][2] and board[0][1] != 0:
			return players['1'] if board[0][1] == players['1'] else players['2']
		elif board[2][1] == board[2][0] and board[2][1] == board[2][2] and board[2][1] != 0:
			return players['1'] if board[2][1] == players['1'] else players['2']
		elif board[1][0] == board[0][0] and board[1][0] == board[2][0] and board[1][0] != 0:
			return players['1'] if board[1][0] == players['1'] else players['2']
		elif board[1][2] == board[0][2] and board[1][2] == board[2][2] and board[1][2] != 0:
			return players['1'] if board[1][2] == players['1'] else players['2']
		
		for i in range(3):
			for j in range(3):
				if board[i][j] == 0:
					return 'None'
		return 'Draw'


def player_input(turn):
    position = str(input(f"Player {turn}'s Turn\nEnter the position where you want to keep your symbol:")) + str(turn)
    return position


def update_board(position, players, board):
    characters = [i for i in position]
    board[int(characters[0]) - 1][int(characters[1]) - 1] = players[characters[2]]
    return board


def initialize_board():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def initialize_players():
    return {'1': 'X', '2': 'O'}


def print_board(board):
    printable = f"""```
                    1   2   3
                ===============
                ||   |   |   ||
              1 || {board[0][0] if board[0][0] != 0 else ' '} | {board[0][1] if board[0][1] != 0 else ' '} | {board[0][2] if board[0][2] != 0 else ' '} ||
                ||   |   |   ||
                ===============
                ||   |   |   ||
              2 || {board[1][0] if board[1][0] != 0 else ' '} | {board[1][1] if board[1][1] != 0 else ' '} | {board[1][2] if board[1][2] != 0 else ' '} ||
                ||   |   |   ||
                ===============
                ||   |   |   ||
              3 || {board[2][0] if board[2][0] != 0 else ' '} | {board[2][1] if board[2][1] != 0 else ' '} | {board[2][2] if board[2][2] != 0 else ' '} ||
                ||   |   |   ||
                ===============
    ```"""
    return printable


def main():
    board = initialize_board()
    players = initialize_players()
    print_board(board)
    count = 1
    while validation(board, players) == 'None':
        turn = 1 if count % 2 != 0 else 2
        inp = player_input(turn)
        board = update_board(inp, players, board)
        print('\n' * 1000)
        print_board(board)
        count += 1
    print_board(board)
    print(f"{'Player 1' if validation(board, players) == 'X' else 'Player 2'} wins")
