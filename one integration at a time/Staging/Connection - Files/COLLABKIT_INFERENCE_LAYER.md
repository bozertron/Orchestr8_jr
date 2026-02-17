# CollabKit Generator: Inference Layer Specification

## Version: 1.0.0
## Date: 2025-12-20
## Status: Ready for Implementation

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Generator Module UI                          │
│                     (GeneratorView.vue)                             │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      useInference() Composable                      │
│  • Provider management                                              │
│  • Streaming handler                                                │
│  • Error recovery                                                   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│   Cloud Providers        │   │   Local Providers        │
│  ├─ HuggingFace         │   │  ├─ Ollama               │
│  ├─ OpenAI-compatible   │   │  └─ LM Studio            │
│  └─ Anthropic (future)  │   │     (same API)           │
└──────────────────────────┘   └──────────────────────────┘
```

---

## File Structure

```
src/modules/generator/
├── index.ts                    # Module definition
├── GeneratorView.vue           # Main UI
├── components/
│   ├── PromptInput.vue         # Prompt textarea + submit
│   ├── FileViewer.vue          # Generated files display
│   ├── ModelSelector.vue       # Provider/model picker
│   └── SettingsPanel.vue       # Inference settings
├── composables/
│   ├── useInference.ts         # Main inference orchestration
│   ├── useProviders.ts         # Provider management
│   └── useHardwareDetection.ts # Auto-detect capabilities
├── providers/
│   ├── types.ts                # Provider interfaces
│   ├── huggingface.ts          # HuggingFace Inference API
│   ├── ollama.ts               # Local Ollama
│   └── registry.ts             # Provider registration
├── prompts/
│   ├── system.ts               # System prompts
│   └── templates.ts            # Module templates
├── parser/
│   ├── markers.ts              # Marker constants
│   └── extract.ts              # File extraction logic
└── types.ts                    # TypeScript interfaces
```

---

## Provider Interface

```typescript
// src/modules/generator/providers/types.ts

export interface Model {
  id: string;
  name: string;
  provider: string;
  contextLength: number;
  // For local models:
  size?: 'small' | 'medium' | 'large' | 'xlarge';
  ramRequired?: number;  // GB
  vramRequired?: number; // GB (if GPU accelerated)
}

export interface ProviderConfig {
  id: string;
  name: string;
  type: 'cloud' | 'local';
  icon?: string;
  requiresAuth: boolean;
  baseUrl?: string;
}

export interface GenerateParams {
  model: string;
  systemPrompt: string;
  userPrompt: string;
  context?: string[];      // Existing files for context
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  topK?: number;
}

export interface GenerateResult {
  content: string;
  finishReason: 'stop' | 'length' | 'error';
  usage?: {
    promptTokens: number;
    completionTokens: number;
  };
}

export interface InferenceProvider {
  readonly config: ProviderConfig;
  
  // Lifecycle
  isAvailable(): Promise<boolean>;
  initialize?(): Promise<void>;
  
  // Models
  getModels(): Promise<Model[]>;
  
  // Generation
  generate(params: GenerateParams): AsyncIterable<string>;
  generateComplete?(params: GenerateParams): Promise<GenerateResult>;
  
  // Abort
  abort(): void;
}
```

---

## HuggingFace Provider

```typescript
// src/modules/generator/providers/huggingface.ts

import type { InferenceProvider, ProviderConfig, Model, GenerateParams } from './types';

const HF_MODELS: Model[] = [
  {
    id: 'deepseek-ai/DeepSeek-V3-0324',
    name: 'DeepSeek V3',
    provider: 'huggingface',
    contextLength: 64000,
  },
  {
    id: 'deepseek-ai/DeepSeek-V3.2',
    name: 'DeepSeek V3.2',
    provider: 'huggingface',
    contextLength: 64000,
  },
  {
    id: 'Qwen/Qwen3-Coder-480B-A35B-Instruct',
    name: 'Qwen3 Coder 480B',
    provider: 'huggingface',
    contextLength: 32000,
  },
  {
    id: 'moonshotai/Kimi-K2-Instruct',
    name: 'Kimi K2',
    provider: 'huggingface',
    contextLength: 128000,
  },
];

