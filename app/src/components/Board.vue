<template>
  <div class="board">
    <h2>
      {{ board.name }}
    </h2>
    <div class="columns">
      <div class="column">
        <h3>Todo</h3>
        <ul>
          <li>Item</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import BoardModel from "@/lib/Board";

@Component({
  components: {},
})
export default class Board extends Vue {
  @Prop({ default: null })
  board: BoardModel | null = null;
}
</script>

<style lang="scss" scoped>
.columns {
  display: flex;
}

.column {
  width: 250px;
  margin: 20px;
  padding: 10px;
  border: 1px solid hsl(0, 0%, 85%);
  border-radius: 10px;
}

h3 {
  text-align: center;
}
</style>
