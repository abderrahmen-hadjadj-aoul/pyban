<template>
  <div class="board" v-if="board">
    <h2>
      {{ board.name }}
    </h2>
    <div class="columns">
      <div class="column" v-for="column in board.columns_list" :key="column.id">
        <h3>
          <vs-input
            v-model="column.title"
            placeholder="New ticket title"
            @change="updateColumn(column)"
          />
          <vs-button
            icon
            danger
            size="mini"
            id="delete-column"
            @click="deleteColumn(column)"
          >
            <i class="bx bx-trash"></i>
          </vs-button>
        </h3>
        <div class="line">
          <vs-input
            v-model="column._new_ticket_title"
            :id="'title-input-' + column.id"
            :ref="'title-input-' + column.id"
            placeholder="New ticket title"
            @keypress.enter="addTicket(column)"
          />
          <vs-button
            icon
            id="create-ticket"
            :ref="'add-' + column.id"
            @click="addTicket(column)"
            :disabled="!column._new_ticket_title.trim()"
          >
            <i class="bx bx-plus"></i>
          </vs-button>
        </div>
        <draggable
          class="list-group"
          tag="ul"
          v-model="column.tickets_list"
          v-bind="dragOptions"
          @change="onTicketChange($event, column)"
          @start="drag = true"
          @end="drag = false"
          handle=".handle"
        >
          <transition-group
            type="transition"
            :name="!drag ? 'flip-list' : null"
          >
            <li
              class="list-group-item"
              v-for="(ticket, index) in column.tickets_list"
              :key="ticket.id"
              :data-index="index"
              @dblclick="openTicketDetailDialog(ticket)"
            >
              <div class="handle">
                <i class="bx bx-menu"></i>
              </div>
              <input
                type="text"
                v-model="ticket.title"
                @change="changeTicketTitle(ticket)"
              />
            </li>
          </transition-group>
        </draggable>
      </div>

      <div class="add-column-container">
        <vs-button icon @click="addColumn">
          <i class="bx bx-plus"></i>
          Add column
        </vs-button>
      </div>
    </div>

    <vs-dialog width="300px" not-center v-model="ticketDetailDialogOpened">
      <template #header>
        <h4 class="not-margin">Update ticket</h4>
      </template>

      <div class="con-content" v-if="ticket">
        <vs-input
          data-name="dialog-title"
          v-model="ticket.title"
          @change="changeTicketTitle(ticket)"
          placeholder="Name"
        ></vs-input>
        <div class="description-container">
          <textarea
            data-name="dialog-description"
            rows="7"
            class="description"
            v-model="ticket.description"
            @change="changeTicket(ticket)"
            placeholder="Description"
          ></textarea>
        </div>
      </div>
      <template #footer>
        <div class="con-footer">
          <vs-button id="delete-button" danger @click="deleteTicket(ticket)">
            Delete
          </vs-button>
        </div>
      </template>
    </vs-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import BoardModel from "@/lib/Board";
import TicketModel from "@/lib/Ticket";
import ColumnModel from "@/lib/Column";
import draggable from "vuedraggable";

interface DragOption {
  animation: number;
  group: string;
  disabled: boolean;
  ghostClass: string;
}

@Component({
  components: { draggable },
})
export default class Board extends Vue {
  @Prop({ default: null })
  board!: BoardModel;
  ticketDetailDialogOpened = false;
  ticket: TicketModel | null = null;
  drag = false;

  mounted(): void {
    this.$store.dispatch("loadBoard", this.board);
  }

  async addTicket(column: ColumnModel): Promise<void> {
    console.log("addTicket");
    const title = column._new_ticket_title;
    console.log("title", title);
    const ticket = {
      title: title,
      description: "",
      column: column.id,
    };
    const payload = {
      column,
      ticket,
    };
    column._new_ticket_title = "";
    const loading = this.$vs.loading({
      target: this.$refs["add-" + column.id][0],
      scale: "0.6",
      background: "primary",
      opacity: 1,
      color: "#fff",
    });
    await this.$store.dispatch("createTicket", payload);
    loading.close();
  }

  async changeTicketTitle(ticket: TicketModel): Promise<void> {
    console.log("changeTicket", ticket);
    const payload = {
      id: ticket.id,
      patch: {
        title: ticket.title,
      },
    };
    this.$store.dispatch("updateTicket", payload);
  }

  async changeTicket(ticket: TicketModel): Promise<void> {
    console.log("changeTicket", ticket);
    const payload = {
      id: ticket.id,
      patch: {
        title: ticket.title,
        description: ticket.description,
      },
    };
    this.$store.dispatch("updateTicket", payload);
  }

  async updateColumn(column: ColumnModel): Promise<void> {
    console.log("updateColumn", column);
    this.$store.dispatch("updateColumn", column);
  }

  openTicketDetailDialog(ticket: TicketModel): void {
    console.log("open ticket", ticket);
    this.ticket = ticket;
    this.ticketDetailDialogOpened = true;
  }

  closeTicketDetailDialog(): void {
    this.ticket = null;
    this.ticketDetailDialogOpened = false;
  }

  async deleteTicket(ticket: TicketModel): Promise<void> {
    this.$store.dispatch("deleteTicket", ticket);
    this.closeTicketDetailDialog();
  }

  async addColumn(): Promise<void> {
    console.log("addColumn");
    const payload = {
      board: this.board,
      column: {
        title: "New Column",
      },
    };
    this.$store.dispatch("addColumn", payload);
  }

  async deleteColumn(column: ColumnModel): Promise<void> {
    this.$store.dispatch("deleteColumn", column);
  }

  onTicketChange(e, column): void {
    console.log("change", column, e);
    if (e.added) {
      const ticket = e.added.element;
      ticket.column = column.id;
      const payload = {
        id: ticket.id,
        patch: {
          column: ticket.column,
        },
      };
      this.$store.dispatch("updateTicket", payload);
    }
  }

  get dragOptions(): DragOption {
    return {
      animation: 200,
      group: "tickets",
      disabled: false,
      ghostClass: "ghost",
    };
  }
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

.line {
  display: flex;
}

ul,
li {
  margin: 0;
  padding: 0;
  list-style-type: none;
}

li {
  display: flex;
  padding: 5px;
  padding-left: 10px;
  border-radius: 25px;
  margin-top: 10px;
  background-color: hsl(0, 0%, 97%);
  color: hsl(0, 0%, 50%);
  transition: 0.3s;
  font-size: 14px;
}

li input {
  margin-left: 5px;
  flex: 1;
  border: none;
  background: none;
}

li:hover {
  background-color: #e6ecff;
}

.description-container {
  width: 100%;
  display: flex;
}

textarea {
  flex: 1;
  margin-top: 20px;
  padding: 7px 13px;
  color: rgb(44, 62, 80);
  background-color: rgb(244, 247, 248);
  border: none;
  border-radius: 12px;
  outline: none;
}

.add-column-container {
  margin-top: 20px;
}

h3 {
  display: flex;
}

.handle {
  cursor: move;
}

.flip-list-move {
  transition: transform 0.5s;
}

.no-move {
  transition: transform 0s;
}

.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}

.list-group {
  min-height: 20px;
}

.list-group-item {
  cursor: move;
}
</style>

<style>
h3 input.vs-input {
  font-size: 25px;
}
</style>
