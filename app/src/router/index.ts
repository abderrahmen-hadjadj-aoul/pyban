import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";
import Boards from "../views/Boards.vue";
import MyTickets from "../views/MyTickets.vue";
import MyAccount from "../views/MyAccount.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
    redirect: "/boards",
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/my-account",
    name: "MyAccount",
    component: MyAccount,
  },
  {
    path: "/tickets/mine",
    name: "MyTickets",
    component: MyTickets,
  },
  {
    path: "/tickets/mine/:ticket_id",
    name: "MyTickets",
    component: MyTickets,
  },
  {
    path: "/boards",
    name: "Boards",
    component: Boards,
  },
  {
    path: "/boards/:board_id",
    name: "Board",
    component: Boards,
  },
  {
    path: "/boards/:board_id/tickets/:ticket_id",
    name: "Board",
    component: Boards,
  },
];

const router = new VueRouter({
  // mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
