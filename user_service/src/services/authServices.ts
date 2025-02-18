import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs'; 
import { UserService } from "./configServices";
import { data } from "../repo/data";

export class AuthService {
  private userService: UserService;
  private secretKey: string = process.env.SECRET as string;

  constructor() {
    this.userService = new UserService(new data());
  }

  async login(credentials: { email: string; password: string }) {
    const user = await this.userService.getUserbyEmail(credentials.email);

    if (!user || !(await this.comparePassword(credentials.password, user.password))) {
      return null;
    }

    const token = this.generateToken(user);
    return token;
  }

  async hashPassword(password: string): Promise<string> {
    const salt = await bcrypt.genSalt(10); 
    return bcrypt.hash(password, salt); 
  }

  private async comparePassword(plainPassword: string, hashedPassword: string): Promise<boolean> {
    return bcrypt.compare(plainPassword, hashedPassword); 
  }

  private generateToken(user: any) {
    const payload = {
      id: user.id,
      email: user.email
    };

    const token = jwt.sign(payload, this.secretKey, { expiresIn: '1h' }); 
    return token;
  }

  public verifyToken(token: string) {
    try {
      const decoded = jwt.verify(token, this.secretKey); 
      return decoded;
    } catch (error) {
      return null; 
    }
  }
}
