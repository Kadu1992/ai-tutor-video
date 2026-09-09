# Platform Sync Workflow

Use when the user invokes `/platform-sync` or wants to synchronize study progress with the local course platform (e.g. `cursos-estudo` / PythonWay SQLite database and API).

Read `references/architecture.md`, `references/state-contract.md`, and `references/learning-contract.md`.

## 1. Direct SQLite & Platform Inspection (Pull)

1. Check platform connection and registered courses:
   `python <skill_root>/scripts/sync_platform.py --action pull`
   * The script automatically discovers and reads directly from `pythonway.db` via `sqlite3` without needing a web server running.
   * If working with a remote web portal, pass `--api-url <platform_api_url>` or `--no-db`.
2. Inspect courses and recorded progress (`status`, `notes`, `last_watched`, `completed_playlists`).
3. If both SQLite and HTTP are unreachable, proceed seamlessly with local IDE tutoring using `.ai-tutor/state.json`.

## 2. Platform Update (Push)

1. When a video lesson progress point is reached or mastery criteria are met:
   - Prepare payload containing `course_id`, `status` (`in-progress` or `completed`), tutor `notes`, `lastWatched` (with timestamp), and `completedPlaylists`.
2. Push updates directly to the platform database:
   `python <skill_root>/scripts/sync_platform.py --action push --course-id <course_id> --notes "<notes>" --last-watched "<title_and_checkpoint>"`
3. Confirm that both the local course database (`pythonway.db`) and `.ai-tutor/state.json` reflect the same reality.
