#!/usr/bin/env node

import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { URL } from "node:url";

const GATEWAY_HOST = process.env.MEMORY_GATEWAY_HOST || "127.0.0.1";
const GATEWAY_PORT = Number(process.env.MEMORY_GATEWAY_PORT || "37888");
const WORKER_HOST = process.env.CLAUDE_MEM_WORKER_HOST || "127.0.0.1";
const WORKER_PORT = Number(process.env.CLAUDE_MEM_WORKER_PORT || "37777");
const WORKER_BASE_URL = `http://${WORKER_HOST}:${WORKER_PORT}`;
const BODY_LIMIT_BYTES = 1_048_576; // 1MB
const GUIDE_INDEX_PATH =
  process.env.MEMORY_GUIDES_INDEX ||
  path.resolve(process.cwd(), ".taskmaster/docs/file-guides/_SORT_BY_FILENAME.tsv");
const GUIDE_CACHE_TTL_MS = Number(process.env.MEMORY_GUIDES_CACHE_TTL_MS || "5000");

let GUIDE_INDEX_CACHE = {
  loadedAtMs: 0,
  rows: []
};

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization"
  });
  res.end(body);
}

function toSearchParams(data) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(data || {})) {
    if (value === undefined || value === null || value === "") {
      continue;
    }
    if (Array.isArray(value)) {
      for (const entry of value) {
        params.append(key, String(entry));
      }
      continue;
    }
    params.append(key, String(value));
  }
  return params;
}

function clampNumber(value, fallback, min, max) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, Math.floor(parsed)));
}

function toBool(value, fallback = false) {
  if (value === undefined || value === null || value === "") {
    return fallback;
  }
  if (typeof value === "boolean") {
    return value;
  }
  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return false;
  }
  return fallback;
}

function truncateText(text, maxLen = 140) {
  const value = String(text || "").trim();
  if (value.length <= maxLen) {
    return value;
  }
  return `${value.slice(0, Math.max(0, maxLen - 1)).trim()}…`;
}

function parseGuideRow(line) {
  const cols = line.split("\t");
  if (cols.length < 4) {
    return null;
  }
  return {
    basename: cols[0],
    source: cols[1],
    guide_md: cols[2],
    guide_json: cols[3]
  };
}

function resolveLocalPath(maybePath) {
  if (!maybePath) {
    return "";
  }
  if (path.isAbsolute(maybePath)) {
    return maybePath;
  }
  return path.resolve(process.cwd(), maybePath);
}

function readGuideIndexRows() {
  const now = Date.now();
  if (now - GUIDE_INDEX_CACHE.loadedAtMs < GUIDE_CACHE_TTL_MS && GUIDE_INDEX_CACHE.rows.length > 0) {
    return GUIDE_INDEX_CACHE.rows;
  }

  if (!fs.existsSync(GUIDE_INDEX_PATH)) {
    GUIDE_INDEX_CACHE = { loadedAtMs: now, rows: [] };
    return GUIDE_INDEX_CACHE.rows;
  }

  const rows = [];
  const raw = fs.readFileSync(GUIDE_INDEX_PATH, "utf8");
  for (const line of raw.split(/\r?\n/)) {
    if (!line.trim()) {
      continue;
    }
    if (line.startsWith("basename\tsource\tguide_md\tguide_json")) {
      continue;
    }
    const row = parseGuideRow(line);
    if (row) {
      rows.push(row);
    }
  }

  GUIDE_INDEX_CACHE = { loadedAtMs: now, rows };
  return rows;
}

function queryTokens(query) {
  return String(query || "")
    .toLowerCase()
    .split(/[^a-z0-9_./-]+/)
    .filter((token) => token.length > 1);
}

function scoreGuideRow(row, query, tokens) {
  const q = String(query || "").toLowerCase().trim();
  const base = `${row.basename} ${row.source}`.toLowerCase();
  let score = 0;

  if (!q) {
    return score;
  }
  if (base.includes(q)) {
    score += 8;
  }
  if (row.basename.toLowerCase() === q) {
    score += 8;
  }
  for (const token of tokens) {
    if (base.includes(token)) {
      score += 1;
    }
  }
  return score;
}

function searchGuides(query, limit = 8) {
  const rows = readGuideIndexRows();
  const tokens = queryTokens(query);
  const scored = [];

  for (const row of rows) {
    const score = scoreGuideRow(row, query, tokens);
    if (score <= 0) {
      continue;
    }
    scored.push({ ...row, _score: score });
  }

  scored.sort((a, b) => {
    if (b._score !== a._score) {
      return b._score - a._score;
    }
    return a.source.localeCompare(b.source);
  });

  return scored.slice(0, limit);
}

