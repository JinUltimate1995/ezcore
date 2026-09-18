# ezCore Cloud Saves Specification

> **Version:** 1.0
> **Date:** 2026-09-16
> **Status:** Draft
> **Priority:** P0 — Primary selling point

---

## Overview

Cloud saves are ezCore's **#1 feature and primary differentiator**. Users can start a game on one device and continue on another — save states, in-game saves, settings, and cheat states all sync automatically.

**Privacy-first:** Login is optional. Guest mode stores everything locally with zero accounts. Cloud sync is opt-in — only save state bytes are uploaded. No usage analytics, no telemetry, no tracking. See ADR-007 in DECISIONS.md.

---

## What Syncs

| Data | Description | Size (typical) |
|---|---|---|
| **Save states** | Slot 0-9 per game | 1-10 MB each |
| **In-game saves** | SRAM/EEPROM/flash | 8 KB - 1 MB |
| **Settings** | Per-game and global settings | < 1 KB |
| **Cheat states** | Enabled/disabled cheats | < 1 KB |
| **Play time** | Total time played | < 100 bytes |
| **Last played** | Timestamp of last session | < 100 bytes |
| **Screenshots** | User-captured screenshots | 1-5 MB each |

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Device A  │────▶│  Cloud API  │◀────│   Device B  │
│  (Windows)  │     │  (REST)     │     │  (Android)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Local vault │     │  Firebase / │     │ Local vault │
│ (encrypted) │     │  Supabase   │     │ (encrypted) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Sync Flow

```
1. User plays a game on Device A
       ↓
2. Save state created (local)
       ↓
3. ezCore uploads save to cloud (background)
       ↓
4. User opens ezCore on Device B
       ↓
5. ezCore downloads save from cloud
       ↓
6. User continues where they left off
```

---

## Backend

**Firebase** (locked in — ADR-007).

| Service | Purpose |
|---|---|
| **Firebase Auth** | Optional account creation (email/password + OAuth) |
| **Firebase Storage** | Save state bytes (opaque, encrypted at rest) |
| **Firestore** | User profile, Pro status, last login (no usage data) |

**What we DON'T store:**
- Games played, play time, IP address, device info
- Crash logs, analytics events, telemetry
- Anything beyond save bytes + account basics

**Guest mode (default):** No account, no cloud, all saves local. Full functionality.

---

## Data Model

### User (opt-in only)

```json
{
  "uid": "abc123",
  "email": "user@example.com",
  "displayName": "RetroGamer",
  "pro": false,
  "createdAt": "2026-09-16T12:00:00Z",
  "lastLogin": "2026-09-16T12:00:00Z"
}
```

**No account = no data.** Guest mode stores everything locally. The cloud only ever sees opaque save bytes — never game titles, play history, or usage patterns.

### Game Save

```json
{
  "id": "game-save-001",
  "uid": "abc123",
  "gameId": "mesen-super-mario-bros",
  "coreId": "mesen",
  "slot": 0,
  "saveState": "<base64-encoded bytes>",
  "sram": "<base64-encoded bytes>",
  "settings": {
    "shader": "crt",
    "scale": "fit",
    "volume": 0.8
  },
  "cheats": [
    { "index": 0, "enabled": true, "code": "C2E9-..." }
  ],
  "playTime": 3600,
  "lastPlayed": "2026-09-16T12:00:00Z",
  "createdAt": "2026-09-16T12:00:00Z",
  "updatedAt": "2026-09-16T12:00:00Z"
}
```

### Save Slot

```json
{
  "id": "slot-001",
  "uid": "abc123",
  "gameId": "mesen-super-mario-bros",
  "slot": 0,
  "data": "<base64-encoded bytes>",
  "screenshot": "<base64-encoded image>",
  "createdAt": "2026-09-16T12:00:00Z"
}
```

---

## Sync Strategy

### Upload (Push)

1. User creates a save state
2. Save is written to local vault (encrypted)
3. Save is queued for cloud upload
4. Background task uploads to cloud
5. On success: mark as synced
6. On failure: retry with exponential backoff

### Download (Pull)

1. User opens a game
2. ezCore checks cloud for newer saves
3. If cloud save is newer: download and replace local
4. If local save is newer: upload to cloud
5. If conflict: prompt user to choose

### Conflict Resolution

| Strategy | Description |
|---|---|
| **Last-write-wins** | Most recent save wins (default) |
| **Manual merge** | User chooses which save to keep |
| **Keep both** | Rename and keep both saves |

**Default:** Last-write-wins with manual merge option.

---

## Offline Support

