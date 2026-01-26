project_root/
├── IP/
│   ├── __init__.py         # (Empty) Makes IP importable
│   ├── orchestr8_app.py    # (Host) The Main Marimo Application
│   ├── louis_core.py       # (Logic) The File Warden
│   ├── carl_core.py        # (Logic) The Context Bridge
│   ├── connie.py           # (Logic) The Database Converter
│   └── plugins/            # (Python UI Plugins)
│       ├── 01_generator.py # The 7-Phase Wizard
│       ├── 02_explorer.py  # The Carl UI
│       ├── 03_gatekeeper.py# The Louis UI
│       ├── 04_connie_ui.py # The Connie UI
│       └── 05_cli_bridge.py# (New) The TypeScript Scaffold Bridge
├── frontend/tools/
│   ├── scaffold-cli.ts     # (The TS Protocol Source)
│   ├── unified-context-system.ts
│   └── parsers/            # (Future TS Plugins live here)
└── .louis-control/         # Configuration storage
