import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "./components-setup.ts";
import "vuesax/dist/vuesax.css";
import "boxicons";
import "boxicons/css/boxicons.min.css";

interface IPrototype {
  /* eslint-disable */
  prototype: any;
}

Vue.config.productionTip = false;
Vue.config.devtools = true;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
