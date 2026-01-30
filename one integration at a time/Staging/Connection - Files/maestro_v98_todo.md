# MAESTRO AWAKENING v9.8 — BUILD SPECIFICATION & PROGRESS TRACKER

## CONTEXT REFRESH PROMPT

When resuming this task, use this prompt to restore full context:

```
I am working on Maestro Awakening v9.8, a 30-second cinematic boot sequence for stereOS V2. 
This is a Three.js WebGL particle system (12,000 particles) with Web Audio API synthesis.

KEY FILES:
- Source template: /mnt/user-data/uploads/ai_studio_code_9_.html (v9.4)
- Base64 asset: /mnt/user-data/uploads/maestro_mark_teal.b64 (90,607 chars, 519×339px)
- Progress tracker: /home/claude/maestro_v98_todo.md
- Output target: /mnt/user-data/outputs/maestro_awakening_v9.8.html

CRITICAL DEFECT HISTORY:
- v9.3-v9.6: Base64 truncation → Rectangle blob (10,000 voxels captured)
- v9.7: Color detection too strict → Scattered particles (0 voxels captured)
- v9.8 GOAL: Hybrid approach with procedural SDF fallback → Guaranteed M shape

Please read /home/claude/maestro_v98_todo.md for current progress and next task.
```

---

## PROJECT OVERVIEW

**Objective:** Create a 30-second cinematic boot sequence where 12,000 particles emerge from void, form interference waves, then coalesce into the Maestro "M" brand mark.

**Phase Timeline:**
| Phase | Time | Visual | Audio |
|-------|------|--------|-------|
| VOID | 0-1s | Black screen | Silence |
| AWAKENING | 1-10s | Particles emerge from deep Z | Dm9 chord swell |
| TUNING | 10-16s | Interference wave patterns | Filter opening |
| COALESCING | 16-22s | Smooth convergence to M | Full chord |
| EMERGENCE | 22-26s | M shape locked, breathing | Shimmer active |
| TRANSITION | 26-28s | Diagonal gold sweep | Filter sweep |
| READY | 28-30s | Gold M breathing | Fade out |

---

## TASK REGISTRY

### PRIORITY 1 — BLOCKING ISSUES (Must Fix for M to Form)

#### [P1-01] Hybrid Voxel Generator with Procedural Fallback
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Create dual-path voxel generation: try Base64 first, validate count, fall back to SDF
- **Implementation:**
  ```javascript
  async function loadMarkVoxels() {
      // Try Base64 approach first
      const base64Voxels = await tryBase64Voxels();
      
      // Validate count (must be 1000-6000 for valid M shape)
      if (base64Voxels.length >= 1000 && base64Voxels.length <= 6000) {
          console.log(`Base64 voxels valid: ${base64Voxels.length}`);
          return { points: base64Voxels, bounds: calculateBounds(base64Voxels), source: 'base64' };
      }
      
      // Fallback to procedural SDF
      console.warn(`Base64 invalid (${base64Voxels.length}), using procedural fallback`);
      const proceduralVoxels = generateProceduralM(3500);
      return { points: proceduralVoxels, bounds: calculateBounds(proceduralVoxels), source: 'procedural' };
  }
  ```
- **Acceptance Criteria:** Console shows either "Base64 voxels valid: XXXX" or "using procedural fallback"
- **Completed:** ⬜

#### [P1-02] Relaxed Color Detection with Brightness Threshold
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Replace strict teal detection with brightness-based detection that excludes black background
- **Implementation:**
  ```javascript
  // Detect any non-black pixel (teal mark is bright, background is black)
  const brightness = r + g + b;
  const isNotBlack = brightness > 30;
  const hasTealHue = (g > r) || (b > r); // Teal has higher G/B than R
  
  if (isNotBlack && hasTealHue) {
      v.push({ x, y, z });
  }
  ```
- **Acceptance Criteria:** Voxel count between 2000-5000 when using Base64
- **Completed:** ⬜

