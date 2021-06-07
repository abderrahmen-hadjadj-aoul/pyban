<template>
  <div class="board" v-if="board">
    <h2>
      {{ board.name }}
    </h2>
    <div class="columns">
      <div
        class="column"
        v-for="(column, column_index) in board.columns_list"
        :key="column.id"
        :data-column-index="column_index"
      >
        <h3>
          <vs-input
            class="column-title"
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
            class="ticket-title"
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

    <Ticket :ticket="ticket" v-if="ticketDetailDialogOpened" @close="onClose" />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import BoardModel from "@/lib/Board";
import TicketModel from "@/lib/Ticket";
import ColumnModel from "@/lib/Column";
import Ticket from "@/components/Ticket.vue";
import draggable from "vuedraggable";

interface DragOption {
  animation: number;
  group: string;
  disabled: boolean;
  ghostClass: string;
}

interface DragEvent {
  added: {
    element: TicketModel;
  };
}

@Component({
  components: { Ticket, draggable },
})
export default class Board extends Vue {
  @Prop({ default: null })
  board!: BoardModel;
  ticketDetailDialogOpened = false;
  ticket: TicketModel | null = null;
  drag = false;

  async mounted(): Promise<void> {
    await this.$store.dispatch("loadBoard", this.board);
    const ticket_id = this.$route.params.ticket_id;
    const tickets = this.board.getTickets();
    if (ticket_id) {
      console.log("has ticket_id", ticket_id);
      const ticket = tickets.find((t) => "" + t.id === ticket_id);
      console.log(tickets);
      console.log("found ticket", ticket);
      if (ticket) {
        this.openTicketDetailDialog(ticket);
      }
    }
  }

  async addTicket(column: ColumnModel): Promise<void> {
    const title = column._new_ticket_title;
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
    const refs = this.$refs["add-" + column.id] as Element[];
    const loading = this.$vs.loading({
      target: refs[0],
      scale: "0.6",
      background: "primary",
      opacity: 1,
      color: "#fff",
    });
    await this.$store.dispatch("createTicket", payload);
    loading.close();
  }

  async changeTicketTitle(ticket: TicketModel): Promise<void> {
    const payload = {
      id: ticket.id,
      patch: {
        title: ticket.title,
      },
    };
    this.$store.dispatch("updateTicket", payload);
  }

  async changeTicket(ticket: TicketModel): Promise<void> {
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
    this.$store.dispatch("updateColumn", column);
  }

  openTicketDetailDialog(ticket: TicketModel): void {
    this.ticket = ticket;
    this.ticketDetailDialogOpened = true;
    this.$router.push(`/boards/${this.board.id}/tickets/${ticket.id}`);
  }

  async addColumn(): Promise<void> {
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

  onTicketChange(e: DragEvent, column: ColumnModel): void {
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

  onClose(): void {
    this.ticketDetailDialogOpened = false;
    this.$router.push(`/boards/${this.board.id}`);
  }
}
</script>

<style lang="scss" scoped>
.columns {
  display: flex;
}

.column {
  width: 250px;
  min-width: 250px;
  margin: 20px;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 5px 3px 10px hsl(0, 0%, 90%);
  transition: 0.3s;
}

.column:hover {
  box-shadow: 2px 2px 10px #9acfeb;
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
