# CLAUDE_EXECUTION_PROMPT.md Integration Guide

- Source: `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md`
- Total lines: `943`
- SHA256: `22eb7725099fd681fcc577fe5c1838233549fdeec297edcfa8d5e922461f119c`
- Memory chunks: `8`
- Observation IDs: `407..414`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:12` Build "Orchestr8" - a VS Code fork with a 3D "Code City" overlay that visualizes the codebase as an abstract cityscape. Gold buildings = working code, Blue = broken, Purple = active debugging. LLM "Generals" are assigned to neighborhoods (directories) to fix problems.
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:28` git clone https://github.com/microsoft/vscode.git orchestr8-editor
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:29` cd orchestr8-editor
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:57` "applicationName": "orchestr8",
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:58` "dataFolderName": ".orchestr8",
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:60` "darwinBundleIdentifier": "com.epoinc.orchestr8",
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:62` "licenseUrl": "https://github.com/yourusername/orchestr8/blob/main/LICENSE",
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:64` "reportIssueUrl": "https://github.com/yourusername/orchestr8/issues",
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:65` "urlProtocol": "orchestr8"
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:88` src/vs/workbench/contrib/orchestr8/
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:90` │   ├── orchestr8.contribution.ts    # Register the contribution
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:97` │   └── orchestr8.ts                 # Shared types
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:116` // src/vs/workbench/contrib/orchestr8/browser/codeCityRenderer.ts
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:123` working: 0xD4AF37,  // Gold
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:125` combat: 0x9D4EDD,   // Purple
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:425` // src/vs/workbench/contrib/orchestr8/node/codeAnalyzer.ts
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:456` if (this.shouldSkip(entry.name)) continue;
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:467` private shouldSkip(name: string): boolean {
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:546` **KENNEY ASSETS (Gold Standard - CC0 License, glTF format):**
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:637` │  [SYSTEM]       [JFDI]        [Projects]      [Waves/Settings]  │  ← Top Bar
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:645` │         Gold = Working    Blue = Broken                   │ I │
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:646` │                Purple = Combat                            │ C │
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:655` maestro toggle
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:691` **maestro Toggle:**
- `one integration at a time/docs/CLAUDE_EXECUTION_PROMPT.md:830` Already implemented at: `orchestr8_mcp.py`

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
