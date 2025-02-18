import express, { Request, Response } from "express";
import { AuthService } from "../services/authServices";  
import { UserService } from "../services/configServices"; 
import { CreateUserRequest, LoginRequest } from "../dto/userDto"; 
import { RequestValidator } from "../utils/requestValidators";
import { data } from "../repo/data";

const router = express.Router();
const authService = new AuthService();
const userService = new UserService(new data());

router.post("/register", async (req: Request, res: Response) => {
  try {
    const { errors, input } = await RequestValidator(CreateUserRequest, req.body);
    if (errors) return res.status(400).json(errors);
    const hashedPassword = await authService.hashPassword(input.password);
  
    input.password = hashedPassword;
    const data = await userService.createUser(input);
    return res.status(201).json(data);
  } catch (error) {
    const err = error as Error;
    return res.status(500).json({ message: err.message });
  }
});

router.post("/login", async (req: Request, res: Response) => {
  try {
    const { errors, input } = await RequestValidator(LoginRequest, req.body);
    if (errors) return res.status(400).json(errors);

    const token = await authService.login(input);  
    if (!token) return res.status(401).json({ message: "Invalid credentials" });

    return res.status(200).json({ token });
  } catch (error) {
    const err = error as Error;
    return res.status(500).json({ message: err.message });
  }
});

export default router;
