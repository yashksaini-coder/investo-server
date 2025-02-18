import { PrismaClient } from "@prisma/client";
import { comands } from "../interface/comandingTheRepo";
import { User } from "../models/User";

export class data implements comands {
  prism: PrismaClient;

  constructor() {
    this.prism = new PrismaClient();
  }

  async create(data: User): Promise<User> {
    return this.prism.user.create({
      data,
    });
  }

  async update(data: User): Promise<User> {
    return this.prism.user.update({
      where: { id: data.id },
      data,
    });
  }

  async delete(id: number): Promise<any> {
    return this.prism.user.delete({
      where: { id },
    });
  }

  async find(limit: number, offset: number): Promise<User[]> {
    return this.prism.user.findMany({
      skip: offset,
      take: limit,
    });
  }

  async findOne(id?: number, email?: string): Promise<User | null> {
    if (!id && !email) {
      throw new Error("Either 'id' or 'email' must be provided");
    }
  
    return this.prism.user.findUnique({
      where: id ? { id } : { email }, 
    });
  }
}
