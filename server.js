const http = require("node:http");
const fs = require("node:fs/promises");
const path = require("node:path");
const { randomUUID } = require("node:crypto");

const PORT = Number(process.env.PORT || 5000);
const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, "public");
const DB_FILE = path.join(ROOT, "synthetic_db.json");
const MAX_BODY_BYTES = 100_000;
let mutationQueue = Promise.resolve();

function runMutation(task) {
  const result = mutationQueue.then(task);
  mutationQueue = result.catch(() => {});
  return result;
}

const INITIAL_DATA = {
  suppliers: [
    {
      name: "Pak Ali Eggs Enterprise",
      item: "Grade A Eggs (Per Board)",
      cost: 15,
      email: "pakali@supplier.com",
    },
    {
      name: "Marigold Dairy Corp",
      item: "Fresh Milk Box (Per Crate)",
      cost: 45,
      email: "accounts@marigold.com",
    },
    {
      name: "Gombak Veggie WholeSale",
      item: "Fresh Mustard Greens (Per KG)",
      cost: 8.5,
      email: "sales@gombakveggie.com",
    },
  ],
  claims: [],
};

async function readDatabase() {
  try {
    const contents = await fs.readFile(DB_FILE, "utf8");
    const data = JSON.parse(contents);
    if (!Array.isArray(data.suppliers) || !Array.isArray(data.claims)) {
      throw new Error("Database has an invalid structure.");
    }
    return data;
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    await writeDatabase(INITIAL_DATA);
    return structuredClone(INITIAL_DATA);
  }
}

async function writeDatabase(data) {
  const temporaryFile = `${DB_FILE}.${process.pid}.tmp`;
  await fs.writeFile(temporaryFile, JSON.stringify(data, null, 2), "utf8");
  await fs.rename(temporaryFile, DB_FILE);
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  response.end(JSON.stringify(payload));
}

async function readJsonBody(request) {
  let body = "";
  for await (const chunk of request) {
    body += chunk;
    if (Buffer.byteLength(body) > MAX_BODY_BYTES) {
      const error = new Error("Request body is too large.");
      error.statusCode = 413;
      throw error;
    }
  }
  try {
    return JSON.parse(body || "{}");
  } catch {
    const error = new Error("Request body must be valid JSON.");
    error.statusCode = 400;
    throw error;
  }
}

function createClaimLetter(supplier, quantity, notes, loss) {
  return [
    `Dear Accounts Team at ${supplier.name},`,
    "",
    "We are writing to report a delivery discrepancy from a recent order.",
    `Our floor team recorded ${quantity} unit${quantity === 1 ? "" : "s"} of ${supplier.item} as defective.`,
    notes ? `Incident notes: ${notes}` : "",
    "",
    `We request a credit note for RM ${loss.toFixed(2)} to be reviewed against the upcoming invoice settlement.`,
    "",
    "Please confirm receipt and verify this adjustment with your delivery team.",
    "",
    "Best regards,",
    "Manager, Orbyte Retail Hub Network",
  ].join("\n");
}

