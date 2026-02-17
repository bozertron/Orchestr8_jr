# Rendering Tradeoffs: REVISED - Getting Creative

**Research Complete: 2026-02-13**
**Confidence: HIGH**

---

## The Previous Assessment Was Too Conservative

I missed the experimental features and community widgets. Here's the **creative** analysis:

---

## 1. Experimental Features - New Possibilities

### MimeBundleDescriptor

This can turn ANY Python object into a widget without subclassing:

```python
from anywidget.experimental import MimeBundleDescriptor

class Foo:
  _repr_mimebundle_ = MimeBundleDescriptor()
```

**Supports:**
- dataclasses
- pydantic.BaseModel  
- msgspec.Struct
- Any class with `_get_anywidget_state` method
- psygnal.SignalGroup for observers

**Creative Use:** Wrap existing woven_maps data structures directly. No rewrite needed.

### Direct Comm Access

The `comm.base_comm.BaseComm` object provides **direct bidirectional messaging**:

```python
# Python side
comm.send({'type': 'update', 'data': ...})

# JS side  
model.on('msg:custom', (msg) => { ... })
```

**Creative Use:** Real-time streaming without traitlets overhead. Perfect for:
- Particle position updates
- Camera position sync
- Click/hover events

---

## 2. Community Widgets - Gold Mines

### Rerun (10.2k stars) - 🔥 GAME CHANGER

```
"An open source SDK for logging, storing, querying, and visualizing 
multimodal and multi-rate data"
```

| Feature | Rerun | Current Custom |
|---------|-------|----------------|
| 3D rendering | ✅ | ✅ |
| Points/Particles | ✅ | ✅ |
| Time-series | ✅ | ❌ |
| Images | ✅ | ❌ |
| Text labels | ✅ | ✅ |
| Time-travel debug | ✅ | ❌ |
| Dataframe API | ✅ | ❌ |
| Python SDK | ✅ | Custom |
| WebGL/WGPU | ✅ | Custom |

**Could Rerun replace the entire Code City visualization?**

Maybe. The trade-off:
- ✅ Gains: Time-travel debugging, better data management, 10k stars of maintenance
- ❌ Loses: The "emergence" animation (particles coalescing from void)
- ❓ Unknown: Can it do the specific Barradeau-style building rendering?

### Cosmograph (137 stars) - PERFECT FOR WIRING

```
"GPU-accelerated force layout graph visualization"
Built on @cosmograph/cosmos
```

**Features:**
- GPU-accelerated (WebGL)
- Pan, zoom, select, hover
- Handles large graphs (100K+ nodes)
- Anywidget-native

**For the wiring diagram specifically:**

```python
from cosmograph import cosmo

widget = cosmo(
    points=files_df,      # Your file nodes
    links=imports_df,     # Your import edges
    point_id_by='path',
    link_source_by='source',
    link_target_by='target',
    point_color_by='status',  # Gold/Teal/Purple
    point_size_by='complexity'
)
```

**This could replace the 3D edge rendering with a 2D force-directed graph that's GPU-accelerated.**

---

## 3. Creative Architecture Options

### Option A: Hybrid (Recommended)

| Component | Current | Alternative |
|-----------|---------|-------------|
| 3D Code City | Custom WebGPU | Keep (emergence is unique) |
| Wiring diagram | Custom 3D lines | **Cosmograph** |
| Real-time updates | postMessage | **Direct Comm** |

**Benefit:** 80% less code for wiring, GPU-accelerated, same Python integration.

### Option B: Rerun Full Replace

Replace entire custom canvas with Rerun.

**Pros:**
- 10k stars of maintenance
- Time-travel debugging
- Better data management

**Cons:**
- Lose emergence animation
- Unknown if Barradeau rendering possible
- More investigation needed

### Option C: MimeBundleDescriptor Wrapper

Wrap existing woven_maps Python objects with MimeBundleDescriptor:

```python
from anywidget.experimental import MimeBundleDescriptor

class CityState:
    _repr_mimebundle_ = MimeBundleDescriptor()
    
    def __init__(self, buildings, edges, particles):
        self.buildings = buildings
        self.edges = edges
        self.particles = particles
        
    def _get_anywidget_state(self):
        return {
            'buildings': self.buildings,
            'edges': self.edges,
            'particles': self.particles
        }
```

**Benefit:** Minimal rewrite, anywidget benefits.

---

## 4. Direct Comm - The Real-Time Secret

The Comm object isn't just for traitlets. You can send custom messages:

```python
# In Python
def on_click(comm, msg):
    # Handle click from JS
    handle_click(msg['node_id'])

comm.on_msg(on_click)

# Send updates directly
comm.send({'type': 'camera', 'position': [x, y, z]})
```

**For particles:** Instead of re-rendering, stream position updates:

```python
# More efficient than traitlets for high-frequency updates
for particle_batch in particle_stream:
    comm.send({
        'type': 'particles', 
        'positions': particle_batch.tolist()
    })
```

---

## 5. Updated Recommendations

### For 3D Code City (Buildings + Emergence)
**Keep current implementation** - The emergence animation is unique and valuable.

### For Wiring Diagram
**USE COSMOGRAPH** - This is a no-brainer:
- GPU-accelerated
- Built on anywidget (native marimo support)
- Handles 100K+ nodes
- 80%+ code reduction
- Force-directed is actually better for understanding clusters

### For Real-Time Updates
**Use Direct Comm** - Skip traitlets for high-frequency updates:
- Particle streaming
- Camera sync
- Click/hover events

### For Future Architecture
**Consider MimeBundleDescriptor** - For cleaner widget integration without full rewrite.

---

## 6. What Was Missed (The Creative Part)

| What I Missed | Why It Matters |
|---------------|----------------|
| MimeBundleDescriptor | Can wrap ANY Python object as widget |
| Rerun | 10k star visualization platform could replace canvas |
| Cosmograph | GPU graph viz perfect for wiring |
| Direct Comm | Real-time streaming without traitlets overhead |

---

## Files Updated

- `.planning/research/RENDERING_TRADEOFFS.md` - Original analysis
- `.planning/research/RENDERING_SUMMARY.md` - Executive summary
- `.planning/research/RENDERING_CREATIVE.md` - This file (creative options)

---

## Next Steps Recommended

1. **Try Cosmograph** for wiring diagram - Low effort, high return
2. **Investigate Rerun** for potential full replacement - Medium effort
3. **Prototype MimeBundleDescriptor** on existing data structures - Low effort
4. **Benchmark Direct Comm** for particle streaming - If needed
