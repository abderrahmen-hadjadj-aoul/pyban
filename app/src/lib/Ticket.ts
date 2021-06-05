export interface TicketCreate {
  id: number;
  title: string;
  description: string;
  board: number;
}

export default class TicketModel {
  id: number;
  title: string;
  description: string;
  board: number;

  constructor(ticket: TicketCreate) {
    this.id = ticket.id;
    this.board = ticket.board;
    this.title = ticket.title;
    this.description = ticket.description;
  }
}
