# JFDI: HuggingFace Approach

## Strategic Overview

**Philosophy**: GPU-enabled cloud development with native local LLM integration.

This approach uses HuggingFace Spaces as a bridge environment—you get free GPU access for running local models while maintaining cloud accessibility. Think of it as the "integrate and validate local LLMs" phase before committing to full local infrastructure.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   HUGGINGFACE SPACES                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Gradio / Streamlit UI                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │   Chat      │  │   Code      │  │  Settings   │      │   │
│  │  │   Panel     │  │   Preview   │  │   Panel     │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│  ┌───────────────────────────┴───────────────────────────┐     │
│  │                    GPU Runtime                         │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │     │
│  │  │ Seed-Coder  │  │  Dolphin-v2 │  │   Ollama    │    │     │
│  │  │  8B Models  │  │  (Doc Parse)│  │  (Runtime)  │    │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │     │
│  └───────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      ┌──────────┐     ┌──────────────┐   ┌──────────────┐
      │  Convex  │     │   Claude /   │   │   GitHub     │
      │ (Backend)│     │  OpenRouter  │   │   (Repo)     │
      └──────────┘     └──────────────┘   └──────────────┘
```

---

## What You Get

| Capability | Status | Notes |
|------------|--------|-------|
| GPU Access | ✅ | Free T4 (16GB) or A10G |
| Local LLMs | ✅ | Seed-Coder, Dolphin-v2 |
| Cloud APIs | ✅ | Claude, OpenRouter |
| Convex Backend | ✅ | Same as Codespaces |
| Gradio UI | ✅ | Rapid prototyping |
| Persistent Storage | ⚠️ | 50GB, resets on rebuild |
| Custom Frontend | ⚠️ | Gradio/Streamlit only |
| Full React App | ❌ | Not native (workarounds exist) |
| Self-Modification | ⚠️ | Limited filesystem access |
| Team Access | ✅ | Public or private Spaces |

---

## Prerequisites

1. **HuggingFace Account** (free)
2. **HuggingFace Token** with write access
3. **Convex Account** (from Stage 1)
4. **API Keys** (from Stage 1: Anthropic, OpenRouter)
5. **Working JFDI Core** (from Stage 1)

---

## HuggingFace Space Types

| Type | GPU | Use Case | Cost |
|------|-----|----------|------|
| **CPU Basic** | ❌ | Testing UI only | Free |
| **CPU Upgrade** | ❌ | More RAM | $0.03/hr |
| **T4 Small** | ✅ 16GB | Seed-Coder 8B | Free (community) |
| **T4 Medium** | ✅ 16GB | More CPU/RAM | $0.06/hr |
| **A10G Small** | ✅ 24GB | Larger models | $1.05/hr |
| **A100 Large** | ✅ 40GB | Full 70B models | $4.13/hr |

**Recommendation**: Start with **T4 Small (Free)** for Seed-Coder 8B.

---

## Setup Steps

### Step 1: Create HuggingFace Space

```bash
# Via HuggingFace CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create Space
huggingface-cli repo create jfdi-space --type space --space-sdk gradio
```

Or via web:
1. Go to https://huggingface.co/new-space
2. Name: `jfdi-space`
3. SDK: **Gradio**
4. Hardware: **T4 Small** (free tier)
5. Visibility: Private (for now)

### Step 2: Clone Space Repository

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/jfdi-space
cd jfdi-space
```

### Step 3: Create Core Application Files

**File: `requirements.txt`**
```
gradio>=4.0.0
transformers>=4.35.0
torch>=2.0.0
accelerate
bitsandbytes
anthropic
httpx
convex
python-dotenv
```

