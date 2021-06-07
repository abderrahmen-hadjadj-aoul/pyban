import { mount } from "@vue/test-utils";
import Boards from "@/views/Boards.vue";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

describe("Boards", () => {
  let actions: any;
  let store: any;

  beforeEach(() => {
    actions = {
      getBoards: jest.fn(),
      createBoard: jest.fn(),
    };
    store = new Vuex.Store({
      actions,
    });
  });

  it("should create a board", async () => {
    const name = "Board Name here";
    const $route = {
      params: {},
    };
    store.state.boards = [{ name }];
    const wrapper = mount(Boards, {
      store,
      mocks: {
        $route,
      },
    });
    const item = wrapper.find(".board-item");
    expect(item.exists()).toBe(true);
    expect(actions.getBoards).toHaveBeenCalled();
    // Open Dialog
    const buttonOpen = wrapper.get("#open-dialog");
    buttonOpen.trigger("click");
    // Set name
    wrapper.setData({ boardName: name });
    await wrapper.vm.$nextTick();
    // Create board
    const buttonCreate = wrapper.get("#create-board");
    await buttonCreate.trigger("click");
    expect(actions.createBoard).toHaveBeenCalled();
  });
});
