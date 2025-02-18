import express, { NextFunction, Request, Response } from "express";
import { UserService } from "../services/configServices";
import { data } from "../repo/data";
import { RequestValidator } from "../utils/requestValidators";
import { CreateUserRequest, UpdateUserRequest } from "../dto/userDto";

const app = express();

export const userService = new UserService(new data());

// endpoints
app.post(
  "/users",
  async (req: Request, res: Response) => {
    try {
      const { errors, input } = await RequestValidator(
        CreateUserRequest,
        req.body
      );
      if (errors) return res.status(400).json(errors);
      const data = await userService.createUser(input);
      return res.status(201).json(data);
    } catch (error) {
      const err = error as Error;
      return res.status(500).json(err.message);
    }
  }
);

app.patch(
  "/users/:id",
  async (req: Request, res: Response) => {
    try {
      const { errors, input } = await RequestValidator(
        UpdateUserRequest,
        req.body
      );

      const id = parseInt(req.params.id) || 0;

      if (errors) return res.status(400).json(errors);

      const data = await userService.updateUser({ id, ...input });
      return res.status(200).json(data);
    } catch (error) {
      const err = error as Error;
      return res.status(500).json(err.message);
    }
  }
);

app.get(
  "/users",
  async (req: Request, res: Response) => {
    const limit = Number(req.query["limit"] || 10);
    const offset = Number(req.query["offset"] || 1);
    try {
      const data = await userService.getUsers(limit, offset);
      return res.status(200).json(data);
    } catch (error) {
      const err = error as Error;
      return res.status(500).json(err.message);
    }
  }
);

app.get(
  "/users/:id",
  async (req: Request, res: Response, next: NextFunction) => {
    const id = parseInt(req.params.id) || 0;
    try {
      const data = await userService.getUser(id);
      return res.status(200).json(data);
    } catch (error) {
      return next(error);
    }
  }
);

app.delete(
  "/users/:id",
  async (req: Request, res: Response) => {
    const id = parseInt(req.params.id) || 0;
    try {
      const data = await userService.deleteUser(id);
      return res.status(200).json(data);
    } catch (error) {
      const err = error as Error;
      return res.status(500).json(err.message);
    }
  }
);

export default app;