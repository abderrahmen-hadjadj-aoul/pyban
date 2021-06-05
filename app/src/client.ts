import axios from "axios";

export default class Client {
  base = "http://localhost:8000/";
  instance: any;
  token: string | null = null;

  constructor() {
    const token = localStorage.getItem("token");
    if (token) {
      this.token = token;
    }
    this.initInstance();
  }

  initInstance(): void {
    const headers: any = {};
    if (this.token) {
      headers.Authorization = "Token " + this.token;
    }
    this.instance = axios.create({
      baseURL: this.base,
      headers,
    });
    console.log("instance", headers);
  }

  // USERS

  async register(credentials: any): Promise<any> {
    try {
      const res = await this.instance.post("/tickets/users", credentials);
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }

  async login(credentials: any): Promise<any> {
    try {
      const res = await this.instance.post(
        "/tickets/api-token-auth",
        credentials
      );
      this.token = "" + res.data.token;
      localStorage.setItem("token", this.token);
      this.initInstance();
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }

  async getUserInfo(): Promise<any> {
    try {
      const res = await this.instance.get("/tickets/users/me");
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }

  // BOARDS

  async createBoard(board: any): Promise<any> {
    try {
      const res = await this.instance.post("/tickets/boards", board);
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }

  async getBoards(): Promise<any> {
    try {
      const res = await this.instance.get("/tickets/boards");
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }
}
