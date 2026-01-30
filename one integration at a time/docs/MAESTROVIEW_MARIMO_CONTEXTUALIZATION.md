# MaestroView.vue -> Marimo Contextualization

**Version:** 1.0
**Date:** 2026-01-26
**Purpose:** Map the stereOS Vue architecture to Orchestr8's Marimo implementation

---

## Executive Summary

MaestroView.vue is the **Command Center** of stereOS - a unified interface that orchestrates agents, tasks, file exploration, terminal access, and LLM interaction from a single view. This document translates its architecture into actionable Marimo implementation patterns.

**Key Insight:** MaestroView isn't just a dashboard - it's a **spatial UI** with:
- Fixed anchors (Top Row, Bottom Fifth)
- Emergence patterns (panels slide in/out from void)
- Central void for AI conversation
- Panel layering with z-index hierarchy

---

## 1. Architectural DNA Extraction

### 1.1 The Spatial Layout Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│ TOP ROW (z-index: 50) - Fixed Navigation                       │
│ [stereOS] ←──────────────────────→ [Collabor8] [JFDI] [Gener8] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    THE VOID (flex: 1)                          │
│               Pure collaboration space                          │
│                                                                 │
│     ┌──────────────────────────────────────────┐               │
│     │   LLM Messages Emerge Here               │               │
│     │   (TransitionGroup with "emerge" effect) │               │
│     └──────────────────────────────────────────┘               │
│                                                                 │
│                                    [Settings Portal]           │
├─────────────────────────────────────────────────────────────────┤
│ BOTTOM FIFTH (z-index: 20) - The Overton Anchor                │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ [Attachment Bar - files selected]                           ││
│ │ [Chat Input - Full Width TextArea]                          ││
│ │ [Control Surface - Button Groups]                           ││
│ │   Left: Apps|Matrix|Calendar|Comms|Files                    ││
│ │   Center: [maestro]                                         ││
│ │   Right: Search|Record|Playback|Phreak>|Send|Attach         ││
│ └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Panel Emergence System

MaestroView uses **overlay panels** that emerge from specific directions:

| Panel | Direction | z-index | Trigger |
|-------|-----------|---------|---------|
| Agents Panel | slides-down | 40 | `Collabor8` button |
| Tasks Panel | slides-right | 45 | `JFDI` button |
| Agent Chat | slides-right | 50 | Agent selection |
| File Explorer | modal | 60 | `Files` button |
| Terminal (Nexus) | modal | 60 | `Phreak>` button |
| Summon Results | overlay | 70 | `Search` / `/` key |

**Marimo Translation:** Use `mo.ui.tabs` for primary navigation, but implement **conditional rendering** for panel states using `mo.state()` booleans.

---

## 2. State Management Translation

### 2.1 Vue Refs -> Marimo State

**MaestroView.vue State:**
```typescript
// Panel visibility
const showAgentsPanel = ref(false)
const showTasksPanel = ref(false)
const showAgentChat = ref(false)
const showFileExplorer = ref(false)
const showTerminal = ref(false)
const showSummonResults = ref(false)
const showAppGrid = ref(false)

// Selection state
const selectedAgent = ref<DomainAgent | null>(null)
const focusedTask = ref<Task | null>(null)
const selectedFiles = ref<string[]>([])

// Chat state
const userInput = ref('')
const messages = ref<Message[]>([])
const isRecording = ref(false)
```

**Marimo Translation (orchestr8_maestro.py):**
```python
def render(STATE_MANAGERS):
    import marimo as mo

    # Panel visibility states
    get_show_agents, set_show_agents = mo.state(False)
    get_show_tasks, set_show_tasks = mo.state(False)
    get_show_terminal, set_show_terminal = mo.state(False)
    get_show_explorer, set_show_explorer = mo.state(False)

    # Selection states (from global STATE_MANAGERS)
    get_selected, set_selected = STATE_MANAGERS["selected"]

    # Chat conversation state
    get_messages, set_messages = mo.state([])
    get_user_input, set_user_input = mo.state("")

    # Agent focus
    get_focused_agent, set_focused_agent = mo.state(None)
    get_focused_task, set_focused_task = mo.state(None)
```

### 2.2 Composables -> Python Modules

| Vue Composable | Purpose | Marimo Equivalent |
|----------------|---------|-------------------|
| `useProvider('maestro')` | LLM interface | `llm_bridge.py` module |
| `useSummon()` | Global search | `carl_core.py` integration |
| `useTasks()` | Task management | `task_state.py` module |
| `useNavigation()` | Module switching | Tab switching logic |
| `useCloudSearch()` | External search | WebFetch integration |

