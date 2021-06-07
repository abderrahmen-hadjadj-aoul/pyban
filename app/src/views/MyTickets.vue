<template>
  <div class="my-tickets">
    <vs-table striped>
      <template #thead>
        <vs-tr>
          <vs-th> Title </vs-th>
          <vs-th> Board </vs-th>
          <vs-th> Column </vs-th>
          <vs-th> Description </vs-th>
        </vs-tr>
      </template>
      <template #tbody>
        <vs-tr v-for="ticket in tickets" :key="ticket.id">
          <vs-td>
            <router-link :to="'/tickets/mine/' + ticket.id">
              <div @click="openTicket(ticket)">
                {{ ticket.title }}
              </div>
            </router-link>
          </vs-td>
          <vs-td>
            {{ ticket.board.name }}
          </vs-td>
          <vs-td>
            {{ ticket.column.title }}
          </vs-td>
          <vs-td>
            {{ ticket.description }}
          </vs-td>
        </vs-tr>
      </template>
    </vs-table>
    <Ticket :ticket="ticket" v-if="ticket" @close="onClose" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TicketModel from "@/lib/Ticket";
import Ticket from "@/components/Ticket.vue";

@Component({
  components: { Ticket },
})
export default class MyTickets extends Vue {
  tickets: TicketModel[] = [];
  ticket: TicketModel | null = null;

  async mounted(): Promise<void> {
    this.tickets = await this.$store.dispatch("getMyTickets");
    const ticket_id = this.$route.params.ticket_id;
    if (ticket_id) {
      console.log("has ticket_id", ticket_id);
      const ticket = this.tickets.find((t) => "" + t.id === ticket_id);
      console.log(this.tickets);
      console.log("found ticket", ticket);
      if (ticket) {
        this.openTicket(ticket);
      }
    }
  }

  openTicket(ticket: TicketModel): void {
    this.ticket = ticket;
  }

  onClose(): void {
    this.ticket = null;
    this.$router.push("/tickets/mine");
  }
}
</script>

<style lang="scss" scoped>
.ticket-title {
  display: flex;
}
</style>
