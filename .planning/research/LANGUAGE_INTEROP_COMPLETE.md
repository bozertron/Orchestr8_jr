# Other Languages ↔ Python ↔ Marimo Interoperability Research

**Project:** Orchestr8 / ∅明nos
**Researched:** 2026-02-13
**Mode:** Ecosystem Survey + Feasibility Assessment
**Confidence:** MEDIUM-HIGH (well-documented technologies, some emerging options)

---

## Executive Summary

This research surveys language interoperability options beyond Rust and Forth for the Python/Marimo stack. The goal is identifying practical integration paths for Orchestr8 across three use cases: **high-performance computation**, **DSL/scripting for users**, and **code analysis/parsing**.

### Key Findings

| Category | Best Option | Feasibility | Notes |
|----------|-------------|-------------|-------|
| **High-Perf Compute** | **PyO3 (Rust)** | ✅ HIGH | Already covered in RUST_INTEROP.md |
| **C/C++ Extensions** | **pybind11** | ✅ HIGH | Industry standard, excellent docs |
| **Go Integration** | **gopy** | ⚠️ MEDIUM | Active but complex setup |
| **Zig Integration** | **ziglang (PyPI)** | ⚠️ MEDIUM | Toolchain wrapper, not bindings |
| **WASM → Python** | **Pyodide** | ✅ HIGH | Python in browser via WASM |
| **JVM → Python** | **JPype** | ✅ HIGH | Mature, production-ready |
| **Kotlin/Scala** | **GraalVM** | ⚠️ MEDIUM | Complex, powerful |
| **Functional Langs** | **Not recommended** | ❌ LOW | Limited bindings, high complexity |

### Recommendation for Orchestr8

For Orchestr8's three target use cases:

1. **High-Performance Computation:** Use **PyO3 (Rust)** — already researched, production-proven
2. **Code Analysis/Parsing:** Use **pybind11 with C/C++** — mature ecosystem, excellent parsers exist
3. **DSL/Scripting:** Use **Python directly** or **Pyodide for sandboxed execution**

Avoid: Go, Zig, JVM languages, and functional languages — all add complexity without clear benefit for Orchestr8.

---

## 1. C/C++ Integration Options

### 1.1 Comparison: Cython vs pybind11

| Criterion | Cython | pybind11 | Winner |
|-----------|--------|----------|--------|
| **Primary purpose** | Compile Python-like syntax to C | Bind existing C++ to Python | Different |
| **Ease of use** | Easy (Python-like syntax) | Medium (requires C++) | Cython |
| **Performance** | Good | Excellent | pybind11 |
| **Type safety** | Partial | Full C++ type safety | pybind11 |
| **Documentation** | Good | Excellent | pybind11 |
| **Maintenance** | Active | Very Active | pybind11 |
| **Binary size** | Larger | Smaller | pybind11 |

### 1.2 pybind11 (Recommended)

**Status:** Production-ready, actively maintained (v3.x)

**Why pybind11:**
- Header-only library (~4K lines)
- Supports CPython 3.8+, PyPy, GraalPy
- Excellent type conversion (STL, Eigen, NumPy)
- Used by major projects: PyRosetta, scientific computing libraries

**Install:**
```bash
pip install pybind11
```

**Minimal Example:**
```cpp
// math.cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(math, m) {
    m.def("add", &add, "Add two integers");
}
```

**Compile:**
```bash
c++ -O3 -Wall -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) math.cpp -o math$(python3-config --extension-suffix)
```

**Key Features:**
- Automatic type conversions
- Exception handling
- NumPy array support
- Smart pointers (shared_ptr, unique_ptr)
- Virtual methods overridable in Python

### 1.3 Cython

**Status:** Production-ready (v3.x)

**Use Cython when:**
- Converting Python-like code to C for performance
- Need to gradually port Python to C
- Writing new extension modules from scratch

**Use pybind11 when:**
- Binding existing C++ code
- Need full C++ type safety
- Performance is critical

### 1.4 Assessment for Orchestr8

| Use Case | Recommendation | Confidence |
|----------|---------------|------------|
| Code parsing/AST | C++ via pybind11 | HIGH |
| Graph algorithms | Rust via PyO3 (better) | HIGH |
| Performance-critical paths | Either | HIGH |

**Verdict:** For code analysis, C++ libraries (like Clang for C/C++, tree-sitter bindings) are available. pybind11 provides the best integration path.

---

