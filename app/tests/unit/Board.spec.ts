import { mount } from "@vue/test-utils";
import Board from "@/components/Board.vue";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

describe("Board", () => {
  let actions: any;
  let store: any;

  beforeEach(() => {
    actions = {
      loadBoard: jest.fn(),
      createTicket: jest.fn(),
      updateTicket: jest.fn(),
      deleteTicket: jest.fn(),
    };
    store = new Vuex.Store({
      actions,
    });
  });

  it("should load a board", async () => {
    const ticketItem = {
      id: 1,
      title: "Ticket title",
      description: "Something",
    };
    const column = {
      _new_ticket_title: "",
      tickets_list: [ticketItem],
    };
    const board = {
      name: "My board name",
      columns_list: [column],
    };
    const propsData = {
      board,
    };
    const wrapper = mount(Board, { propsData, store });
    // Check loading
    expect(actions.loadBoard).toHaveBeenCalled();
    // Check title
    const drag = wrapper.findComponent({ name: "Draggable" });
    expect(drag.exists()).toBe(true);
    const title = wrapper.find("h2");
    expect(title.exists()).toBe(true);
    expect(title.text()).toBe(board.name);
    // Check ticket list
    await wrapper.vm.$nextTick();
    const ticket = wrapper.find("li");
    expect(ticket.exists()).toBe(true);
    const input = ticket.find("input").element as HTMLInputElement;
    expect(input.value).toBe(ticketItem.title);
    // Check ticket creation
    const buttonCreate = wrapper.find("#create-ticket");
    expect(buttonCreate.attributes("disabled")).toBe("disabled");
    column._new_ticket_title = "New title";
    await wrapper.vm.$nextTick();
    expect(buttonCreate.attributes("disabled")).not.toBe("disabled");
    await buttonCreate.trigger("click");
    expect(actions.createTicket).toHaveBeenCalled();
    // Check Ticket Dialog
    ticket.trigger("dblclick");
    await wrapper.vm.$nextTick();
    // Title
    const dialogInput = wrapper.find("input[data-name='dialog-title']");
    expect(dialogInput.exists()).toBe(true);
    const dialogInputEl = dialogInput.element as HTMLInputElement;
    expect(dialogInputEl.value).toBe(ticketItem.title);
    // Description
    const dialogTextarea = wrapper.find(
      "textarea[data-name='dialog-description']"
    );
    expect(dialogInput.exists()).toBe(true);
    const dialogTextareaEl = dialogTextarea.element as HTMLInputElement;
    expect(dialogTextareaEl.value).toBe(ticketItem.description);
    // Save ticket
    dialogInput.trigger("change");
    await wrapper.vm.$nextTick();
    expect(actions.updateTicket).toHaveBeenCalled();
    // Delete
    await wrapper.find("#delete-button").trigger("click");
    expect(actions.deleteTicket).toHaveBeenCalled();
  });
});
