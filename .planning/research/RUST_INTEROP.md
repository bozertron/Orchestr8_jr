# Rust ↔ Python ↔ Marimo Interoperability Research

**Project:** Orchestr8  
**Researched:** 2026-02-13  
**Confidence:** HIGH

## Executive Summary

Rust ↔ Python integration is well-established and production-ready via PyO3, with multiple viable paths for integration with the Orchestr8/Marimo stack. The most practical approaches are:

1. **PyO3 with maturin** — Mature, production-proven (used by Polars, Pydantic, Orjson)
2. **rustimport** — Enables direct Rust file imports from Python with auto-compilation
3. **anywidget** — Marimo's native custom widget system (Rust → browser visualization)

Rerun SDK is a powerful Rust visualization library available to Python, but requires Python ≥3.10 and has large binary sizes (~100-125 MB).

---

## 1. Rust → Python Integration

### 1.1 PyO3 (Recommended)

| Aspect | Details |
|--------|---------|
| **Status** | Production-ready, actively maintained |
| **Python versions** | 3.7+ (CPython, PyPy, GraalPy) |
| **Rust version** | 1.63+ |
| **Build tool** | maturin (recommended), setuptools-rust |
| **Examples** | Polars, Pydantic-core, Orjson, Tiktoken, HuggingFace tokenizers |

**Why PyO3:**
- Industry standard (used by major Python libraries)
- Excellent type conversion support
- Supports both "Rust from Python" and "Python from Rust"
- Well-documented with active community

### 1.2 PyO3 Code Example

```rust
// Cargo.toml
[dependencies.pyo3]
version = "0.22.0"
features = ["extension-module"]

[lib]
crate-type = ["cdylib"]
```

```rust
// src/lib.rs
use pyo3::prelude::*;

#[pyfunction]
fn compute_heavy(x: usize, y: usize) -> PyResult<usize> {
    // Your Rust computation here
    Ok(x * y + (x + y).pow(2))
}

#[pymodule]
fn orchestr8_compute(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compute_heavy, m)?)?;
    Ok(())
}
```

```python
# Python usage
from orchestr8_compute import compute_heavy

result = compute_heavy(10, 20)  # Returns 700
```

### 1.3 maturin Workflow

```bash
# Install maturin
pip install maturin

# Create new project
maturin init --bindings pyo3

# Development (auto-rebuilds on changes)
maturin develop

# Build for distribution
maturin build --release
```

### 1.4 rustimport (Alternative for Prototyping)

**rustimport** allows importing Rust files directly from Python without manual build steps:

```python
import rustimport.import_hook

# This compiles and imports the Rust file automatically
import my_rust_module

result = my_rust_module.square(9)  # Returns 81
```

With Jupyter/marimo support:
```python
%load_ext rustimport

%%rustimport
use pyo3::prelude::*;

#[pyfunction]
fn square(x: i32) -> i32 {
    x * x
}
```

**Pros:**
- Zero build configuration
- Auto-recompilation on source changes
- Good for prototyping

**Cons:**
- Not suitable for production (compilation overhead on import)
- Less control over build process
- Lower adoption than maturin/PyO3

### 1.5 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Function call overhead | ~50-100ns | PyO3 adds minimal overhead |
| GIL considerations | Releases GIL by default | Parallel computation supported |
| Memory | Native Rust memory | Can be more efficient than Python |
| Startup time | ~1-5s for compilation | Cached after first import |

---

## 2. Existing Rust → Visualization Examples

### 2.1 Rerun SDK

| Aspect | Details |
|--------|---------|
| **PyPI** | rerun-sdk 0.29.2 |
| **Python requirement** | ≥3.10 |
| **Binary size** | ~100-125 MB (large) |
| **Build tool** | maturin |
| **Use case** | Robotics/Physical AI visualization |

**Architecture:**
- Rerun is primarily designed for time-series 3D visualization (robotics, sensors)
- Works with Python, Rust, C++ SDKs
- Sends data to Rerun viewer (separate application or embedded)

**Integration with Orchestr8:**
- Can run Rerun viewer as external application
- Could embed Rerun iframe in marimo via HTML component
- Not directly integrated with marimo's reactive model

**Example:**
```python
import rerun as rr

rr.init("orchestr8-viz")
rr.connect()  # Connect to Rerun viewer

# Log 3D data
rr.log("robot/position", rr.Transform3D(translation, rotation))
rr.log("robot/sensor/image", rr.Image(numpy_array))
```

### 2.2 Marimo's anywidget Integration

Marimo supports **anywidget** for custom interactive widgets:

```python
import marimo as mo
import anywidget
import traitlets

class MyWidget(anywidget.AnyWidget):
    # JavaScript/ESM for frontend
    js = """
    export function render({model, el}) {
        el.innerHTML = `<div>Hello from widget!</div>`;
    }
    """
    count = traitlets.Int(default_value=0).tag(sync=True)

widget = mo.ui.anywidget(MyWidget())
```

**Rust → Browser Visualization Options:**

1. **Compile Rust to WASM** → Use anywidget with JavaScript wrapper that calls WASM
2. **Use PyO3 in backend** → Compute in Rust, display via standard marimo outputs
3. **Third-party Rust viz** → Rerun, Plotly, etc. via HTML embedding

---

## 3. WASM Integration

### 3.1 Rust → WASM → Browser

| Approach | Tool | Status |
|----------|------|--------|
| Rust → WASM | `wasm-pack` | Production-ready |
| WASM → Python | Pyodide (limited) | Experimental |

**Rust → WASM workflow:**
```bash
# Install wasm-pack
cargo install wasm-pack

# Build for web
wasm-pack build --target web

# Generates pkg/ with:
# - .wasm binary
# - JavaScript glue code
```

