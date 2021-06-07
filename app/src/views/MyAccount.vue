<template>
  <div class="my-account">
    <div>
      <label>Email</label>
      <vs-input v-model="email" placeholder="email" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class MyAccount extends Vue {
  email = "";
}
</script>

<style lang="scss" scoped></style>
