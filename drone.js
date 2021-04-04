var arDrone = require('ar-drone');
var http    = require('http');
var fs = require('fs');
console.log('Connecting png stream ...');
var client  = arDrone.createClient();
client.createRepl();
var pngStream = arDrone.createClient().getPngStream();
var lastPng;

var trackNum = 0;
fs.writeFile('run.txt', "Start", function (err) {
  if (err) return console.log(err);
});

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
  pngStream
    .on('error', console.log)
    .on('data', function(pngBuffer) {
      lastPng = pngBuffer;
      fs.readFile('run.txt', 'utf8', function (err,data) {
        if (err) {
          return console.log(err);
        }
        //console.log(data);
        //console.log(lastPng);
      });
      fs.writeFile("pic.png", lastPng, function(err) {
          if (err) throw err;
      });
      console.log(lastPng);
    });


}

/*async function save() {
  fs.writeFile("pic.png", lastPng, function(err) {
      if (err) throw err;
  });
  while (true) {
    client.left(0.1);
    client.after(1000, function() {
      this.stop();
      fs.writeFile("pic.png", lastPng, function(err) {
          if (err) throw err;
      });
    });
    trackNum += 1;
    console.log("Saved image");
    console.log(lastPng);
    console.log(trackNum);
  }
}*/

fs.writeFile('run.txt', "Start", function (err) {
  if (err) return console.log(err);
});
run();
setTimeout(function(){
  console.log("Taking off...");
  client.takeoff();

  client
    .after(100, function() {
      this.stop();
    })
    .after(5000, function() {
      this.left(0.065);
    })
    .after(4000, function() {
      this.stop();
    })
    .after(6000, function() {
      this.stop();
      this.land();
      fs.writeFile('run.txt', "Land", function (err) {
        if (err) return console.log(err);
      });
    });

}, 1000);
