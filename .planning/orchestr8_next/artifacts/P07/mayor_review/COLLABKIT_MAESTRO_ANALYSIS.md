# Collabkit MaestroView Analysis

**Source Files (byte-identical to UI Reference):**
- `/one integration at a time/UI Reference/MaestroView.vue`
- `/one integration at a time/FileExplorer/FileExplorer.vue`

**Analysis Date:** 2026-02-16
**Focus:** Mayor's review of overlay patterns, terminal hooks, file navigation, and state management

---

## 1. Overlay Patterns

### 1.1 MaestroView Overlay Architecture

The MaestroView employs a **layered overlay system** with the Void (`#0A0A0B`) as the foundational canvas. Key overlay patterns:

| Overlay | Trigger | Position | Transition |
|---------|---------|----------|-------------|
| `agents-panel` | `toggleCollabor8()` | Fixed top, slides down | `slide-down` (300ms) |
| `tasks-panel` | `toggleJFDI()` | Right side, slides in | `slide-right` (300ms) |
| `task-focus` | Task selection | Full overlay | `fade` (200ms) |
| `agent-chat` | Agent selection | Right panel | `slide-right` (300ms) |
| `file-explorer` | Files button | Center modal | Vue `v-if` |
| `nexus-terminal` | Phreak button | Center modal | Vue `v-if` |
| `summon-results` | Search/maestro click | Full overlay | Vue `v-if` |

### 1.2 Overlay Z-Index Strategy

```css
/* Z-index layering */
.top-row        { z-index: 50; }   /* Fixed header */
.agents-panel   { z-index: 40; }   /* Slides from top */
.tasks-panel    { z-index: 45; }   /* Right sidebar */
.agent-chat     { z-index: 50; }   /* Right panel */
.settings-corner{ z-index: 100; } /* Above bottom-fifth */
.file-explorer  { z-index: 1000; }/* Modal level */
```

### 1.3 Dismissal Hierarchy

The Escape key handler implements a **priority dismissal chain**:

```typescript
// Line 406-424 in MaestroView.vue
if (e.key === 'Escape') {
  if (focusedTask)           dismiss task focus
  else if (isRecording)     stop recording
  else if (showAgentChat)   close agent chat
  else if (showTasksPanel)  close tasks
  else if (showAgentsPanel) close agents
  else if (showSummonResults) dismiss summon
  else if (showTerminal)    close terminal
  else if (showFileExplorer) close file explorer
}
```

### 1.4 Key Overlay Patterns to Port

1. **Backdrop blur** - `backdrop-filter: blur(4px)` on overlay containers
2. **Click-outside-to-close** - `@click.self` on overlay containers
3. **Panel-dismiss button** - `HollowDiamond` component in corner
4. **Transition composition** - Multiple transitions can stack (e.g., fade + slide)

---

## 2. Terminal Hook Integration

### 2.1 NexusTerminal Component

The terminal is integrated via:

```typescript
// Lines 54, 176-178, 536-541
const showTerminal = ref(false)

function handlePhreakClick() {
  showTerminal.value = true
}

function handleTerminalCopy(content: string) {
  console.log('[Maestro] Terminal content copied:', content.substring(0, 50))
  showTerminal.value = false
}
```

**Template integration:**
```vue
<NexusTerminal
  :visible="showTerminal"
  @close="showTerminal = false"
  @copy="handleTerminalCopy"
/>
```

### 2.2 Terminal Trigger Points

