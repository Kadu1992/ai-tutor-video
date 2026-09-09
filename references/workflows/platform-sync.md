# Platform Sync Workflow

Use when the user invokes `/platform-sync` or wants to synchronize study progress with the local course web platform (e.g. `cursos-estudo` / PythonWay API).

Read `references/architecture.md`, `references/state-contract.md`, and `references/learning-contract.md`.

## 1. Platform inspection (Pull)

1. Check platform connection and registered courses:
   `python <skill_root>/scripts/sync_platform.py --action pull --api-url <platform_api_url>`
2. Read course list from `GET /api/courses` and current recorded progress from `GET /api/progress`.
3. If the platform server is offline, display the friendly warning and proceed seamlessly with local IDE tutoring without halting.

## 2. Platform update (Push)

1. When a video lesson progress point is reached or mastery criteria are met:
   - Prepare payload containing `course_id`, `status` (`in-progress` or `completed`), tutor `notes`, `lastWatched` (with timestamp), and `completedPlaylists`.
2. Push updates to the platform API:
   `python <skill_root>/scripts/sync_platform.py --action push --api-url <platform_api_url> --course-id <course_id> --notes "<notes>" --last-watched "<title_and_checkpoint>"`
3. Confirm that both the web dashboard and local state in `.ai-tutor/state.json` reflect the same reality.
