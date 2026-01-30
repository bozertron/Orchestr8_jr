<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'

import DecoWindow from './DecoWindow.vue'
import HollowDiamond from './HollowDiamond.vue'
import { useFileSystem, type FileInfo } from '@/platform/useFileSystem'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits(['close', 'select'])

// Filesystem state
const { currentPath, entries, isLoading, error, navigate } = useFileSystem()
const selectedPaths = ref<Set<string>>(new Set())

const breadcrumbs = computed(() => {
  if (!currentPath.value) return []
  const parts = currentPath.value.split(/[/\\]/).filter(Boolean)
  const isAbsolute = currentPath.value.startsWith('/') || currentPath.value.startsWith('\\')
  
  const crumbs: { name: string; path: string }[] = []
  let acc = ''
  
  if (isAbsolute && !currentPath.value.includes(':')) {
    acc = '/'
  }

  parts.forEach((part) => {
    if (acc === '/' || acc === '') acc = acc + part
    else acc = acc + '/' + part
    crumbs.push({ name: part, path: acc })
  })
  
  return crumbs
})

const locations = [
  { name: 'HOME', icon: '◇', path: '~' },
  { name: 'DOCUMENTS', icon: '◇', path: 'Documents' },
  { name: 'DOWNLOADS', icon: '◇', path: 'Downloads' },
  { name: 'APP STORAGE', icon: '💾', path: 'APP_STORAGE' }
]

const activeLocation = ref('HOME')

function navigateTo(path: string) {
  selectedPaths.value.clear()
  navigate(path)
}

function handleItemClick(event: MouseEvent, item: FileInfo) {
  if (event.metaKey || event.ctrlKey) {
    if (selectedPaths.value.has(item.path)) {
      selectedPaths.value.delete(item.path)
    } else {
      selectedPaths.value.add(item.path)
    }
  } else if (event.shiftKey && selectedPaths.value.size > 0) {
    // Basic range selection could go here, but sticking to single/multi for now
    selectedPaths.value.add(item.path)
  } else {
    selectedPaths.value.clear()
    selectedPaths.value.add(item.path)
  }
}

function handleItemDoubleClick(item: FileInfo) {
  if (item.isDirectory) {
    navigateTo(item.path)
  } else {
    emit('select', Array.from(selectedPaths.value))
  }
}

function getIcon(item: FileInfo) {
  if (item.isDirectory) return '📁'
  const ext = item.name.split('.').pop()?.toLowerCase()
  switch (ext) {
    case 'md':
    case 'txt': return '📄'
    case 'js':
    case 'ts':
    case 'vue': return '📜'
    case 'png':
    case 'jpg':
    case 'svg': return '🖼️'
    default: return '◇'
  }
}