| Trigger | Location | Action |
|---------|----------|--------|
| `Phreak>` button | Bottom control surface | Opens terminal |
| `Ctrl/Cmd + \` | Not implemented | Candidate for terminal toggle |
| Escape | Global handler | Closes terminal |

### 2.3 Terminal-to-Chat Flow

The terminal has a **copy-to-dismiss** pattern:
- User copies content from terminal
- Content is logged to chat context
- Terminal auto-closes after copy

### 2.4 Terminal Patterns to Port

1. **Conditional rendering** - `v-if="showTerminal"` only when needed
2. **Copy hook** - `@copy` event handler for content capture
3. **Auto-dismiss on action** - Terminal closes after meaningful interaction

---

## 3. File Explorer + Code City Navigation Alignment

### 3.1 FileExplorer Component Structure

The FileExplorer is a **modal overlay** with:

```typescript
// Lines 8-12
const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['close', 'select'])
```

### 3.2 Navigation Model

**Breadcrumb navigation:**
```typescript
// Lines 18-37
const breadcrumbs = computed(() => {
  const parts = currentPath.value.split(/[/\\]/).filter(Boolean)
  // Builds hierarchical path array
  return crumbs  // { name: string, path: string }[]
})
```

**Sidebar locations:**
```typescript
// Lines 39-46
const locations = [
  { name: 'HOME', icon: '◇', path: '~' },
  { name: 'DOCUMENTS', icon: '◇', path: 'Documents' },
  { name: 'DOWNLOADS', icon: '◇', path: 'Downloads' },
  { name: 'APP STORAGE', icon: '💾', path: 'APP_STORAGE' }
]
```

### 3.3 Selection Patterns

**Multi-select with modifier keys:**
```typescript
// Lines 53-67
function handleItemClick(event: MouseEvent, item: FileInfo) {
  if (event.metaKey || event.ctrlKey) {
    // Toggle selection
  } else if (event.shiftKey && selectedPaths.value.size > 0) {
    // Range selection (basic)
  } else {
    // Single select, clear others
  }
}
```

**Double-click behavior:**
- Directory: Navigate into
- File: Emit selection

### 3.4 Code City Integration Points

| FileExplorer Feature | Code City Alignment |
|---------------------|---------------------|
| Path-based navigation | Code City file-to-building mapping |
| Breadcrumbs | Code City fiefdom hierarchy |
| Selection state | Code City multi-file highlighting |
| File icons | Code City building types |
| "ADD TO CHAT" action | Code City file context injection |

### 3.5 FileExplorer-to-Code City Bridge

The FileExplorer emits `select` with file paths:

```typescript
// Lines 107-112
function handleEmitSelect() {
  if (selectedPaths.value.size > 0) {
    emit('select', Array.from(selectedPaths.value))
    selectedPaths.value.clear()
  }
}
```

**Integration pattern:** When files are selected:
1. File paths flow to chat context
2. Chat can query Code City for file visualization
3. Code City can highlight selected buildings

### 3.6 Patterns to Port

1. **Composable filesystem** - `useFileSystem()` for path/entry state
2. **Computed breadcrumbs** - Path decomposition for navigation
3. **Multi-select with modifiers** - Standard desktop UX
4. **Selection state persistence** - `Set<string>` for efficient lookups
5. **Modal with DecoWindow** - Consistent window chrome

---

## 4. State Management in Vue Components

### 4.1 MaestroView State Architecture

**Local reactive state (ref):**
```typescript
// Panel visibility
const showAgentsPanel = ref(false)
const showTasksPanel = ref(false)
const showAgentChat = ref(false)
const showFileExplorer = ref(false)
const showTerminal = ref(false)
const showSummonResults = ref(false)

// Selection state
const selectedAgent = ref<DomainAgent | null>(null)
const focusedTask = ref<Task | null>(null)
const selectedFiles = ref<string[]>([])

// Input state
const userInput = ref('')
const messages = ref<Message[]>([])
```

**Composable state (external):**
```typescript
// LLM provider
const { isLoading, complete } = useProvider('maestro')

// Summon system
const { state: summonState, summon, clearResults } = useSummon()

// Cloud search
const { state: cloudSearchState, search: cloudSearch, init: initCloudSearch } = useCloudSearch()

