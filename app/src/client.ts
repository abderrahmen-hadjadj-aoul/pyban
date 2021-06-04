import axios from "axios";

export default class Client {
  base = "http://localhost:8000/";
  instance: any;

  constructor() {
    this.instance = axios.create({
      baseURL: this.base,
    });
  }

  async register(credentials: any): Promise<any> {
    try {
      const res = await this.instance.post("/tickets/users", credentials);
      return res;
    } catch (e) {
      const data = e.response.data;
      throw new Error(data.message);
    }
  }
}