#### [P1-03] Dynamic Aspect Ratio Preservation
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Calculate canvas dimensions from actual image aspect ratio to prevent distortion
- **Implementation:**
  ```javascript
  img.onload = () => {
      const aspect = img.width / img.height; // ~1.54 for 100×65
      const sampleWidth = 128; // Power of 2 for WebGL compatibility
      const sampleHeight = Math.round(sampleWidth / aspect);
      
      canvas.width = sampleWidth;
      canvas.height = sampleHeight;
      
      ctx.drawImage(img, 0, 0, sampleWidth, sampleHeight);
      // ... rest of sampling
  };
  ```
- **Acceptance Criteria:** M shape has correct proportions (not squashed)
- **Completed:** ⬜

#### [P1-04] Procedural SDF "M" Generator
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Mathematical definition of M shape using signed distance function
- **Implementation:**
  ```javascript
  function generateProceduralM(targetCount = 3500) {
      const voxels = [];
      const legWidth = 0.45;
      const height = 2.2;
      const width = 2.8;
      
      function isInsideM(x, y) {
          // Left vertical leg
          if (x >= -width - legWidth && x <= -width + legWidth && y >= -height && y <= height) return true;
          // Right vertical leg
          if (x >= width - legWidth && x <= width + legWidth && y >= -height && y <= height) return true;
          // Left diagonal (top-left to center-bottom)
          if (x >= -width && x <= 0 && y >= -0.3) {
              const expectedY = height - (x + width) * (height / width);
              if (Math.abs(y - expectedY) < legWidth * 1.2) return true;
          }
          // Right diagonal (center-bottom to top-right)
          if (x >= 0 && x <= width && y >= -0.3) {
              const expectedY = height - (width - x) * (height / width);
              if (Math.abs(y - expectedY) < legWidth * 1.2) return true;
          }
          return false;
      }
      
      // Rejection sampling
      let attempts = 0;
      while (voxels.length < targetCount && attempts < targetCount * 25) {
          attempts++;
          const x = (Math.random() - 0.5) * 7.5;
          const y = (Math.random() - 0.5) * 5.5;
          if (isInsideM(x, y)) {
              voxels.push({ x, y, z: (Math.random() - 0.5) * 0.4 });
          }
      }
      return voxels;
  }
  ```
- **Acceptance Criteria:** Procedural generator creates recognizable M shape with 3000+ voxels
- **Completed:** ⬜

#### [P1-05] Empty Array Guard in Physics Loop
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Prevent division by zero and fallback to original positions if no voxels
- **Implementation:**
  ```javascript
  // At start of physics loop
  const voxelList = mVoxels.points || [];
  const hasVoxels = voxelList.length > 0;
  
  // In particle iteration
  const voxel = hasVoxels 
      ? voxelList[Math.floor((i / particleCount) * voxelList.length)]
      : { x: origX * 0.1, y: origY * 0.1, z: 0 };
  ```
- **Acceptance Criteria:** No console errors when mVoxels is empty; particles still animate
- **Completed:** ⬜

#### [P1-06] Dynamic Bounds Calculation
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Calculate actual voxel bounds for normalized transition sweep
- **Implementation:**
  ```javascript
  function calculateBounds(voxels) {
      if (voxels.length === 0) return null;
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      voxels.forEach(v => {
          if (v.x < minX) minX = v.x;
          if (v.x > maxX) maxX = v.x;
          if (v.y < minY) minY = v.y;
          if (v.y > maxY) maxY = v.y;
      });
      return { minX, maxX, minY, maxY };
  }
  ```
- **Acceptance Criteria:** Bounds object has valid numeric values for all four properties
- **Completed:** ⬜

---

### PRIORITY 2 — HIGH ISSUES (Should Fix for Stability)

#### [P2-01] RequestAnimationFrame Cancellation
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Store RAF ID and cancel on termination to prevent memory leak
- **Implementation:**
  ```javascript
  let animationFrameId = null;
  
  function animate() {
      if (!isRunning) {
          if (animationFrameId) cancelAnimationFrame(animationFrameId);
          return;
      }
      animationFrameId = requestAnimationFrame(animate);
      // ... rest of loop
  }
  ```
