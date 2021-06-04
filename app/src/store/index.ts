import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);
import Client from "../client";
const client = new Client();

export default new Vuex.Store({
  state: {
    logged: false,
  },
  mutations: {},
  actions: {
    login(context, credentials) {
      console.log("login", credentials);
    },
    async register(context, credentials) {
      console.log("register", credentials);
      const res = await client.register(credentials);
      return res;
    },
  },
  modules: {},
});
