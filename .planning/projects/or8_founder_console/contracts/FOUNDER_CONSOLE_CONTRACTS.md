# Founder Console Contracts (Draft)

## PacketCard
- phase
- packet_id
- lane
- owner
- percent_complete
- gate_color
- eta
- blockers_count
- last_observation_id

## ArtifactComment
- artifact_path
- anchor
- author
- text
- media_refs[]
- ts

## CommsMessageDraft
- to
- from
- phase
- packet_id
- kind
- requires_ack
- body

## UnreadStatus
- agent_id
- unread_messages
- unread_guidance_phases[]
