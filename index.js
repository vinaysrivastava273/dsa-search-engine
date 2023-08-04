const express = require('express'); //Import the express dependency
const ejs = require('ejs');
const path = require('path');
const spawner = require('child_process').spawn;

const app = express();              //Instantiate an express app, the main work horse of this server
const PORT = process.env.PORT || 3000;                  //Save the PORT number where your server will be listening

app.use(express.json());
app.set("view engine", "ejs");
app.use(express.static(path.join(__dirname, "/public")));

//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => {        //get requests to the root ("/") will route here
    // console.log("hey there I'm in the home route.")
    res.render("index");
    // res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser
    //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile 
});

app.get("/search", (req, res) => {
    const query = req.query;
    const question = query.question;
    address = path.join(__dirname, 'LeetCode', 'user_query.py');
    // console.log('current directory:', address);

    console.log("Data sent to Python:", question);
    const python_process = spawner('python', [address, JSON.stringify(question)]);

    try{
        python_process.stdout.on('data', (data) => {
            arr = JSON.parse(data.toString());
            console.log("Data received from Python:", arr);
            res.json(arr);
        });    
    }catch(error){
        console.log("error");
        res.json('no data recieved');
    }
});

// app.get("/question/:id", (req, res) => {
//     const id = req.params.id;
//     res.locals.question = "The sum of two elements";
//     res.render("question");
// })

app.listen(PORT, () => {            //server starts listening for any attempts from a client to connect at port: {port}
    console.log(`Now listening on port ${PORT}`); 
});