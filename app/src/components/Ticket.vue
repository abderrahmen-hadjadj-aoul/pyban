<template>
  <div class="ticket" v-if="ticket">
    <vs-dialog
      width="300px"
      not-center
      v-model="ticketDetailDialogOpened"
      @close="onClose"
    >
      <template #header>
        <h4 class="not-margin">Update ticket</h4>
      </template>

      <div class="con-content" v-if="ticket">
        <vs-input
          data-name="dialog-title"
          v-model="ticket.title"
          @change="changeTicket(ticket)"
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
import TicketModel from "@/lib/Ticket";

@Component({
  components: {},
})
export default class Board extends Vue {
  @Prop({ default: null })
  ticket!: TicketModel;
  ticketDetailDialogOpened = true;

  mounted(): void {
    this.ticketDetailDialogOpened = true;
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

  async deleteTicket(ticket: TicketModel): Promise<void> {
    this.$store.dispatch("deleteTicket", ticket);
    this.onClose();
  }

  onClose(): void {
    this.$emit("close");
  }
}
</script>

<style lang="scss" scoped>
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
