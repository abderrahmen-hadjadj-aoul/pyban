import { mount } from "@vue/test-utils";
import Landing from "@/components/Landing.vue";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

describe("Landing", () => {
  let actions: any;
  let state: any;
  let store: any;
  beforeEach(() => {
    actions = {
      register: jest.fn(),
      login: jest.fn(),
    };
    state = {
      client: {
        hasToken: () => false,
      },
    };
    store = new Vuex.Store({
      state,
      actions,
    });
  });

  it("should create an account", () => {
    const wrapper = mount(Landing, { store });
    const button = wrapper.get("#create-account");
    button.trigger("click");
    expect(actions.register).toHaveBeenCalled();
  });

  it("should login", async () => {
    const wrapper = mount(Landing, { store });
    const button = wrapper.get("#login");
    await button.trigger("click");
    expect(actions.login).toHaveBeenCalled();
  });
});