async function handleApi(request, response, url) {
  if (request.method === "GET" && url.pathname === "/api/bootstrap") {
    const data = await readDatabase();
    return sendJson(response, 200, data);
  }

  if (request.method === "POST" && url.pathname === "/api/claims") {
    const input = await readJsonBody(request);
    const data = await readDatabase();
    const supplier = data.suppliers.find((entry) => entry.name === input.supplier);
    const quantity = Number(input.quantity);
    const notes = typeof input.notes === "string" ? input.notes.trim() : "";

    if (!supplier) {
      return sendJson(response, 400, { error: "Choose a valid supplier." });
    }
    if (!Number.isInteger(quantity) || quantity < 1 || quantity > 100_000) {
      return sendJson(response, 400, { error: "Quantity must be a whole number from 1 to 100,000." });
    }
    if (!notes || notes.length > 5_000) {
      return sendJson(response, 400, { error: "Incident notes must contain 1 to 5,000 characters." });
    }

    const loss = Number((quantity * supplier.cost).toFixed(2));
    const claim = {
      id: randomUUID(),
      supplier: supplier.name,
      item: supplier.item,
      quantity,
      unitCost: supplier.cost,
      loss,
      notes,
      letter: createClaimLetter(supplier, quantity, notes, loss),
      status: "pending_review",
      createdAt: new Date().toISOString(),
    };

    data.claims.unshift(claim);
    await writeDatabase(data);
    return sendJson(response, 201, { claim });
  }

  const authorizeMatch = url.pathname.match(/^\/api\/claims\/([^/]+)\/authorize$/);
  if (request.method === "POST" && authorizeMatch) {
    const claimId = decodeURIComponent(authorizeMatch[1]);
    const input = await readJsonBody(request);
    const authorizedBy = typeof input.authorizedBy === "string" ? input.authorizedBy.trim() : "";
    const finalLetter = typeof input.finalLetter === "string" ? input.finalLetter.trim() : "";

    if (!authorizedBy || authorizedBy.length > 160) {
      return sendJson(response, 400, { error: "Enter the manager's full name (160 characters or fewer)." });
    }
    if (!finalLetter || finalLetter.length > 10_000) {
      return sendJson(response, 400, { error: "The reviewed letter must contain 1 to 10,000 characters." });
    }

    const data = await readDatabase();
    const claim = data.claims.find((entry) => entry.id === claimId);
    if (!claim) return sendJson(response, 404, { error: "Claim not found." });
    if (claim.status !== "pending_review") {
      return sendJson(response, 409, { error: "This claim has already been authorized." });
    }

    claim.status = "authorized_demo";
    claim.authorizedBy = authorizedBy;
    claim.authorizedAt = new Date().toISOString();
    claim.finalLetter = finalLetter;
    await writeDatabase(data);
    return sendJson(response, 200, { claim });
  }

  return sendJson(response, 404, { error: "API route not found." });
}

const CONTENT_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".webp": "image/webp",
};

async function serveStatic(response, pathname) {
  const requestedPath = pathname === "/" ? "/index.html" : pathname;
  const normalizedPath = path.normalize(requestedPath).replace(/^(\.\.[/\\])+/, "");
  const filePath = path.join(PUBLIC_DIR, normalizedPath);
  if (!filePath.startsWith(`${PUBLIC_DIR}${path.sep}`)) {
    response.writeHead(403);
    return response.end("Forbidden");
  }

  try {
    const content = await fs.readFile(filePath);
    response.writeHead(200, {
      "Content-Type": CONTENT_TYPES[path.extname(filePath)] || "application/octet-stream",
      "Cache-Control": "no-cache",
    });
    response.end(content);
  } catch (error) {
    if (error.code === "ENOENT" || error.code === "EISDIR") {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      return response.end("Not found");
    }
    throw error;
  }
}

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url, `http://${request.headers.host || "localhost"}`);
  try {
    if (url.pathname.startsWith("/api/")) {
      if (request.method === "POST") {
        await runMutation(() => handleApi(request, response, url));
      } else {
        await handleApi(request, response, url);
      }
    } else if (request.method === "GET" || request.method === "HEAD") {
      await serveStatic(response, url.pathname);
    } else {
      sendJson(response, 405, { error: "Method not allowed." });
    }
  } catch (error) {
    console.error("Request failed:", error);
    if (!response.headersSent) {
      sendJson(response, error.statusCode || 500, {
        error: error.statusCode ? error.message : "The server could not complete the request.",
      });
    } else {
      response.destroy();
    }
  }
});

readDatabase()
  .then(() => {
    server.listen(PORT, "0.0.0.0", () => {
      console.log(`Orbyte Smart-Defect Tracker listening on port ${PORT}`);
    });
  })
  .catch((error) => {
    console.error("Could not initialize the workspace database:", error);
    process.exitCode = 1;
  });
