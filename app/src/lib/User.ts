interface UserCreate {
  id: number;
  username: string;
}
export default class UserModel {
  id: number;
  username: string;

  constructor(user: UserCreate) {
    this.id = user.id;
    this.username = user.username;
  }
}
