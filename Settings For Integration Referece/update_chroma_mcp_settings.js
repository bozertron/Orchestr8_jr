#!/usr/bin/env node
/**
 * Updates the Cline MCP settings to point the 'chroma' server at the wrapper script.
 * - Backs up the entire settings JSON alongside the original file
 * - Writes the previous 'chroma' block into the repo under docs/
 * - Updates the chroma command/args to use the wrapper
 */

const fs = require('node:fs');
const path = require('node:path');

const SETTINGS_PATH = path.join(process.env.HOME, '.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json');
const REPO_ROOT = process.cwd();
const WRAPPER_PATH = path.join(REPO_ROOT, 'scripts', 'chroma_mcp_wrapper.js');
const BACKUP_DIR = path.dirname(SETTINGS_PATH);
const TS = new Date().toISOString().replace(/[:.]/g, '-');

function readJson(p){ return JSON.parse(fs.readFileSync(p, 'utf8')); }
function writeJson(p, obj){ fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n', 'utf8'); }

(function main(){
  if (!fs.existsSync(SETTINGS_PATH)) {
    console.error('Settings file not found:', SETTINGS_PATH);
    process.exit(1);
  }
  if (!fs.existsSync(WRAPPER_PATH)) {
    console.error('Wrapper script not found:', WRAPPER_PATH);
    process.exit(1);
  }
  const settings = readJson(SETTINGS_PATH);
  if (!settings.mcpServers || !settings.mcpServers.chroma) {
    console.error('No mcpServers.chroma entry found in settings');
    process.exit(1);
  }
  const prevChroma = settings.mcpServers.chroma;

  // Backup full settings
  const backupPath = path.join(BACKUP_DIR, `cline_mcp_settings.backup-${TS}.json`);
  writeJson(backupPath, settings);

  // Write previous chroma block into repo docs
  const docsDir = path.join(REPO_ROOT, 'docs');
  try { fs.mkdirSync(docsDir, { recursive: true }); } catch {}
  const prevChromaOut = path.join(docsDir, `chroma_mcp_prev-${TS}.json`);
  writeJson(prevChromaOut, prevChroma);

  // Update chroma to point to wrapper
  const updated = { ...prevChroma };
  updated.command = 'node';
  updated.args = [ WRAPPER_PATH ];
  settings.mcpServers.chroma = updated;

  // Atomic-ish write: write temp then rename
  const tmpPath = SETTINGS_PATH + '.tmp';
  writeJson(tmpPath, settings);
  fs.renameSync(tmpPath, SETTINGS_PATH);

  // Log summary to stdout
  console.log('Updated mcpServers.chroma to use wrapper.');
  console.log('Wrapper path:', WRAPPER_PATH);
  console.log('Settings backup:', backupPath);
  console.log('Previous chroma block saved at:', prevChromaOut);
  console.log('Before -> command:', prevChroma.command, 'args:', JSON.stringify(prevChroma.args));
  console.log('After  -> command:', updated.command, 'args:', JSON.stringify(updated.args));
})();