**File: `app.py`**
```python
import gradio as gr
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from anthropic import Anthropic
import httpx

# ============================================
# JFDI - HuggingFace Spaces Edition
# ============================================

# System prompt for manufacturing context
JFDI_SYSTEM_PROMPT = """You are JFDI - Just Fucking Do It.
An expert manufacturing engineering app builder for Electronic Pixel Orchestra.
Generate production-ready React + TypeScript + Tailwind code.

MANUFACTURING CONTEXT:
- Understand purchase orders, BOMs, inventory systems
- Generate validation logic for compliance requirements
- Create forms with proper error handling
- Output ONLY valid, runnable code. No markdown fences."""

# ============================================
# Model Loading
# ============================================

class LLMRouter:
    def __init__(self):
        self.local_model = None
        self.local_tokenizer = None
        self.anthropic_client = None
        self.load_providers()
    
    def load_providers(self):
        # Load Anthropic if key available
        if os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            print("✅ Anthropic client loaded")
        
        # Load local Seed-Coder model
        try:
            model_id = "ByteDance-Seed/Seed-Coder-8B-Instruct"
            print(f"Loading {model_id}...")
            
            self.local_tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.local_model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True  # Quantize for T4
            )
            print("✅ Seed-Coder loaded on GPU")
        except Exception as e:
            print(f"⚠️ Local model failed to load: {e}")
    
    def generate(self, prompt: str, provider: str = "auto") -> tuple[str, str]:
        """Generate code, returns (code, provider_used)"""
        
        if provider == "auto":
            # Try Claude first, then local
            if self.anthropic_client:
                try:
                    return self._call_claude(prompt), "Claude 3.5 Sonnet"
                except Exception as e:
                    print(f"Claude failed: {e}")
            
            if self.local_model:
                return self._call_local(prompt), "Seed-Coder 8B"
            
            raise Exception("No LLM providers available")
        
        elif provider == "claude":
            return self._call_claude(prompt), "Claude 3.5 Sonnet"
        
        elif provider == "local":
            return self._call_local(prompt), "Seed-Coder 8B"
        
        elif provider == "openrouter":
            return self._call_openrouter(prompt), "OpenRouter"
    
    def _call_claude(self, prompt: str) -> str:
        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=JFDI_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _call_local(self, prompt: str) -> str:
        full_prompt = f"{JFDI_SYSTEM_PROMPT}\n\nUser: {prompt}\n\nAssistant:"
        inputs = self.local_tokenizer(full_prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = self.local_model.generate(
                **inputs,
                max_new_tokens=2048,
                temperature=0.3,
                do_sample=True,
                pad_token_id=self.local_tokenizer.eos_token_id
            )
        
        response = self.local_tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract just the assistant's response
        return response.split("Assistant:")[-1].strip()
    
    def _call_openrouter(self, prompt: str) -> str:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://jfdi.electronicpixelorchestra.com",
                "X-Title": "JFDI"
            },
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {"role": "system", "content": JFDI_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=60.0
        )
        return response.json()["choices"][0]["message"]["content"]

# Initialize router
router = LLMRouter()

# ============================================
# Gradio UI
# ============================================

def generate_code(prompt: str, provider: str, history: list) -> tuple[list, str, str]:
    """Main generation function"""
    try:
        code, used_provider = router.generate(prompt, provider.lower())
        history.append((prompt, code))
        return history, code, f"✅ Generated via {used_provider}"
    except Exception as e:
        return history, "", f"❌ Error: {str(e)}"

def clear_history():
    return [], "", ""

# Build UI
with gr.Blocks(title="JFDI - Manufacturing AI Coder", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🏭 JFDI - Just Fucking Do It
    ### Manufacturing AI Code Platform
    
    Generate production-ready React + TypeScript + Tailwind code for manufacturing applications.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Settings Panel (Scrollable)
            gr.Markdown("## ⚙️ Settings")
            
            provider_dropdown = gr.Dropdown(
                choices=["Auto", "Claude", "Local", "OpenRouter"],
                value="Auto",
                label="LLM Provider"
            )
            
            gr.Markdown("### 🤖 Provider Status")
            provider_status = gr.Markdown(f"""
            - Claude: {'✅' if router.anthropic_client else '❌'}
            - Seed-Coder: {'✅' if router.local_model else '❌'}
            - OpenRouter: {'✅' if os.getenv('OPENROUTER_API_KEY') else '❌'}
            """)
            
            gr.Markdown("### 📊 Model Info")
            gr.Markdown("""
            **Seed-Coder 8B** (Local)
            - SWE-Bench: 19.2%
            - Context: 32K tokens
            - Speed: ~15-25s
            
            **Claude 3.5 Sonnet** (Cloud)
            - Best quality
            - Cost: ~$0.003/1K tokens
            """)
        
        with gr.Column(scale=2):
            # Chat Panel
            chatbot = gr.Chatbot(
                label="JFDI Chat",
                height=400,
                show_copy_button=True
            )
            
            prompt_input = gr.Textbox(
                label="What do you want to build?",
                placeholder="Build an inventory reorder form with validation...",
                lines=3
            )
            
            with gr.Row():
                submit_btn = gr.Button("🚀 Generate", variant="primary")
                clear_btn = gr.Button("🗑️ Clear")
            
            status_text = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column(scale=2):
            # Code Preview Panel
            code_output = gr.Code(
                label="Generated Code",
                language="typescript",
                lines=25,
                show_label=True
            )
    
    # Wire up events
    submit_btn.click(
        generate_code,
        inputs=[prompt_input, provider_dropdown, chatbot],
        outputs=[chatbot, code_output, status_text]
    )
    
    clear_btn.click(
        clear_history,
        outputs=[chatbot, code_output, status_text]
    )
    
    prompt_input.submit(
        generate_code,
        inputs=[prompt_input, provider_dropdown, chatbot],
        outputs=[chatbot, code_output, status_text]
    )

# Launch
if __name__ == "__main__":
    app.launch()
```

### Step 4: Configure Secrets

In HuggingFace Space Settings → Repository secrets:

```
ANTHROPIC_API_KEY=sk-ant-your-key
OPENROUTER_API_KEY=sk-or-your-key
CONVEX_URL=https://your-deployment.convex.cloud
```

### Step 5: Push and Deploy

```bash
git add .
git commit -m "Initial JFDI HuggingFace Space"
git push origin main
```

HuggingFace will automatically build and deploy. First build takes 5-10 minutes.

---

## Advanced: Ollama on HuggingFace