- **Acceptance Criteria:** No console warnings about animation after 30s
- **Completed:** ⬜

#### [P2-02] Audio Node Cleanup with Disconnect
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Track all created audio nodes and properly disconnect on termination
- **Implementation:**
  ```javascript
  let audioNodes = []; // Track all nodes
  
  // When creating: audioNodes.push(node);
  
  function cleanupAudio() {
      audioNodes.forEach(node => {
          try { node.disconnect(); } catch(e) {}
      });
      if (audioContext && audioContext.state !== 'closed') {
          audioContext.close().catch(() => {});
      }
      audioNodes = [];
  }
  ```
- **Acceptance Criteria:** No audio playing or nodes active after termination
- **Completed:** ⬜

#### [P2-03] Three.js Resource Disposal
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Dispose geometry, material, and textures on termination
- **Implementation:**
  ```javascript
  function cleanupThreeJS() {
      geometry.dispose();
      material.dispose();
      renderer.dispose();
  }
  ```
- **Acceptance Criteria:** Memory usage returns to baseline after termination
- **Completed:** ⬜

#### [P2-04] AudioContext Error Handling
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Wrap audio initialization in try-catch with state verification
- **Implementation:**
  ```javascript
  async function initAudio() {
      try {
          audioContext = new (window.AudioContext || window.webkitAudioContext)();
          if (audioContext.state === 'suspended') {
              await audioContext.resume();
          }
          if (audioContext.state !== 'running') {
              throw new Error('AudioContext failed to start');
          }
          // ... rest of setup
      } catch(e) {
          console.error('Audio init failed:', e);
          // Continue without audio
          return false;
      }
      return true;
  }
  ```
- **Acceptance Criteria:** Visual experience works even if audio fails
- **Completed:** ⬜

#### [P2-05] LFO Stop with State Check
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Check oscillator state before calling stop() to prevent errors
- **Implementation:**
  ```javascript
  function safeStopOscillator(osc) {
      try {
          if (osc && osc.context && osc.context.state !== 'closed') {
              osc.stop();
          }
      } catch(e) { /* Already stopped */ }
  }
  ```
- **Acceptance Criteria:** No "InvalidStateError" in console on termination
- **Completed:** ⬜

---

### PRIORITY 3 — MEDIUM ISSUES (Nice to Have)

#### [P3-01] Color Value Clamping
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Ensure all color calculations stay within 0.0-1.0 range
- **Implementation:** Add `Math.min(1.0, value)` to all color assignments
- **Completed:** ⬜

#### [P3-02] Normalized Transition Sweep
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Use calculated bounds for transition sweep instead of magic numbers
- **Implementation:** Replace hardcoded values with `mVoxels.bounds.minX`, etc.
- **Completed:** ⬜

#### [P3-03] Remove Global shimmerGain
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Move shimmerGain to closure scope instead of window
- **Implementation:** `let shimmerGain = null;` at module scope
- **Completed:** ⬜

#### [P3-04] Power-of-2 Sample Resolution
- **Status:** ✅ COMPLETED (Session 1)
- **Description:** Change sampleRes from 100 to 128 for WebGL compatibility
- **Implementation:** `const sampleRes = 128;`
- **Completed:** ⬜

---

### PRIORITY 4 — LOW ISSUES (Polish)

#### [P4-01] Basic ARIA Labels
- **Status:** ⬜ NOT STARTED
- **Completed:** ⬜

#### [P4-02] Keyboard Navigation
- **Status:** ⬜ NOT STARTED
- **Completed:** ⬜

#### [P4-03] Resize Handler Debounce
- **Status:** ⬜ NOT STARTED
- **Completed:** ⬜

#### [P4-04] Mobile Viewport CSS Fix
- **Status:** ⬜ NOT STARTED
- **Completed:** ⬜

---

## EXECUTION LOG

### Session 1: January 2, 2026

**Time Started:** Current session

