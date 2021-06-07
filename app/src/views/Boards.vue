<template>
  <div class="board">
    <div class="buttons">
      <vs-button id="open-dialog" icon @click="openDialog" v-if="!board">
        <i class="bx bx-plus"></i> Create board
      </vs-button>
      <vs-button icon border danger @click="deleteBoard" v-if="board">
        <i class="bx bx-trash"></i> Delete this board
      </vs-button>
      <vs-button icon border @click="returnToBoardList" v-if="board">
        <i class="bx bx-left-arrow-alt"></i> Return to board list
      </vs-button>
    </div>
    <vs-dialog ref="dialog" width="300px" not-center v-model="dialogOpened">
      <template #header>
        <h4 class="not-margin">What is the board <b>Name</b></h4>
      </template>

      <div class="con-content">
        <vs-input
          ref="boardNameInput"
          id="board-name"
          v-model="boardName"
          placeholder="Name"
          @keypress.enter="createBoard"
        ></vs-input>
      </div>

      <template #footer>
        <div class="con-footer">
          <vs-button
            ref="createBoard"
            color="primary"
            id="create-board"
            @click="createBoard"
          >
            Create board
          </vs-button>
          <vs-button id="cancel" @click="closeDialog" dark transparent>
            Cancel
          </vs-button>
        </div>
      </template>
    </vs-dialog>

    <main v-if="board">
      <Board :board="board" />
    </main>
    <main class="board-container" v-else>
      <article
        class="board-item"
        v-for="item in boards"
        @click="openBoard(item)"
        :key="item.id"
        :data-boardid="item.id"
      >
        <h1>
          {{ item.name }}
        </h1>
      </article>
    </main>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Board from "@/components/Board.vue";
import BoardModel from "@/lib/Board";

@Component({
  components: { Board },
})
export default class Boards extends Vue {
  dialogOpened = false;
  boardName = "";
  board: BoardModel | null = null;

  async mounted(): Promise<void> {
    await this.$store.dispatch("getBoards");
    const board_id = this.$route.params.board_id;
    if (board_id) {
      const board = this.$store.state.boards.find(
        (board: BoardModel) => "" + board.id === board_id
      );
      if (board) {
        this.board = board;
      }
    }
  }

  openDialog(): void {
    this.dialogOpened = true;
    this.$nextTick(() => {
      const els = this.$refs["boardNameInput"].$el;
      const input = els.getElementsByTagName("input")[0];
      console.log("input", input);
      setTimeout(() => {
        input.focus();
      }, 50);
    });
  }

  closeDialog(): void {
    this.dialogOpened = false;
  }

  async createBoard(): Promise<void> {
    const loading = this.$vs.loading({
      target: this.$refs.createBoard,
      scale: "0.6",
      background: "primary",
      opacity: 1,
      color: "#fff",
    });
    try {
      const board = await this.$store.dispatch("createBoard", {
        name: this.boardName,
      });
    } catch (e) {
      console.error("create board error", e);
    }
    this.dialogOpened = false;
    this.boardName = "";
    loading.close();
  }

  get boards(): BoardModel[] {
    return this.$store.state.boards;
  }

  openBoard(board: BoardModel): void {
    this.board = board;
    this.$router.push("/boards/" + board.id);
  }

  returnToBoardList(): void {
    this.board = null;
    this.$router.push("/boards");
  }

  deleteBoard(): void {
    this.$store.dispatch("deleteBoard", this.board);
    this.returnToBoardList();
  }
}
</script>

<style lang="scss" scoped>
>>> .con-content,
>>> .vs-input,
>>> .vs-input-content,
>>> .vs-input-parent {
  width: 100%;
}

.con-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.buttons {
  display: flex;
  margin-bottom: 10px;
}

main.board-container {
  display: flex;
  flex-wrap: wrap;
}

main article {
  border-radius: 15px;
  box-shadow: 5px 3px 10px hsl(0, 0%, 90%);
  cursor: pointer;
  transition: 0.3s;
  margin: 20px;
}

main article:hover {
  border-radius: 15px;
  box-shadow: 2px 2px 10px #9acfeb;
  color: #166fb8;
}

main article h1 {
  margin: 25px;
}
</style>