---

## 3. Component Mapping

### 3.1 Vue Components -> Marimo Plugins

| Vue Component | File | Marimo Plugin |
|---------------|------|---------------|
| `DomainAgentBar` | components/DomainAgentBar.vue | `06_collabor8.py` (NEW) |
| `TasksPanel` | components/TasksPanel.vue | `07_jfdi.py` (NEW) |
| `AgentChatPanel` | components/AgentChatPanel.vue | `08_agent_chat.py` (NEW) |
| `FileExplorer` | components/FileExplorer.vue | `02_explorer.py` (EXISTS) |
| `NexusTerminal` | components/NexusTerminal.vue | `09_nexus.py` (NEW) |
| `SummonResultCard` | components/SummonResultCard.vue | `10_summon.py` (NEW) |
| `TaskFocusOverlay` | components/TaskFocusOverlay.vue | Integrated into `07_jfdi.py` |

### 3.2 The Control Surface Pattern

MaestroView's "Bottom Fifth" is the **command center** - a permanent input area with:

1. **Attachment Bar** - Shows selected files as chips
2. **Chat Input** - Full-width textarea
3. **Control Surface** - Action buttons in 3 groups

**Marimo Implementation:**
```python
def build_control_surface():
    # Attachment chips
    selected_files = get_selected_files()
    if selected_files:
        chips = mo.hstack([
            mo.md(f"`{f}` [x]") for f in selected_files
        ])
    else:
        chips = mo.md("")

    # Chat input
    chat_input = mo.ui.text_area(
        value=get_user_input(),
        placeholder="What would you like to accomplish?",
        on_change=set_user_input,
        full_width=True
    )

    # Control buttons - Left Group
    left_group = mo.hstack([
        mo.ui.button(label="Apps", on_change=lambda _: toggle_apps()),
        mo.ui.button(label="Matrix", on_change=lambda _: open_diagnostics()),
        mo.ui.button(label="Files", on_change=lambda _: set_show_explorer(True)),
    ])

    # Center - maestro
    center_btn = mo.ui.button(
        label="maestro",
        on_change=lambda _: show_summon()
    )

    # Right Group
    right_group = mo.hstack([
        mo.ui.button(label="Search", on_change=lambda _: show_summon()),
        mo.ui.button(label="Terminal", on_change=lambda _: set_show_terminal(True)),
        mo.ui.button(label="Send", on_change=lambda _: send_message()),
    ])

    return mo.vstack([
        chips,
        chat_input,
        mo.hstack([left_group, center_btn, right_group], justify="space-between")
    ])
```

---

## 4. Event Handler Translation

### 4.1 Top Row Actions

**Vue:**
```typescript
function handleStereoSClick() {
  messages.value = []
  showAgentsPanel.value = false
  showTasksPanel.value = false
}

function toggleCollabor8() {
  showAgentsPanel.value = !showAgentsPanel.value
  if (showAgentsPanel.value) showTasksPanel.value = false
}
```

**Marimo:**
```python
def handle_home_click():
    set_messages([])
    set_show_agents(False)
    set_show_tasks(False)

def toggle_collabor8():
    current = get_show_agents()
    set_show_agents(not current)
    if not current:  # Opening
        set_show_tasks(False)
```

### 4.2 Keyboard Shortcuts

**Vue:**
```typescript
function handleGlobalKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 't') toggleJFDI()
  if ((e.metaKey || e.ctrlKey) && e.key === 'a') toggleCollabor8()
  if (e.key === '/') showSummonResults.value = true
  if (e.key === 'Escape') handleEscapeDismissal()
}
```

**Marimo Note:** Marimo doesn't have direct keyboard shortcut support. Options:
1. Use browser-level JavaScript injection via `mo.Html()`
2. Implement as button-based shortcuts in the UI
3. Wait for Marimo keyboard events feature

---

## 5. The Void - LLM Conversation Space

### 5.1 Message Emergence Pattern

**Vue Template:**
```html
<TransitionGroup name="emerge" tag="div" class="void-emergence">
  <div
    v-for="message in messages.filter(m => m.role === 'assistant').slice(-3)"
    :key="message.id"
    class="emerged-message"
  >
    <div class="message-content">{{ message.content }}</div>
    <div class="message-meta">
      <span class="message-time">{{ message.timestamp.toLocaleTimeString() }}</span>
    </div>
  </div>
</TransitionGroup>
```

