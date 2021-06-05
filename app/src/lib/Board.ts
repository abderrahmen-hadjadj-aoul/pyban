import TicketModel from "@/lib/Ticket";

interface BoardCreate {
  id: number;
  name: string;
}

export default class BoardModel {
  id: number;
  name: string;
  tickets: TicketModel[];
  _ticketsLoaded = false;

  constructor(board: BoardCreate) {
    this.id = board.id;
    this.name = board.name;
    this.tickets = [];
  }

  setTicketsLoaded(value: boolean): void {
    this._ticketsLoaded = value;
  }
}