## 2. Go Integration (gopy)

### 2.1 gopy Overview

**Status:** Active development (2.3k stars, 130 forks)
**Last release:** v0.4.8 (Dec 2023)

gopy generates CPython extension modules from Go packages.

**Install:**
```bash
go install github.com/go-python/gopy@latest
pip install pybindgen
```

**Workflow:**
```bash
gopy build -output=mygo -vm=python3 github.com/user/mypackage
```

### 2.2 Limitations

| Issue | Severity | Notes |
|-------|----------|-------|
| **Python version matching** | HIGH | Must specify correct `-vm=python3` |
| **Go runtime required** | HIGH | Adds dependency |
| **Complex types** | MEDIUM | Not all Go types map cleanly |
| **Windows support** | MEDIUM | Improved but still tricky |
| **Maintenance** | MEDIUM | Singlemaintainer, community-driven |

### 2.3 Assessment for Orchestr8

**Practical value:** LOW-MEDIUM

Go is excellent for concurrent services, but:
- Python ecosystem already has excellent libraries (NetworkX, pandas)
- Go bindings add deployment complexity
- No clear advantage for Orchestr8's use cases

**Verdict:** Not recommended for Orchestr8. Python/Rust cover the use cases.

---

## 3. Zig Integration

### 3.1 ziglang Python Package

**Status:** Active (v0.15.2, Nov 2025)

The `ziglang` PyPI package doesn't provide Zig → Python bindings. Instead, it redistributes the Zig toolchain for use as a C/C++ compiler.

**Install:**
```bash
pip install ziglang
```

**Use case:** Building C/C++ extensions with Zig as a drop-in compiler replacement.

### 3.2 Zig → Python Bindings

**Current state:** EXPERIMENTAL / EMERGING

No mature Zig-to-Python binding library equivalent to pybind11 exists. Options:

1. **Zig → C → pybind11** — Compile Zig to C, then bind with pybind11
2. **Zig → WASM → Pyodide** — Compile to WebAssembly
3. **ziglang stdlib** — Use Zig as build tool only

### 3.3 Assessment for Orchestr8

**Practical value:** LOW

Zig is exciting for systems programming but:
- No mature Python bindings ecosystem
- Still pre-1.0 (v0.15.x)
- Add complexity without clear benefit

**Verdict:** Not recommended for Orchestr8. Use Rust (PyO3) instead for systems-level code.

---

## 4. WASM-Based Options

### 4.1 Pyodide (Python in Browser via WASM)

**Status:** Production-ready (v0.29.x)
**Documentation:** https://pyodide.org/

Pyodide is a Python distribution compiled to WebAssembly that runs in the browser or Node.js.

**Key capabilities:**
- Pure Python packages from PyPI work
- Many C/C++/Rust extensions also ported (NumPy, pandas, SciPy, matplotlib)
- JavaScript ↔ Python FFI with full error handling

**Use cases for Orchestr8:**
- Sandboxed code execution in browser
- Client-side computation
- Offline-capable Python

**Limitations:**
- Large download (~20MB initial)
- No native file system access
- Some packages not yet compatible

### 4.2 Other WASM Languages → Python

| Language | WASM Target | Python Integration | Notes |
|----------|-------------|-------------------|-------|
| **Rust** | ✅ wasm-pack | Via Pyodide (complex) | Not practical |
| **C/C++** | ✅ Emscripten | Via Pyodide | Limited |
| **Go** | ✅ tinygo | Not available | WASM-only |

### 4.3 Data Flow: WASM → Python → Marimo

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  WASM       │     │  Python      │     │  Marimo         │
│  (Rust/C/Go)│────→│  (Pyodide)   │────→│  (Frontend)    │
└─────────────┘     └──────────────┘     └─────────────────┘
     ↓                    ↓                      ↓
  Compute            Serialize results        Display via
  results            via pyodide.ffi         mo.ui.html()
```

**Example (Pyodide):**
```python
import pyodide

# Load Pyodide in browser
pyodide.loadPackage("numpy")
import numpy as np

