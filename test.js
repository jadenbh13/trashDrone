
const readline = require('readline');
var arDrone = require('ar-drone');

var client  = arDrone.createClient();
client.createRepl();
var yaw;
var inYaw;
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);
keyName = null;

async function run() {
  // everything below is guaranteed to run after the "sleep"
  client.on('navdata', (data)=>{
    yaw = data.demo.rotation.yaw;
    console.log(inYaw);
    console.log(yaw);
    if (inYaw != undefined) {
			var t = inYaw;
			var u = t + 0.3;
			var l = t - 0.3;
			if (yaw > u) {
				client.counterClockwise(0.07);
				console.log("Turn left");
			} else if (yaw < l)  {
				client.clockwise(0.07);
				console.log("Turn right");
			} else {
				console.log("Reached angle");
				client.stop();
			}
    }
  });
  setTimeout(function(){
    inYaw = yaw;
  }, 5000);
}
process.stdin.on('keypress', (str, key) => {
 if (key.ctrl && key.name === 'c') {
   process.exit();
 } else {
  console.log(key.name);

  if(key.name == 't') {
  	client.takeoff();
    client.stop();
    run();
  }

  if(key.name == 'l') {
  	client.land();
  }

  if(key.name == 'w') {
  	client.front(0.1);
	client.after(200, function() {
		this.stop();
	});
  }

  if(key.name == 's') {
  	client.back(0.1);
	client.after(200, function() {
		this.stop();
	});
  }

  if(key.name == 'd') {
  	client.right(0.1);
	client.after(200, function() {
		this.stop();
	});
  }

  if(key.name == 'a') {
  	client.left(0.1);
	client.after(200, function() {
		this.stop();
	});
  }

 }
});
console.log('Initialized');
