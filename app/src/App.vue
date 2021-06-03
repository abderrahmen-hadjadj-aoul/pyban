<template>
  <div id="app">
    <div id="nav">
      <vs-sidebar absolute v-model="showNav" open>
        <vs-sidebar-item id="my-account" to="/my-account">
          <template #icon>
            <i class="bx bx-user"></i>
          </template>
          My account
        </vs-sidebar-item>
        <vs-sidebar-item id="home" to="/">
          <template #icon>
            <i class="bx bx-home"></i>
          </template>
          Home
        </vs-sidebar-item>
        <vs-sidebar-item id="boards" to="/boards">
          <template #icon>
            <i class="bx bx-columns"></i>
          </template>
          Boards
        </vs-sidebar-item>
        <vs-sidebar-item id="my-tickets" to="/tickets/mine">
          <template #icon>
            <i class="bx bx-purchase-tag"></i>
          </template>
          My Tickets
        </vs-sidebar-item>
      </vs-sidebar>
    </div>
    <div id="center">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class App extends Vue {
  showNav = true;
}
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");

body {
  font-family: Roboto;
}
#center {
  margin-left: 300px;
}
</style>
