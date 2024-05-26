<template>
  <div id="app">
    <h1>Tic Tac Toe</h1>
    <GameBoard :board="board" @move="makeMove" />
    <div v-if="status" class="status">{{ status }}</div>
    <div class="button-group">
      <button @click="newGame" class="new-game-button">Play Against Human</button>
      <button @click="newGameAgainstComputer" class="new-game-button">Play Against Computer</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import GameBoard from './components/GameBoard.vue';

axios.defaults.baseURL = 'http://localhost:5000';

export default {
  components: {
    GameBoard
  },
  data() {
    return {
      board: [['', '', ''], ['', '', ''], ['', '', '']],
      status: '',
      currentPlayer: 'X',
      againstComputer: false
    }
  },
  methods: {
    async newGame() {
      await axios.post('/api/new_game');
      this.board = [['', '', ''], ['', '', ''], ['', '', '']];
      this.status = '';
      this.currentPlayer = 'X';
      this.againstComputer = false;
    },
    async newGameAgainstComputer() {
      await axios.post('/api/new_game');
      this.board = [['', '', ''], ['', '', ''], ['', '', '']];
      this.status = '';
      this.currentPlayer = 'X';
      this.againstComputer = true;
    },
    async makeMove({ row, col }) {
      if (this.board[row][col] !== '') {
        this.status = 'INVALID MOVE';
        return;
      }
      const player = this.currentPlayer;
      if (this.againstComputer) {
        const response = await axios.post('/api/computer_move', { row, col });
        this.board = response.data.board;
        this.status = response.data.status;
      } else {
        const response = await axios.post('/api/move', { row, col, player });
        if (response.data.status !== 'INVALID MOVE') {
          this.board[row][col] = player;
          if (response.data.status === 'CONTINUE') {
            this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
            this.status = '';
          } else {
            this.status = response.data.status;
          }
        } else {
          this.status = response.data.status;
        }
      }
    }
  },
  mounted() {
    this.newGame();
  }
}
</script>

<style scoped>
#app {
  display: flex;
  overflow: hidden;
  flex-direction: column;
  align-items: center;
  font-family: 'Arial', sans-serif;
  background: #f5f5f5;
  min-height: 97vh;
  justify-content: center;
}

h1 {
  color: #2ecc71;
  font-size: 3em;
  margin-bottom: 20px;
}

.status {
  margin-top: 20px;
  font-size: 1.5em;
  color: #27ae60;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.new-game-button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 1.2em;
  color: white;
  background-color: #2ecc71;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.new-game-button:hover {
  background-color: #27ae60;
}
</style>