function readJsonFileOrNull(filePath) {
  try {
    const realPath = resolveLocalPath(filePath);
    if (!realPath || !fs.existsSync(realPath)) {
      return null;
    }
    return JSON.parse(fs.readFileSync(realPath, "utf8"));
  } catch {
    return null;
  }
}

function summarizeGuide(row, anchorLimit = 3, riskLimit = 3, obsLimit = 10) {
  const payload = readJsonFileOrNull(row.guide_json) || {};
  const risks = Array.isArray(payload.risks) ? payload.risks.slice(0, riskLimit) : [];
  const anchorsRaw = Array.isArray(payload.anchors) ? payload.anchors : [];
  const anchors = anchorsRaw.slice(0, anchorLimit).map((anchor) => ({
    line: Number(anchor.line || 0),
    text: truncateText(anchor.text || "", 180)
  }));
  const obsRaw = Array.isArray(payload.observation_ids) ? payload.observation_ids : [];
  const observation_ids = obsRaw
    .map((id) => Number(id))
    .filter((id) => Number.isInteger(id) && id > 0)
    .slice(0, obsLimit);

  return {
    basename: row.basename,
    source: row.source,
    guide_md: row.guide_md,
    guide_json: row.guide_json,
    score: row._score || 0,
    total_lines: Number(payload.total_lines || 0),
    sha256: payload.sha256 || null,
    risks,
    anchors,
    observation_ids
  };
}