For more flexibility, you can run Ollama as a subprocess:

**File: `start_ollama.py`**
```python
import subprocess
import time
import os

def start_ollama():
    """Start Ollama server in background"""
    # Download Ollama binary
    subprocess.run([
        "curl", "-fsSL", 
        "https://ollama.com/install.sh", 
        "-o", "/tmp/install_ollama.sh"
    ])
    subprocess.run(["bash", "/tmp/install_ollama.sh"])
    
    # Start server
    ollama_process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)  # Wait for server to start
    
    # Pull models
    subprocess.run(["ollama", "pull", "seed-coder:8b-instruct"])
    subprocess.run(["ollama", "pull", "seed-coder:8b-reasoning"])
    
    return ollama_process

if __name__ == "__main__":
    start_ollama()
```

---

## WebLink Integration (HuggingFace Edition)

WebLink can be embedded as an iframe or run as a separate Space:

```python
# In app.py, add WebLink tab

with gr.Tab("📁 Workspaces"):
    gr.Markdown("## WebLink Workspaces")
    
    workspace_list = gr.Dataframe(
        headers=["Name", "Status", "Created"],
        label="Active Workspaces"
    )
    
    with gr.Row():
        workspace_name = gr.Textbox(label="Workspace Name")
        create_workspace_btn = gr.Button("➕ Create Workspace")
    
    # Embed WebLink iframe
    weblink_frame = gr.HTML("""
        <iframe 
            src="https://your-weblink-instance.com" 
            width="100%" 
            height="600px"
            frameborder="0">
        </iframe>
    """)
```

---

## Connecting to Convex

```python
# convex_client.py
from convex import ConvexClient
import os

client = ConvexClient(os.getenv("CONVEX_URL"))

async def save_generation(prompt: str, code: str, provider: str):
    """Save generation to Convex database"""
    await client.mutation("generations:create", {
        "prompt": prompt,
        "code": code,
        "provider": provider,
        "createdAt": int(time.time() * 1000)
    })

async def get_recent_generations(limit: int = 10):
    """Fetch recent generations"""
    return await client.query("generations:recent", {"limit": limit})
```

---

## Cost Analysis

| Item | Free Tier | Paid Estimate |
|------|-----------|---------------|
| HuggingFace T4 Space | Unlimited (community) | N/A |
| HuggingFace A10G | 2 hrs/day | $1.05/hr |
| Claude API | N/A | ~$0.003-0.015/1K tokens |
| OpenRouter | Varies | Pass-through + 5% |
| Convex | Same as Stage 1 | Same |

**Estimated Monthly (Solo Dev):** $0-30 (mostly API calls)
**Estimated Monthly (Heavy Usage):** $50-150

---

## Limitations

1. **Gradio/Streamlit Only** - Not a full React dev environment
2. **Cold Starts** - GPU instances spin down after inactivity
3. **50GB Storage** - Resets on rebuild
4. **No Full Terminal** - Limited shell access
5. **Model Size Limits** - T4 (16GB) can't run 70B models
6. **Rate Limits** - Community GPU has queue times

---

## When to Use This Approach

✅ **Use HuggingFace when:**
- Testing local LLM integration before local hardware commitment
- Prototyping GPU-accelerated features
- Sharing demos with stakeholders
- Running comparative benchmarks (Claude vs Seed-Coder)
- Building proof-of-concept for document processing

❌ **Don't use HuggingFace when:**
- Need full React/Vite development environment
- Require persistent storage
- Self-modification is critical
- Cost optimization is primary concern (local is cheaper long-term)

---

## Migration Path

When ready to move to Stage 3 (Local):

```bash
# Export your working code
git clone https://huggingface.co/spaces/YOUR_USERNAME/jfdi-space
cd jfdi-space

# The LLM router and model loading code transfers directly
# Just change from Gradio to your React frontend

# Key files to migrate:
# - LLMRouter class → convex/lib/llm-router.ts
# - Model loading patterns → local Ollama setup
# - Provider configurations → .env.local
```

---

## Success Criteria (Stage 2 Complete)

- [ ] Seed-Coder 8B loads successfully on GPU
- [ ] Local generation produces quality code
- [ ] Fallback chain works (Claude → Seed-Coder → OpenRouter)
- [ ] Generation times acceptable (<30s for local)
- [ ] Output quality comparable to Claude (within 10%)
- [ ] Document parsing with Dolphin-v2 works
- [ ] Convex integration persists generations

---

## Benchmark Tests to Run

Before moving to Stage 3, validate local model quality:

```python
TEST_PROMPTS = [
    "Build a simple counter component with increment/decrement buttons",
    "Create an inventory form with SKU, quantity, and reorder point fields",
    "Build a data table that displays purchase orders with sorting",
    "Create a validation function for CSA A277 compliance checking",
    "Build a dashboard card showing manufacturing KPIs"
]

# Run each prompt through both Claude and Seed-Coder
# Compare: correctness, code style, completion time
# Document results before proceeding to Stage 3
```

---

*Document Version: 1.0*
*Last Updated: December 2024*
*Stage: 2 of 3 (Integrate)*
