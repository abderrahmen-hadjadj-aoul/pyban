<template>
  <div class="board" v-if="board">
    <h2>
      {{ board.name }}
    </h2>
    <div class="columns">
      <div class="column" v-for="column in board.columns_list" :key="column.id">
        <h3>{{ column.title }}</h3>
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
        <ul>
          <li
            v-for="(ticket, index) in column.tickets_list"
            :key="ticket.id"
            :data-index="index"
            @dblclick="openTicketDetailDialog(ticket)"
          >
            <div class="handle"></div>
            <input
              type="text"
              v-model="ticket.title"
              @change="changeTicketTitle(ticket)"
            />
          </li>
        </ul>
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
import ColumnModel from "@/lib/ColumnTicket";

@Component({
  components: {},
})
export default class Board extends Vue {
  @Prop({ default: null })
  board!: BoardModel;
  ticketDetailDialogOpened = false;
  ticket: TicketModel | null = null;

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
  padding: 5px;
  padding-left: 15px;
  border-radius: 25px;
  margin-top: 10px;
  background-color: hsl(0, 0%, 97%);
  color: hsl(0, 0%, 50%);
  transition: 0.3s;
  font-size: 14px;
}

li {
  display: flex;
}

li input {
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
</style>
