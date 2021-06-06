import ColumnModel from "@/lib/Column";

interface BoardCreate {
  id: number;
  name: string;
  columns: number[];
}

export default class BoardModel {
  id: number;
  name: string;
  _ticketsLoaded = false;
  columns: number[];
  columns_list: ColumnModel[];
  _columns_loaded = false;

  constructor(board: BoardCreate) {
    this.id = board.id;
    this.name = board.name;
    this.columns = board.columns;
    this.columns_list = [];
  }

  setTicketsLoaded(value: boolean): void {
    this._ticketsLoaded = value;
  }
}
