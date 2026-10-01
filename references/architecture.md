# Architecture and Roots

## Root contract

`skill_root` is the directory containing the installed `SKILL.md`. Treat it as read-only. Resolve packaged files from it, never from the current shell directory.

`study_root` is the absolute directory explicitly selected by the user. One `study_root` contains one learning program. Do not guess it when more than one plausible directory exists.

Initialize with `python <skill_root>/scripts/init_study.py --study-root <study_root> --config-json <json>`.

## Study layout

When initializing in a project workspace, all study files are encapsulated in a single `ai-tutor/` directory:

```text
<workspace>/ai-tutor/
├── .ai-tutor/
│   ├── study-config.json
│   ├── state.json
│   ├── media-index.json
│   └── migrations/
├── curriculum.md
├── session-log.md
├── flashcards.md
├── lessons/
├── media/
├── projects/
└── transcripts/
```

Structured files are canonical. Markdown is a readable projection and carries stable IDs from structured state. The `transcripts/` directory stores Markdown transcripts ingested from YouTube via `yt-tool` and parsed by `scripts/parse_transcript.py`. All study artifacts live together inside `ai-tutor/`, preventing any clutter in the root of the user's workspace.

## Safe update protocol

1. Read and validate all canonical JSON.
2. Prepare the complete next revision in memory.
3. Check IDs, references, transitions, and learning invariants.
4. Write a temporary file beside each destination.
5. Replace canonical files atomically.
6. Update Markdown projections.
7. Run `python <skill_root>/scripts/validate_study.py <study_root>`.
## Dual storage architecture (IDE + Web Cockpit SQLite)

The AI Tutor Video operates on a synchronized dual storage pattern:

1. **IDE Workspace (`study_root`)**:
   - Holds 100% of the evidence-based study artifacts derived from the Lucas Mendes pedagogical model.
   - The student actively writes and runs executable Python code inside `projects/` (e.g. `projects/<topic-slug>/<script>.py`).
   - Lesson guides are generated under `lessons/<sequence>-<slug>.md`.
   - Active recall questions live in `flashcards.md`, the progressive roadmap in `curriculum.md`, and session logs in `session-log.md`.
   - Transcripts ingested from YouTube via `yt-tool` reside in `transcripts/`.
   - If the study directory layout is missing when a session or course starts, invoke `scripts/init_study.py` immediately to create all directories and baseline files.

2. **Relational Database & Web Cockpit (`pythonway.db`)**:
   - Stores course progress in the `user_progress` table (`status`, `notes`, `last_watched`, `completed_playlists`).
   - The web frontend/portal reads directly from SQLite to render visual dashboards, badges, and playlist checklists.
   - Sincronização bidirecional occurs seamlessly via `scripts/sync_platform.py` (`--action pull` at session start, `--action push` at session close/checkpoints).

## Portability

Scripts require Python 3.11+ and the standard library. Describe operations independently of shell; command examples may be adapted to PowerShell or POSIX shells.
