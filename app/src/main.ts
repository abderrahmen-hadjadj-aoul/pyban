import Vue from "vue";
import Vuesax from "vuesax";
import "vuesax/dist/vuesax.css";
import "boxicons";
import "boxicons/css/boxicons.min.css";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

Vue.use(Vuesax, {
  // options here
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