// Inference providers that HuggingFace routes to
const HF_INFERENCE_PROVIDERS = [
  'fireworks-ai',
  'nebius',
  'sambanova',
  'novita',
  'hyperbolic',
  'together',
  'groq',
] as const;

export class HuggingFaceProvider implements InferenceProvider {
  readonly config: ProviderConfig = {
    id: 'huggingface',
    name: 'HuggingFace',
    type: 'cloud',
    icon: '🤗',
    requiresAuth: true,
  };

  private token: string;
  private billTo: string | null;
  private abortController: AbortController | null = null;
  private inferenceProvider: string = 'auto';

  constructor(options: { 
    token: string; 
    billTo?: string;
    inferenceProvider?: string;
  }) {
    this.token = options.token;
    this.billTo = options.billTo ?? null;
    this.inferenceProvider = options.inferenceProvider ?? 'auto';
  }

  async isAvailable(): Promise<boolean> {
    try {
      const res = await fetch('https://huggingface.co/api/whoami-v2', {
        headers: { Authorization: `Bearer ${this.token}` },
      });
      return res.ok;
    } catch {
      return false;
    }
  }

  async getModels(): Promise<Model[]> {
    return HF_MODELS;
  }

  async *generate(params: GenerateParams): AsyncIterable<string> {
    this.abortController = new AbortController();

    // Build model string with provider routing
    const modelString = this.inferenceProvider !== 'auto'
      ? `${params.model}:${this.inferenceProvider}`
      : params.model;

    const messages = [
      { role: 'system', content: params.systemPrompt },
      { role: 'user', content: params.userPrompt },
    ];

    // Add context files if provided
    if (params.context && params.context.length > 0) {
      messages.splice(1, 0, {
        role: 'assistant',
        content: `Current project files:\n${params.context.join('\n\n')}`,
      });
    }

    const response = await fetch('https://api-inference.huggingface.co/models/' + params.model + '/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        ...(this.billTo ? { 'X-Bill-To': this.billTo } : {}),
      },
      body: JSON.stringify({
        model: modelString,
        messages,
        max_tokens: params.maxTokens ?? 16384,
        temperature: params.temperature ?? 0.7,
        top_p: params.topP ?? 0.95,
        stream: true,
      }),
      signal: this.abortController.signal,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new HuggingFaceError(error.message || 'API request failed', error);
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          if (line === 'data: [DONE]') continue;

          try {
            const data = JSON.parse(line.slice(6));
            const content = data.choices?.[0]?.delta?.content;
            if (content) {
              yield content;
            }
          } catch {
            // Skip malformed JSON
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  abort(): void {
    this.abortController?.abort();
    this.abortController = null;
  }
}

export class HuggingFaceError extends Error {
  constructor(
    message: string,
    public readonly details: {
      openLogin?: boolean;
      openProModal?: boolean;
      openSelectProvider?: boolean;
    } = {}
  ) {
    super(message);
    this.name = 'HuggingFaceError';
  }
}
```

---

## Ollama Provider (Local)

```typescript
// src/modules/generator/providers/ollama.ts

import type { InferenceProvider, ProviderConfig, Model, GenerateParams } from './types';

// Models we want to support for CollabKit generation
const RECOMMENDED_MODELS = {
  // Code generation (primary)
  'seedcoder:latest': {
    name: 'Seedcoder (ByteDance)',
    size: 'medium' as const,
    ramRequired: 16,
    contextLength: 32000,
    purpose: 'code',
  },
  // Document understanding
  'dolphin2:latest': {
    name: 'Dolphin 2 (ByteDance)',
    size: 'medium' as const,
    ramRequired: 16,
    contextLength: 32000,
    purpose: 'document',
  },
  // Smaller alternatives
  'deepseek-coder:6.7b': {
    name: 'DeepSeek Coder 6.7B',
    size: 'small' as const,
    ramRequired: 8,
    contextLength: 16000,
    purpose: 'code',
  },
  'codellama:7b': {
    name: 'Code Llama 7B',
    size: 'small' as const,
    ramRequired: 8,
    contextLength: 16000,
    purpose: 'code',
  },
  // Larger alternatives
  'deepseek-coder:33b': {
    name: 'DeepSeek Coder 33B',
    size: 'large' as const,
    ramRequired: 32,
    contextLength: 16000,
    purpose: 'code',
  },
  'qwen2.5-coder:32b': {
    name: 'Qwen 2.5 Coder 32B',
    size: 'large' as const,
    ramRequired: 32,
    contextLength: 32000,
    purpose: 'code',
  },
};

export class OllamaProvider implements InferenceProvider {
  readonly config: ProviderConfig = {
    id: 'ollama',
    name: 'Ollama (Local)',
    type: 'local',
    icon: '🦙',
    requiresAuth: false,
  };

  private baseUrl: string;
  private abortController: AbortController | null = null;

  constructor(baseUrl = 'http://localhost:11434') {
    this.baseUrl = baseUrl;
  }

  async isAvailable(): Promise<boolean> {
    try {
      const res = await fetch(`${this.baseUrl}/api/tags`, {
        signal: AbortSignal.timeout(2000),
      });
      return res.ok;
    } catch {
      return false;
    }
  }

  async getModels(): Promise<Model[]> {
    try {
      const res = await fetch(`${this.baseUrl}/api/tags`);
      if (!res.ok) return [];

      const data = await res.json();
      const installedModels = data.models || [];

      return installedModels.map((m: any) => {
        const recommended = RECOMMENDED_MODELS[m.name as keyof typeof RECOMMENDED_MODELS];
        return {
          id: m.name,
          name: recommended?.name ?? m.name,
          provider: 'ollama',
          contextLength: recommended?.contextLength ?? 8000,
          size: recommended?.size ?? 'medium',
          ramRequired: recommended?.ramRequired ?? 16,
        };
      });
    } catch {
      return [];
    }
  }

  async getRecommendedModels(): Promise<typeof RECOMMENDED_MODELS> {
    return RECOMMENDED_MODELS;
  }

  async pullModel(modelName: string, onProgress?: (progress: number) => void): Promise<void> {
    const res = await fetch(`${this.baseUrl}/api/pull`, {
      method: 'POST',
      body: JSON.stringify({ name: modelName }),
    });

    if (!res.ok) {
      throw new Error(`Failed to pull model: ${modelName}`);
    }

    const reader = res.body!.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const lines = decoder.decode(value).split('\n');
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          if (data.total && data.completed) {
            onProgress?.(data.completed / data.total);
          }
        } catch {}
      }
    }
  }

  async *generate(params: GenerateParams): AsyncIterable<string> {
    this.abortController = new AbortController();

    const messages = [
      { role: 'system', content: params.systemPrompt },
      { role: 'user', content: params.userPrompt },
    ];

    if (params.context && params.context.length > 0) {
      messages.splice(1, 0, {
        role: 'assistant',
        content: `Current project files:\n${params.context.join('\n\n')}`,
      });
    }

    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: params.model,
        messages,
        stream: true,
        options: {
          temperature: params.temperature ?? 0.7,
          top_p: params.topP ?? 0.95,
          top_k: params.topK ?? 40,
          num_predict: params.maxTokens ?? 16384,
        },
      }),
      signal: this.abortController.signal,
    });

    if (!response.ok) {
      throw new Error(`Ollama request failed: ${response.statusText}`);
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const lines = decoder.decode(value, { stream: true }).split('\n');
        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            if (data.message?.content) {
              yield data.message.content;
            }
          } catch {}
        }
      }
    } finally {
      reader.releaseLock();
    }
  }

  abort(): void {
    this.abortController?.abort();
    this.abortController = null;
  }
}
```

---

## Hardware Detection

```typescript
// src/modules/generator/composables/useHardwareDetection.ts

