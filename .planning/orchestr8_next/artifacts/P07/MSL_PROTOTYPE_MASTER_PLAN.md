# Code City Prototype Master Plan: Proving the Mechanism

## 1. Vision Statement

A high-fidelity, real-time **Code City** visualization serving as the critical proof of concept for the eventual megacity, **∅明nos**. This settlement proves that code can become space, humans and agents can co-inhabit it, and the environment itself can catalyze emergence.

## 2. Strategic Phases (Long-Run)

### Phase 1: The Obsidian Shell (Waves 4-5) – *Foundation*

- **Objective:** Establish the "Void" aesthetic and layout parity.
- **Key Tasks:**
  - **CSS Token Injection:** Map `MSL-05` HEX codes to `:root` variables in `void.css`.
  - **Spatial Anchor:** Layout the `Deck Row`, `Maestro Bar`, and `Header` per the NEXUS reference.
  - **VFX Baseline:** Implement the constant scanline overlay and the 12k particle background.
- **Lane Responsibility:**
  - `msl`: Design constraint verification.
  - `orchestr8_jr`: CSS/DOM implementation.
  - `a_codex_plan`: `/theme` and `/config` API endpoints.

### Phase 2: The Pulse (Waves 6-7) – *Live Systems*

- **Objective:** Connect the city to live project activity.
- **Key Tasks:**
  - **Citizen Mapping:** Bound agent processes to 3D entities.
  - **Grid Energization:** Visualize `Power Grid` health through glowing transmission lines (Teal vs. Warning Gold).
  - **Tool-Call Bloom:** Visual pulse triggers whenever an agent executes a command.
- **Lane Responsibility:**
  - `a_codex_plan`: Event bus wiring (`CITIZEN_MOVED`, `GRID_OUTAGE`).
  - `orchestr8_jr`: THREE.js material updates and shader transitions.

### Phase 3: The Time Machine (Waves 8-9) – *Observability*

- **Objective:** Enable historical "Time-Machine" navigation.
- **Key Tasks:**
  - **Quantum Slider:** Implement the vertical scrub bar for temporal state.
  - **Epoch Desaturation:** Past states render in desaturated/greyscale palettes (Legacy mode).
  - **Archive Library:** Integrate the virtualized `HistoryPanel` with direct seek-on-click functionality.
- **Lane Responsibility:**
  - `a_codex_plan`: `temporal_state.py` persistence and snapshot retrieval.
  - `2ndFid`: Refined extraction of time-series visualization logic.

### Phase 4: The Singularity (Wave 10+) – *Promotion*

- **Objective:** Final polish for P08 Promotion.
- **Key Tasks:**
  - **Perf Optimization:** Ensure 60FPS fluid motion during rapid script execution.
  - **Parity Audit:** Strict HSL-space matching against the NEXUS reference.
  - **Review Bundle:** Automate the "Founder Review" snapshot of the city state.

## 3. Communication Model

- **Design Constraints:** Owned by `mingos_settlement_lab`.
- **Implementation:** Driven by `a_codex_plan` (Services) and `orchestr8_jr` (Visuals).
- **Provedance:** Every UI element must link to a `P07` event observation.

## 4. Immediate Next Step

1. Refactor `orchestr8_jr`'s CSS to use the centralized `ThemeConfig`.
2. Test the first "Quantum Tick" visual feedback loop.
