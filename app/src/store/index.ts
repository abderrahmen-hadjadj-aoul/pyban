import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
import Client from "../client";
const client = new Client();

const boards: any[] = [];

export default new Vuex.Store({
  state: {
    logged: false,
    token: null,
    user: null,
    boards,
  },
  mutations: {
    setUser(state, user) {
      state.logged = true;
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
    addBoard(state, board) {
      state.boards.push(board);
    },
    setBoards(state, boards) {
      state.boards = boards;
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
      context.commit("addBoard", createdBoard);
      return createdBoard;
    },
    async getBoards(context) {
      console.log("getBoards");
      const res = await client.getBoards();
      const boards = res.data;
      context.commit("setBoards", boards);
      return boards;
    },
  },
  modules: {},
});