**Tasks Completed:**
- [x] P1-01: Hybrid Voxel Generator — Implemented dual-path with Base64 + SDF fallback
- [x] P1-02: Relaxed Color Detection — brightness > 30 && (g > r || b > r)
- [x] P1-03: Dynamic Aspect Ratio — canvas.height = sampleRes / aspect
- [x] P1-04: Procedural SDF Generator — Mathematical M with rejection sampling
- [x] P1-05: Empty Array Guard — Safe voxel access with distribution
- [x] P1-06: Dynamic Bounds — calculateBounds() for normalized sweep
- [x] P2-01: RAF Cancellation — animationFrameId tracking
- [x] P2-02: Audio Cleanup — audioNodes[] array with disconnect()
- [x] P2-03: Three.js Disposal — geometry.dispose(), material.dispose()
- [x] P2-04: Audio Error Handling — try-catch with graceful degradation
- [x] P2-05: LFO State Check — safeStopOscillator() helper
- [x] P3-01: Color Value Clamping — Math.min(1.0, value) everywhere
- [x] P3-02: Normalized Transition Sweep — bounds-based u/v calculation
- [x] P3-03: Remove Global shimmerGain — local closure scope
- [x] P3-04: Power-of-2 Sample Resolution — CONFIG.SAMPLE_RESOLUTION = 128

**Build Output:** /mnt/user-data/outputs/maestro_awakening_v9.9.html

**v9.9 Fixes (Color Balance):**
- [x] Reduced COL_TEAL from (0, 0.83, 1.0) to (0, 0.45, 0.55)
- [x] Reduced COL_GOLD from (0.757, 0.608, 0.345) to (0.45, 0.35, 0.15)
- [x] Reduced base particle size from 0.12 to 0.08
- [x] Reduced opacity targets: TRANSITION 1.0→0.7, READY 1.0→0.65
- [x] Shortened white flash from 0.1s to 0.05s
- [x] Dimmed white flash from 1.0 to 0.7

**Validation Results:**
- [ ] Voxel count: _____ (target: 2000-5000) — AWAITING USER TEST
- [ ] M shape visible at t=22s: ⬜ — AWAITING USER TEST
- [ ] Gold transition at t=26s: ⬜ — AWAITING USER TEST
- [ ] Clean termination at t=30s: ⬜ — AWAITING USER TEST
- [ ] No console errors: ⬜ — AWAITING USER TEST

---

## VALIDATION CHECKLIST

### Visual Validation
| Time | Expected | Actual | Pass |
|------|----------|--------|------|
| 0s | Black screen | | ⬜ |
| 5s | Particles emerging from depth | | ⬜ |
| 12s | Wave interference patterns | | ⬜ |
| 18s | Particles converging (no jump) | | ⬜ |
| 24s | M shape visible in teal | | ⬜ |
| 27s | Gold sweep with white flash | | ⬜ |
| 29s | Gold M breathing | | ⬜ |
| 30s | "SEQUENCE COMPLETE" | | ⬜ |

### Audio Validation
| Phase | Expected | Actual | Pass |
|-------|----------|--------|------|
| AWAKENING | Dm9 chord fading in | | ⬜ |
| TUNING | Filter opening, LFO audible | | ⬜ |
| EMERGENCE | Shimmer layer active | | ⬜ |
| READY | Graceful fade out | | ⬜ |

### Console Validation
| Log | Expected | Actual | Pass |
|-----|----------|--------|------|
| Voxel count | 2000-5000 | | ⬜ |
| Voxel source | "base64" or "procedural" | | ⬜ |
| No errors | Zero red messages | | ⬜ |

---

## FILE MANIFEST

| File | Purpose | Location |
|------|---------|----------|
| Source Template | v9.4 base code | /mnt/user-data/uploads/ai_studio_code_9_.html |
| Teal Base64 | Full resolution asset | /mnt/user-data/uploads/maestro_mark_teal.b64 |
| Gold Base64 | Alternative color | /mnt/user-data/uploads/maestro_mark_gold.png |
| This Tracker | Progress & context | /home/claude/maestro_v98_todo.md |
| Final Output | v9.8 build | /mnt/user-data/outputs/maestro_awakening_v9.8.html |

---

## NOTES & OBSERVATIONS

[Space for runtime notes during execution]