import { ref, computed, onMounted } from 'vue';
import { invoke } from '@tauri-apps/api/core';

export interface HardwareCapabilities {
  totalRam: number;           // GB
  availableRam: number;       // GB
  hasGpu: boolean;
  gpuVram: number;            // GB (0 if no GPU or unknown)
  gpuName: string | null;
  cpuCores: number;
  recommendedModelSize: 'small' | 'medium' | 'large' | 'xlarge';
}

export function useHardwareDetection() {
  const capabilities = ref<HardwareCapabilities | null>(null);
  const isDetecting = ref(true);
  const error = ref<string | null>(null);

  const recommendedModelSize = computed(() => {
    if (!capabilities.value) return 'small';
    
    const ram = capabilities.value.availableRam;
    const vram = capabilities.value.gpuVram;
    
    // GPU-accelerated recommendations
    if (vram >= 24) return 'xlarge';  // 70B+ models
    if (vram >= 12) return 'large';   // 33B models
    if (vram >= 8) return 'medium';   // 13B models
    
    // CPU-only recommendations (slower but works)
    if (ram >= 64) return 'large';
    if (ram >= 32) return 'medium';
    if (ram >= 16) return 'small';
    
    return 'small';  // 7B models minimum
  });

  const canRunModel = computed(() => (ramRequired: number) => {
    if (!capabilities.value) return false;
    return capabilities.value.availableRam >= ramRequired * 1.2; // 20% headroom
  });

  async function detect(): Promise<HardwareCapabilities> {
    isDetecting.value = true;
    error.value = null;

    try {
      // Call Tauri command for system info
      const sysInfo = await invoke<{
        total_memory: number;
        available_memory: number;
        cpu_cores: number;
        gpu_info: { name: string; vram_mb: number } | null;
      }>('get_system_info');

      const result: HardwareCapabilities = {
        totalRam: Math.round(sysInfo.total_memory / (1024 * 1024 * 1024)),
        availableRam: Math.round(sysInfo.available_memory / (1024 * 1024 * 1024)),
        hasGpu: sysInfo.gpu_info !== null,
        gpuVram: sysInfo.gpu_info ? Math.round(sysInfo.gpu_info.vram_mb / 1024) : 0,
        gpuName: sysInfo.gpu_info?.name ?? null,
        cpuCores: sysInfo.cpu_cores,
        recommendedModelSize: 'small', // Will be computed
      };

      // Calculate recommended size
      if (result.gpuVram >= 24 || result.availableRam >= 64) {
        result.recommendedModelSize = 'xlarge';
      } else if (result.gpuVram >= 12 || result.availableRam >= 32) {
        result.recommendedModelSize = 'large';
      } else if (result.gpuVram >= 8 || result.availableRam >= 16) {
        result.recommendedModelSize = 'medium';
      } else {
        result.recommendedModelSize = 'small';
      }

      capabilities.value = result;
      return result;
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to detect hardware';
      
      // Fallback to conservative defaults
      capabilities.value = {
        totalRam: 8,
        availableRam: 4,
        hasGpu: false,
        gpuVram: 0,
        gpuName: null,
        cpuCores: 4,
        recommendedModelSize: 'small',
      };
      
      return capabilities.value;
    } finally {
      isDetecting.value = false;
    }
  }

  onMounted(() => {
    detect();
  });

  return {
    capabilities,
    isDetecting,
    error,
    recommendedModelSize,
    canRunModel,
    detect,
  };
}
```

**Rust side for Tauri:**

```rust
// src-tauri/src/commands/system_info.rs

