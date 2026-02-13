# contracts/__init__.py Integration Guide

- Source: `IP/contracts/__init__.py`
- Total lines: `56`
- SHA256: `b4f335422db517f892feed174246e0032a37e0e9292322185e03cfd4a8762b51`
- Role: **Contract export hub** — canonical imports for blind-safe integration schemas

## Why This Is Painful

- Export drift here silently breaks downstream imports.
- New contract modules must be added in both import section and `__all__` to be discoverable.
- This file is the stable API surface for bridge and validator code.

## Anchor Lines

- `IP/contracts/__init__.py:16` node event contract exports
- `IP/contracts/__init__.py:24` building panel contract exports
- `IP/contracts/__init__.py:30` connection action contract exports
- `IP/contracts/__init__.py:52` `ConnectionActionEvent` included in `__all__`
- `IP/contracts/__init__.py:54` `validate_connection_action_event` included in `__all__`

## Integration Use

- Import contracts from `IP.contracts` in runtime code and tests.
- Keep export list additive and explicit for compact-safe discovery.
