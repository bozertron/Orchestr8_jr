    # VISUAL TOKEN LOCK

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Immutable registry of visual design tokens. Changes require Founder approval.

## Color Tokens (LOCKED)

### Primary Palette

| Token | Hex | RGB | Usage | Lock Status |
|-------|-----|-----|-------|-------------|
| `--bg-obsidian` | #050505 | 5,5,5 | Background base | LOCKED |
| `--gold-dark` | #C5A028 | 197,160,40 | Primary accent, borders | LOCKED |
| `--gold-light` | #F4C430 | 244,196,48 | Highlight accent, hover | LOCKED |
| `--teal` | #00E5E5 | 0,229,229 | Secondary accent, text | LOCKED |
| `--text-grey` | #CCC | 204,204,204 | Standard text | LOCKED |

### Extended Palette (Derived)

| Token | Hex | Usage | Lock Status |
|-------|-----|-------|-------------|
| `--void-text` | rgba(255,255,255,0.04) | Void label opacity | LOCKED |
| `--button-bg-subtle` | rgba(197,160,40,0.1) | Subtle button fill | LOCKED |
| `--border-gold-faint` | rgba(197,160,40,0.3) | Faint gold border | LOCKED |
| `--text-dim` | rgba(255,255,255,0.4) | Dimmed text | LOCKED |
| `--scanline-black` | rgba(0,0,0,0.25) | Scanline effect | LOCKED |

### State Colors

| State | Token | Hex | Usage |
|-------|-------|-----|-------|
| Working | `--state-working` | #D4AF37 | Gold - operational |
| Broken | `--state-broken` | #1fbdea | Blue - needs attention |
| Combat | `--state-combat` | #9D4EDD | Purple - agents active |

## Typography Tokens (LOCKED)

### Font Stack

| Token | Value | Weight | Usage |
|-------|-------|--------|-------|
| `--font-header` | 'Marcellus SC', serif | 400 | Major headers, top buttons |
| `--font-ui` | 'Poiret One', cursive | 400 | UI labels, mini buttons |
| `--font-data` | 'VT323', monospace | 400 | Data, status, terminal |

### Size Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--size-xs` | 10px | Status text |
| `--size-sm` | 11px | Mini button text |
| `--size-md` | 14px | MAESTRO button |
| `--size-lg` | 1.2rem | Top buttons |
| `--size-xl` | 1.5rem | Init button |
| `--size-void` | 3rem | Void label |

### Letter Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--tracking-tight` | 1px | Mini buttons |
| `--tracking-normal` | 2px | Top buttons |
| `--tracking-wide` | 3px | MAESTRO button |
| `--tracking-void` | 12px | Void label |

## Spacing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 8px | Internal button padding |
| `--space-sm` | 12px | Mini button horizontal |
| `--space-md` | 15-25px | Button deck margins |
| `--space-lg` | 30-40px | Header/footer padding |
| `--gap-btn-group` | 8px | Button group gap |
| `--gap-deck-row` | 20px | Deck row gap |

## Dimension Tokens

### Header

| Token | Value |
|-------|-------|
| `--header-height` | 80px |
| `--top-btn-height` | 50px |
| `--top-btn-min-width` | 160px |

### Footer (Lower Fifth)

| Token | Value |
|-------|-------|
| `--input-padding` | 8px 0 |
| `--btn-mini-height` | 22px |
| `--btn-mini-min-width` | 60px |
| `--btn-maestro-height` | 36px |

## Effect Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--glow-gold-hover` | 0 0 20px rgba(197,160,40,0.3) | Button hover |
| `--glow-gold-intense` | 0 0 30px rgba(197,160,40,0.4) | Button intense |
| `--shadow-btn` | 0 4px 10px rgba(0,0,0,0.5) | Button shadow |
| `--shadow-maestro` | 0 0 15px rgba(197,160,40,0.3) | MAESTRO button |

## Animation Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--transition-fast` | 0.2s | Button micro-interactions |
| `--transition-normal` | 0.3s | Standard transitions |
| `--transition-slow` | 0.5s | Overlay fade |
| `--transition-emergence` | 2s | UI layer fade |

## Change Protocol

Token changes require:

1. Proposal via packet with rationale
2. Visual comparison evidence
3. Codex review
4. Founder approval

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial token lock | P07-A1 |
