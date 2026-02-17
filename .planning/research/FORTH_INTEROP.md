# Research: Forth ↔ Python ↔ Marimo Interop

**Project:** Orchestr8 / ∅明nos
**Researched:** 2026-02-13
**Mode:** Feasibility + Ecosystem
**Confidence:** MEDIUM (limited current ecosystem, some packages dated)

## Executive Summary

Forth integration with the Python/Marimo stack is **technically feasible but practically limited**. Several Forth implementations exist for both Python and JavaScript, but most are minimal, dated, or have unusual dependencies. The primary use case in Orchestr8 would likely be educational code visualization or as a sandbox environment - not as a production component.

**Key findings:**
- **Python:** `pyforth` is installable but minimal; `forth` package has strange TensorFlow dependency
- **JavaScript:** `forth` (npm) provides more complete implementation
- **Browser/WASM:** No dedicated Forth→WASM compilers found; would require custom compilation
- **Practical value:** Limited for Orchestr8; best as educational sandbox or novelty code city entity

---

## 1. Forth Implementation Options

### 1.1 Python Implementations

| Implementation | Status | Assessment | Notes |
|---------------|--------|------------|-------|
| **pyforth** | ✅ Available (v1.2.0) | Minimal | Basic stack operations, tokenizer, interpreter. No standard word library. Source is ~200 lines. |
| **forth** | ⚠️ PyPI shows v1.0 | **AVOID** | Requires TensorFlow as dependency - inappropriate for a Forth interpreter. Likely abandoned or malicious. |
| **pForth** | ❌ Not on PyPI | Requires build | Portable Forth - C-based, would need compilation. Not available as Python package. |
| **gForth** | ❌ Not on PyPI | System package | GNU Forth - typically installed via system package manager, not Python-native. |

**Tested: pyforth**
```python
import pyforth
# Available: interpret(), tokenize(), stack, shuffle, source
# Missing: Standard Forth word library (+, -, *, /, etc. not defined)
```

**Verdict:** No production-ready Python Forth implementation available via pip.

### 1.2 JavaScript Implementations

| Implementation | npm Package | Version | Status |
|---------------|-------------|---------|--------|
| **forth** | `forth` | 0.17.0 | Active-ish (2015) - more complete than pyforth |
| **js-forth** | `js-forth` | 0.2.0 | Minimal (2016) - basic implementation |

**forth (npm) details:**
- Dependencies: escodegen, esprima, estraverse (AST tools)
- More complete than pyforth but dated
- Could run in browser via bundler or in Node.js

**Verdict:** JavaScript implementations exist but are dated. Could be integrated into marimo frontend via custom JS cells.

### 1.3 Embedded/Standalone Forth

- **eForth**: Simplified Forth implementation, often used in embedded systems
- **F83**: Historical Forth for IBM PC
- **Retro**: Modern Forth dialect, C-based

These would require custom integration and are not Python-native.

---

## 2. Python Integration

### 2.1 Can Forth Run from Python?

**Yes, technically possible** via:
1. **pyforth** - Python-native (minimal)
2. **Subprocess** - Run gForth as external process
3. **WebAssembly** - Compile Forth to WASM, run via Pyodide or wasmtime

### 2.2 Data Exchange Mechanisms

| Mechanism | Complexity | Notes |
|-----------|------------|-------|
| **Direct import** (pyforth) | Low | Python calls Forth functions directly |
| **Subprocess/pipes** | Medium | Serialize data via stdin/stdout |
| **WASM bridge** | High | Requires WASM runtime in Python |

**pyforth example:**
```python
import pyforth
# Limited - no standard words defined
result = pyforth.interpret('5 3 +')  # Fails - '+' not defined
```

### 2.3 Performance Characteristics

- **pyforth**: Pure Python - slow for any non-trivial computation
- **gForth (subprocess)**: Native speed but IPC overhead
- **WASM**: Near-native speed, requires additional runtime

---

## 3. Browser/WASM Options

### 3.1 Forth → WASM

**No dedicated Forth→WASM compilers found.**

Possibilities:
1. **Compile gForth to WASM** - Non-trivial, requires Emscripten toolchain
2. **Retro Forth with WASM target** - Would need custom build
3. **Use JavaScript Forth in browser** - Most practical approach

### 3.2 JavaScript in Marimo

Marimo supports custom JavaScript via:
- `mo.ui.html()` - Embed arbitrary HTML/JS
- Custom output transforms

**Could integrate `forth` npm package via:**
```python
mo.ui.html("""
<script src="https://unpkg.com/forth"></script>
<script>
  // Use forth here
</script>
""")
```

**Verdict:** Browser integration is possible but requires custom JS bridging - not seamless.

---

## 4. Practical Assessment for Orchestr8

### 4.1 Would Forth Be Useful?

**Honest assessment: Probably not.**

Forth's strengths (tiny footprint, interactive, direct hardware access) don't align with:
- Orchestr8's visualization-focused architecture
- Python/NetworkX data pipeline
- Marimo's reactive model

### 4.2 Potential Use Cases (If Pursued)

| Use Case | Value | Complexity |
|----------|-------|------------|
| **Code City entity** | Novelty/educational | Low - just display a Forth file |
| **Sandbox playground** | Educational | Medium - needs JS integration |
| **Code generation tool** | Low - Python is better | High |
| **Plugin scripting** | Low - marimo has Python | N/A |

### 4.3 What Would Make It Practical?

1. **Better Python library** - Current options are minimal
2. **WASM runtime** - Native-speed Forth in browser
3. **Clear use case** - Would need defined purpose beyond novelty

---

## 5. Alternatives Considered

If the goal is **scriptable extensions** in Orchestr8:

| Alternative | Python Native | Browser | Ecosystem |
|-------------|---------------|---------||-----------|
| **Lua** | ✅ via lupa | ✅ via Fengari | Active |
| **JavaScript** | ✅ via QuickJS | ✅ Native | Very active |
| **Python (subset)** | ✅ Native | ✅ via Pyodide | Excellent |
| **Forth** | ⚠️ Minimal | ⚠️ Dated | Limited |

**Recommendation:** If scripting is needed, JavaScript (via Pyodide or QuickJS) or Python itself would be more practical than Forth.

---

## 6. Research Summary

| Question | Answer | Confidence |
|----------|--------|------------|
| Forth implementations for Python? | pyforth (minimal), forth (avoid) | HIGH |
| gForth/pForth available? | Not via pip; pForth exists but C-based | HIGH |
| Forth from Python? | Yes via pyforth or subprocess | HIGH |
| Forth → WASM? | No dedicated tools found | MEDIUM |
| JavaScript Forth? | Yes (`forth` npm, `js-forth`) | HIGH |
| Practical for Orchestr8? | Limited value | MEDIUM |

---

## 7. Files Created

| File | Purpose |
|------|---------|
| `.planning/research/FORTH_INTEROP.md` | This comprehensive assessment |

---

## 8. Recommendation

**Do not pursue Forth integration for Orchestr8.** 

The ecosystem is too limited, implementations are dated, and there's no clear practical benefit. If the interest is in:
- **Scripting**: Use Python directly or QuickJS
- **Educational visualization**: Consider displaying Forth code in Code City without execution
- **Novelty**: Could add a "Forth" entity type to Code City as a curiosity, but not execute it

The research confirms Forth is an interesting historical language but impractical for modern integration with the marimo/Python stack.