// Navigation
const { openSettingsAt } = useNavigation()
```

### 4.2 Dependency Injection

```typescript
// Line 41 - Inject parent module switcher
const switchModule = inject<(id: string) => void>('switchModule')
```

Pattern: Child components can trigger parent module changes via injection.

### 4.3 Event-Driven Communication

**Outbound events (defineEmits):**
```typescript
// MaestroView emits to parent:
// - No explicit emits defined (uses switchModule injection)

// FileExplorer emits:
const emit = defineEmits(['close', 'select'])
```

**Inbound event handling:**
```typescript
// Lines 233-322 - Comprehensive event handlers
function handleAgentSelect(agent: DomainAgent) { ... }
function handleTaskFocus(task: Task) { ... }
function handleFileSelect(files: string[]) { ... }
function handleSummonOpen(result: SummonResult) { ... }
```

### 4.4 Lifecycle Integration

```typescript
// Lines 431-439
onMounted(async () => {
  window.addEventListener('keydown', handleGlobalKeydown)
  await initCloudSearch()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
```

### 4.5 State Patterns to Port

1. **Boolean flags for panel visibility** - Clear toggle state
2. **Selection state as Set** - O(1) lookup for large file lists
3. **Composable extraction** - Business logic in reusable hooks
4. **Inject for parent communication** - Decoupled module switching
5. **Lifecycle cleanup** - Remove event listeners on unmount
6. **Message queue** - LLM responses as message array

---

## 5. Key Architectural Insights

### 5.1 Emergence Philosophy

The UI uses **emergence metaphors** rather than animation:
- Messages "emerge from the void" (no loading spinners for LLM)
- Panels "slide" rather than "animate in"
- No "breathing" or continuous animations

### 5.2 Color System (EXACT)

```css
--blue-dominant: #1fbdea    /* UI default state */
--gold-metallic: #D4AF37    /* UI highlight/active */
--gold-dark: #B8860B        /* Maestro default */
--gold-saffron: #F4C430    /* Maestro highlight */
--bg-primary: #0A0A0B      /* The Void */
--bg-elevated: #121214     /* Surface */
```

### 5.3 Control Surface Layout

The bottom 5th follows an **Overton window** concept:
- Left group: Apps, Matrix, Calendar, Comms, Files
- Center: maestro (summon trigger)
- Right group: Search, Record, Playback, Phreak>, Send, Attach

### 5.4 Keyboard Shortcut Matrix

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + T` | Toggle Tasks (JFDI) |
| `Cmd/Ctrl + A` | Toggle Agents (Collabor8) |
| `Cmd/Ctrl + G` | Open Generator |
| `Cmd/Ctrl + ,` | Open Settings |
| `/` | Open Summon |
| `Escape` | Hierarchy dismissal |

---

## 6. Orchestr8 Porting Recommendations

### 6.1 High-Priority Patterns

1. **Overlay z-index strategy** - Implement in Orchestr8 CSS
2. **Escape key dismissal chain** - Add to global key handler
3. **Backdrop blur on modals** - Match FileExplorer style
4. **Click-outside-to-close** - Apply to all overlay panels

### 6.2 FileExplorer Integration

The FileExplorer can be adapted for:
- Code City file selection
- Fiefdom navigation
- Multi-file context injection

### 6.3 Terminal Integration

NexusTerminal pattern for:
- Execution output display
- Code City query results
- Agent communication logs

### 6.4 State Management

Adopt composable pattern:
- `useSummon` → Orchestr8 search
- `useCloudSearch` → Code City API
- `useNavigation` → Tab switching

---

## Appendix: File Locations

| Component | Source Path |
|-----------|-------------|
| MaestroView | `/one integration at a time/UI Reference/MaestroView.vue` |
| FileExplorer | `/one integration at a time/FileExplorer/FileExplorer.vue` |
| DecoWindow | `/one integration at a time/FileExplorer/DecoWindow.vue` |
| HollowDiamond | `/one integration at a time/FileExplorer/HollowDiamond.vue` |

---

*Analysis completed for Mayor's review - P07 integration path*