ezCore works offline — cloud sync is a convenience, not a requirement:

1. All saves are stored locally first
2. Cloud sync happens in the background when online
3. When offline: saves are queued and synced when connection returns
4. No data is ever lost due to network issues

### Offline Queue

```dart
class SyncQueue {
  // Queue of pending uploads
  List<SyncOperation> pending;

  // Process queue when online
  Future<void> processQueue();

  // Add operation to queue
  void enqueue(SyncOperation op);

  // Clear queue after successful sync
  void clear();
}
```

---

## Security

### Encryption

- **Local vault:** AES-256 encryption (key stored in OS keychain)
- **Cloud data:** Encrypted at rest (Firebase/Supabase default)
- **Transport:** TLS 1.3 for all API calls

### Access Control

- Users can only access their own saves
- Firebase Security Rules / Supabase RLS enforce this
- No public read access to any save data

### Privacy

- Save bytes are opaque — ezCore never interprets them
- No telemetry or analytics on save data
- Users can delete all cloud data at any time

---

## API Endpoints

### Firebase (v1) — Opt-In Auth

**Authentication is optional.** Users who never sign in use Guest mode (local saves only). Authentication only happens when the user explicitly opts into cloud sync.

| Auth Method | Platform | Notes |
|---|---|---|
| Email/password | All | Desktop + mobile |
| Google OAuth | All | One-tap sign-in |
| Apple OAuth | iOS / macOS | Required for App Store |
| Guest mode | All | No auth, no cloud, local-only |

**Firestore (user data — only if opted in):**

| Endpoint | Method | Description |
|---|---|---|
| `/saves/{uid}/{gameId}` | GET | Get all saves for a game |
| `/saves/{uid}/{gameId}/{slot}` | GET | Get a specific save slot |
| `/saves/{uid}/{gameId}/{slot}` | PUT | Upload a save |
| `/saves/{uid}/{gameId}/{slot}` | DELETE | Delete a save |
| `/users/{uid}` | GET | Get user profile |
| `/users/{uid}` | PUT | Update user profile |

**What we never collect (even from opted-in users):**
- Game titles played
- Play time, session duration
- IP addresses, device fingerprints
- Crash logs with usage context
- Analytics events

### Supabase (v2)

| Endpoint | Method | Description |
|---|---|---|
| `/rest/v1/saves?uid=eq.{uid}` | GET | Get all saves for a user |
| `/rest/v1/saves?id=eq.{id}` | GET | Get a specific save |
| `/rest/v1/saves` | POST | Upload a save |
| `/rest/v1/saves?id=eq.{id}` | DELETE | Delete a save |

---

## Save State Flow (C++ Runtime)

```
1. User presses "Save State"
       ↓
2. Flutter calls ezcore_serialize_size(s)
       ↓
3. Flutter allocates buffer
       ↓
4. Flutter calls ezcore_serialize(s, buffer, size)
       ↓
5. C++ runtime calls retro_serialize(s, buffer, size)
       ↓
6. Flutter receives opaque bytes
       ↓
7. Flutter writes to local vault
       ↓
8. Flutter queues for cloud upload
       ↓
9. Background task uploads to cloud
```

---

## Implementation Phases

### Phase 1: Local Saves (Weeks 5-10)

- [ ] C++ runtime: `ezcore_serialize`, `ezcore_unserialize`
- [ ] Flutter: Local save/load (file system)
- [ ] Save state slots (0-9)
- [ ] In-game save (SRAM) backup

### Phase 2: Cloud Sync (Weeks 17-22)

- [ ] Firebase setup
- [ ] User authentication
- [ ] Cloud upload/download
- [ ] Conflict resolution
- [ ] Offline queue

### Phase 3: Advanced (Weeks 23-28)

- [ ] Save state screenshots
- [ ] Save state sharing (export/import)
- [ ] Cloud storage management
- [ ] Storage quota enforcement

---

## Free vs Pro

| Feature | Free | Pro |
|---|---|---|
| Local saves | ✅ | ✅ |
| Cloud saves | ❌ | ✅ |
| Save slots | 3 | 10 |
| Cloud storage | — | 1 GB |
| Save sharing | ❌ | ✅ |
| Priority sync | ❌ | ✅ |

---

## Open Questions

1. **Storage quota:** How much cloud storage for Pro users? (Current: 1 GB)
2. **Save sharing:** Should users be able to share save states publicly?
3. **Migration:** How to migrate from Firebase to Supabase if needed?
4. **Guest → Pro upgrade path:** How seamless is the transition when a guest creates an account?