function extractObservationIdsFromSearchBody(body) {
  const ids = new Set();
  const textCandidates = [];

  if (body && Array.isArray(body.content)) {
    for (const item of body.content) {
      if (item && typeof item.text === "string") {
        textCandidates.push(item.text);
      }
    }
  }
  if (body && typeof body.raw === "string") {
    textCandidates.push(body.raw);
  }
  if (typeof body === "string") {
    textCandidates.push(body);
  }

  for (const text of textCandidates) {
    const hashMatches = text.matchAll(/#(\d+)/g);
    for (const match of hashMatches) {
      ids.add(Number(match[1]));
    }
    const idMatches = text.matchAll(/\bid[:=\s]+(\d+)\b/gi);
    for (const match of idMatches) {
      ids.add(Number(match[1]));
    }
  }

  return [...ids]
    .filter((id) => Number.isInteger(id) && id > 0)
    .sort((a, b) => a - b);
}

function dedupeNumericIds(values, limit = 20) {
  const seen = new Set();
  const out = [];
  for (const raw of values) {
    const id = Number(raw);
    if (!Number.isInteger(id) || id <= 0 || seen.has(id)) {
      continue;
    }
    seen.add(id);
    out.push(id);
    if (out.length >= limit) {
      break;
    }
  }
  return out;
}

function paramsFromUrlSearch(searchParams) {
  const out = {};
  for (const [key, value] of searchParams.entries()) {
    out[key] = value;
  }
  return out;
}

async function buildBrief(params) {
  const query = String(params.q || params.query || "").trim();
  if (!query) {
    return { status: 400, body: { error: "Missing query. Use ?q=... or body.query" } };
  }

  const maxChars = clampNumber(params.budget || params.max_chars, 2400, 400, 12000);
  const fileLimit = clampNumber(params.file_limit, 8, 1, 40);
  const anchorLimit = clampNumber(params.anchor_limit, 3, 1, 12);
  const riskLimit = clampNumber(params.risk_limit, 3, 1, 12);
  const memoryLimit = clampNumber(params.memory_limit, 15, 1, 60);
  const includeMemory = toBool(params.include_memory, true);

  const candidateRows = searchGuides(query, fileLimit * 4);
  const fileSummaries = [];
  let usedChars = 0;

  for (const row of candidateRows) {
    if (fileSummaries.length >= fileLimit) {
      break;
    }
    const summary = summarizeGuide(row, anchorLimit, riskLimit, 12);
    const approx = JSON.stringify(summary).length;
    if (usedChars + approx > maxChars && fileSummaries.length > 0) {
      break;
    }
    usedChars += approx;
    fileSummaries.push(summary);
  }

  const localIds = dedupeNumericIds(fileSummaries.flatMap((item) => item.observation_ids), 50);
  let memoryIds = [];
  let memorySearchStatus = null;

  if (includeMemory) {
    const memoryParams = new URLSearchParams({
      query,
      limit: String(memoryLimit)
    });
    const upstream = await proxyGet("/api/search", memoryParams);
    memorySearchStatus = upstream.status;
    if (upstream.status >= 200 && upstream.status < 300) {
      memoryIds = extractObservationIdsFromSearchBody(upstream.body);
    }
  }

  const recommendedIds = dedupeNumericIds([...localIds, ...memoryIds], 20);

  return {
    status: 200,
    body: {
      query,
      budget: { max_chars: maxChars, used_chars_estimate: usedChars },
      strategy: ["local-sidecars", "memory-index", "fetch-by-id-only"],
      files: fileSummaries,
      memory: {
        local_observation_ids: localIds,
        search_observation_ids: memoryIds,
        recommended_fetch_ids: recommendedIds,
        search_status: memorySearchStatus
      },
      next: {
        fetch_observations: {
          endpoint: "/v1/memory/observations",
          method: "POST",
          body: { ids: recommendedIds.slice(0, 8) }
        }
      }
    }
  };
}

async function buildGraph(params) {
  const query = String(params.q || params.query || "").trim();
  if (!query) {
    return { status: 400, body: { error: "Missing query. Use ?q=... or body.query" } };
  }

  const fileLimit = clampNumber(params.file_limit, 8, 1, 30);
  const anchorLimit = clampNumber(params.anchor_limit, 3, 1, 12);
  const riskLimit = clampNumber(params.risk_limit, 3, 1, 12);
  const memoryLimit = clampNumber(params.memory_limit, 20, 1, 80);
  const maxNodes = clampNumber(params.max_nodes, 240, 20, 1200);
  const maxEdges = clampNumber(params.max_edges, 400, 20, 2400);
  const includeMemory = toBool(params.include_memory, true);

  const rows = searchGuides(query, fileLimit);
  const files = rows.map((row) => summarizeGuide(row, anchorLimit, riskLimit, 20));

  const nodes = [];
  const edges = [];
  const nodeSeen = new Set();

  function addNode(node) {
    if (!nodeSeen.has(node.id) && nodes.length < maxNodes) {
      nodeSeen.add(node.id);
      nodes.push(node);
    }
  }

  function addEdge(edge) {
    if (edges.length < maxEdges) {
      edges.push(edge);
    }
  }

  const queryNodeId = `query:${query}`;
  addNode({ id: queryNodeId, type: "query", label: query });

  for (const file of files) {
    const fileNodeId = `file:${file.source}`;
    addNode({
      id: fileNodeId,
      type: "file",
      label: file.basename,
      source: file.source,
      guide: file.guide_md,
      score: file.score
    });
    addEdge({ source: queryNodeId, target: fileNodeId, type: "matches" });

    for (const risk of file.risks) {
      const riskNodeId = `risk:${file.source}:${risk}`;
      addNode({ id: riskNodeId, type: "risk", label: truncateText(risk, 120) });
      addEdge({ source: fileNodeId, target: riskNodeId, type: "has_risk" });
    }

    for (const anchor of file.anchors) {
      const anchorNodeId = `anchor:${file.source}:${anchor.line}`;
      addNode({
        id: anchorNodeId,
        type: "anchor",
        label: `L${anchor.line}`,
        line: anchor.line,
        text: anchor.text
      });
      addEdge({ source: fileNodeId, target: anchorNodeId, type: "has_anchor" });
    }

    for (const obsId of file.observation_ids.slice(0, 8)) {
      const obsNodeId = `obs:${obsId}`;
      addNode({ id: obsNodeId, type: "observation", label: `#${obsId}` });
      addEdge({ source: fileNodeId, target: obsNodeId, type: "maps_to_observation" });
    }
  }

  if (includeMemory) {
    const upstream = await proxyGet(
      "/api/search",
      new URLSearchParams({ query, limit: String(memoryLimit) })
    );
    if (upstream.status >= 200 && upstream.status < 300) {
      const ids = extractObservationIdsFromSearchBody(upstream.body).slice(0, memoryLimit);
      for (const obsId of ids) {
        const obsNodeId = `obs:${obsId}`;
        addNode({ id: obsNodeId, type: "observation", label: `#${obsId}` });
        addEdge({ source: queryNodeId, target: obsNodeId, type: "search_hit" });
      }
    }
  }

  return {
    status: 200,
    body: {
      query,
      counts: { nodes: nodes.length, edges: edges.length },
      nodes,
      edges,
      meta: {
        guide_index: GUIDE_INDEX_PATH,
        file_limit: fileLimit,
        anchor_limit: anchorLimit,
        risk_limit: riskLimit,
        include_memory: includeMemory
      }
    }
  };
}

async function readJsonBody(req) {
  let body = "";
  for await (const chunk of req) {
    body += chunk;
    if (Buffer.byteLength(body, "utf8") > BODY_LIMIT_BYTES) {
      throw new Error("Request body too large");
    }
  }
  if (!body.trim()) {
    return {};
  }
  return JSON.parse(body);
}

async function parseUpstreamResponse(response) {
  const text = await response.text();
  if (!text) {
    return {};
  }
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

async function proxyGet(path, params) {
  const query = params?.toString();
  const target = query ? `${WORKER_BASE_URL}${path}?${query}` : `${WORKER_BASE_URL}${path}`;
  const response = await fetch(target);
  return {
    status: response.status,
    body: await parseUpstreamResponse(response)
  };
}

async function proxyPost(path, data) {
  const target = `${WORKER_BASE_URL}${path}`;
  const response = await fetch(target, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data || {})
  });
  return {
    status: response.status,
    body: await parseUpstreamResponse(response)
  };
}

