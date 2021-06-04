// https://docs.cypress.io/api/introduction/api.html

describe("Test general features", () => {
  it("Create an account", () => {
    cy.visit("/");
    cy.contains("h1", "Create an account");
    const username = "user-" + Date.now();
    const password = "123";
    cy.get("#register-username").type(username);
    cy.get("#register-password").type(password);
    cy.get("#register-password2").type(password);
    cy.get("#create-account").click();
    const alert = cy.get("#register-alert");
    alert.contains("div", "Account created").should("exist");
  });

  it("Create an account with two password different", () => {
    cy.visit("/");
    cy.contains("h1", "Create an account");
    const username = "user-" + Date.now();
    const password = "123";
    const password2 = "1234";
    cy.get("#register-username").type(username);
    cy.get("#register-password").type(password);
    cy.get("#register-password2").type(password2);
    cy.get("#create-account").should("have.attr", "disabled", "disabled");
    cy.contains("div", "Passwords are not identical").should("exist");
  });
});
