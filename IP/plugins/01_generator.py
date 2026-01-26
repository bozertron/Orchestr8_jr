"""
01_generator Plugin - 7-Phase Project Wizard
Orchestr8 v3.0 - The Fortress Factory

A comprehensive project generation wizard that guides users through
7 phases to create a complete BUILD_SPEC.json for project scaffolding.

Phases:
    1. Project Identity - Name, description, type
    2. Technology Stack - Languages, frameworks, tools
    3. Architecture - Structure, patterns, layers
    4. Features - Core functionality, modules
    5. Dependencies - External packages, APIs
    6. Configuration - Environment, settings
    7. Review & Export - Final review and BUILD_SPEC.json generation
"""

import json
from pathlib import Path
from datetime import datetime

PLUGIN_NAME = "⚙️ Generator"
PLUGIN_ORDER = 1

# Phase definitions
PHASES = [
    {"id": 1, "name": "Project Identity", "fields": ["name", "description", "type", "version"]},
    {"id": 2, "name": "Technology Stack", "fields": ["languages", "frameworks", "tools"]},
    {"id": 3, "name": "Architecture", "fields": ["structure", "patterns", "layers"]},
    {"id": 4, "name": "Features", "fields": ["core_features", "modules", "integrations"]},
    {"id": 5, "name": "Dependencies", "fields": ["packages", "apis", "services"]},
    {"id": 6, "name": "Configuration", "fields": ["environment", "settings", "secrets"]},
    {"id": 7, "name": "Review & Export", "fields": []}
]

def render(STATE_MANAGERS):
    """Render the 7-phase generator wizard."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Phase state (using mo.state for reactivity)
    get_phase, set_phase = mo.state(1)
    get_spec, set_spec = mo.state({
        "project_identity": {"name": "", "description": "", "type": "application", "version": "1.0.0"},
        "technology_stack": {"languages": [], "frameworks": [], "tools": []},
        "architecture": {"structure": "modular", "patterns": [], "layers": []},
        "features": {"core_features": [], "modules": [], "integrations": []},
        "dependencies": {"packages": [], "apis": [], "services": []},
        "configuration": {"environment": "development", "settings": {}, "secrets": []}
    })
    get_locked, set_locked = mo.state([])  # List of locked phase IDs
    
    current_phase = get_phase()
    spec = get_spec()
    locked_phases = get_locked()
    
    # Progress bar
    progress = mo.md(f"**Phase {current_phase} of 7** - {PHASES[current_phase-1]['name']}")
    progress_bar = mo.ui.progress(value=current_phase/7, show_value=True)
    
    # Phase content builder
    def build_phase_content():
        phase = PHASES[current_phase - 1]
        is_locked = current_phase in locked_phases
        
        if current_phase == 1:
            # Project Identity
            name_input = mo.ui.text(
                value=spec["project_identity"]["name"],
                label="Project Name",
                placeholder="my-awesome-project",
                disabled=is_locked
            )
            desc_input = mo.ui.text_area(
                value=spec["project_identity"]["description"],
                label="Description",
                placeholder="A brief description of your project...",
                disabled=is_locked
            )
            type_select = mo.ui.dropdown(
                options=["application", "library", "service", "cli", "plugin"],
                value=spec["project_identity"]["type"],
                label="Project Type",
                disabled=is_locked
            )
            version_input = mo.ui.text(
                value=spec["project_identity"]["version"],
                label="Initial Version",
                placeholder="1.0.0",
                disabled=is_locked
            )
            return mo.vstack([name_input, desc_input, type_select, version_input])
        
        elif current_phase == 2:
            # Technology Stack
            lang_input = mo.ui.text(
                value=", ".join(spec["technology_stack"]["languages"]),
                label="Languages (comma-separated)",
                placeholder="Python, TypeScript, SQL",
                disabled=is_locked
            )
            fw_input = mo.ui.text(
                value=", ".join(spec["technology_stack"]["frameworks"]),
                label="Frameworks",
                placeholder="Marimo, React, FastAPI",
                disabled=is_locked
            )
            tools_input = mo.ui.text(
                value=", ".join(spec["technology_stack"]["tools"]),
                label="Tools",
                placeholder="pytest, eslint, docker",
                disabled=is_locked
            )
            return mo.vstack([lang_input, fw_input, tools_input])
        
        elif current_phase == 3:
            # Architecture
            struct_select = mo.ui.dropdown(
                options=["monolithic", "modular", "microservices", "serverless", "plugin-based"],
                value=spec["architecture"]["structure"],
                label="Architecture Style",
                disabled=is_locked
            )
            patterns_input = mo.ui.text(
                value=", ".join(spec["architecture"]["patterns"]),
                label="Design Patterns",
                placeholder="MVC, Observer, Factory",
                disabled=is_locked
            )
            layers_input = mo.ui.text(
                value=", ".join(spec["architecture"]["layers"]),
                label="Architectural Layers",
                placeholder="UI, Business Logic, Data Access",
                disabled=is_locked
            )
            return mo.vstack([struct_select, patterns_input, layers_input])
        
        elif current_phase == 4:
            # Features
            features_input = mo.ui.text_area(
                value="\n".join(spec["features"]["core_features"]),
                label="Core Features (one per line)",
                placeholder="User authentication\nData visualization\nAPI integration",
                disabled=is_locked
            )
            modules_input = mo.ui.text(
                value=", ".join(spec["features"]["modules"]),
                label="Modules",
                placeholder="auth, dashboard, api",
                disabled=is_locked
            )
            integrations_input = mo.ui.text(
                value=", ".join(spec["features"]["integrations"]),
                label="Integrations",
                placeholder="GitHub, Stripe, AWS",
                disabled=is_locked
            )
            return mo.vstack([features_input, modules_input, integrations_input])
        
        elif current_phase == 5:
            # Dependencies
            packages_input = mo.ui.text_area(
                value="\n".join(spec["dependencies"]["packages"]),
                label="Packages (one per line)",
                placeholder="pandas>=2.0.0\nrequests\nfastapi",
                disabled=is_locked
            )
            apis_input = mo.ui.text(
                value=", ".join(spec["dependencies"]["apis"]),
                label="External APIs",
                placeholder="REST, GraphQL, WebSocket",
                disabled=is_locked
            )
            services_input = mo.ui.text(
                value=", ".join(spec["dependencies"]["services"]),
                label="Services",
                placeholder="PostgreSQL, Redis, S3",
                disabled=is_locked
            )
            return mo.vstack([packages_input, apis_input, services_input])
        
        elif current_phase == 6:
            # Configuration
            env_select = mo.ui.dropdown(
                options=["development", "staging", "production"],
                value=spec["configuration"]["environment"],
                label="Default Environment",
                disabled=is_locked
            )
            settings_input = mo.ui.text_area(
                value=json.dumps(spec["configuration"]["settings"], indent=2) if spec["configuration"]["settings"] else "{}",
                label="Default Settings (JSON)",
                placeholder='{"debug": true, "log_level": "INFO"}',
                disabled=is_locked
            )
            secrets_input = mo.ui.text(
                value=", ".join(spec["configuration"]["secrets"]),
                label="Required Secrets/Env Vars",
                placeholder="DATABASE_URL, API_KEY, SECRET_KEY",
                disabled=is_locked
            )
            return mo.vstack([env_select, settings_input, secrets_input])
        
        elif current_phase == 7:
            # Review & Export
            spec_json = json.dumps(spec, indent=2)
            review_display = mo.md(f"""
