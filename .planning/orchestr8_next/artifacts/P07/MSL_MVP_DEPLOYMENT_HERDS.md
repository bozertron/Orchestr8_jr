# Code City MVP Deployment — Engineering Herd Strategy

## Canonical Design Source

**All visual tokens derive from [VISUAL_TOKEN_LOCK.md](/home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md)**
This is the final blended state from all references. Changes require Founder approval.

## Five Parallel Herds

### Herd 1: Obsidian Shell (HTML/CSS/JS)

- Pixel-perfect static shell from VISUAL_TOKEN_LOCK tokens
- CSS uses `var(--token-name)` for every value — zero hardcoded hex
- Header, Maestro Bar, Deck Row, scanlines, particles, Void animations
- **Owner:** `mingos_settlement_lab` | **Dependencies:** None

### Herd 2: City Renderer (THREE.js)

- Barradeau-style particle city from topology data
- State colors from token lock: working=#D4AF37, broken=#1fbdea, combat=#9D4EDD
- **Owner:** `a_codex_plan` | **Dependencies:** Herd 4 (can mock)

### Herd 3: Time Machine (Frontend + Backend)

- Quantum slider, epoch desaturation, Archive Library
- Transition tokens: emergence=2s, normal=0.3s
- **Owner:** `orchestr8_jr` | **Dependencies:** Herd 4

### Herd 4: Data API (Python)

- `/map/topology`, `/map/theme`, `/map/temporal`, `/map/citizens`, `/map/grid`
- `/map/theme` serves JSON of VISUAL_TOKEN_LOCK
- **Owner:** `a_codex_plan` | **Dependencies:** Existing services

### Herd 5: Founder Review HUD (Overlay)

- Action inspector, coordination buffer, intent scanner
- **Owner:** `or8_founder_console` | **Dependencies:** Herds 1 + 4

## MSL Immediate Contribution

Build **Herd 1 now** — `void.css` mapping 1:1 to VISUAL_TOKEN_LOCK + the HTML/JS shell.