# Use JavaScript APIs from Python
js_result = js.some_wasm_function()
```

### 4.4 Assessment for Orchestr8

| Use Case | Recommendation | Confidence |
|----------|---------------|------------|
| Sandboxed execution | Pyodide | HIGH |
| Client-side compute | Not needed | — |
| Browser-only deployment | Pyodide | MEDIUM |

**Verdict:** Pyodide could enable sandboxed DSL execution in browser, but not required for current architecture. Keep as future option.

---

## 5. JVM Languages (Java/Kotlin/Scala)

### 5.1 JPype (Java → Python)

**Status:** Production-ready (v1.6.x)
**Documentation:** https://jpype.readthedocs.io/

JPype enables Python programs to access Java libraries.

**Install:**
```bash
pip install JPype1
```

**Example:**
```python
import jpype

# Start JVM
jpype.startJVM()

# Import Java classes
from java.util import Random
random = Random()
random.nextInt(10)

# Call Python from Java (via JPype)
```

**Use cases:**
- Use Java libraries from Python
- Integrate with Java enterprise systems
- Access JVM-only libraries

**Limitations:**
- Requires Java runtime
- Not trivial to package
- Performance overhead of JVM

### 5.2 py4j (Java ↔ Python)

**Status:** Active (v0.10.9.x, maintained since 2009)
**Documentation:** https://www.py4j.org/

py4j enables Python programs to access Java objects in a JVM.

**Architecture:** Unlike JPype (shared memory), py4j uses socket communication between Python and Java processes.

**Example:**
```python
from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
random = gateway.jvm.java.util.Random()
number = random.nextInt(10)
```

**Use case:** When Java application must stay running, Python connects as client.

### 5.3 GraalVM (Polyglot)

**Status:** Production-ready (Oracle maintained)
**Documentation:** https://www.graalvm.org/python/

GraalVM provides:
- **GraalPy:** Python 3 runtime on Truffle
- **Polyglot:** Embed multiple languages in one program
- **Native Image:** Compile to standalone binary

**Key feature:** Can embed Python in Java or vice versa.

**Assessment for Orchestr8:**
- **GraalPy:** Alternative Python implementation, not needed
- **Polyglot:** Overkill for Orchestr8
- **Native Image:** Could package Python apps as binaries

### 5.4 Kotlin/Scala → Python

| Language | Integration | Status |
|----------|-------------|--------|
| **Kotlin** | GraalVM (limited) | Experimental |
| **Scala** | Ammonite-REPL | Not relevant |

### 5.5 Assessment for Orchestr8

**Practical value:** LOW

JVM integration adds:
- Java runtime dependency
- Significant complexity
- No clear benefit for Orchestr8

Python ecosystem already has excellent libraries for:
- Data processing (pandas, numpy)
- Graph analysis (networkx)
- Code parsing (tree-sitter, ast)

**Verdict:** Not recommended for Orchestr8.

---

## 6. Functional Languages

### 6.1 Haskell → Python

| Option | Status | Assessment |
|--------|--------|------------|
| **hv (hs-python)** | Abandoned | Not usable |
| **pyhaskell** | Dormant | Not maintained |
| **GHC ( Glasgow Haskell Compiler)** | Can compile to C | Complex FFI |

**Verdict:** No practical Haskell → Python path exists.

### 6.2 OCaml → Python

| Option | Status | Assessment |
|--------|--------|------------|
| **pyocaml** | Minimal | Not production-ready |
| **OCaml → C bindings** | Complex | Requires C FFI |

**Verdict:** Not practical for Python integration.

### 6.3 Elixir/Erlang → Python

| Option | Status | Notes |
|--------|--------|-------|
| **Erlport** | Abandoned | Last release 2017 |
| **Elixir → Rust → Python** | Complex | Would need 2 layers |

**Verdict:** Not practical.

### 6.4 Assessment for Orchestr8

**Practical value:** NONE

Functional languages have excellent compilers and type systems, but:
- No mature Python bindings ecosystem
- Would require significant infrastructure
- No clear advantage for Orchestr8's use cases

**Verdict:** Not recommended. If functional features needed (parsing, formal verification), use specialized tools/libraries rather than embedding languages.

---

## 7. Summary Matrix

### 7.1 All Options Compared

| Language/Option | Python Integration | Marimo Compatible | Practical for Orchestr8 | Confidence |
|-----------------|-------------------|-------------------|------------------------|------------|
| **Rust (PyO3)** | ✅ Excellent | ✅ Yes | ✅ **Recommended** | HIGH |
| **C/C++ (pybind11)** | ✅ Excellent | ✅ Yes | ✅ **Recommended** | HIGH |
| **Cython** | ✅ Good | ✅ Yes | ⚠️ For porting | MEDIUM |
| **Go (gopy)** | ⚠️ Complex | ✅ Yes | ❌ Not recommended | MEDIUM |
| **Zig** | ❌ Not available | ⚠️ WASM only | ❌ Not recommended | LOW |
| **Pyodide (WASM)** | ✅ Native | ✅ Yes | ⚠️ Future option | HIGH |
| **Java (JPype)** | ✅ Good | ✅ Yes | ❌ Not needed | HIGH |
| **Java (py4j)** | ✅ Good | ⚠️ External | ❌ Not needed | HIGH |
| **Kotlin (GraalVM)** | ⚠️ Complex | ⚠️ Complex | ❌ Not needed | MEDIUM |
| **Haskell** | ❌ None | N/A | ❌ Not available | LOW |
| **OCaml** | ❌ None | N/A | ❌ Not available | LOW |
| **Elixir** | ❌ Abandoned | N/A | ❌ Not available | LOW |

### 7.2 Use Case Mapping

| Orchestr8 Use Case | Recommended Language | Tool | Confidence |
|-------------------|---------------------|------|------------|
| **High-Performance Computation** | Rust | PyO3 + maturin | HIGH |
| **Code Analysis/Parsing** | C/C++ | pybind11 + existing parsers | HIGH |
| **Sandboxed Scripting** | Python (native) | marimo cells | HIGH |
| **Sandboxed Scripting (browser)** | Python | Pyodide | MEDIUM |
| **DSL Implementation** | Python | Embedded DSL | HIGH |

---

## 8. Recommendations for Orchestr8

### 8.1 Immediate Recommendations

1. **Stick with Rust (PyO3)** for high-performance computation
   - Already researched in RUST_INTEROP.md
   - Production-proven, excellent ecosystem

2. **Use C/C++ via pybind11** for code analysis
   - Bind to tree-sitter (C library for parsing)
   - Access Clang for C/C++ analysis
   - Existing libraries already have Python bindings

3. **Keep Python as the scripting language**
   - marimo already supports Python natively
   - No need for additional DSL layer

### 8.2 Future Options

| Option | When to Consider | Complexity |
|--------|-----------------|------------|
| **Pyodide** | Browser-only deployment needed | Medium |
| **anywidget** | Custom interactive visualizations | Medium |
| **WASM from Rust** | Client-side computation | High |

### 8.3 What NOT to Pursue

- **Go (gopy):** Adds complexity, no advantage
- **Zig:** Pre-1.0, no Python bindings ecosystem
- **JVM languages:** Overkill, no clear benefit
- **Functional languages:** No practical integration path

---

## 9. Sources

### Primary Sources (HIGH Confidence)

| Source | URL | Relevance |
|--------|-----|-----------|
| pybind11 Docs | https://pybind11.readthedocs.io/ | C++ bindings |
| Cython Docs | https://cython.readthedocs.io/ | Python→C |
| JPype Docs | https://jpype.readthedocs.io/ | Java→Python |
| py4j | https://www.py4j.org/ | Java↔Python |
| gopy | https://github.com/go-python/gopy | Go→Python |
| Pyodide | https://pyodide.org/ | Python in browser |
| GraalVM Python | https://www.graalvm.org/python/ | Polyglot |

### Secondary Sources (MEDIUM Confidence)

| Source | URL | Relevance |
|--------|-----|-----------|
| ziglang PyPI | https://pypi.org/project/ziglang/ | Zig toolchain |
| Rust+WASM | https://rustwasm.github.io/ | WASM (sunsetted org) |

---

## 10. Files Created

| File | Purpose |
|------|---------|
| `.planning/research/LANGUAGE_INTEROP_COMPLETE.md` | This comprehensive assessment |

---

## 11. Conclusion

For Orchestr8, the practical language interoperability options are:

1. **Rust (PyO3)** — Already recommended for high-performance computation
2. **C/C++ (pybind11)** — For binding existing C/C++ code (parsers, algorithms)
3. **Python (native)** — For scripting, DSLs, and user-facing features
4. **Pyodide (future)** — If browser-only deployment becomes necessary

All other options (Go, Zig, JVM languages, functional languages) add significant complexity without clear benefit for Orchestr8's use cases.

**The Python ecosystem is sufficiently rich that external language integration is rarely needed.** Focus on leveraging existing Python libraries and Rust for performance bottlenecks.

---

*Research complete. Recommend proceeding with Rust (PyO3) and C/C++ (pybind11) paths as needed.*
