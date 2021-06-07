import ColumnModel from "@/lib/Column";
import TicketModel from "@/lib/Ticket";

interface BoardCreate {
  id: number;
  name: string;
  columns: number[];
}

export default class BoardModel {
  id: number;
  name: string;
  columns: number[];
  columns_list: ColumnModel[];
  _columns_loaded = false;

  constructor(board: BoardCreate) {
    this.id = board.id;
    this.name = board.name;
    this.columns = board.columns;
    this.columns_list = [];
  }

  getTickets(): TicketModel[] {
    const tickets: TicketModel[] = [];
    this.columns_list.forEach((column) => {
      column.tickets_list.forEach((ticket) => {
        tickets.push(ticket);
      });
    });
    return tickets;
  }
}
