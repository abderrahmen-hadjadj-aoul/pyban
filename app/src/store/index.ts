import Vue from "vue";
import Vuex from "vuex";
import BoardModel from "@/lib/Board";
import TicketModel from "@/lib/Ticket";
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

export default new Vuex.Store({
  state: {
    logged: false,
    token: null,
    user: null,
    boards,
  },
  mutations: {
    // USER
    setUser(state, user) {
      state.logged = true;
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
    addTicket(state, ticket) {
      console.log("add ticket", ticket);
      const board = state.boards.find((board) => board.id === ticket.board);
      console.log("add ticket in board", board);
      console.log("searching ticket", ticket.id);
      if (board) {
        const index = board.tickets
          .map((ticket) => ticket.id)
          .indexOf(ticket.id);
        console.log("index", index);
        if (index > -1) {
          board.tickets[index] = ticket;
        } else {
          board.tickets.push(ticket);
        }
      }
    },
    deleteTicket(state, ticket) {
      console.log("delete ticket", ticket);
      const board = state.boards.find((board) => board.id === ticket.board);
      if (board) {
        const index = board.tickets
          .map((ticket) => ticket.id)
          .indexOf(ticket.id);
        if (index > -1) {
          board.tickets.splice(index, 1);
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
    // TICKET
    async loadTickets(context, board) {
      console.log("loadTickets", board);
      const res = await client.loadTickets(board);
      const tickets = res.data.map(
        (ticket: TicketModel) => new TicketModel(ticket)
      );

      tickets.forEach((ticket: TicketModel) => {
        context.commit("addTicket", ticket);
      });
      return tickets;
    },
    async createTicket(context, ticket) {
      console.log("createTicket", ticket);
      const res = await client.createTicket(ticket);
      const createdTicket = new TicketModel(res.data);
      context.commit("addTicket", createdTicket);
      return createdTicket;
    },
    async updateTicket(context, payload: TicketPatchPayload) {
      console.log("updateTicket", payload);
      await client.updateTicket(payload);
    },
    async deleteTicket(context, ticket: TicketModel) {
      console.log("deleteTicket", ticket);
      await client.deleteTicket(ticket);
      context.commit("deleteTicket", ticket);
    },
  },
  modules: {},
});