**Key Insight:** Only shows **last 3 assistant messages** - creates "emergence from void" effect.

**Marimo Translation:**
```python
def build_void_messages():
    messages = get_messages()
    assistant_msgs = [m for m in messages if m["role"] == "assistant"][-3:]

    if not assistant_msgs:
        return mo.md("")  # Empty void

    message_cards = []
    for msg in assistant_msgs:
        card = mo.md(f"""
<div style="
    padding: 16px 20px;
    background: rgba(18, 18, 20, 0.9);
    border: 1px solid rgba(184, 134, 11, 0.3);
    border-radius: 8px;
    margin-bottom: 16px;
">
<div style="color: #e8e8e8; font-size: 14px; line-height: 1.6;">
{msg["content"]}
</div>
<div style="text-align: right; margin-top: 8px;">
<span style="font-family: monospace; font-size: 10px; color: #B8860B;">
{msg["timestamp"]}
</span>
</div>
</div>
        """)
        message_cards.append(card)

    return mo.vstack(message_cards)
```

---

## 6. Color System - The Void Palette

### 6.1 Exact Colors (NO EXCEPTIONS)

```css
--blue-dominant: #1fbdea  /* UI default */
--gold-metallic: #D4AF37  /* UI highlight */
--gold-dark: #B8860B      /* Maestro default */
--gold-saffron: #F4C430   /* Maestro highlight */
--bg-primary: #0A0A0B     /* The Void */
--bg-elevated: #121214    /* Surface */
```

### 6.2 Marimo CSS Injection

```python
MAESTRO_STYLES = """
<style>
:root {
    --blue-dominant: #1fbdea;
    --gold-metallic: #D4AF37;
    --gold-dark: #B8860B;
    --gold-saffron: #F4C430;
    --bg-primary: #0A0A0B;
    --bg-elevated: #121214;
}

.marimo-container {
    background: var(--bg-primary) !important;
}

.maestro-btn {
    padding: 5px 12px;
    border-radius: 4px;
    background: var(--bg-elevated);
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: var(--blue-dominant);
    font-size: 10px;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 200ms ease-out;
}

.maestro-btn:hover {
    background: rgba(212, 175, 55, 0.1);
    border-color: var(--gold-metallic);
    color: var(--gold-metallic);
}
</style>
"""
```

---

## 7. Implementation Roadmap

### Phase 1: Core Maestro Plugin (Week 1)
- [ ] Create `06_maestro.py` plugin with void layout
- [ ] Implement bottom control surface
- [ ] Add chat input and message display
- [ ] Integrate with existing STATE_MANAGERS

### Phase 2: Panel Emergence (Week 2)
- [ ] Implement `07_collabor8.py` (Agent Bar)
- [ ] Implement `08_jfdi.py` (Tasks Panel)
- [ ] Add panel toggle logic with mutual exclusion

### Phase 3: LLM Integration (Week 3)
- [ ] Create `llm_bridge.py` for LLM calls
- [ ] Implement conversation history
- [ ] Add Summon (global search) feature

### Phase 4: Advanced Features (Week 4)
- [ ] Implement `09_nexus.py` (Terminal)
- [ ] Add keyboard shortcut workarounds
- [ ] Polish animations via CSS injection

---

## 8. Critical Differences: Vue vs Marimo

| Aspect | Vue (MaestroView) | Marimo |
|--------|-------------------|--------|
| Reactivity | Fine-grained via Refs | Cell-level via `mo.state()` |
| Transitions | CSS Transitions + Vue | CSS only via `mo.Html()` |
| Keyboard Events | `window.addEventListener` | Not native (JS injection needed) |
| Layout | Flexbox + Fixed positioning | `mo.hstack` / `mo.vstack` |
| Overlays | z-index layering | Conditional rendering |
| Async | Native async/await | `asyncio` + careful handling |

---

## 9. Recommended Plugin Structure

```
IP/plugins/
├── 00_welcome.py           # Landing page
├── 01_generator.py         # 7-Phase Wizard (EXISTS)
├── 02_explorer.py          # File Explorer (EXISTS)
├── 03_gatekeeper.py        # Louis Protection (EXISTS)
├── 04_connie_ui.py         # Schema Mapper (EXISTS)
├── 05_universal_bridge.py  # Tool Registry (EXISTS)
├── 06_maestro.py           # NEW: The Void (Central Command)
├── 07_collabor8.py         # NEW: Agent Management
├── 08_jfdi.py              # NEW: Task Management
├── 09_nexus.py             # NEW: Terminal Interface
├── 10_summon.py            # NEW: Global Search
└── output_renderer.py      # Shared output formatting
```

