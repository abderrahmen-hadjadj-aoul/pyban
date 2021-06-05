// https://docs.cypress.io/api/introduction/api.html

describe("Test boards", () => {
  it("Create a board", () => {
    const name = "Board name here - " + Date.now();
    cy.visit("/");
    cy.get("#login-username").type("test");
    cy.get("#login-password").type("test");
    cy.get("#login").click();
    cy.get("[data-nav='nav-boards']").click();
    cy.get("#open-dialog").click();
    cy.get("#board-name").type(name);
    cy.get("#create-board").click();
    cy.contains("article.board-item > h1", name).should("be.visible");
  });
});