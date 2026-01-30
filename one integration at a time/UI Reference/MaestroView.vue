<script setup lang="ts">
/**
 * MaestroView - The Void
 *
 * stereOS home: maestro overlooks the abyss.
 *
 * Top Row: stereOS (home) | Collabor8 (agents) | JFDI (tasks) | Gener8 (generator)
 * Center: maestro identity with soundwave (settings portal)
 * Bottom 5th: Control surface with "maestro" centered
 *
 * Colors (EXACT - NO EXCEPTIONS):
 * --blue-dominant: #1fbdea (UI default)
 * --gold-metallic: #D4AF37 (UI highlight)
 * --gold-dark: #B8860B (Maestro default)
 * --gold-saffron: #F4C430 (Maestro highlight)
 * --bg-primary: #0A0A0B (The Void)
 * --bg-elevated: #121214 (Surface)
 *
 * NO breathing animations. NO emojis. NO clock.
 */

import { ref, computed, onMounted, onUnmounted, inject, nextTick } from 'vue'
import { useProvider, type DomainAgent } from '../../llm'
import DomainAgentBar from '../../components/DomainAgentBar.vue'
import TasksPanel from '../../components/TasksPanel.vue'
import AgentChatPanel from '../../components/AgentChatPanel.vue'
import SummonResultCard from '../../components/SummonResultCard.vue'
import HollowDiamond from '../../components/HollowDiamond.vue'
import TaskFocusOverlay from '../../components/TaskFocusOverlay.vue'
import FileExplorer from '../../components/FileExplorer.vue'
import NexusTerminal from '../../components/NexusTerminal.vue'
import { useSummon, type SummonResult } from '../../composables/useSummon'
import { useTasks, type Task } from '../../llm/tasks'
import { useNavigation } from '@/platform/useNavigation'
import { useCloudSearch } from '../../composables/useCloudSearch'

// LLM provider
const { isLoading, complete } = useProvider('maestro')

// Navigation
const switchModule = inject<(id: string) => void>('switchModule')
const { openSettingsAt } = useNavigation()

// Panel visibility
const showAgentsPanel = ref(false)
const showTasksPanel = ref(false)
const showAgentChat = ref(false)
const selectedAgent = ref<DomainAgent | null>(null)
const focusedTask = ref<Task | null>(null)
const chatTaskId = ref<string | null>(null)
const isRecording = ref(false)
const showFileExplorer = ref(false)
const selectedFiles = ref<string[]>([])
const showTerminal = ref(false)
const showAppGrid = ref(false)

// Chat input state
const userInput = ref('')
const inputRef = ref<HTMLTextAreaElement | null>(null)

// Conversation state
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}
const messages = ref<Message[]>([])

// Summon from Void
const { state: summonState, summon, clearResults } = useSummon()
const showSummonResults = ref(false)

// Cloud Search
const { state: cloudSearchState, search: cloudSearch, init: initCloudSearch } = useCloudSearch()

// ─────────────────────────────────────────────────────────────────────────────
// TOP ROW ACTIONS
// ─────────────────────────────────────────────────────────────────────────────

function handleStereoSClick() {
  // Already home - clear any state
  messages.value = []
  showAgentsPanel.value = false
  showTasksPanel.value = false
}

function toggleCollabor8() {
  showAgentsPanel.value = !showAgentsPanel.value
  if (showAgentsPanel.value) {
    showTasksPanel.value = false
  }
}

function toggleJFDI() {
  showTasksPanel.value = !showTasksPanel.value
  if (showTasksPanel.value) {
    showAgentsPanel.value = false
  }
}

function openGener8() {
  switchModule?.('generator')
}

// ─────────────────────────────────────────────────────────────────────────────
// SETTINGS PORTAL (Soundwave click)
// ─────────────────────────────────────────────────────────────────────────────

function openSettings() {
  switchModule?.('settings')
}