### 3.2 Python ↔ WASM Bridge

**Pyodide** runs Python in the browser via WebAssembly:
- Can load Pyodide with pre-compiled Rust extensions (via wasm-pack)
- Complexity: Requires building Rust → WASM → Pyodide-compatible package
- **Not recommended** for Orchestr8 unless browser-based deployment required

**More practical approach for Orchestr8:**
- Keep Rust computation on server/backend
- Return data to marimo frontend via standard Python→JavaScript communication
- Use anywidget for custom visualizations if needed

### 3.3 Data Transfer Overhead

| Transfer | Overhead |
|----------|----------|
| Python → Rust (PyO3) | ~50-100ns (minimal) |
| Rust → Python → JavaScript | Serialization cost |
| WASM → JavaScript | ~1-10ms (minimal) |
| Python dict → JS via pyodide | ~10-100ms |

---

## 4. Practical Assessment for Orchestr8

### 4.1 Use Cases for Rust Integration

| Use Case | Feasibility | Recommended Approach |
|----------|-------------|----------------------|
| **Heavy computation** (graph analysis, code metrics) | ✅ High | PyO3 + maturin |
| **Real-time visualization** | ⚠️ Medium | Rerun SDK (external viewer) or custom JS |
| **Code City performance** | ⚠️ Medium | PyO3 for graph algorithms, JS for rendering |
| **File parsing** (AST, imports) | ✅ High | PyO3 + maturin |

### 4.2 Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestr8 (marimo)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────┐│
│  │   UI Layer      │    │      Rust Backend (compiled)    ││
│  │  - Code City    │    │  ┌───────────────────────────┐  ││
│  │  - Graphs       │ ←→ │  │ PyO3 Extension Module     │  ││
│  │  - Tables       │    │  │ - Graph algorithms        │  ││
│  └─────────────────┘    │  │ - Code metrics computation │  ││
│         ↑               │  │ - Import graph analysis     │  ││
│         │               │  └──────────────────────────────┘  ││
│  ┌──────┴──────────────┐         ↑                          ││
│  │   Python Layer      │         │ (PyO3 FFI)               ││
│  │  - Data transform   │         │                          ││
│  │  - Orchestration    │         │                          ││
│  └─────────────────────┘         │                          ││
└───────────────────────────────────┼──────────────────────────┘
                                    │
                              [Compiled .so/.pyd]
```

### 4.3 Implementation Workflow

**Phase 1: Backend Computation (Recommended First Step)**
1. Identify computationally expensive operations in Orchestr8
2. Implement in Rust with PyO3 bindings
3. Package with maturin
4. Import and use from marimo cells

**Phase 2: Visualization (If Needed)**
- Use Rerun for external viewer visualization
- Consider anywidget for custom interactive elements
- Keep heavy rendering in JavaScript (Three.js already used)

### 4.4 Existing PyO3 Usage in Orchestr8 Ecosystem

The `one integration at a time/888/` project already demonstrates PyO3 integration:

```python
# From 888/director/adapter.py
def update_context(telemetry_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update the Director's context with new telemetry events.
    Returns Python primitives (following Option B enforcement).
    """
    # Called from Rust via PyO3
```

This pattern shows **Option B enforcement**: Rust calls Python, Python returns primitive types only. This is the recommended approach for clean PyO3 boundaries.

---

## 5. Comparison Matrix

| Criterion | PyO3 + maturin | rustimport | Rerun SDK | Pyodide + WASM |
|-----------|---------------|------------|-----------|----------------|
| **Maturity** | Production | Beta | Production | Experimental |
| **Ease of use** | Medium | Easy | Easy | Hard |
| **Performance** | Excellent | Good | Excellent | Good |
| **Binary size** | Small | Small | Large | Medium |
| **Marimo compatible** | ✅ | ✅ | ⚠️ (external) | ⚠️ (limited) |
| **Best for** | Backend compute | Prototyping | 3D viz | Browser-only |
| **Maintenance** | Active | Active | Active | Community |

---

## 6. Recommendations

### For Orchestr8

1. **Use PyO3 + maturin for computational bottlenecks**
   - Code City graph algorithms
   - Import graph analysis
   - File metrics computation

2. **Skip Rerun SDK unless specific need**
   - Large binary (~100 MB)
   - Requires external viewer
   - Orchestr8's visualization needs already met with Three.js

3. **Avoid Pyodide + WASM for now**
   - Complexity not justified
   - No clear browser-only requirement

4. **Consider anywidget for custom UI**
   - If custom interactive visualizations needed
   - Keep rendering in JavaScript, compute in Rust/Python

### Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| 1 | Identify compute bottlenecks | Low |
| 2 | Create PyO3 module skeleton | Medium |
| 3 | Port specific functions to Rust | Medium |
| 4 | Add anywidget if custom UI needed | High |

---

## 7. Sources

- **PyO3**: [pyo3.rs](https://pyo3.rs/v0.22.0/) — Official documentation (HIGH confidence)
- **maturin**: [github.com/PyO3/maturin](https://github.com/PyO3/maturin) — Build tool (HIGH confidence)
- **rustimport**: [github.com/mityax/rustimport](https://github.com/mityax/rustimport) — Direct import (MEDIUM confidence)
- **Rerun SDK**: [pypi.org/project/rerun-sdk](https://pypi.org/project/rerun-sdk/) — Visualization library (HIGH confidence)
- **Pyodide**: [pyodide.org](https://pyodide.org/) — Python in browser (HIGH confidence)
- **Marimo anywidget**: Internal code analysis — marimo's widget system (HIGH confidence)