use sysinfo::{System, SystemExt, CpuExt};

#[derive(serde::Serialize)]
pub struct GpuInfo {
    name: String,
    vram_mb: u64,
}

#[derive(serde::Serialize)]
pub struct SystemInfo {
    total_memory: u64,
    available_memory: u64,
    cpu_cores: usize,
    gpu_info: Option<GpuInfo>,
}

#[tauri::command]
pub async fn get_system_info() -> Result<SystemInfo, String> {
    let mut sys = System::new_all();
    sys.refresh_all();

    // Try to detect GPU (platform-specific)
    let gpu_info = detect_gpu();

    Ok(SystemInfo {
        total_memory: sys.total_memory(),
        available_memory: sys.available_memory(),
        cpu_cores: sys.cpus().len(),
        gpu_info,
    })
}

#[cfg(target_os = "linux")]
fn detect_gpu() -> Option<GpuInfo> {
    // Try nvidia-smi first
    if let Ok(output) = std::process::Command::new("nvidia-smi")
        .args(["--query-gpu=name,memory.total", "--format=csv,noheader,nounits"])
        .output()
    {
        if output.status.success() {
            let stdout = String::from_utf8_lossy(&output.stdout);
            let parts: Vec<&str> = stdout.trim().split(", ").collect();
            if parts.len() >= 2 {
                return Some(GpuInfo {
                    name: parts[0].to_string(),
                    vram_mb: parts[1].parse().unwrap_or(0),
                });
            }
        }
    }
    None
}

