import app from "./nodeApp"
export const serverStart = async()=>{
    try{
    app.listen(process.env.PORT || 3000 ,()=>{
        console.log("It is running")
    });}
    catch(err){
        console.log(err)
        process.exit(1);
    }
}
serverStart().then(()=>{
    console.log("server is up")
});