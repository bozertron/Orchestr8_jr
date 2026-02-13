# VOID_SPEC_ROADMAP_v1.1.md Integration Guide

- Source: `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md`
- Total lines: `543`
- SHA256: `2bcc56adb92fc00029266a97769922040cadff55d4501742ee8d5aa184462f62`
- Memory chunks: `7`
- Observation IDs: `109..115`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.
- State pipeline coupling: root state keys and health flow ordering must stay aligned.
- Visual canon risk: color/motion contract regressions are easy to introduce.
- Behavioral sequencing risk: mode transitions need explicit state machine handling.

## Anchor Lines

- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:21` **This is the razor's edge:** The same visualization must be beautiful enough for humans to *want* to use it, while being data-dense enough for LLMs to extract actionable information.
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:220` 4. **Color edge** → Based on connection health (both endpoints must be gold for gold edge)
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:238` - **Gold padlock icon** appears at EACH connection point on the panel
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:250` | **Pan/zoom the void** | Navigate between fiefdoms |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:257` ### 4.2 The Sitting Room
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:294` | Implement three-color system | 🔄 In Progress | Gold/Purple/Blue only |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:328` | Color connections by health | ⬜ | Gold/Purple/Blue per connection |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:329` | Padlock indicator for locked files | ⬜ | Gold block icon |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:367` ### Phase 4: The Sitting Room
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:391` | Void navigation (pan/zoom) | ⬜ | Camera controls |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:405` | Reflect agent deployment visually | ⬜ | Purple = agent working |
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:461` │   └── HealthChecker.ts         # Determine gold/purple/blue
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:467` └── ColorSystem.ts           # Three-state color management
- `one integration at a time/from-contextualize-branch/SOT/VOID_SPEC_ROADMAP_v1.1.md:524` 3. **Developer clicks into Sitting Room** → Understands exactly what they're editing and what it touches

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
