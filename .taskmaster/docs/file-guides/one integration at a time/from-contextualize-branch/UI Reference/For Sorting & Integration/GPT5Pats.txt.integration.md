# GPT5Pats.txt Integration Guide

- Source: `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt`
- Total lines: `127`
- SHA256: `dbf18279a6f6530489e1b8559e1eec448ca2eabd7a5be9d32b96d69e26188859`
- Memory chunks: `2`
- Observation IDs: `502..503`

## Why This Is Painful

- JS/Python bridge risk: event transport and payload validation can silently fail.

## Anchor Lines

- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:65` Your `Particle_Studio2.ts` + `Particle_Studio3.js` strongly suggests you’re heading toward a VS Code Webview setup (you already do `panel.webview.postMessage({ command: 'injectDNA' ... })`).
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:78` if (name === 'rig') viewportPanel?.webview.postMessage(msg);
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:79` else rigPanel?.webview.postMessage(msg);
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:84` viewportPanel = vscode.window.createWebviewPanel('maestroViewport', 'Maestro Viewport', vscode.ViewColumn.One, { enableScripts: true });
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:85` rigPanel = vscode.window.createWebviewPanel('maestroRig', 'Maestro Rig', vscode.ViewColumn.Two, { enableScripts: true });
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/GPT5Pats.txt:125` If you want, I can also refactor this into **two HTML files** (viewport-only + rig-only) with the exact message contract between them — that tends to be the cleanest foundation for VS Code panel detachment.

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
