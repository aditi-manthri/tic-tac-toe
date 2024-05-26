from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

board = [['', '', ''], ['', '', ''], ['', '', '']]
current_player = 'X'

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def check_draw(board):
    return all(cell != '' for row in board for cell in row)

def computer_move(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                return i, j
    return None, None

@app.route('/api/new_game', methods=['POST'])
def new_game():
    global board, current_player
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    current_player = 'X'
    return jsonify(status='New Game Started')

@app.route('/api/move', methods=['POST'])
def move():
    global board, current_player
    data = request.json
    row, col, player = data['row'], data['col'], data['player']
    if board[row][col] == '':
        board[row][col] = player
        winner = check_winner(board)
        if winner:
            return jsonify(status=f'{winner} Wins')
        if check_draw(board):
            return jsonify(status='Draw')
        current_player = 'O' if player == 'X' else 'X'
        return jsonify(status='CONTINUE')
    return jsonify(status='Invalid Move')

@app.route('/api/computer_move', methods=['POST'])
def computer_move_endpoint():
    global board, current_player
    data = request.json
    row, col = data['row'], data['col']
    player = 'X'
    if board[row][col] == '':
        board[row][col] = player
        winner = check_winner(board)
        if winner:
            return jsonify(status=f'{winner} Wins')
        if check_draw(board):
            return jsonify(status='Draw')
        computer_row, computer_col = computer_move(board)
        if computer_row is not None:
            board[computer_row][computer_col] = 'O'
            winner = check_winner(board)
            if winner:
                return jsonify(status=f'{winner} Wins')
            if check_draw(board):
                return jsonify(status='Draw')
        current_player = 'X'
        return jsonify(status='CONTINUE', board=board)
    return jsonify(status='Invalid Move')

if __name__ == '__main__':
    app.run(debug=True)