// ─────────────────────────────────────────────────────────────────────────────
// BOTTOM 5TH CONTROL ACTIONS
// ─────────────────────────────────────────────────────────────────────────────

function toggleAppGrid() {
  showAppGrid.value = !showAppGrid.value
}

function handleCalendarClick() {
  console.log('[Maestro] Calendar feature coming soon')
  openSettingsAt('roadmap')
}

function handleCommsClick() {
  console.log('[Maestro] Comms feature coming soon')
  openSettingsAt('roadmap')
}

async function handleSearch() {
  // Open summon overlay
  showSummonResults.value = true
}

function handleFilesClick() {
  showFileExplorer.value = true
}

function handleRecordClick() {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

async function startRecording() {
  try {
    const { invoke } = await import('@tauri-apps/api/core')
    await invoke('audio_start')
    isRecording.value = true
    console.log('[Maestro] Recording started')
  } catch (error) {
    console.error('[Maestro] Failed to start recording:', error)
  }
}

async function stopRecording() {
  try {
    const { invoke } = await import('@tauri-apps/api/core')
    await invoke('audio_stop')
    isRecording.value = false
    console.log('[Maestro] Recording stopped')
  } catch (error) {
    console.error('[Maestro] Failed to stop recording:', error)
  }
}

function handlePlaybackClick() {
  console.log('[Maestro] Playback feature coming soon')
  openSettingsAt('roadmap')
}

function handlePhreakClick() {
  showTerminal.value = true
}

async function handleSendClick() {
  const text = userInput.value.trim()
  if (!text) return

  // Add user message
  messages.value.push({
    id: crypto.randomUUID(),
    role: 'user',
    content: text,
    timestamp: new Date()
  })

  userInput.value = ''

  try {
    // Get response from LLM
    const response = await complete([
      { role: 'system', content: 'You are maestro, the conductor of stereOS. Help the user accomplish their goals.' },
      ...messages.value.map(m => ({ role: m.role, content: m.content }))
    ])

    // Add assistant response - this will emerge from the void
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'assistant',
      content: response,
      timestamp: new Date()
    })
  } catch (error) {
    console.error('[Maestro] Failed to get response:', error)
  }
}

function handleInputKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSendClick()
  }
}

function handleAttachClick() {
  showFileExplorer.value = true
}

// Center maestro button - summon action
function handleMaestroClick() {
  showSummonResults.value = true
}

// ─────────────────────────────────────────────────────────────────────────────
// PANEL & OVERLAY HANDLERS
// ─────────────────────────────────────────────────────────────────────────────

function handleAgentSelect(agent: DomainAgent) {
  if (agent.status === 'offline') {
    openSettingsAt('llm-diagnostics')
    showAgentsPanel.value = false
    return
  }
  selectedAgent.value = agent
  chatTaskId.value = null
  showAgentChat.value = true
  showAgentsPanel.value = false
  console.log('[Maestro] Selected agent:', agent.name)
}

function handleTaskFocus(task: Task) {
  focusedTask.value = task
  showTasksPanel.value = false
  console.log('[Maestro] Focusing task:', task.title)
}

function handleAgentThrowToChat(agent: DomainAgent, taskId?: string) {
  chatTaskId.value = taskId || null
  selectedAgent.value = agent
  showAgentChat.value = true
  showAgentsPanel.value = false
  console.log('[Maestro] Agent thrown to chat:', agent.name)
}

function closeAgentChat() {
  showAgentChat.value = false
  selectedAgent.value = null
}

function handleFileSelect(files: string[]) {
  files.forEach(file => {
    if (!selectedFiles.value.includes(file)) {
      selectedFiles.value.push(file)
    }
  })
  showFileExplorer.value = false
}

function removeFile(index: number) {
  selectedFiles.value.splice(index, 1)
}

function handleTerminalCopy(content: string) {
  console.log('[Maestro] Terminal content copied:', content.substring(0, 50))
  showTerminal.value = false
}