#[cfg(target_os = "windows")]
fn detect_gpu() -> Option<GpuInfo> {
    // Use DXGI or WMI on Windows
    // ... implementation
    None
}

#[cfg(target_os = "macos")]
fn detect_gpu() -> Option<GpuInfo> {
    // Use Metal API on macOS
    // ... implementation
    None
}
```

---

## Main Inference Composable

```typescript
// src/modules/generator/composables/useInference.ts

import { ref, computed, shallowRef } from 'vue';
import { useProviders } from './useProviders';
import { useHardwareDetection } from './useHardwareDetection';
import type { InferenceProvider, GenerateParams, Model } from '../providers/types';

export interface GenerationState {
  status: 'idle' | 'generating' | 'streaming' | 'complete' | 'error';
  content: string;
  error: string | null;
  startTime: number | null;
  tokensGenerated: number;
}

export function useInference() {
  const { activeProvider, providers, setActiveProvider } = useProviders();
  const { capabilities, recommendedModelSize, canRunModel } = useHardwareDetection();

  const state = ref<GenerationState>({
    status: 'idle',
    content: '',
    error: null,
    startTime: null,
    tokensGenerated: 0,
  });

  const currentModel = ref<Model | null>(null);
  const availableModels = shallowRef<Model[]>([]);

  // Load models when provider changes
  async function loadModels(): Promise<void> {
    if (!activeProvider.value) return;

    try {
      const models = await activeProvider.value.getModels();
      
      // Filter by hardware capability for local providers
      if (activeProvider.value.config.type === 'local') {
        availableModels.value = models.filter(m => 
          !m.ramRequired || canRunModel.value(m.ramRequired)
        );
      } else {
        availableModels.value = models;
      }

      // Auto-select best model
      if (!currentModel.value && availableModels.value.length > 0) {
        currentModel.value = selectBestModel(availableModels.value);
      }
    } catch (e) {
      console.error('Failed to load models:', e);
    }
  }

  function selectBestModel(models: Model[]): Model {
    const size = recommendedModelSize.value;
    
    // Find model matching recommended size
    const sizeOrder = ['xlarge', 'large', 'medium', 'small'];
    const startIndex = sizeOrder.indexOf(size);
    
    for (let i = startIndex; i < sizeOrder.length; i++) {
      const match = models.find(m => m.size === sizeOrder[i]);
      if (match) return match;
    }
    
    return models[0];
  }

  async function generate(params: Omit<GenerateParams, 'model'>): Promise<string> {
    if (!activeProvider.value || !currentModel.value) {
      throw new Error('No provider or model selected');
    }

    state.value = {
      status: 'generating',
      content: '',
      error: null,
      startTime: Date.now(),
      tokensGenerated: 0,
    };

    try {
      const fullParams: GenerateParams = {
        ...params,
        model: currentModel.value.id,
      };

      state.value.status = 'streaming';

      for await (const chunk of activeProvider.value.generate(fullParams)) {
        state.value.content += chunk;
        state.value.tokensGenerated += 1; // Approximate
      }

      state.value.status = 'complete';
      return state.value.content;

    } catch (e) {
      state.value.status = 'error';
      state.value.error = e instanceof Error ? e.message : 'Generation failed';
      
      // Handle specific errors
      if (state.value.error.includes('exceeded your monthly')) {
        throw new InferenceError('quota_exceeded', state.value.error);
      }
      if (state.value.error.includes('inference provider')) {
        throw new InferenceError('provider_error', state.value.error);
      }
      
      throw e;
    }
  }

  function abort(): void {
    activeProvider.value?.abort();
    state.value.status = 'idle';
  }

  // Computed helpers
  const isGenerating = computed(() => 
    state.value.status === 'generating' || state.value.status === 'streaming'
  );

  const tokensPerSecond = computed(() => {
    if (!state.value.startTime || state.value.tokensGenerated === 0) return 0;
    const elapsed = (Date.now() - state.value.startTime) / 1000;
    return Math.round(state.value.tokensGenerated / elapsed);
  });

  return {
    // State
    state,
    currentModel,
    availableModels,
    
    // Provider management
    providers,
    activeProvider,
    setActiveProvider,
    
    // Hardware
    capabilities,
    recommendedModelSize,
    canRunModel,
    
    // Actions
    loadModels,
    generate,
    abort,
    
    // Computed
    isGenerating,
    tokensPerSecond,
  };
}

