import express from "express"
import router from "./api/routes"
import authRouter from "./api/authRoutes";
import { json } from "body-parser";
const app=express()
app.use(express.json())
app.use("/api/routes", router);
app.use("/api/auth", authRouter);
app.get("/",(req,res)=>{
    res.send("Hello")
})
export default app;