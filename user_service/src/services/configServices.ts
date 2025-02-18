import { comands } from "../interface/comandingTheRepo";

export class UserService {
  private _repository: comands;

  constructor(repository: comands) {
    this._repository = repository;
  }

  async createUser(input: any) {
    
    const existingUser = await this._repository.findOne(undefined, input.email);
    if (existingUser) {
      throw new Error("User already exists");
    }
    const data = await this._repository.create(input);
    if (!data.id) {
      throw new Error("Not able to create user");
    }
    return data;
  }

  async updateUser(input: any) {
    const data = await this._repository.update(input);
    if (!data.id) {
      throw new Error("Unable to update user");
    }
    return data;
  }

  async getUsers(limit: number, offset: number) {
    const users = await this._repository.find(limit, offset);
    return users;
  }

  async getUser(id: number) {
    const user = await this._repository.findOne(id);
    return user;
  }
  async getUserbyEmail(email: string) {
    const user = await this._repository.findOne(undefined, email);
    return user;
  }
  async deleteUser(id: number) {
    const response = await this._repository.delete(id);
    return response;
  }
}
