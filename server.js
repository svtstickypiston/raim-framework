const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();

// Enable CORS
app.use(cors({origin: ['http://127.0.0.1:5500']}));

// Directory to list files from
const directoryPath = './pillars';
let pillars = [];

// API endpoint to list files
fs.readdir(directoryPath, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      return;
    }
  
    // Log the list of file names
    console.log('Files in the directory:');
    files.forEach(pillarName => {
      console.log(pillarName);
      
      const featureList = [];

      const pillarPath = path.join(directoryPath, pillarName);

      fs.readdir(pillarPath, (err, files) => {
        if (err) {
            console.error('Error reading directory:', err);
            return;
        }
        
        // Log the list of file names
        files.forEach(feature => {
            console.log(feature);
            featureList.push(feature);
        });
      });

      var item = {
        pillar: pillarName,
        features: featureList
      };

      pillars.push(item);
    });
});

// Start the server
var http = require('http');

// http.createServer(function (req, res) => fs.readFile("index.html",(error, data)=>{
//   res.writeHead(200, {'Content-Type': 'text/html'});
//   for (let i = 0; i<pillars.length; i++){
//     res.write(String(pillars[i].pillar));
//     res.write(',[');
//     res.write(String(pillars[i].features));
//     res.write(']\n');
//   }
//   res.end()
// })

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  fs.readFile("index.html",(error, data) => {
    res.write(data);
    if (error) {
      res.writeHead(404);
      res.write("Error");
    }
    else {
      res.write(data);
    }
  })
  res.end();
  }
).listen(5500);