# IP/maestro.py (The Brain)
import socketio
import json

sio = socketio.AsyncServer(cors_allowed_origins='*')

@sio.event
async def update_fiefdom(sid, data):
    # When Carl detects a health change
    fiefdom_state = {
        "path": "src/modules/generator",
        "status": "BROKEN", # or WORKING, COMBAT
        "errors": ["TS2322..."],
        "active_agents": 3
    }
    # Broadcast to all connected browsers (The Eyes)
    await sio.emit('fiefdom_update', fiefdom_state)
