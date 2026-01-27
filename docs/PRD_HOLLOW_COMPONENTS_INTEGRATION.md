# PRD: Hollow Components Integration

**Version:** 1.0  
**Created:** 2026-01-25  
**Status:** READY FOR BIG PICKLE  
**Priority:** CRITICAL - These are the gaps blocking actual coding use

---

## Executive Summary

The Orchestr8 UI has beautiful components that are **not wired to actual functionality**. This PRD addresses the hollow shells that need real implementation to make Orchestr8 usable for coding.

**Current State:**
```
USER TYPES MESSAGE → handle_send() → FAKE PLACEHOLDER RESPONSE
                                      ↓
                              No API call, no LLM, nothing
```

**Target State:**
```
USER TYPES MESSAGE → handle_send() → API Call → Real LLM Response
                                      ↓
                              Combat Tracker → Purple Glow in Code City
```

---

## Component Gap Analysis

### 1. LLM Integration (CRITICAL)

**File:** `IP/plugins/06_maestro.py`  
**Line:** 355 - `# TODO: Replace with actual LLM integration`

**Current:** `handle_send()` creates a fake placeholder response  
**Needed:** Real API call to Claude/OpenAI with context injection

**Existing Assets:**
- `IP/briefing_generator.py` - Can generate context
- `IP/combat_tracker.py` - Can track active deployments
- `.taskmaster/config.json` - Has model configuration

### 2. Terminal Spawning (HIGH)

**File:** `IP/plugins/06_maestro.py`  
**Line:** 677-679 - Phreak> button toggles state but spawns nothing

**Current:** Button sets `get_show_terminal()` state, no terminal appears  
**Needed:** Call `TerminalSpawner` to actually spawn actu8 terminal

**Existing Assets:**
- `IP/terminal_spawner.py` - Already built, just not wired

### 3. Combat Tracker → Woven Maps (HIGH)

**File:** `IP/woven_maps.py`  
**Current:** Nodes only show Gold (working) or Blue (broken)  
**Needed:** Query CombatTracker and show Purple for files with active LLM

**Existing Assets:**
- `IP/combat_tracker.py` - Has `is_in_combat(file_path)` method
- `IP/woven_maps.py` - Has purple color defined but not used

### 4. Settings → Actual Config (MEDIUM)

**File:** `IP/plugins/07_settings.py`  
**Current:** Reads/writes TOML but nothing consumes the settings  
**Needed:** LLM integration should read model/API key from settings

---

## Technical Specifications

### Task 1: Wire LLM API Call

**File:** `IP/plugins/06_maestro.py`

Replace the placeholder in `handle_send()` with:

```python
def handle_send() -> None:
    """Send message to Claude API."""
    text = get_user_input().strip()
    if not text:
        return

    messages = get_messages()
    root = get_root()
    selected = get_selected()

    # Add user message
    user_msg = {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": text,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    messages.append(user_msg)

    # Generate context using existing BriefingGenerator
    briefing = BriefingGenerator(root)
    context = briefing.generate_context(selected or root)

    # Call Claude API
    try:
        import anthropic
        client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            system=context,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages if m["role"] in ("user", "assistant")]
        )
        
        assistant_content = response.content[0].text
        
        # Track as combat if working on a file
        if selected:
            from IP.combat_tracker import CombatTracker
            tracker = CombatTracker(root)
            tracker.deploy(selected, "maestro-chat", "claude-sonnet-4")
        
    except Exception as e:
        assistant_content = f"Error calling Claude API: {str(e)}"
        log_action(f"API Error: {str(e)}")

    assistant_msg = {
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_content,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    messages.append(assistant_msg)

    set_messages(messages)
    set_user_input("")
    log_action(f"Message sent: {text[:50]}...")
```

### Task 2: Wire Terminal Spawner

**File:** `IP/plugins/06_maestro.py`

The import already exists (line 40). Add terminal spawn to Phreak> handler:

```python
def handle_terminal() -> None:
    """Toggle terminal panel and spawn actu8 if opening."""
    current = get_show_terminal()
    set_show_terminal(not current)
    
    if not current:  # Opening terminal
        root = get_root()
        selected = get_selected()
        
        spawner = TerminalSpawner(root)
        terminal_id = spawner.spawn_terminal(
            working_dir=root,
            title=f"actu8 - {selected or 'maestro'}"
        )
        
        # Track in combat if file selected
        if selected:
            from IP.combat_tracker import CombatTracker
            tracker = CombatTracker(root)
            tracker.deploy(selected, terminal_id, "terminal")
        
        log_action(f"Terminal spawned: {terminal_id}")
    else:
        log_action("Terminal closed")
```

### Task 3: Combat Status in Woven Maps

**File:** `IP/woven_maps.py`

In `build_graph_data()` function, after creating nodes, check combat status:

```python
# After node creation loop, check combat status
try:
    from IP.combat_tracker import CombatTracker
    tracker = CombatTracker(root)
    combat_files = tracker.get_combat_files()
    
    for node in nodes:
        if node.path in combat_files:
            node.status = "combat"  # Will render as Purple
except ImportError:
    pass  # Combat tracker not available
```

### Task 4: Settings Integration

**File:** `IP/plugins/06_maestro.py`

Read model settings from TOML:

```python
def get_model_config() -> dict:
    """Get model configuration from settings."""
    try:
        import toml
        settings_file = Path("orchestr8_settings.toml")
        if settings_file.exists():
            settings = toml.load(settings_file)
            return settings.get("agents", {}).get("director", {})
    except Exception:
        pass
    
    # Fallback defaults
    return {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8192
    }
```

---

## Color Constants (NO EXCEPTIONS)

| State | Color | Hex | When Used |
|-------|-------|-----|-----------|
| Working | Gold | `#D4AF37` | All imports resolve, no active LLM |
| Broken | Blue | `#1fbdea` | Has unresolved imports |
| Combat | Purple | `#9D4EDD` | LLM currently deployed to this file |

---

## Dependencies

| Task | Depends On | Priority |
|------|------------|----------|
| LLM API Integration | anthropic package | CRITICAL |
| Terminal Spawner | None (already built) | HIGH |
| Combat → Woven Maps | CombatTracker | HIGH |
| Settings Integration | toml package | MEDIUM |

---

## Testing Strategy

1. **LLM Integration:** Type message, verify actual Claude response appears
2. **Terminal:** Click Phreak>, verify terminal window spawns
3. **Combat Status:** Deploy to file, verify purple glow in Code City
4. **Settings:** Change model in Settings, verify new model used

---

## Files Modified

- `IP/plugins/06_maestro.py` - Main integration point
- `IP/woven_maps.py` - Combat status query
- `IP/terminal_spawner.py` - May need spawn method enhancement

## Files Referenced (Read-Only)

- `IP/combat_tracker.py` - Already complete
- `IP/briefing_generator.py` - Already complete
- `orchestr8_settings.toml` - Settings source