### Build Specification Review

```json
{spec_json}
```

Click **Export** to save as `BUILD_SPEC.json` in your project root.
            """)
            return review_display
        
        return mo.md("Unknown phase")
    
    phase_content = build_phase_content()
    
    # Navigation buttons
    def go_prev():
        if current_phase > 1:
            set_phase(current_phase - 1)
    
    def go_next():
        if current_phase < 7:
            set_phase(current_phase + 1)
    
    def lock_phase():
        if current_phase not in locked_phases:
            set_locked(locked_phases + [current_phase])
            logs = get_logs()
            set_logs(logs + [f"[Generator] Phase {current_phase} locked"])
    
    def export_spec():
        root = get_root()
        output_path = Path(root) / "BUILD_SPEC.json"
        try:
            with open(output_path, 'w') as f:
                json.dump({
                    **spec,
                    "metadata": {
                        "generated_by": "Orchestr8 v3.0 Generator",
                        "generated_at": datetime.now().isoformat(),
                        "locked_phases": locked_phases
                    }
                }, f, indent=2)
            logs = get_logs()
            set_logs(logs + [f"[Generator] Exported BUILD_SPEC.json to {output_path}"])
            return mo.md(f"✅ **Exported successfully!**\n\nSaved to: `{output_path}`")
        except Exception as e:
            return mo.md(f"❌ **Export failed:** {str(e)}")
    
    prev_btn = mo.ui.button(
        label="← Previous",
        on_change=lambda _: go_prev(),
        disabled=current_phase == 1
    )
    
    next_btn = mo.ui.button(
        label="Next →",
        on_change=lambda _: go_next(),
        disabled=current_phase == 7
    )
    
    lock_btn = mo.ui.button(
        label="🔒 Lock Phase",
        on_change=lambda _: lock_phase(),
        disabled=current_phase in locked_phases
    )
    
    export_btn = mo.ui.button(
        label="📤 Export BUILD_SPEC.json",
        on_change=lambda _: export_spec()
    ) if current_phase == 7 else None
    
    # Phase indicator
    phase_indicators = " ".join([
        f"{'🔒' if i+1 in locked_phases else '⬜' if i+1 > current_phase else '✅' if i+1 < current_phase else '🔵'}"
        for i in range(7)
    ])
    
    # Build layout
    nav_row = mo.hstack([prev_btn, lock_btn, next_btn], justify="space-between")
    
    if current_phase == 7 and export_btn:
        nav_row = mo.hstack([prev_btn, export_btn], justify="space-between")
    
    return mo.vstack([
        mo.md(f"## ⚙️ Project Generator Wizard"),
        mo.md(f"**Phases:** {phase_indicators}"),
        progress,
        progress_bar,
        mo.md("---"),
        phase_content,
        mo.md("---"),
        nav_row
    ])
