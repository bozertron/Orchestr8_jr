# LOWER FIFTH TRUTH TABLE

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Definitive specification for the Lower Fifth control surface (footer).

## Anatomy

```
+------------------------------------------------------------------+
|                    [Maestro Input Bar]                            |
|              "What would you like to accomplish?"                 |
+------------------------------------------------------------------+
|   [Apps][Calendar*][Comms*][Files]  [MAESTRO]  [Search][Record][Play][Phreak>][Send][Attach]   |
+------------------------------------------------------------------+
```

## Component Specification

### Input Bar

| Property | Value |
|----------|-------|
| Width | 100% (max 800px) |
| Padding | 8px 0 |
| Font | Poiret One, 1.2rem |
| Color | #fff |
| Border | none, bottom 1px rgba(255,255,255,0.3) |
| Align | center |
| Placeholder | "What would you like to accomplish?" |
| Focus Border | --teal (#00E5E5) |

### MAESTRO Button (Center Anchor)

| Property | Value |
|----------|-------|
| Height | 36px |
| Padding | 0 25px |
| Background | --gold-dark (#C5A028) |
| Color | --teal (#00E5E5) |
| Border | 1px solid --gold-light (#F4C430) |
| Font | Poiret One, 14px, weight 900 |
| Transform | uppercase |
| Letter Spacing | 3px |
| Shadow | 0 0 15px rgba(197,160,40,0.3) |
| Border Radius | 2px |
| Margin | 0 15px (separation from groups) |

MAESTRO Hover:
- Background: #dcb32d
- Shadow: 0 0 25px rgba(197,160,40,0.6)
- Transform: scale(1.05)

### Mini Buttons

| Property | Value |
|----------|-------|
| Height | 22px |
| Padding | 0 12px |
| Min Width | 60px |
| Background | rgba(255,255,255,0.05) |
| Color | #AAA |
| Border | 1px solid rgba(255,255,255,0.15) |
| Border Radius | 2px |
| Font | Poiret One, 11px, weight 600 |
| Transform | uppercase |
| Letter Spacing | 1px |

Mini Button Hover:
- Background: rgba(255,255,255,0.2)
- Color: #FFF
- Border Color: #FFF

### Phreak Button Variant

| Property | Difference |
|----------|------------|
| Font Style | italic |
| Border | rgba(255,255,255,0.3) |

## Layout Truth Table

| Condition | Left Group | Center | Right Group |
|-----------|------------|--------|-------------|
| Standard | 4 buttons | MAESTRO | 6 buttons |
| Mobile (future) | 2 buttons | MAESTRO | 3 buttons |
| Compact | 3 buttons | MAESTRO | 4 buttons |

## Button Group Composition

### Left Group (4)

| Order | Button | Type |
|-------|--------|------|
| 1 | Apps | Standard |
| 2 | Calendar* | Future marker |
| 3 | Comms* | Future marker |
| 4 | Files | Standard |

### Right Group (6)

| Order | Button | Type |
|-------|--------|------|
| 1 | Search | Standard |
| 2 | Record | Standard |
| 3 | Play | Standard |
| 4 | Phreak> | Special (italic) |
| 5 | Send | Standard |
| 6 | Attach | Standard |

## Interaction Semantics

| Button | Current State | Target Behavior | Contract |
|--------|---------------|-----------------|----------|
| Apps | Placeholder | Application launcher | TBD |
| Calendar* | Placeholder | Calendar integration | TBD |
| Comms* | Placeholder | Communications panel | TBD |
| Files | Placeholder | File browser | TBD |
| MAESTRO | Interactive | Flagship agent activation | CRITICAL |
| Search | Placeholder | Search function | TBD |
| Record | Placeholder | Recording toggle | TBD |
| Play | Placeholder | Playback control | TBD |
| Phreak> | Placeholder | Special action | TBD |
| Send | Placeholder | Send action | TBD |
| Attach | Placeholder | Attachment function | TBD |

## Symmetry Rules

1. MAESTRO is always center-anchored
2. Left and right groups symmetrically spaced
3. Button heights: MAESTRO (36px) > Mini (22px)
4. Gap between groups and MAESTRO: 15px margin

## Container Properties

| Property | Value |
|----------|-------|
| Background | linear-gradient(to top, #000 80%, transparent) |
| Padding | 0 40px 30px 40px |
| Display | flex, column |
| Gap | 15px |

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial truth table | P07-A1 |
