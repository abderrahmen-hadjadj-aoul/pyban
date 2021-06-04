import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
import Client from "../client";
const client = new Client();

export default new Vuex.Store({
  state: {
    logged: false,
    user: null,
  },
  mutations: {
    setUser(state, user) {
      state.logged = true;
      state.user = user;
    },
  },
  actions: {
    async register(context, credentials) {
      console.log("register", credentials);
      const res = await client.register(credentials);
      return res;
    },
    async login(context, credentials) {
      console.log("login", credentials);
      const res = await client.login(credentials);
      context.commit("setUser", res);
      return res;
    },
  },
  modules: {},
});