export class InferenceError extends Error {
  constructor(
    public readonly code: 'quota_exceeded' | 'provider_error' | 'network_error' | 'abort',
    message: string
  ) {
    super(message);
    this.name = 'InferenceError';
  }
}
```

---

## Provider Registry

```typescript
// src/modules/generator/providers/registry.ts

import { ref, computed } from 'vue';
import { HuggingFaceProvider } from './huggingface';
import { OllamaProvider } from './ollama';
import type { InferenceProvider, ProviderConfig } from './types';

// Token storage (uses Tauri secure storage)
import { invoke } from '@tauri-apps/api/core';

export interface ProviderRegistry {
  providers: Map<string, InferenceProvider>;
  activeProviderId: string | null;
}

const registry = ref<ProviderRegistry>({
  providers: new Map(),
  activeProviderId: null,
});

export async function initializeProviders(): Promise<void> {
  // Always register Ollama (may or may not be available)
  const ollama = new OllamaProvider();
  registry.value.providers.set('ollama', ollama);

  // Check if HuggingFace token exists
  try {
    const hfToken = await invoke<string | null>('get_api_token', { key: 'huggingface' });
    if (hfToken) {
      const hf = new HuggingFaceProvider({ token: hfToken });
      registry.value.providers.set('huggingface', hf);
    }
  } catch {
    // No HF token stored
  }

  // Auto-select best available provider
  await autoSelectProvider();
}

export async function autoSelectProvider(): Promise<void> {
  // Prefer local if available
  const ollama = registry.value.providers.get('ollama');
  if (ollama && await ollama.isAvailable()) {
    registry.value.activeProviderId = 'ollama';
    return;
  }

  // Fall back to cloud
  const hf = registry.value.providers.get('huggingface');
  if (hf && await hf.isAvailable()) {
    registry.value.activeProviderId = 'huggingface';
    return;
  }

  registry.value.activeProviderId = null;
}

export async function setHuggingFaceToken(token: string): Promise<void> {
  // Store securely
  await invoke('store_api_token', { key: 'huggingface', token });
  
  // Create/update provider
  const hf = new HuggingFaceProvider({ token });
  registry.value.providers.set('huggingface', hf);
}

export async function getSharedToken(): Promise<string> {
  // Get shared token for colleagues (from Tauri config or env)
  return invoke<string>('get_shared_token');
}

export function useProviders() {
  const providers = computed(() => 
    Array.from(registry.value.providers.values())
  );

  const activeProvider = computed(() => {
    if (!registry.value.activeProviderId) return null;
    return registry.value.providers.get(registry.value.activeProviderId) ?? null;
  });

  function setActiveProvider(id: string): void {
    if (registry.value.providers.has(id)) {
      registry.value.activeProviderId = id;
    }
  }

  return {
    providers,
    activeProvider,
    setActiveProvider,
    initializeProviders,
    autoSelectProvider,
    setHuggingFaceToken,
    getSharedToken,
  };
}
```

---

## Token Management (Tauri Rust)

```rust
// src-tauri/src/commands/tokens.rs

use keyring::Entry;

const SERVICE_NAME: &str = "collabkit-generator";

#[tauri::command]
pub async fn store_api_token(key: String, token: String) -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, &key)
        .map_err(|e| e.to_string())?;
    
    entry.set_password(&token)
        .map_err(|e| e.to_string())?;
    
    Ok(())
}

