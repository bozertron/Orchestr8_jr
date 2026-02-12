# Building Panel Template

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  BUILDING: [FILENAME]                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  IMPORTS              │  EXPORTS              │  FUNCTIONS                  │
│  ────────             │  ────────             │  ──────────                 │
│  ○ [module]           │  ● [export]           │  ◆ [func]()    [COLOR]     │
│  ○ [module]           │  ● [export]           │  ◆ [func]()    [COLOR]     │
│  ○ [module]           │  ● [export]           │  ◆ [Class]     [COLOR]     │
├─────────────────────────────────────────────────────────────────────────────┤
│  WIRING:                                                                    │
│  → [module].[func]() [COLOR - status]                                       │
│  ← [export] consumed by [file] [COLOR - status]                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  METRICS: [tokens] tokens │ complexity [N] │ [rooms] rooms                  │
│  AGENTS: [N] assigned │ [N] complete │ [N] active                           │
└─────────────────────────────────────────────────────────────────────────────┘

Colors:
• GOLD (#D4AF37) = working
• TEAL (#1fbdea) = needs work / needs rewiring
• PURPLE (#9D4EDD) = agents actively deployed
```
