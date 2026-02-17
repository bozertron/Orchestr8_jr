# Button Patterns - Orchestr8 Stylization PRD Tasks 12 & 19

## Typography Variables (Task 12)

### Source: legacy pattern bible + font_profiles.py

```css
--font-headline: 'Orchestr8 HardCompn', 'Orchestr8 CalSans', 'Trebuchet MS', sans-serif;
--font-body: 'Orchestr8 CalSans', 'Segoe UI', 'Helvetica Neue', sans-serif;
--font-mono: 'Orchestr8 Mini Pixel', 'Courier New', monospace;
```

**Status:** Implemented in `orchestr8.css` via `--orchestr8-font-*` runtime variables from `font_profiles.py`.

---

## Button Patterns (Task 19)

### Source: `Settings For Integration Referece/settings.html`

#### Base Button (.btn)
```css
.btn {
    padding: 10px 16px;
    border-radius: 8px;
    border: 1px solid var(--bd);
    background: transparent;
    color: var(--t1);
    cursor: pointer;
    font-size: 14px;
    font-family: inherit;
    transition: all 0.2s;
}
.btn:hover { background: var(--n2); border-color: var(--vio); }
```

#### Primary Button (.btn-primary)
```css
.btn-primary {
    background: var(--vio);
    border-color: var(--vio);
    color: #fff;
}
.btn-primary:hover { filter: brightness(1.1); }
```

#### Danger Button (.btn-danger)
```css
.btn-danger {
    border-color: var(--mag);
    color: var(--mag);
}
.btn-danger:hover { background: rgba(255, 0, 153, 0.1); }
```

#### Toggle Switch (.toggle)
```css
.toggle {
    position: relative;
    width: 44px;
    height: 24px;
    background: var(--n2);
    border: 1px solid var(--bd);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s;
}
.toggle.active { background: var(--vio); border-color: var(--vio); }
.toggle::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 18px;
    height: 18px;
    background: var(--t1);
    border-radius: 50%;
    transition: transform 0.2s;
}
.toggle.active::after { transform: translateX(20px); }
```

#### Slider/Range Input (.slider)
```css
.slider {
    flex: 1;
    height: 6px;
    background: var(--n2);
    border-radius: 3px;
    appearance: none;
}
.slider::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    background: var(--cyan);
    border-radius: 50%;
    cursor: pointer;
}
.slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background: var(--cyan);
    border-radius: 50%;
    cursor: pointer;
    border: none;
}
```

#### Form Inputs
```css
.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea,
.form-group select {
    width: 100%;
    background: var(--n2);
    color: var(--t1);
    border: 1px solid var(--bd);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 14px;
    font-family: inherit;
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    outline: none;
    border-color: var(--cyan);
    background: #0b1118;
}
```

---

### Source: `one integration at a time/UI Reference/MaestroView.vue`

#### Top Button (.top-btn)
```css
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
```

#### Control Button (.ctrl-btn)
```css
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
.ctrl-btn:hover { color: #D4AF37; }
.ctrl-btn.active { color: #D4AF37; }
.ctrl-btn:disabled { opacity: 0.3; cursor: not-allowed; }
```

#### Center Button (.maestro-center)
```css
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
```

---

## Color Token Mapping

| Legacy Token | Orchestr8 Variable |
|---------------|-------------------|
| `--n0` | `--bg-primary` (#0A0A0B) |
| `--n1` | `--bg-elevated` (#121214) |
| `--n2` | `--bg-surface` (#1a1a1c) |
| `--bd` | `rgba(31, 189, 234, 0.3)` |
| `--t1` | `--text-primary` (#e8e8e8) |
| `--t2` | `--text-secondary` (#a0a0a0) |
| `--t3` | `--text-muted` (#666666) |
| `--vio` | `--gold-metallic` (#D4AF37) |
| `--cyan` | `--blue-dominant` (#1fbdea) |
| `--mag` | `--purple-combat` (#9D4EDD) |
| `--grn` | (not defined - use cyan or add) |

---

## Files Modified

1. **orchestr8.css** - Added toggle, slider, and form patterns
2. **button_patterns.md** - This documentation

## Usage

Import via Python:
```python
from IP.styles.font_profiles import build_font_profile_css
```

CSS is auto-loaded by `06_maestro.py` via `load_orchestr8_css()`.
