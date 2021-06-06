import TicketModel from "@/lib/Ticket";

interface ColumnCreate {
  id: number;
  title: string;
  board: number;
}

export default class ColumnModel {
  id: number;
  title: string;
  board: number;
  tickets: number[];
  tickets_list: TicketModel[];
  _new_ticket_title = "";

  constructor(column: ColumnCreate) {
    this.id = column.id;
    this.title = column.title;
    this.board = column.board;
    this.tickets = [];
    this.tickets_list = [];
  }
}
