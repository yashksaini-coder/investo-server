import {User} from "../models/User"
export interface comands{
    create(data: User): Promise <User>;
    update(data: User): Promise <User>;
    delete(id: any): Promise<any>;
    find(limit:number, offset: number): Promise <User[]>;
    findOne(id?: number, email?: string): Promise<User | null>;
}