---

## 10. The Maestro Plugin Skeleton

```python
"""
06_maestro Plugin - The Void
Orchestr8 v3.0 - Central Command Interface

The heart of Orchestr8 - a unified command center inspired by stereOS MaestroView.
Implements the spatial UI pattern with:
- Top navigation bar
- Central void for AI conversation
- Bottom control surface (the Overton anchor)

Design Principles:
- NO breathing animations
- NO emojis in UI chrome (only in content)
- NO clock display
- Messages EMERGE from the void
"""

PLUGIN_NAME = "The Void"
PLUGIN_ORDER = 6

# Color constants - EXACT, NO EXCEPTIONS
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_PRIMARY = "#0A0A0B"
BG_ELEVATED = "#121214"


def render(STATE_MANAGERS):
    import marimo as mo
    from datetime import datetime

    # Global state
    get_root, set_root = STATE_MANAGERS["root"]
    get_selected, set_selected = STATE_MANAGERS["selected"]
    get_logs, set_logs = STATE_MANAGERS["logs"]

    # Local state
    get_messages, set_messages = mo.state([])
    get_user_input, set_user_input = mo.state("")
    get_show_agents, set_show_agents = mo.state(False)
    get_show_tasks, set_show_tasks = mo.state(False)

    def send_message():
        text = get_user_input().strip()
        if not text:
            return

        messages = get_messages()
        messages.append({
            "id": len(messages),
            "role": "user",
            "content": text,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        # TODO: LLM integration
        messages.append({
            "id": len(messages),
            "role": "assistant",
            "content": f"Processing: {text}",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        set_messages(messages)
        set_user_input("")

    def build_void_display():
        messages = get_messages()
        assistant_msgs = [m for m in messages if m["role"] == "assistant"][-3:]

        if not assistant_msgs:
            return mo.md("*The void awaits your command...*")

        return mo.vstack([
            mo.md(f"""
**{msg['content']}**

<small style="color: {GOLD_DARK}">{msg['timestamp']}</small>

---
            """) for msg in assistant_msgs
        ])

    # Top row
    top_row = mo.hstack([
        mo.md(f"<span style='color:{BLUE_DOMINANT}'>stere</span><span style='color:{GOLD_METALLIC}'>OS</span>"),
        mo.hstack([
            mo.ui.button(label="Collabor8", on_change=lambda _: set_show_agents(not get_show_agents())),
            mo.ui.button(label="JFDI", on_change=lambda _: set_show_tasks(not get_show_tasks())),
            mo.ui.button(label="Gener8", on_change=lambda _: None),  # Tab switch
        ])
    ], justify="space-between")

    # The Void (center)
    void_content = build_void_display()

    # Control surface (bottom)
    chat_input = mo.ui.text_area(
        value=get_user_input(),
        placeholder="What would you like to accomplish?",
        on_change=set_user_input,
        full_width=True
    )

    control_buttons = mo.hstack([
        mo.ui.button(label="Files"),
        mo.ui.button(label="maestro"),
        mo.ui.button(label="Search"),
        mo.ui.button(label="Send", on_change=lambda _: send_message()),
    ], justify="space-around")

    # Conditional panels
    agents_panel = mo.md("### Collabor8 Panel\n*Agent management UI*") if get_show_agents() else mo.md("")
    tasks_panel = mo.md("### JFDI Panel\n*Task management UI*") if get_show_tasks() else mo.md("")

    return mo.vstack([
        top_row,
        mo.md("---"),
        agents_panel,
        tasks_panel,
        void_content,
        mo.md("---"),
        chat_input,
        control_buttons
    ])
```

---

## Conclusion

MaestroView.vue is a **masterclass in spatial UI design**. Its patterns translate well to Marimo with these adaptations:

1. **Vue Refs** -> `mo.state()` tuples
2. **Components** -> Plugin modules with `render(STATE_MANAGERS)`
3. **Transitions** -> CSS injection via `mo.Html()`
4. **Event Handlers** -> Button `on_change` callbacks
5. **The Void** -> Central `mo.vstack` with conditional content

The key insight: **Marimo's cell-based reactivity maps well to MaestroView's panel-based architecture**, where each panel is essentially an independent reactive unit that can be shown/hidden based on state.

---

*Document generated for Orchestr8 v3.0 - The Fortress Factory*
