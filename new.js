var arDrone = require('ar-drone');
var pngStream = arDrone.createClient().getPngStream();
var client  = arDrone.createClient();
var fs = require('fs');

async function run() {
  pngStream
    .on('error', console.log)
    .on('data', function(pngBuffer) {
      lastPng = pngBuffer;

      fs.writeFile("pic.png", lastPng, function(err) {
          if (err) throw err;
      });
      console.log(lastPng);
    });
}

run();
//client.takeoff();
client.stop();

client
  .after(100000, function() {
    this.stop();
    this.land();
    fs.writeFile("run.txt", "Land", function(err) {
        if (err) throw err;
    });
  });
