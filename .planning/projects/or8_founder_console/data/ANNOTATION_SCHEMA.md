# Annotation Schema (SQLite)

Table: annotations
- id TEXT PRIMARY KEY
- artifact_path TEXT NOT NULL
- anchor TEXT NOT NULL
- author TEXT NOT NULL
- text TEXT NOT NULL
- media_json TEXT NOT NULL DEFAULT '[]'
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Table: packets_view_state
- packet_id TEXT PRIMARY KEY
- state_json TEXT NOT NULL
- updated_at TEXT NOT NULL
