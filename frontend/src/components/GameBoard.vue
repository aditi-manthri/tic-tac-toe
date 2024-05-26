<template>
  <div class="game-board">
    <div v-for="(row, rowIndex) in board" :key="rowIndex" class="row">
      <div
        v-for="(cell, colIndex) in row"
        :key="colIndex"
        class="cell"
        @click="handleClick(rowIndex, colIndex)"
      >
        {{ cell }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['board'],
  methods: {
    handleClick(row, col) {
      this.$emit('move', { row, col });
    }
  }
}
</script>

<style scoped>
.game-board {
  display: grid;
  grid-template-rows: repeat(3, 100px);
  grid-gap: 5px;
}

.row {
  display: grid;
  grid-template-columns: repeat(3, 100px);
}

.cell {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ecf0f1;
  color: #2ecc71;
  font-size: 2em;
  border: 2px solid #2ecc71;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cell:hover {
  background-color: #bdc3c7;
}
</style>
