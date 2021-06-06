<template>
  <div id="app" v-if="logged">
    <div id="nav">
      <vs-sidebar v-model="showNav" open>
        <vs-sidebar-item id="my-account" to="/my-account">
          <template #icon>
            <i class="bx bx-user"></i>
          </template>
          My account ({{ username }})
        </vs-sidebar-item>
        <vs-sidebar-item id="logout" @click.native="logout" to="/logout">
          <template #icon>
            <i class="bx bx-log-out-circle"></i>
          </template>
          Logout
        </vs-sidebar-item>
        <vs-sidebar-item id="home" to="/">
          <template #icon>
            <i class="bx bx-home"></i>
          </template>
          Home
        </vs-sidebar-item>
        <vs-sidebar-item data-nav="nav-boards" id="nav-boards" to="/boards">
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
  <Landing v-else />
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Landing from "@/components/Landing.vue";
import User from "@/lib/User";

@Component({
  components: { Landing },
})
export default class App extends Vue {
  showNav = true;

  get logged(): boolean {
    return this.$store.state.logged;
  }

  get user(): User {
    return this.$store.state.user;
  }

  get username(): string {
    return this.user ? this.user.username : "";
  }

  logout(): void {
    this.$store.dispatch("logout");
  }
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