#[tauri::command]
pub async fn get_api_token(key: String) -> Result<Option<String>, String> {
    let entry = Entry::new(SERVICE_NAME, &key)
        .map_err(|e| e.to_string())?;
    
    match entry.get_password() {
        Ok(password) => Ok(Some(password)),
        Err(keyring::Error::NoEntry) => Ok(None),
        Err(e) => Err(e.to_string()),
    }
}

#[tauri::command]
pub async fn delete_api_token(key: String) -> Result<(), String> {
    let entry = Entry::new(SERVICE_NAME, &key)
        .map_err(|e| e.to_string())?;
    
    entry.delete_credential()
        .map_err(|e| e.to_string())?;
    
    Ok(())
}

#[tauri::command]
pub fn get_shared_token() -> Result<String, String> {
    // Read from embedded config or env
    std::env::var("COLLABKIT_SHARED_HF_TOKEN")
        .or_else(|_| {
            // Fallback to bundled token (encrypted in release builds)
            include_str!("../config/shared_token.txt")
                .trim()
                .to_string()
                .into()
        })
        .map_err(|e| e.to_string())
}
```

---

## Tauri Configuration

```json
// src-tauri/tauri.conf.json (relevant sections)

{
  "tauri": {
    "allowlist": {
      "http": {
        "request": true,
        "scope": [
          "https://api-inference.huggingface.co/*",
          "https://huggingface.co/api/*",
          "http://localhost:11434/*",
          "http://127.0.0.1:11434/*"
        ]
      },
      "shell": {
        "open": true
      }
    },
    "security": {
      "csp": "default-src 'self'; connect-src 'self' https://api-inference.huggingface.co https://huggingface.co http://localhost:11434 http://127.0.0.1:11434"
    }
  }
}
```

---

## Model Selection UI Component

```vue
<!-- src/modules/generator/components/ModelSelector.vue -->

<script setup lang="ts">
import { computed } from 'vue';
import { useInference } from '../composables/useInference';

const { 
  providers, 
  activeProvider, 
  setActiveProvider,
  availableModels,
  currentModel,
  capabilities,
  recommendedModelSize,
} = useInference();

const modelsBySize = computed(() => {
  const grouped = {
    xlarge: [] as typeof availableModels.value,
    large: [] as typeof availableModels.value,
    medium: [] as typeof availableModels.value,
    small: [] as typeof availableModels.value,
  };
  
  for (const model of availableModels.value) {
    const size = model.size ?? 'medium';
    grouped[size].push(model);
  }
  
  return grouped;
});

function selectModel(model: typeof currentModel.value) {
  currentModel.value = model;
}
</script>

<template>
  <div class="space-y-4 p-4 bg-slate-800 rounded-lg">
    <!-- Provider Selection -->
    <div>
      <label class="text-sm text-slate-400 mb-2 block">Provider</label>
      <div class="flex gap-2">
        <button
          v-for="provider in providers"
          :key="provider.config.id"
          @click="setActiveProvider(provider.config.id)"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            activeProvider?.config.id === provider.config.id
              ? 'bg-blue-600 text-white'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          ]"
        >
          {{ provider.config.icon }} {{ provider.config.name }}
        </button>
      </div>
    </div>

    <!-- Hardware Info (for local) -->
    <div v-if="activeProvider?.config.type === 'local' && capabilities" 
         class="text-sm text-slate-400 bg-slate-900 p-3 rounded">
      <div class="flex justify-between">
        <span>Available RAM:</span>
        <span class="text-slate-200">{{ capabilities.availableRam }} GB</span>
      </div>
      <div v-if="capabilities.hasGpu" class="flex justify-between">
        <span>GPU:</span>
        <span class="text-slate-200">{{ capabilities.gpuName }} ({{ capabilities.gpuVram }} GB)</span>
      </div>
      <div class="flex justify-between mt-2 pt-2 border-t border-slate-700">
        <span>Recommended:</span>
        <span class="text-green-400 capitalize">{{ recommendedModelSize }} models</span>
      </div>
    </div>

    <!-- Model Selection -->
    <div>
      <label class="text-sm text-slate-400 mb-2 block">Model</label>
      <div class="space-y-3">
        <div v-for="(models, size) in modelsBySize" :key="size">
          <div v-if="models.length > 0" class="space-y-1">
            <div class="text-xs text-slate-500 uppercase tracking-wide">
              {{ size }}
              <span v-if="size === recommendedModelSize" class="text-green-500 ml-1">
                ✓ Recommended
              </span>
            </div>
            <button
              v-for="model in models"
              :key="model.id"
              @click="selectModel(model)"
              :class="[
                'w-full text-left px-3 py-2 rounded transition-colors',
                currentModel?.id === model.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              ]"
            >
              <div class="font-medium">{{ model.name }}</div>
              <div class="text-xs opacity-70">
                {{ model.contextLength.toLocaleString() }} ctx
                <span v-if="model.ramRequired"> · {{ model.ramRequired }}GB RAM</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

