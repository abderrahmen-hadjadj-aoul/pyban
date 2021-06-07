<template>
  <div class="landing">
    <form>
      <h1>Login</h1>
      <vs-alert
        id="register-alert"
        v-if="messageLogin.display"
        :color="messageLogin.type"
        :key="messageLogin.type"
      >
        {{ messageLogin.text }}
      </vs-alert>
      <vs-input
        id="login-username"
        v-model="credentials.username"
        placeholder="Username"
        :border="true"
      />
      <vs-input
        id="login-password"
        type="password"
        v-model="credentials.password"
        placeholder="Password"
        :border="true"
      />
      <vs-button id="login" @click.prevent="login"> Login </vs-button>
    </form>
    <form>
      <h1>Create an account</h1>
      <vs-alert
        id="register-alert"
        v-if="messageRegister.display"
        :color="messageRegister.type"
        :key="messageRegister.type"
      >
        {{ messageRegister.text }}
      </vs-alert>
      <vs-input
        id="register-username"
        v-model="register.username"
        placeholder="Username"
        :border="true"
      />
      <vs-input
        id="register-password"
        type="password"
        v-model="register.password"
        placeholder="Password"
        :border="true"
      />
      <vs-input
        id="register-password2"
        type="password"
        v-model="register.password2"
        placeholder="Password"
        :border="true"
      >
        <template
          v-if="register.password !== register.password2"
          #message-danger
        >
          Passwords are not identical
        </template>
      </vs-input>
      <vs-button
        id="create-account"
        @click.prevent="create"
        :disabled="loading || !registerFormValid"
        ref="createAccountButton"
      >
        Create account
      </vs-button>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Client from "@/client";

@Component({
  components: {},
})
export default class Landing extends Vue {
  credentials = {
    username: "",
    password: "",
  };
  messageLogin = {
    display: false,
    type: "",
    text: "",
  };
  register = {
    username: "",
    password: "",
    password2: "",
  };
  messageRegister = {
    display: false,
    type: "",
    text: "",
  };
  loading_ = false;
  // eslint-disable-next-line
  loadingRef: any = null;

  get client(): Client {
    return this.$store.state.client;
  }

  async mounted(): Promise<void> {
    if (this.client.hasToken()) {
      const loader = this.$vs.loading();
      try {
        await this.$store.dispatch("checkUser");
      } catch (e) {
        console.error("userInfo error", e);
      }
      setTimeout(() => {
        loader.close();
      }, 1000);
    }
  }

  async login(): Promise<void> {
    try {
      await this.$store.dispatch("login", this.credentials);
    } catch (e) {
      console.error("login error", e);
      this.messageLogin.display = true;
      this.messageLogin.text = "Wrong credentials";
      this.messageLogin.type = "danger";
    }
  }

  async create(): Promise<void> {
    try {
      this.loading = true;
      const response = await this.$store.dispatch("register", this.register);
      console.log("response", response);
      this.messageRegister.display = true;
      this.messageRegister.text = "Account created";
      this.messageRegister.type = "success";
    } catch (e) {
      console.error("error", e.message);
      this.messageRegister.display = true;
      this.messageRegister.text = e.message;
      this.messageRegister.type = "danger";
    }
    this.loading = false;
  }

  get loading(): boolean {
    return this.loading_;
  }

  set loading(value: boolean) {
    if (value) {
      this.loading_ = value;
      this.loadingRef = this.$vs.loading({
        target: this.$refs.createAccountButton,
        scale: "0.6",
        background: "primary",
        opacity: 1,
        color: "#fff",
      });
    } else {
      this.loading_ = value;
      this.loadingRef.close();
    }
  }

  get registerFormValid(): boolean {
    return this.register.password == this.register.password2;
  }
}
</script>

<style lang="scss">
h1 {
  text-align: center;
}

.landing {
  width: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
}

form {
  padding: 20px;
  border: 1px solid hsl(0, 0%, 80%);
  border-radius: 5px;
  margin-bottom: 20px;
}

form > * {
  margin-bottom: 20px;
}
</style>
