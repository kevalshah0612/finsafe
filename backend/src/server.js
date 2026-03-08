import { app } from "./app.js";
import { env } from "./config/env.js";

console.log("PORT =", env.port);
console.log("ML_SERVICE_URL =", env.mlServiceUrl);

app.listen(env.port, "0.0.0.0", () => {
  console.log(`FinSafe backend listening on port ${env.port}`);
});
