// audit.js
const os = require("os");
const { exec } = require("child_process");

console.log("🔍 Network Audit Report");

// Interfaces réseau
const interfaces = os.networkInterfaces();
for (let name in interfaces) {
  interfaces[name].forEach((iface) => {
    if (!iface.internal && iface.family === "IPv4") {
      console.log(`- Interface: ${name}`);
      console.log(`  IP Address: ${iface.address}`);
      console.log(`  MAC Address: ${iface.mac}`);
    }
  });
}

// Passerelle par défaut (Unix only)
exec("ip route | grep default", (error, stdout) => {
  if (!error) {
    const match = stdout.match(/default via ([0-9.]+)/);
    if (match) {
      console.log(`- Default Gateway: ${match[1]}`);
    }
  } else {
    console.log("- Could not determine default gateway.");
  }
});
