const express = require('express')
const {spawn} = require('child_process');
const app = express();

require('./startup/routes')(app);
require('./startup/logging')();
app.get('/', (req, res) => {
 
 var dataToSend;
 // spawn new child process to call the python script
 const python = spawn('python', ['get_inventory.py', '172.29.9.0/30']);
 // collect data from script
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 // in close event we are sure that stream from child process is closed
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 // send data to browser
 res.send(dataToSend)
 });
 
})
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));