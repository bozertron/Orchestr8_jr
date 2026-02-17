# Orchestr8 Stylized Components Extraction PRD

Date: 2026-02-13  
Status: Draft (decision-gated)  
Owner: Founder + implementation agent

## 1. Objective

Ship a style-only extraction wave for Orchestr8 that:

1. Locks visual quality and compatibility before adding new wiring.
2. Preserves the current Orchestr8 UI architecture and placement model.
3. Imports only stylized component patterns from MaestroView references.
4. Adds desired deco-like font options into Settings from local `Font/`.

## 2. Locked Execution Order

1. Visual contract pass:
   - colors, typography, spacing, emergence behavior.
2. Browser compatibility pass:
   - CSS syntax validity, unsupported features, 3D/runtime compatibility checks.
3. Responsive pass:
   - desktop and mobile-safe layout behavior.
4. Pattern extraction pass:
   - style motifs, button rhythm, and component-level aesthetics only.
5. Implementation pass:
   - apply style-only updates with no macro layout changes.

## 3. Canonical Constraints

1. Entry/runtime:
   - `orchestr8.py -> IP/plugins/06_maestro.py -> IP/woven_maps.py`
2. Color system:
   - working `#D4AF37`
   - broken `#1fbdea`
   - combat `#9D4EDD`
3. Motion:
   - emergence-only, no breathing/pulsing.
4. Top row canon:
   - `[orchestr8] [collabor8] [JFDI]`
5. Interaction rule:
   - marimo button callbacks use `on_click`.
6. Layout preservation rule:
   - keep current placement model ("where everything goes") while refining style and compatibility.
7. Style-reference lock:
   - use `one integration at a time/UI Reference/MaestroView.vue` as the primary visual/layout reference for control styling and lower-fifth button rhythm.
   - preserve the settled regal palette and no-breathing motion rules.
8. Lower-fifth invariants:
   - do not change the macro surface geometry or width usage.
   - evaluate only relative symmetry and button-layout rhythm.
   - no resizing of the control surface concept itself.

## 4. Product Direction (Founder Inputs to Preserve)

1. Art direction:
   - Art-deco flare in visual language.
   - Low-res, high-style overlays where intentional.
2. Documentation experience:
   - Replace bland “wall-poster” docs with “arcade + zine” style delivery surfaces.
   - “City Hall” remains structured info anchor; “Arcade” becomes full-experience guidance layer.
   - City Hall serious lanes:
     - banking node (money)
     - safety node (legal/accounting)
     - subscriptions node ("love" renewals)
   - Arcade:
     - full-depth "whole enchilada" onboarding, playful interactive docs, and zine-style explainers.
3. Interaction concepts:
   - Low-expectation gesture interface (within reason) for high-level navigation and simple media control.
   - Particle presence system: stylized likeness/persona rendered using canonical system colors.
4. Near-future hardware prep:
   - Architectural readiness for mmWave radar based “particle cam” integration.
5. Signature moments:
   - Overview-to-dive Code City camera experience as marquee differentiator.
   - Playable arcade layer to separate tools by place and function.
6. Theme fidelity:
   - follow MaestroView design theme details, including pronounced art-deco-future cues visible in the terminal app style language.
7. Font direction:
   - preferred font aesthetic is deco-like (matching MaestroView/stereOS tone).
   - include local font assets in `/home/bozertron/Orchestr8_jr/Font` as selectable Settings options.
8. External settings reference:
   - identify the settings file referenced by `MaestroView.vue` and prepare for optional import from stereOS project.

## 5. Scope by Wave

### Wave A: Pattern Extraction + Compatibility (No New Wiring)

Deliverables:

1. Color and typography normalization across active UI surfaces.
2. CSS/browser compatibility audit with source-level fixes.
3. 3D frontend compatibility checklist for `IP/static/woven_maps_3d.js`.
4. Responsive layout pass for top row, VOID center, bottom control surface, right-side panels.
5. MaestroView theme pass:
   - import button styling/layout cues from `MaestroView.vue` where compatible with current Orchestr8 placement.
   - prioritize lower-fifth control surface rhythm and terminal-adjacent visual treatment.
   - keep existing color palette and macro-layout placement unchanged.
