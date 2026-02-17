# COLLABKIT VUE COMPONENT MAPPING

**Purpose:** Map sophisticated Vue components in Collabkit for Orchestr8 integration  
**Source:** `/home/bozertron/JFDI - Collabkit/Application/src/`  
**Target:** Orchestr8 (`IP/plugins/06_maestro.py`)  
**Date:** 2026-02-16

---

## EXECUTIVE SUMMARY

Collabkit's stereOS is a Tauri-native Vue 3 application with sophisticated UI patterns that can inform Orchestr8's Marimo-based architecture. Key findings:

- **12 major UI patterns** identified across 50+ Vue components
- **Tauri integration** via `@tauri-apps/api/core`, `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-shell`
- **Composable-first architecture** for business logic separation
- **Art Deco visual language** (#D4AF37 gold, #1fbdea blue, #0A0A0B void)
- **Overlay/panel system** with emergence animations

---

## 1. MAESTROVIEW.VUE — FULL ANALYSIS

**Path:** `/home/bozertron/JFDI - Collabkit/Application/src/modules/maestro/MaestroView.vue`  
**Lines:** 1,194  
**Classification:** Tauri-Native + Browser Fallback

### 1.1 Overlay Patterns

| Pattern | Implementation | Orchestr8 Relevance |
|---------|----------------|---------------------|
| **Slide-down Panel** | `Transition name="slide-down"` from top | Settings dropdowns |
| **Slide-right Panel** | `Transition name="slide-right"` from right | Task/agent panels |
| **Fade Overlay** | `Transition name="fade"` for modals | Confirmation dialogs |
| **Backdrop Blur** | `backdrop-filter: blur(4px)` | Focus overlays |

### 1.2 Terminal Hooks

```typescript
// Audio recording via Tauri
async function startRecording() {
  const { invoke } = await import('@tauri-apps/api/core')
  await invoke('audio_start')
}

async function stopRecording() {
  const { invoke } = await import('@tauri-apps/api/core')
  await invoke('audio_stop')
}
```

**Key Hooks:**
- `audio_start` / `audio_stop` — Tauri commands for voice
- Global keyboard shortcuts via `window.addEventListener('keydown')`
- Escape hierarchy dismissal pattern

### 1.3 State Management

```typescript
// Panel visibility refs
const showAgentsPanel = ref(false)
const showTasksPanel = ref(false)
const showAgentChat = ref(false)
const focusedTask = ref<Task | null>(null)

// Chat/messages state
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}
const messages = ref<Message[]>([])
```

### 1.4 Color System (EXACT)

```css
--blue-dominant: #1fbdea    /* UI default */
--gold-metallic: #D4AF37    /* UI highlight */
--gold-dark: #B8860B       /* Maestro default */
--gold-saffron: #F4C430    /* Maestro highlight */
--bg-primary: #0A0A0B     /* The Void */
--bg-elevated: #121214     /* Surface */
```

### 1.5 Integration Vectors for Orchestr8

| Vector | Collabkit Pattern | Marimo Equivalent |
|--------|------------------|-------------------|
| **Panel toggles** | `showAgentsPanel = !showAgentsPanel` | `mo.ui.button(on_click=...)` |
| **Global shortcuts** | `handleGlobalKeydown(e)` | Global keyboard handler |
| **Message emergence** | `<TransitionGroup name="emerge">` | Animated output containers |
| **Soundwave settings** | Settings portal with wave bars | Custom settings trigger |
| **Control surface** | Bottom 5th fixed command bar | Fixed bottom toolbar |

---

## 2. FILEEXPLORER.VUE — FULL ANALYSIS

**Path:** `/home/bozertron/JFDI - Collabkit/Application/src/components/FileExplorer.vue`  
**Lines:** 504  
**Classification:** Tauri-Native with Browser Fallback

### 2.1 Navigation Patterns

```typescript
// Breadcrumb computation
const breadcrumbs = computed(() => {
  const parts = currentPath.value.split(/[/\\]/).filter(Boolean)
  const crumbs: { name: string; path: string }[] = []
  // ... path resolution logic
  return crumbs
})
```

### 2.2 Selection Patterns

| Feature | Implementation | Notes |
|---------|---------------|-------|
| **Single select** | Click clears and selects | Standard |
| **Multi-select** | Meta/Ctrl+Click | Toggle behavior |
| **Range select** | Shift+Click (stubbed) | Basic implementation |
| **Double-click** | Navigate or emit | Folders navigate, files emit |

### 2.3 File System Integration

```typescript
// Platform-aware filesystem
import { readDir, stat, type DirEntry } from '@tauri-apps/plugin-fs'
import { homeDir, documentDir, downloadDir, appDataDir, join } from '@tauri-apps/api/path'

function isTauriAvailable(): boolean {
  return typeof window !== 'undefined' && 
    ('__TAURI__' in window || '__TAURI_INTERNALS__' in window);
}
```

### 2.4 UI Components

- **Sidebar navigation** — Location shortcuts (HOME, DOCUMENTS, DOWNLOADS, APP STORAGE)
- **Breadcrumb header** — Path navigation with root (/) button
- **File table** — Name/Size/Modified columns with sticky headers
- **Selection footer** — Item count + "ADD TO CHAT" action button

### 2.5 Integration Vectors for Orchestr8

| Vector | Collabkit Pattern | Marimo Equivalent |
|--------|------------------|-------------------|
| **Breadcrumb nav** | Computed path → clickable crumbs | File path display |
| **Location sidebar** | Quick-access buttons | Directory shortcuts |
| **File table** | Virtual scrolling table | File listing |
| **Selection model** | Set<string> for multi-select | List selection state |

---

## 3. LARGEST VUE COMPONENTS (BY LINE COUNT)

| Rank | Component | Lines | Module | Classification |
|------|-----------|-------|--------|----------------|
| 1 | CalendarView.vue | 1,208 | calendar/ | Tauri-Native |
| 2 | MaestroView.vue | 1,194 | maestro/ | **Tauri-Native** |
| 3 | VoidComms.vue | 1,141 | vendor/ | Browser-Based |
| 4 | CommsView.vue | 1,029 | comms/ | Tauri-Native |
| 5 | LLMSettings.vue | 1,009 | settings/ | Tauri-Native |
| 6 | OrchestratorView.vue | 963 | orchestrator/ | Browser-Based |
| 7 | SettingsView.vue | 818 | settings/ | Browser-Based |
| 8 | BusinessTaskCard.vue | 813 | components/ | Browser-Based |
| 9 | ModelPicker.vue | 790 | components/ | Browser-Based |
| 10 | GenerationHistory.vue | 735 | generator/ | Browser-Based |
| 11 | TaskFocusOverlay.vue | 730 | components/ | Browser-Based |
| 12 | GeneratorView_V2.vue | 719 | generator/ | Tauri-Native |

### Key Insight

The **Tauri-native** components (1, 2, 4, 5, 12) handle:
- File system access
- Terminal execution
- Audio recording/playback
- Calendar integration
- LLM provider management

The **Browser-based** components (3, 6, 7, 8, 9, 10, 11) handle:
- Pure UI/state management
- Content display
- Settings forms
- Task cards

---

## 4. UI PATTERNS MAPPING

### 4.1 Settings Patterns

**SettingsView.vue (818 lines)**

```typescript
// Tab-based navigation
type SettingsTab = 'llm' | 'appearance' | 'modules' | 'security' | 'storage' | 'about'
const activeTab = ref<SettingsTab>('llm')

// Sub-components
<LLMSettings v-if="activeTab === 'llm'" />
<VisualsSettings v-else-if="activeTab === 'appearance'" />
```

**LLMSettings.vue (1,009 lines)**
- Provider registry management
- API key configuration
- Model selection per domain
- Agent model mapping
- Cloud search (Perplexity) configuration

**Orchestr8 Equivalent Need:**
- Font profile selection (`ui.general.font_profile`)
- Code City configuration
- Output limits

### 4.2 Panel Patterns

| Panel Type | Component | Behavior |
|------------|-----------|----------|
| **Slide-down** | DomainAgentBar | Agents panel from top |
| **Slide-right** | TasksPanel | Task list from right |
| **Overlay** | TaskFocusOverlay | Full-focus modal |
| **Terminal** | NexusTerminal | Command interface |

### 4.3 Overlay Patterns

**TaskFocusOverlay.vue (730 lines)**
- 95% obsidian backdrop with blur
- Central card with DecoWindow container
- Mission gates (completion requirements)
- Agent subscription/chat
- Follow-up task definition

**SummonResultCard.vue**
- Search results overlay
- Agent chat launcher
- Cloud search integration

### 4.4 Container Patterns

**DecoWindow.vue (87 lines)** — Universal container
```vue
<div class="deco-window chrome-bevel">
  <div class="deco-header">
    <div class="deco-gem"></div>
    <span class="title-text">{{ title }}</span>
  </div>
  <div class="deco-content">
    <slot />
  </div>
</div>
```

---

## 5. TAURI-NATIVE VS BROWSER-BASED ANALYSIS

### 5.1 Tauri-Native Components

**Direct Tauri API Usage:**

| API | Components | Purpose |
|-----|------------|---------|
| `@tauri-apps/api/core` invoke() | MaestroView, PlaybackView, Generator | Audio, shell commands |
| `@tauri-apps/plugin-fs` | FileExplorer, useSummon | File read/write |
| `@tauri-apps/plugin-shell` | NexusTerminal | Command execution |
| `@tauri-apps/plugin-http` | Generator providers | HTTP requests |
| `@tauri-apps/api/path` | FileExplorer | Path resolution |
| `@tauri-apps/api/event` | PlaybackView, AudioBridge | Event listeners |

**Pattern:**
```typescript
// Dynamic import for SSR compatibility
const { invoke } = await import('@tauri-apps/api/core')
await invoke('audio_start')
```

### 5.2 Browser Fallback Pattern

**useFileSystem.ts:**
```typescript
function isTauriAvailable(): boolean {
  return typeof window !== 'undefined' && 
    ('__TAURI__' in window || '__TAURI_INTERNALS__' in window);
}

async function navigate(path: string) {
  if (!isTauriAvailable()) {
    // Mock data for browser mode
    entries.value = [...mockData]
    return
  }
  // Real Tauri implementation
  const dirEntries = await readDir(resolved)
}
```

### 5.3 Orchestr8 Implication

| Collabkit Feature | Tauri Dependency | Orchestr8 Status |
|-------------------|------------------|------------------|
| File Explorer | @tauri-apps/plugin-fs | Python fallback needed |
| Terminal | @tauri-apps/plugin-shell | May not be needed |
| Audio Recording | invoke('audio_start') | Future feature |
| Calendar | Tauri calendar API | Future feature |

---

## 6. COMPOSABLES ARCHITECTURE

### 6.1 Platform Layer (`/platform/`)

| Composable | Lines | Tauri Usage | Purpose |
|------------|-------|-------------|---------|
| useFileSystem.ts | 72 | plugin-fs | File navigation |
| useTerminal.ts | 81 | plugin-shell | Command execution |
| usePreferences.ts | 108 | invoke | Settings storage |
| useSecrets.ts | 72 | invoke | API key management |
| useStorage.ts | 206 | invoke | Persistent storage |
| useHttp.ts | 50 | plugin-http | HTTP client |
| useNavigation.ts | 100 | - | Route management |
| useDecisionGate.ts | 200 | invoke | Task gates |
| useFileGuardian.ts | 225 | invoke | File protection |

### 6.2 Business Logic (`/composables/`)

| Composable | Lines | Purpose |
|------------|-------|---------|
| useSummon.ts | 300 | Search/summon UI |
| useCloudSearch.ts | 300 | Perplexity integration |
| useCalendar.ts | 550 | Calendar sync |
| useP2P.ts | 600 | Peer-to-peer |

### 6.3 Orchestr8 Parallel

| Collabkit Composable | Orchestr8 Equivalent | Gap |
|---------------------|---------------------|-----|
| useFileSystem | `IP/woven_maps.py` file ops | Python/JS bridge |
| useTerminal | Not needed | N/A |
| useNavigation | `06_maestro.py` routing | Needs expansion |
| useCloudSearch | Future feature | Perplexity integration |

---

## 7. INTEGRATION VECTORS FOR ORCHESTR8

### 7.1 HIGH-VALUE PATTERNS

| Pattern | Source Component | Complexity | Priority |
|---------|-----------------|------------|----------|
| **Bottom control surface** | MaestroView | High | P0 |
| **Panel slide animations** | MaestroView | Medium | P0 |
| **Breadcrumb navigation** | FileExplorer | Medium | P1 |
| **Settings tab system** | SettingsView | Medium | P1 |
| **Task focus overlay** | TaskFocusOverlay | High | P2 |
| **File selection model** | FileExplorer | Medium | P2 |

### 7.2 SPECIFIC COMPONENT MAPPINGS

| Orchestr8 Need | Collabkit Source | Adaptation |
|---------------|------------------|------------|
| File browser | FileExplorer.vue | Python-based with JS bridge |
| Settings panel | SettingsView.vue | Marimo tab layout |
| Terminal (optional) | NexusTerminal.vue | Not needed for v1 |
| Task cards | BusinessTaskCard.vue | Agent task display |
| Agent chat | AgentChatPanel.vue | LLM chat interface |

### 7.3 EMERGENCE ANIMATIONS

**MaestroView CSS:**
```css
.emerge-enter-active {
  transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
}
.emerge-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
```

**Orchestr8 Equivalent:** Use CSS transitions in Marimo output containers

---

## 8. RECOMMENDATIONS

### 8.1 Immediate Integration Candidates

1. **Settings tab system** — Adapt SettingsView tab architecture for Orchestr8 configuration
2. **Bottom control surface** — Implement fixed command bar with button groups
3. **Panel transitions** — Add slide-down/slide-right CSS animations
4. **Breadcrumb component** — Create file path navigation for Code City

### 8.2 Future Integration Candidates

1. **FileExplorer with Python backend** — Bridge to Python file operations
2. **LLM chat interface** — Agent conversation panel
3. **Task focus overlay** — Deep work mode

### 8.3 NOT RECOMMENDED FOR ORCHESTR8

1. **NexusTerminal** — Orchestr8 doesn't need shell access
2. **Audio recording** — Future feature, not MVP
3. **Calendar integration** — Future feature

---

## 9. FILE LOCATIONS

### Source Components
```
/home/bozertron/JFDI - Collabkit/Application/src/
├── components/
│   ├── FileExplorer.vue (504)
│   ├── TaskFocusOverlay.vue (730)
│   ├── NexusTerminal.vue (207)
│   ├── DecoWindow.vue (87)
│   ├── DomainAgentBar.vue
│   ├── TasksPanel.vue
│   ├── AgentChatPanel.vue
│   └── SummonResultCard.vue
├── modules/
│   ├── maestro/MaestroView.vue (1194)
│   ├── settings/SettingsView.vue (818)
│   └── settings/LLMSettings.vue (1009)
├── platform/
│   ├── useFileSystem.ts (72)
│   ├── useTerminal.ts (81)
│   └── [8 other composables]
└── composables/
    ├── useSummon.ts (300)
    ├── useCloudSearch.ts (300)
    └── [3 other composables]
```

### Target
```
/home/bozertron/Orchestr8_jr/
├── IP/plugins/06_maestro.py
├── IP/styles/orchestr8.css
└── IP/woven_maps.py
```

---

## 10. COLOR SYSTEM REFERENCE

| Name | Hex | Usage |
|------|-----|-------|
| **gold-metallic** | #D4AF37 | Primary highlight, buttons |
| **gold-dark** | #B8860B | Secondary, Maestro default |
| **gold-saffron** | #F4C430 | Hover states, emphasis |
| **blue-dominant** | #1fbdea | Default UI, links |
| **bg-primary** | #0A0A0B | The Void (background) |
| **bg-elevated** | #121214 | Surface, cards |

---

*End of Mapping*