function schema() {
  return {
    name: "orchestr8-shared-memory-gateway",
    version: "1.0.0",
    backend: "claude-mem worker",
    workerBaseUrl: WORKER_BASE_URL,
    endpoints: [
      {
        method: "GET",
        path: "/v1/memory/health",
        description: "Gateway + worker health"
      },
      {
        method: "GET|POST",
        path: "/v1/memory/search",
        description: "Memory index search (query, limit, type, project, dateStart/dateEnd)"
      },
      {
        method: "GET|POST",
        path: "/v1/memory/timeline",
        description: "Timeline context retrieval around anchor id or query"
      },
      {
        method: "POST",
        path: "/v1/memory/observations",
        description: "Fetch full observation payloads (ids array)"
      },
      {
        method: "POST",
        path: "/v1/memory/save",
        description: "Save a manual memory"
      },
      {
        method: "GET|POST",
        path: "/v1/memory/brief",
        description: "Budget-capped brief: sidecar shortlist + memory IDs, no full payload blast"
      },
      {
        method: "GET|POST",
        path: "/v1/memory/graph",
        description: "Lightweight relationship graph (query->files->risks/anchors/observation IDs)"
      }
    ]
  };
}

const server = http.createServer(async (req, res) => {
  if (!req.url) {
    sendJson(res, 400, { error: "Bad request: missing URL" });
    return;
  }

  if (req.method === "OPTIONS") {
    sendJson(res, 204, {});
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || `${GATEWAY_HOST}:${GATEWAY_PORT}`}`);
  const method = (req.method || "GET").toUpperCase();

  try {
    if (method === "GET" && url.pathname === "/health") {
      sendJson(res, 200, {
        status: "ok",
        service: "memory-gateway",
        worker: WORKER_BASE_URL
      });
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/schema") {
      sendJson(res, 200, schema());
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/health") {
      const upstream = await proxyGet("/api/health");
      sendJson(res, upstream.status, {
        gateway: { status: "ok", host: GATEWAY_HOST, port: GATEWAY_PORT },
        worker: upstream.body
      });
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/search") {
      const upstream = await proxyGet("/api/search", url.searchParams);
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (method === "POST" && url.pathname === "/v1/memory/search") {
      const body = await readJsonBody(req);
      const upstream = await proxyGet("/api/search", toSearchParams(body));
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/timeline") {
      const upstream = await proxyGet("/api/timeline", url.searchParams);
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (method === "POST" && url.pathname === "/v1/memory/timeline") {
      const body = await readJsonBody(req);
      const upstream = await proxyGet("/api/timeline", toSearchParams(body));
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (method === "POST" && url.pathname === "/v1/memory/observations") {
      const body = await readJsonBody(req);
      const upstream = await proxyPost("/api/observations/batch", body);
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (
      method === "POST" &&
      (url.pathname === "/v1/memory/save" ||
        url.pathname === "/api/memory/save" ||
        url.pathname === "/api/observations/save")
    ) {
      const body = await readJsonBody(req);
      const upstream = await proxyPost("/api/memory/save", body);
      sendJson(res, upstream.status, upstream.body);
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/brief") {
      const result = await buildBrief(paramsFromUrlSearch(url.searchParams));
      sendJson(res, result.status, result.body);
      return;
    }

    if (method === "POST" && url.pathname === "/v1/memory/brief") {
      const body = await readJsonBody(req);
      const result = await buildBrief(body);
      sendJson(res, result.status, result.body);
      return;
    }

    if (method === "GET" && url.pathname === "/v1/memory/graph") {
      const result = await buildGraph(paramsFromUrlSearch(url.searchParams));
      sendJson(res, result.status, result.body);
      return;
    }

    if (method === "POST" && url.pathname === "/v1/memory/graph") {
      const body = await readJsonBody(req);
      const result = await buildGraph(body);
      sendJson(res, result.status, result.body);
      return;
    }

    sendJson(res, 404, { error: "Not found", path: url.pathname, method });
  } catch (error) {
    sendJson(res, 500, {
      error: "Gateway request failed",
      details: error instanceof Error ? error.message : String(error)
    });
  }
});

server.listen(GATEWAY_PORT, GATEWAY_HOST, () => {
  console.log(
    JSON.stringify(
      {
        status: "listening",
        gateway: `http://${GATEWAY_HOST}:${GATEWAY_PORT}`,
        worker: WORKER_BASE_URL
      },
      null,
      2
    )
  );
});

function shutdown(signal) {
  server.close(() => {
    process.stdout.write(`memory-gateway stopped (${signal})\n`);
    process.exit(0);
  });
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