6. Font option extraction:
   - define local font registration from `Font/`.
   - expose selected fonts as options in Settings UI (no default flip until reviewed).

Acceptance:

1. No parser-breaking CSS warnings from project-owned styles.
2. Canon colors consistently visible across key panels and controls.
3. Layout remains functional across desktop and narrow viewport.
4. Existing controls do not regress.
5. Theme match is visibly aligned with MaestroView references without violating Orchestr8 canon locks.
6. Lower-fifth preserves existing full-width behavior while improving internal symmetry/rhythm.
7. Added font options are selectable in Settings and safely fallback when unavailable.

### Wave B: Style Application (Still No New Wiring)

Deliverables:

1. Apply extracted component style patterns to active Orchestr8 components.
2. Apply lower-fifth symmetry/rhythm refinements without changing macro placement.
3. Keep current regal color palette and emergence behavior unchanged.
4. Keep existing "where everything goes" layout model unchanged.

Acceptance:

1. Styled components read as intentional and art-deco-future without layout regression.
2. Lower-fifth button arrangement feels balanced while preserving current surface model.
3. No major visual regressions in existing panels/views.

### Wave C: Deferred Wiring + Test Drive (Out of Scope for this PRD)

Deliverables:

1. Wiring is explicitly deferred to the next PRD wave.
2. This PRD stops at style extraction/application and compatibility/responsive readiness.
3. Test-drive here is visual and compatibility validation only.

Acceptance:

1. No functional behavior regressions introduced by styling changes.
2. Runtime remains stable under normal visual interaction flow.
3. Wiring backlog remains untouched for follow-on execution.

## 6. Outstanding Backlog to Carry Forward (From `SOT/todo.md`)

Priority carry-ins:

1. Camera + navigation contract:
   - overview lock, warp-dive, round-trip context, keyframes.
2. Error signal behavior:
   - broken-node pollution particles, interaction contract.
3. Boundaries/contracts:
   - neighborhood overlays, crossing badges, lock indicators.
4. Ingestion semantics:
   - settlement survey adapter, status precedence lock.
5. Effects math:
   - short-edge layering, curl noise, wave interference, phase machine.
6. Audio mapping:
   - deterministic band mapping + optional BPM clock.
7. Interaction surface:
   - neighborhood detail card, directional panel emergence, action strip.
8. Broken-node flow:
   - structured ticket payload generation + lock-aware deploy handoff.
9. A/V/Text quality roadmap item (next PRD):
   - perfect the communication stack before final physical integration decisions.

## 7. Critical Decisions Needed

1. Art-deco system:
   - how far to push stylization in primary flow vs themed surfaces.
2. Font default decision:
   - which new deco-like font becomes default vs optional.
3. StereOS settings import:
   - which referenced settings file to import and how to map it safely.
4. Gesture scope:
   - minimum viable gesture set for reliability.
5. Particle presence fidelity:
   - symbolic persona vs pseudo-avatar motion complexity.
6. Arcade architecture:
   - in-VOID native layer vs routed feature districts.
7. Hardware-prep boundary:
   - interfaces to lock now for mmWave particle-cam future.

## 8. Non-Goals (for this PRD wave)

1. Full mmWave integration implementation.
2. Exhaustive mobile-first redesign of all legacy plugin screens.
3. Any macro control-surface layout resize/reposition work.
4. Massive new feature wiring before compatibility and visual contract are complete.

## 9. Exit Criteria

1. Visual and compatibility baseline is production-safe.
2. Stylized components match MaestroView-derived theme cues without changing current Orchestr8 placement.
3. Lower-fifth symmetry/rhythm is improved while surface geometry remains intact.
4. Font options from `Font/` are exposed in Settings and validated for fallback safety.
5. A follow-on PRD explicitly handles wiring and A/V/Text perfection work.
