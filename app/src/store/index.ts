import Vue from "vue";
import Vuex from "vuex";
import BoardModel from "@/lib/Board";
import TicketModel from "@/lib/Ticket";
import ColumnModel from "@/lib/Column";
import Client from "../client";

Vue.use(Vuex);
const client = new Client();

const boards: BoardModel[] = [];

interface TicketPatch {
  title?: string;
  description?: string;
}

interface TicketPatchPayload {
  id: string;
  patch: TicketPatch;
}

interface ColumnAddPayload {
  board: BoardModel;
  column: ColumnModel;
}

export default new Vuex.Store({
  state: {
    client,
    logged: false,
    token: null,
    user: null,
    boards,
  },
  mutations: {
    // USER
    setUser(state, user) {
      state.logged = !!user;
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
    // BOARDS
    addBoard(state, board) {
      state.boards.push(board);
    },
    setBoards(state, boards) {
      state.boards = boards.map((board: BoardModel) => new BoardModel(board));
    },
    // TICKETS
    addTicket(state, { column, ticket }) {
      console.log("add ticket", ticket);
      if (!column) {
        const board = state.boards.find((board) => board.id === ticket.board);
        if (board) {
          console.log("found board");
          column = board.columns_list.find(
            (column) => column.id === ticket.column
          );
        }
      }
      if (column) {
        const index = column.tickets_list
          .map((ticket: TicketModel) => ticket.id)
          .indexOf(ticket.id);
        console.log("index", index);
        if (index > -1) {
          column.tickets_list[index] = ticket;
        } else {
          column.tickets.push(ticket.id);
          column.tickets_list.push(ticket);
        }
      }
    },
    deleteTicket(state, { column, ticket }) {
      console.log("delete ticket", ticket);
      if (!column) {
        const board = state.boards.find((board) => board.id === ticket.board);
        if (board) {
          console.log("found board");
          column = board.columns_list.find(
            (column) => column.id === ticket.column
          );
        }
      }
      if (column) {
        const index = column.tickets.indexOf(ticket.id);
        if (index > -1) {
          column.tickets.splice(index, 1);
        }
        const index2 = column.tickets_list
          .map((ticket: TicketModel) => ticket.id)
          .indexOf(ticket.id);
        if (index2 > -1) {
          column.tickets_list.splice(index2, 1);
        }
      }
    },
    // COLUMNS
    addColumn(state, column: ColumnModel) {
      console.log("store add column", column);
      const board = state.boards.find((board) => board.id === column.board);
      if (board) {
        const index = board.columns_list
          .map((ticket) => ticket.id)
          .indexOf(column.id);
        console.log("index", index);
        if (index > -1) {
          board.columns_list[index] = column;
        } else {
          board.columns_list.push(column);
        }
      }
    },
    deleteColumn(state, column: ColumnModel) {
      console.log("store delete column", column);
      const board = state.boards.find((board) => board.id === column.board);
      if (board) {
        const index = board.columns_list
          .map((ticket) => ticket.id)
          .indexOf(column.id);
        console.log("index", index);
        if (index > -1) {
          board.columns_list.splice(index, 1);
        }
      }
    },
  },
  actions: {
    // USERS
    async register(context, credentials) {
      console.log("register", credentials);
      const res = await client.register(credentials);
      return res;
    },
    async login(context, credentials) {
      console.log("login", credentials);
      const res = await client.login(credentials);
      console.log("login res", res);
      context.commit("setToken", res.data.token);
      const resCurrentUser = await client.getUserInfo();
      console.log("resCurrentUser", resCurrentUser);
      context.commit("setUser", resCurrentUser.data);
      return resCurrentUser;
    },
    async checkUser(context) {
      setTimeout(async () => {
        const res = await client.getUserInfo();
        context.commit("setUser", res.data);
      }, 1000);
    },
    async logout(context) {
      console.log("store logout");
      context.commit("setUser", null);
      client.logout();
    },
    // BOARDS
    async createBoard(context, board) {
      console.log("createBoard", board);
      const res = await client.createBoard(board);
      const createdBoard = res.data;
      context.commit("addBoard", new BoardModel(createdBoard));
      return createdBoard;
    },
    async getBoards(context) {
      console.log("getBoards");
      const res = await client.getBoards();
      const boards = res.data;
      context.commit("setBoards", boards);
      return boards;
    },
    async loadBoard(context, board) {
      const res = await client.loadBoard(board);
      board.columns_list = res.data.map(
        (column: ColumnModel) => new ColumnModel(column)
      );
      await context.dispatch("loadTickets", board);
    },
    // TICKET
    async loadTickets(context, board) {
      console.log("loadTickets", board);
      const res = await client.loadTickets(board);
      const tickets = res.data.map(
        (ticket: TicketModel) => new TicketModel(ticket)
      );

      console.log("tickets", tickets);

      tickets.forEach((ticket: TicketModel) => {
        context.commit("addTicket", { ticket });
      });
      return tickets;
    },
    async createTicket(context, { column, ticket }) {
      console.log("createTicket", ticket);
      const res = await client.createTicket(ticket);
      const createdTicket = new TicketModel(res.data);
      context.commit("addTicket", { column, ticket: createdTicket });
      return createdTicket;
    },
    async updateTicket(context, payload: TicketPatchPayload) {
      console.log("updateTicket", payload);
      await client.updateTicket(payload);
    },
    async deleteTicket(context, ticket: TicketModel) {
      console.log("deleteTicket", ticket);
      await client.deleteTicket(ticket);
      context.commit("deleteTicket", { ticket });
    },
    // COLUMNS
    async addColumn(context, payload: ColumnAddPayload) {
      console.log("addColumn in board", payload);
      const res = await client.addColumn(payload.board, payload.column);
      const createdColumn = new ColumnModel(res.data);
      context.commit("addColumn", createdColumn);
    },
    async updateColumn(context, column: ColumnModel) {
      console.log("updateColumn", column);
      await client.updateColumn(column);
    },
    async deleteColumn(context, column: ColumnModel) {
      console.log("deleteColumn", column);
      await client.deleteColumn(column);
      context.commit("deleteColumn", column);
    },
  },
  modules: {},
});