function formatSize(bytes?: number) {
  if (bytes === undefined) return '--'
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function formatDate(date?: Date) {
  if (!date) return '--'
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function handleEmitSelect() {
  if (selectedPaths.value.size > 0) {
    emit('select', Array.from(selectedPaths.value))
    selectedPaths.value.clear()
  }
}

function handleClose() {
  emit('close')
}

watch(() => props.visible, (isVisible) => {
  if (isVisible && !currentPath.value) {
    navigateTo('~')
  }
})
onMounted(() => {
  if (props.visible) {
    navigateTo('~')
  }
})
</script>


<template>

  <div v-if="visible" class="file-explorer-overlay" @click.self="handleClose">
    <DecoWindow 
      title="FILE EXPLORER" 
      controls 
      @close="handleClose"
      class="explorer-window emerge"
    >
      <div class="explorer-layout">
        <!-- Sidebar -->
        <aside class="explorer-sidebar">
          <nav class="sidebar-nav">
            <button 
              v-for="loc in locations" 
              :key="loc.name"
              class="nav-item"
              :class="{ active: activeLocation === loc.name }"
              @click="activeLocation = loc.name; navigateTo(loc.path)"
            >
              <span class="nav-icon">{{ loc.icon }}</span>
              <span class="nav-label">{{ loc.name }}</span>
            </button>
          </nav>
        </aside>

        <!-- Main Area -->
        <main class="explorer-main">
          <!-- Breadcrumbs -->
          <header class="explorer-header">
            <div class="breadcrumb-nav">
              <button class="crumb-root" @click="navigateTo('/')">/</button>
              <template v-for="(crumb, index) in breadcrumbs" :key="crumb.path">
                <span class="crumb-separator">></span>
                <button 
                  class="crumb-btn"
                  :class="{ last: index === breadcrumbs.length - 1 }"
                  @click="navigateTo(crumb.path)"
                >
                  {{ crumb.name }}
                </button>
              </template>
            </div>
          </header>

          <!-- File List -->
          <div class="explorer-content">
            <div v-if="isLoading" class="explorer-loading">
              <span class="loading-icon">◇</span>
              <p>ACCESSING VOID...</p>
            </div>
            
            <div v-else-if="error" class="explorer-error">
              <span class="error-icon">⚠️</span>
              <p>{{ error }}</p>
              <button class="reset-btn" @click="navigateTo('~')">RETURN HOME</button>
            </div>

            <div v-else-if="entries.length === 0" class="void-placeholder">
              <span class="placeholder-icon">◇</span>
              <p>DIRECTORY IS EMPTY</p>
            </div>

            <table v-else class="file-table">
              <thead>
                <tr>
                  <th class="col-name">NAME</th>
                  <th class="col-size">SIZE</th>
                  <th class="col-date">MODIFIED</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="item in entries" 
                  :key="item.path"
                  class="file-row"
                  :class="{ selected: selectedPaths.has(item.path) }"
                  @click="handleItemClick($event, item)"
                  @dblclick="handleItemDoubleClick(item)"
                >
                  <td class="col-name">
                    <span class="file-icon">{{ getIcon(item) }}</span>
                    <span class="file-name">{{ item.name }}</span>
                  </td>
                  <td class="col-size">{{ formatSize(item.size) }}</td>
                  <td class="col-date">{{ formatDate(item.modifiedAt) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Explorer Footer -->
          <footer class="explorer-footer">
            <div class="selection-info">
              <span v-if="selectedPaths.size > 0">
                {{ selectedPaths.size }} ITEM{{ selectedPaths.size > 1 ? 'S' : '' }} SELECTED
              </span>
            </div>
            <div class="actions">
              <button 
                class="stereos-btn primary" 
                :disabled="selectedPaths.size === 0"
                @click="handleEmitSelect"
              >
                ADD TO CHAT
              </button>
            </div>
          </footer>
        </main>
      </div>
    </DecoWindow>
  </div>
</template>

<style scoped>
.file-explorer-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(10, 10, 11, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
}

.explorer-window {
  width: 900px;
  height: 600px;
  max-width: 95vw;
  max-height: 90vh;
}

.explorer-layout {
  display: flex;
  height: 100%;
  background: var(--bg-primary);
}

/* Sidebar */
.explorer-sidebar {
  width: 200px;
  border-right: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
  padding: var(--space-md) 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-lg);
  background: transparent;
  border: none;
  border-left: 2px solid transparent;
  color: var(--muted);
  font-family: var(--font-headline);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-align: left;
  cursor: pointer;
  transition: all var(--transition-base);
}

.nav-item:hover {
  background: var(--gold-5);
  color: var(--titanium);
}

.nav-item.active {
  background: var(--gold-10);
  border-left-color: var(--gold);
  color: var(--gold);
}

/* Main Area */
.explorer-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.explorer-header {
  height: 40px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  padding: 0 var(--space-md);
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-family: var(--font-mono);
  font-size: 10px;
  overflow-x: auto;
  white-space: nowrap;
}

.crumb-root, .crumb-btn {
  background: transparent;
  border: none;
  color: var(--muted);
  cursor: pointer;
  padding: 2px 4px;
  transition: color var(--transition-fast);
}

.crumb-root:hover, .crumb-btn:hover {
  color: var(--gold);
}

.crumb-btn.last {
  color: var(--gold);
  pointer-events: none;
}

.crumb-separator {
  color: var(--muted-dim);
  font-size: 8px;
}

.explorer-content {
  flex: 1;
  position: relative;
  overflow: auto;
}

.explorer-footer {
  height: 50px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
  background: var(--bg-elevated);
}

.selection-info {
  font-family: var(--font-headline);
  font-size: 10px;
  color: var(--gold-dim);
  letter-spacing: 0.1em;
}

.actions {
  display: flex;
  gap: var(--space-md);
}

.stereos-btn {
  padding: var(--space-xs) var(--space-xl);
  font-family: var(--font-headline);
  font-size: 10px;
  letter-spacing: 0.15em;
  cursor: pointer;
  transition: all var(--transition-base);
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--muted);
}

.stereos-btn.primary {
  background: var(--gold-10);
  border-color: var(--gold);
  color: var(--gold);
}

.stereos-btn.primary:hover:not(:disabled) {
  background: var(--gold-20);
  box-shadow: 0 0 15px var(--gold-glow);
}

.stereos-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: var(--border-subtle);
  color: var(--muted-dim);
  background: transparent;
}

.explorer-loading, .explorer-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--space-md);
  color: var(--muted);
}

.loading-icon {
  font-size: 2rem;
  animation: rotate 2s linear infinite;
}

.error-icon {
  font-size: 2rem;
  color: var(--status-invalid);
}

.file-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-mono);
  font-size: 11px;
}

.file-table th {
  text-align: left;
  padding: var(--space-sm) var(--space-md);
  color: var(--gold-dim);
  border-bottom: 1px solid var(--border-subtle);
  font-weight: normal;
  letter-spacing: 0.1em;
  position: sticky;
  top: 0;
  background: var(--bg-primary);
  z-index: 10;
}

.file-row {
  cursor: pointer;
  transition: background var(--transition-fast);
  color: var(--muted);
}

.file-row:hover {
  background: var(--gold-5);
  color: var(--titanium);
}

.file-row.selected {
  background: var(--gold-10);
  color: var(--gold);
}

.file-table td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.col-name {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.file-icon {
  font-size: 14px;
}

.col-size, .col-date {
  color: var(--muted-dim);
}

.file-row.selected .col-size,
.file-row.selected .col-date {
  color: var(--gold-dim);
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
