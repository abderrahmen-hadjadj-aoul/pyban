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
            {{ ticket.title }}
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TicketModel from "@/lib/Ticket";

@Component({
  components: {},
})
export default class MyTickets extends Vue {
  tickets: TicketModel[] = [];

  async mounted(): Promise<void> {
    this.tickets = await this.$store.dispatch("getMyTickets");
  }
}
</script>

<style lang="scss" scoped></style>
