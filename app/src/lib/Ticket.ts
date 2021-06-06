export interface TicketCreate {
  id: number;
  title: string;
  description: string;
  column: number;
  board: number;
}

export default class TicketModel {
  id: number;
  title: string;
  description: string;
  column: number;
  board: number;

  constructor(ticket: TicketCreate) {
    this.id = ticket.id;
    this.column = ticket.column;
    this.board = ticket.board;
    this.title = ticket.title;
    this.description = ticket.description;
  }
}