function handleTaskDisperse(taskId: string) {
  console.log('[Maestro] Task dispersed:', taskId)
  focusedTask.value = null
}

function handleSummonDismiss() {
  showSummonResults.value = false
  clearResults()
}

function handleSummonOpen(result: SummonResult) {
  console.log('[Maestro] Open result:', result)
  showSummonResults.value = false
  clearResults()
}

function handleSummonDropIntoChat(result: SummonResult) {
  console.log('[Maestro] Result dropped:', result.title)
  showSummonResults.value = false
  clearResults()
}

function handleSummonOpenAgentChat(agentId: string, agentName: string) {
  console.log('[Maestro] Opening agent chat:', agentId, agentName)
  // Find the agent in the domain agents list
  // For now, create a temporary agent object - this will be replaced with proper lookup
  selectedAgent.value = {
    id: agentId,
    name: agentName,
    domain: 'general',
    status: 'online',
    model: '',
    provider: '',
    systemPrompt: `You are ${agentName}, a helpful assistant.`,
  } as any
  chatTaskId.value = null
  showAgentChat.value = true
  showSummonResults.value = false
  clearResults()
}

async function handleCloudSearch(query: string) {
  console.log('[Maestro] Cloud search for:', query)
  showSummonResults.value = false
  clearResults()

  // Show searching message
  messages.value.push({
    id: crypto.randomUUID(),
    role: 'assistant',
    content: `Searching the cloud for "${query}"...`,
    timestamp: new Date()
  })

  try {
    const results = await cloudSearch(query)

    if (results.length > 0) {
      // Format results as a message
      const resultText = results.map(r =>
        `**${r.title}**\n${r.snippet}\n[${r.url}](${r.url})`
      ).join('\n\n---\n\n')

      messages.value.push({
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Found ${results.length} result(s) via ${cloudSearchState.value.source}:\n\n${resultText}`,
        timestamp: new Date()
      })
    } else {
      messages.value.push({
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `No results found for "${query}". Try different search terms.`,
        timestamp: new Date()
      })
    }
  } catch (error) {
    messages.value.push({
      id: crypto.randomUUID(),
      role: 'assistant',
      content: `Cloud search error: ${error}. Configure Perplexity API in Settings for better results.`,
      timestamp: new Date()
    })
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// GLOBAL KEYBOARD SHORTCUTS
// ─────────────────────────────────────────────────────────────────────────────

function handleGlobalKeydown(e: KeyboardEvent) {
  // Cmd/Ctrl + T: Toggle Tasks (JFDI)
  if ((e.metaKey || e.ctrlKey) && e.key === 't') {
    e.preventDefault()
    toggleJFDI()
  }

  // Cmd/Ctrl + A: Toggle Agents (Collabor8)
  if ((e.metaKey || e.ctrlKey) && e.key === 'a') {
    e.preventDefault()
    toggleCollabor8()
  }

  // Cmd/Ctrl + G: Open Generator (Gener8)
  if ((e.metaKey || e.ctrlKey) && e.key === 'g') {
    e.preventDefault()
    openGener8()
  }

  // Cmd/Ctrl + ,: Open Settings
  if ((e.metaKey || e.ctrlKey) && e.key === ',') {
    e.preventDefault()
    openSettings()
  }

  // /: Open Summon
  if (e.key === '/') {
    e.preventDefault()
    showSummonResults.value = true
  }

  // Escape: Hierarchy dismissal
  if (e.key === 'Escape') {
    if (focusedTask.value) {
      focusedTask.value = null
    } else if (isRecording.value) {
      stopRecording()
    } else if (showAgentChat.value) {
      closeAgentChat()
    } else if (showTasksPanel.value) {
      showTasksPanel.value = false
    } else if (showAgentsPanel.value) {
      showAgentsPanel.value = false
    } else if (showSummonResults.value) {
      handleSummonDismiss()
    } else if (showTerminal.value) {
      showTerminal.value = false
    } else if (showFileExplorer.value) {
      showFileExplorer.value = false
    }
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// LIFECYCLE
// ─────────────────────────────────────────────────────────────────────────────

onMounted(async () => {
  window.addEventListener('keydown', handleGlobalKeydown)
  // Initialize cloud search (loads Perplexity API key if configured)
  await initCloudSearch()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<template>
  <div class="maestro-void">
    <!-- ═══════════════════════════════════════════════════════════════════════
         TOP ROW - Fixed position
         stereOS (left) | Collabor8 | JFDI | Gener8 (right)
         ═══════════════════════════════════════════════════════════════════════ -->
    <div class="top-row">
      <button class="top-btn stereos-btn" @click="handleStereoSClick">
        <span class="stereos-text"><span class="stereos-prefix">stere</span>OS</span>
      </button>

      <div class="top-actions">
        <button
          class="top-btn"
          :class="{ active: showAgentsPanel }"
          @click="toggleCollabor8"
        >
          Collabor8
        </button>
        <button
          class="top-btn"
          :class="{ active: showTasksPanel }"
          @click="toggleJFDI"
        >
          JFDI
        </button>
        <button
          class="top-btn"
          @click="openGener8"
        >
          Gener8
        </button>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         PANELS - Emergence pattern
         ═══════════════════════════════════════════════════════════════════════ -->

    <!-- Agents Panel (slides down) -->
    <Transition name="slide-down">
      <div v-if="showAgentsPanel" class="agents-panel">
        <DomainAgentBar
          @select="handleAgentSelect"
          @throw-to-chat="handleAgentThrowToChat"
        />
        <button class="panel-dismiss" @click="showAgentsPanel = false" aria-label="Dismiss">
          <HollowDiamond :size="14" hoverable />
        </button>
      </div>
    </Transition>

    <!-- Tasks Panel (slides from right) -->
    <Transition name="slide-right">
      <div v-if="showTasksPanel" class="tasks-panel-overlay" @click.self="showTasksPanel = false">
        <div class="tasks-panel">
          <TasksPanel
            @close="showTasksPanel = false"
            @focus="handleTaskFocus"
          />
        </div>
      </div>
    </Transition>

    <!-- Task Focus Overlay -->
    <Transition name="fade">
      <TaskFocusOverlay
        v-if="focusedTask"
        :task="focusedTask"
        @close="focusedTask = null"
        @disperse="handleTaskDisperse"
        @throw-to-chat="handleAgentThrowToChat"
      />
    </Transition>

    <!-- Agent Chat Panel -->
    <Transition name="slide-right">
      <div v-if="showAgentChat && selectedAgent" class="agent-chat-overlay" @click.self="closeAgentChat">
        <AgentChatPanel
          :agent="selectedAgent"
          :task-id="chatTaskId ?? undefined"
          @close="closeAgentChat"
          @minimize="closeAgentChat"
        />
      </div>
    </Transition>

    <!-- File Explorer -->
    <FileExplorer
      :visible="showFileExplorer"
      @close="showFileExplorer = false"
      @select="handleFileSelect"
    />

    <!-- Nexus Terminal -->
    <NexusTerminal
      :visible="showTerminal"
      @close="showTerminal = false"
      @copy="handleTerminalCopy"
    />

    <!-- Summon Results -->
    <SummonResultCard
      :visible="showSummonResults"
      :results="summonState.results"
      :query="summonState.query"
      :isSearching="summonState.isSearching"
      @dismiss="handleSummonDismiss"
      @open="handleSummonOpen"
      @dropIntoChat="handleSummonDropIntoChat"
      @openAgentChat="handleSummonOpenAgentChat"
      @searchCloud="handleCloudSearch"
    />

    <!-- ═══════════════════════════════════════════════════════════════════════
         THE VOID - maestro overlooks the abyss
         Pure collaboration space - no permanent UI elements
         ═══════════════════════════════════════════════════════════════════════ -->
    <div class="void-center">
      <!-- Void Collaboration Area - only LLM responses emerge here -->

      <!-- Void Emergence - LLM messages emerge here -->
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
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         BOTTOM 5TH - The Overton anchor
         Full-width command center: chat input + control surface
         "The Input Bar: Docked at the bottom 5th. It NEVER moves."
         ═══════════════════════════════════════════════════════════════════════ -->
    <div class="bottom-fifth">
      <!-- Attachment Bar (when files selected) -->
      <Transition name="fade">
        <div v-if="selectedFiles.length > 0" class="attachment-bar">
          <div
            v-for="(file, index) in selectedFiles"
            :key="file"
            class="attachment-chip"
          >
            <span class="chip-name">{{ file.split(/[/\\]/).pop() }}</span>
            <button class="chip-remove" @click="removeFile(index)">x</button>
          </div>
        </div>
      </Transition>

      <!-- Chat Input - Full Width -->
      <div class="chat-input-container">
        <textarea
          ref="inputRef"
          v-model="userInput"
          class="chat-input"
          placeholder="What would you like to accomplish?"
          rows="1"
          @keydown="handleInputKeydown"
        ></textarea>
      </div>

      <!-- Control Surface - Responsive Button Distribution -->
      <div class="control-surface">
        <!-- Single Row: Left Group | Center (maestro) | Right Group -->
        <div class="control-row">
          <!-- Left Group -->
          <div class="control-group control-left">
            <button class="ctrl-btn apps-btn" :class="{ active: showAppGrid }" @click="toggleAppGrid">
              Apps
            </button>
            <button class="ctrl-btn matrix-btn" @click="openSettingsAt('llm-diagnostics')">
              Matrix
            </button>
            <button class="ctrl-btn" @click="handleCalendarClick" disabled>
              Calendar
            </button>
            <button class="ctrl-btn" @click="handleCommsClick" disabled>
              Comms
            </button>
            <button class="ctrl-btn" @click="handleFilesClick">
              Files
            </button>
          </div>

          <!-- Center: maestro -->
          <button class="maestro-center" @click="handleMaestroClick">
            maestro
          </button>

          <!-- Right Group -->
          <div class="control-group control-right">
            <button class="ctrl-btn" @click="handleSearch" :class="{ active: showSummonResults }">
              Search
            </button>
            <button class="ctrl-btn" :class="{ active: isRecording }" @click="handleRecordClick">
              Record
            </button>
            <button class="ctrl-btn" @click="handlePlaybackClick" disabled>
              Playback
            </button>
            <button class="ctrl-btn" @click="handlePhreakClick">
              Phreak>
            </button>
            <button class="ctrl-btn send-btn" @click="handleSendClick">
              Send
            </button>
            <button class="ctrl-btn attach-btn" @click="handleAttachClick">
              Attach
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings Portal - Above Bottom Fifth, Right Side -->
    <button class="settings-portal-corner" @click="openSettings" aria-label="Open Settings">
      <span class="wave-bar"></span>
      <span class="wave-bar"></span>
      <span class="wave-bar"></span>
      <span class="wave-bar"></span>
      <span class="wave-bar"></span>
    </button>
  </div>
</template>

<style scoped>
/* ═══════════════════════════════════════════════════════════════════════════
   THE VOID - Pure obsidian foundation
   EXACT COLORS - NO EXCEPTIONS
   --bg-primary: #0A0A0B
   --bg-elevated: #121214
   --blue-dominant: #1fbdea
   --gold-metallic: #D4AF37
   --gold-dark: #B8860B
   --gold-saffron: #F4C430
   ═══════════════════════════════════════════════════════════════════════════ */

.maestro-void {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #0A0A0B;
  position: relative;
  min-height: 0;
  overflow: hidden;
}

/* ═══════════════════════════════════════════════════════════════════════════
   TOP ROW
   ═══════════════════════════════════════════════════════════════════════════ */

.top-row {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
}

.stereos-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
}

.stereos-text {
  font-family: var(--font-headline);
  font-size: 14px;
  letter-spacing: 0.08em;
  color: #D4AF37;
}

.stereos-prefix {
  color: #1fbdea;
}

.top-actions {
  display: flex;
  gap: 8px;
}

.top-btn {
  padding: 5px 12px;
  border-radius: 4px;
  background: #121214;
  border: 1px solid rgba(31, 189, 234, 0.3);
  color: #1fbdea;
  font-family: var(--font-headline);
  font-size: 10px;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 200ms ease-out;
}

.top-btn:hover,
.top-btn.active {
  background: rgba(212, 175, 55, 0.1);
  border-color: #D4AF37;
  color: #D4AF37;
}

/* ═══════════════════════════════════════════════════════════════════════════
   THE VOID CENTER - Pure collaboration space
   No permanent UI elements - only LLM responses emerge here
   ═══════════════════════════════════════════════════════════════════════════ */

.void-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 80px 20px 200px;
}

/* Wave bar styles for settings portal */
.wave-bar {
  width: 3px;
  background: #1fbdea;
  transition: all 200ms ease-out;
}

.wave-bar:nth-child(1) { height: 10px; }
.wave-bar:nth-child(2) { height: 18px; }
.wave-bar:nth-child(3) { height: 28px; }
.wave-bar:nth-child(4) { height: 18px; }
.wave-bar:nth-child(5) { height: 10px; }

/* Settings Portal - Positioned above Bottom Fifth */
.settings-portal-corner {
  position: fixed;
  bottom: 180px;
  right: 24px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 3px;
  height: 40px;
  padding: 8px 12px;
  background: rgba(18, 18, 20, 0.9);
  border: 1px solid rgba(31, 189, 234, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 200ms ease-out;
}

.settings-portal-corner:hover {
  background: rgba(31, 189, 234, 0.15);
  border-color: rgba(31, 189, 234, 0.5);
  transform: scale(1.05);
}

.settings-portal-corner:hover .wave-bar {
  background: #D4AF37;
}

/* ═══════════════════════════════════════════════════════════════════════════
   VOID EMERGENCE - LLM messages emerge from the void
   "UI elements do not 'load'; they EMERGE from the void when summoned."
   ═══════════════════════════════════════════════════════════════════════════ */

.void-emergence {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  max-width: 700px;
  margin-top: 32px;
}

.emerged-message {
  padding: 16px 20px;
  background: rgba(18, 18, 20, 0.9);
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}

.message-content {
  color: #e8e8e8;
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.message-meta {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.message-time {
  font-family: var(--font-mono);
  font-size: 10px;
  color: #B8860B;
}

/* Emerge transition */
.emerge-enter-active {
  transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

.emerge-leave-active {
  transition: all 300ms ease-out;
}

.emerge-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.emerge-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}

.emerge-move {
  transition: transform 400ms ease-out;
}

/* ═══════════════════════════════════════════════════════════════════════════
   BOTTOM 5TH - The Overton anchor
   Full width (left edge to right edge), 20vh height
   "The Input Bar: Docked at the bottom 5th. It NEVER moves."
   ═══════════════════════════════════════════════════════════════════════════ */

.bottom-fifth {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 20;
  padding: 12px 20px 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
  background: linear-gradient(to top, #0A0A0B 80%, transparent);
}

/* Chat Input - Full Width */
.chat-input-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.chat-input {
  width: 100%;
  padding: 12px 16px;
  background: #121214;
  border: 1px solid rgba(31, 189, 234, 0.3);
  border-radius: 6px;
  color: #e8e8e8;
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.4;
  resize: none;
  min-height: 44px;
  max-height: 120px;
  transition: border-color 200ms ease-out;
}

.chat-input:focus {
  outline: none;
  border-color: #D4AF37;
}

.chat-input::placeholder {
  color: #666;
}

/* Attachment Bar */
.attachment-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 16px;
  background: #121214;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 6px;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}

.attachment-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 10px;
  color: #D4AF37;
}

.chip-name {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chip-remove {
  background: transparent;
  border: none;
  color: #D4AF37;
  font-size: 12px;
  cursor: pointer;
  padding: 0 2px;
  opacity: 0.6;
}

.chip-remove:hover {
  opacity: 1;
}

/* Control Surface - Edge to Edge (Overton Anchor) */
.control-surface {
  width: 100%;
  background: #121214;
  border-top: 1px solid rgba(31, 189, 234, 0.2);
  border-radius: 0;
  padding: 12px 24px;
}

/* Single Responsive Row */
.control-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

/* Button Groups - Responsive with auto-sizing */
.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.control-left {
  justify-content: flex-start;
}

.control-right {
  justify-content: flex-end;
}

/* Control Buttons */
.ctrl-btn {
  padding: 6px 12px;
  background: transparent;
  border: none;
  color: #1fbdea;
  font-family: var(--font-headline);
  font-size: 10px;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.ctrl-btn:hover {
  color: #D4AF37;
}

.ctrl-btn.active {
  color: #D4AF37;
}

.ctrl-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.ctrl-btn:disabled:hover {
  color: #1fbdea;
}

/* Apps button */
.apps-btn {
  background: rgba(31, 189, 234, 0.1);
  border-radius: 4px;
}

/* Matrix button (diagnostics) */
.matrix-btn {
  background: rgba(31, 189, 234, 0.1);
  border-radius: 4px;
  color: #1fbdea;
}

.matrix-btn:hover {
  background: rgba(212, 175, 55, 0.15);
  color: #D4AF37;
}

/* Send button */
.send-btn {
  background: rgba(212, 175, 55, 0.15);
  border-radius: 4px;
  color: #D4AF37;
}

.send-btn:hover {
  background: rgba(212, 175, 55, 0.25);
  color: #F4C430;
}

/* Attach button */
.attach-btn {
  background: rgba(31, 189, 234, 0.1);
  border-radius: 4px;
}

.attach-btn:hover {
  background: rgba(31, 189, 234, 0.2);
}

/* Center maestro text - with buffer around it */
.maestro-center {
  padding: 10px 32px;
  margin: 0 16px;
  background: none;
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-radius: 4px;
  color: #B8860B;
  font-family: var(--font-headline);
  font-size: 14px;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 200ms ease-out;
  flex-shrink: 0;
}

.maestro-center:hover {
  color: #F4C430;
  border-color: rgba(244, 196, 48, 0.4);
  background: rgba(184, 134, 11, 0.1);
}

/* ═══════════════════════════════════════════════════════════════════════════
   PANELS - Emergence pattern
   ═══════════════════════════════════════════════════════════════════════════ */

/* Agents Panel (slides down from top) */
.agents-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  background: linear-gradient(to bottom, #0A0A0B, rgba(10, 10, 11, 0.95));
  border-bottom: 1px solid rgba(31, 189, 234, 0.2);
  padding: 12px 20px;
}

.panel-dismiss {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px;
  background: none;
  border: none;
  cursor: pointer;
}

/* Tasks Panel (slides from right) */
.tasks-panel-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 11, 0.8);
  display: flex;
  justify-content: flex-end;
  z-index: 45;
}

.tasks-panel {
  width: 320px;
  height: 100%;
  background: #0A0A0B;
  border-left: 1px solid rgba(31, 189, 234, 0.2);
}

/* Agent Chat Panel */
.agent-chat-overlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 11, 0.8);
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 40px;
  z-index: 50;
}

.agent-chat-overlay > * {
  width: 400px;
  max-height: 80vh;
}

/* ═══════════════════════════════════════════════════════════════════════════
   TRANSITIONS
   ═══════════════════════════════════════════════════════════════════════════ */

.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 300ms ease-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 300ms ease-out;
}

.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms ease-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
