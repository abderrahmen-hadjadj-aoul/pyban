<template>
  <div class="board" v-if="board">
    <h2>
      {{ board.name }}
    </h2>
    <div class="columns">
      <div class="column">
        <h3>Todo</h3>
        <div class="line">
          <vs-input
            v-model="title"
            placeholder="New ticket title"
            @keypress.enter="addTicket"
          />
          <vs-button
            icon
            ref="add"
            @click="addTicket"
            :disabled="!title.trim()"
          >
            <i class="bx bx-plus"></i>
          </vs-button>
        </div>
        <ul>
          <li v-for="ticket in board.tickets" :key="ticket.id">
            <div class="handle"></div>
            <input
              type="text"
              v-model="ticket.title"
              @change="changeTicketTitle(ticket)"
              @dblclick="openTicketDetailDialog(ticket)"
            />
          </li>
        </ul>
      </div>
    </div>

    <vs-dialog width="300px" not-center v-model="ticketDetailDialogOpened">
      <template #header>
        <h4 class="not-margin">Update ticket</h4>
      </template>

      <div class="con-content" v-if="ticket">
        <vs-input
          v-model="ticket.title"
          @change="changeTicketTitle(ticket)"
          placeholder="Name"
        ></vs-input>
        <div class="description-container">
          <textarea
            rows="7"
            class="description"
            v-model="ticket.description"
            @change="changeTicket(ticket)"
            placeholder="Description"
          ></textarea>
        </div>
      </div>
    </vs-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import BoardModel from "@/lib/Board";
import TicketModel from "@/lib/Ticket";

@Component({
  components: {},
})
export default class Board extends Vue {
  @Prop({ default: null })
  board!: BoardModel;
  title = "";
  ticketDetailDialogOpened = false;
  ticket: TicketModel | null = null;

  mounted(): void {
    this.$store.dispatch("loadTickets", this.board);
  }

  async addTicket(): Promise<void> {
    console.log("addTicket");
    const payload = {
      title: this.title,
      description: "",
      board: this.board.id,
    };
    this.title = "";
    const loading = this.$vs.loading({
      target: this.$refs.add,
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
</style>
