var arDrone = require('ar-drone');
var client  = arDrone.createClient();

console.log("Emergency landing...");
client.land();
