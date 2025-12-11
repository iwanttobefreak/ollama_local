import { MCPClient } from "@modelcontextprotocol/client";

const client = new MCPClient({ server: "http://localhost:8080" });

await client.connect();

// Ejemplo: clonar repo
const res = await client.call("git.clone", {
  url: "https://github.com/torvalds/linux",
  path: "/tmp/linux"
});

console.log(res);
