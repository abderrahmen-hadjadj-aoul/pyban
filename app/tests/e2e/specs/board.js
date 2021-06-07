// https://docs.cypress.io/api/introduction/api.html

describe("Test boards", () => {

  it("Create a board", () => {
    const name = "Board name here - " + Date.now();
    cy.visit("/");
    const username = "test-" + Date.now();
    cy.get("#register-username").type(username);
    cy.get("#register-password").type("test");
    cy.get("#register-password2").type("test");
    cy.get("#create-account").click();
    cy.get("#login-username").type(username);
    cy.get("#login-password").type("test");
    cy.get("#login").click();
    cy.get("[data-nav='nav-boards']").click();
    cy.get("#open-dialog").click();
    cy.get("#board-name").type(name);
    cy.get("#create-board").click();
    cy.contains("article.board-item > h1", name).should("be.visible");
  });

  it.only("Create and update ticket", () => {
    const name = "Board name here - " + Date.now();
    cy.visit("/");
    const username = "test-" + Date.now();
    cy.get("#register-username").type(username);
    cy.get("#register-password").type("test");
    cy.get("#register-password2").type("test");
    cy.get("#create-account").click();
    cy.get("#login-username").type(username);
    cy.get("#login-password").type("test");
    cy.get("#login").click();
    cy.get("[data-nav='nav-boards']").click();
    cy.get("#open-dialog").click();
    cy.get("#board-name").type(name);
    cy.get("#create-board").click();
    cy.contains("article.board-item > h1", name).click();
    cy.contains("h2", name).should("be.visible");
    // Create new column
    cy.contains("button", "Add column").click();
    // Create new ticket with button
    const title = "Ticket title";
    cy.get("[data-column-index='0'] .ticket-title input").type(title);
    cy.get("#create-ticket").click();
    cy.get("li[data-index='0'] input").should("have.value", title);
    // Create new ticket with enter
    const title2 = "Ticket title for enter";
    cy.get("[data-column-index='0'] .ticket-title input").type(title2 + "{enter}");
    cy.get("li[data-index='1'] input").should("have.value", title2);
    // Delete
    cy.get("li[data-index='1']").dblclick();
    cy.get("input[data-name='dialog-title']").should("have.value", title2);
    cy.get("textarea[data-name='dialog-description']").should("have.value", "");
    cy.get("#delete-button").click();
    cy.get("li[data-index='1']").should("not.exist");
    // Update
    const newTitle = "New title";
    const newDescription = "New description";
    cy.get("li[data-index='0']").dblclick();
    cy.get("input[data-name='dialog-title']").clear().type(newTitle);
    cy.get("textarea[data-name='dialog-description']").clear().type(newDescription);
    cy.get(".vs-dialog__close").click();
    cy.wait(1000);
    // Check persistence
    cy.visit("/");
    cy.get("[data-nav='nav-boards']").click();
    cy.contains("article.board-item > h1", name).click();
    cy.get("li[data-index='0'] input").should("have.value", newTitle);
    cy.get("li[data-index='0']").dblclick();
    cy.get("input[data-name='dialog-title']").should("have.value", newTitle);
    cy.get("textarea[data-name='dialog-description']").should("have.value", newDescription);
    cy.get("li[data-index='1']").should("not.exist");
  });

});