## Settings Storage

```typescript
// src/modules/generator/composables/useSettings.ts

import { ref, watch } from 'vue';
import { invoke } from '@tauri-apps/api/core';

export interface GeneratorSettings {
  // Provider preferences
  preferLocalFirst: boolean;
  defaultProvider: string | null;
  defaultModel: string | null;
  
  // Generation settings
  temperature: number;
  maxTokens: number;
  
  // Local model settings
  ollamaUrl: string;
  autoDownloadModels: boolean;
  maxModelSize: 'small' | 'medium' | 'large' | 'xlarge' | 'auto';
}

const DEFAULT_SETTINGS: GeneratorSettings = {
  preferLocalFirst: true,
  defaultProvider: null,
  defaultModel: null,
  temperature: 0.7,
  maxTokens: 16384,
  ollamaUrl: 'http://localhost:11434',
  autoDownloadModels: true,
  maxModelSize: 'auto',
};

export function useSettings() {
  const settings = ref<GeneratorSettings>({ ...DEFAULT_SETTINGS });
  const isLoaded = ref(false);

  async function load(): Promise<void> {
    try {
      const stored = await invoke<string | null>('get_setting', { 
        key: 'generator_settings' 
      });
      
      if (stored) {
        settings.value = { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
      }
    } catch {
      // Use defaults
    }
    isLoaded.value = true;
  }

  async function save(): Promise<void> {
    await invoke('set_setting', {
      key: 'generator_settings',
      value: JSON.stringify(settings.value),
    });
  }

  // Auto-save on changes
  watch(settings, () => {
    if (isLoaded.value) {
      save();
    }
  }, { deep: true });

  return {
    settings,
    isLoaded,
    load,
    save,
  };
}
```

---

## Summary: What Gets Built

### Phase 1: Core (Days 1-2)
- [ ] `providers/types.ts` — Interfaces
- [ ] `providers/huggingface.ts` — Cloud provider
- [ ] `providers/ollama.ts` — Local provider
- [ ] `providers/registry.ts` — Provider management
- [ ] `composables/useInference.ts` — Main orchestration
- [ ] Tauri commands for token storage

### Phase 2: Hardware Detection (Day 2)
- [ ] `composables/useHardwareDetection.ts` — Vue composable
- [ ] Rust `get_system_info` command
- [ ] GPU detection (NVIDIA, AMD, Apple Silicon)

### Phase 3: UI (Day 3)
- [ ] `components/ModelSelector.vue`
- [ ] `components/SettingsPanel.vue`
- [ ] Integration with GeneratorView.vue

### Phase 4: Model Management (Day 4)
- [ ] Ollama model pulling with progress
- [ ] Auto-download recommended models
- [ ] Model update notifications

---

## Dependencies

**NPM:**
```json
{
  "@tauri-apps/api": "^2.0.0"
}
```

**Cargo:**
```toml
[dependencies]
sysinfo = "0.30"
keyring = "2.0"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

---

## Questions Resolved

| Question | Decision |
|----------|----------|
| Token strategy | Both: User token (pro) + shared token for colleagues |
| Offline priority | Cloud primary during dev, local as goal, settings toggle |
| Hardware | Auto-detect, support all tiers |
| Model selection | User chooses based on hardware capability display |

---

Ready to implement. Want me to start with the core provider interfaces and HuggingFace implementation?
