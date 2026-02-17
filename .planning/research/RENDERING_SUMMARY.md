# Rendering Tradeoffs: Executive Summary

**Research Complete: 2026-02-13**
**Confidence: HIGH**

---

## The Verdict

### For 3D Code City (Buildings + Particles): ✅ KEEP

The custom WebGPU/Three.js canvas is **justified**. No native alternative exists.

| What You Lose | What You Gain |
|---------------|---------------|
| If you switch to native marimo | ❌ Everything — can't do 3D |
| If you switch to anywidget | Better Python integration, simpler state, smaller payloads |
| If you keep current | Working implementation, full control, proven at scale |

**The emergence animation is your signature.** It cannot be replicated with native tools.

---

### For Wiring Diagram (2D Edges): ⚠️ OVERKILL

The current implementation renders 2D import relationships as 3D lines with custom shaders. This is over-engineered.

| Alternative | Capability | Code Reduction |
|-------------|------------|----------------|
| **Pyvis** | Interactive 2D graph | ~80% less code |
| **D3 via anywidget** | 2D/2.5D force-directed | ~60% less code |
| Current Three.js | 3D lines | Baseline (overkill) |

**Recommendation:** Create a separate 2D wiring view using Pyvis.

---

## The Numbers

| Metric | Current Implementation |
|--------|------------------------|
| Particle cap | 1M GPU / 180K CPU |
| Frame spawn rate | 280-700/frame |
| Stream bandwidth | 5MB/sec default |
| Render approach | WebGPU + CPU fallback |

**Is it worth the 18 hours of debugging? For 3D Code City: YES.**

---

## Strategic Question Answered

> "How much worse is it for not a whole lot new money?"

**Answer:** 

- **For 3D Code City:** You're not losing anything meaningful. There's no cheaper path that gives you what you have.

- **For wiring diagram:** You're overpaying significantly. Pyvis could give you 90% functionality at 20% the complexity.

- **For future anywidget migration:** It would simplify Python integration but requires rewrite. Not worth it unless you're hitting pain points.

---

## Files Created

| File | Purpose |
|------|---------|
| `.planning/research/RENDERING_TRADEOFFS.md` | Full analysis |
| `.planning/research/MARIMO_VISUALIZATION_LIMITS.md` | Marimo limits |
| `.planning/research/ANYWIDGET_CAPABILITIES.md` | anywidget analysis |

---

## Recommended Next Steps

1. **Keep** the 3D Code City implementation as-is
2. **Consider** Pyvis for a simplified wiring diagram view (low effort, high return)
3. **Don't migrate** to anywidget unless you hit integration pain points

The custom canvas is worth it. The question was whether you could simplify — and for the 3D parts, you can't.
