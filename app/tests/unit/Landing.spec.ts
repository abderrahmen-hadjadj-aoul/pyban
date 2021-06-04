import { mount } from "@vue/test-utils";
import Landing from "@/components/Landing.vue";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

describe("Landing", () => {
  let actions: any;
  let store: any;
  beforeEach(() => {
    actions = {
      register: jest.fn(),
    };
    store = new Vuex.Store({
      actions,
    });
  });

  it("should create an account", () => {
    const wrapper = mount(Landing, { store });
    expect(wrapper.get("#create-account").text()).toMatch("Create account");
    const button = wrapper.get("#create-account");
    button.trigger("click");
    expect(actions.register).toHaveBeenCalled();
  });
});
