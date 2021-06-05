interface BoardCreate {
  id: number;
  name: string;
}

export default class BoardModel {
  id: number;
  name: string;

  constructor(board: BoardCreate) {
    this.id = board.id;
    this.name = board.name;
  }
}
