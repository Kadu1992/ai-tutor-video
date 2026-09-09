# Session Workflow

Read and validate canonical state before the first learning question.

## Resume

Resume the latest `in_progress` session. If none exists, resume the latest `interrupted` session whose `resumable` field is true by adding the `resumed` transition. Recover its checkpoint, lesson IDs, weak points, and next action. Open a new session only when no resumable work exists.

Reconcile local canonical state with the local course platform database (`pythonway.db` via `python <skill_root>/scripts/sync_platform.py --action pull`). If changes were made on the web portal (such as marking completed playlists or updating notes), reflect them into the study state before beginning the session.

If the previous session was interrupted unexpectedly (e.g. computer shutdown or power outage), detect the missing closure, transition from `interrupted` to `resumed`, recover the last recorded checkpoint atomically, and confirm with the student before continuing.

For video-anchored lessons, inspect `video_metadata.checkpoint` (`paused_at`, `paused_at_seconds`, `concepts_covered`, and `concepts_pending`). Open the session with a contextual check:
- Greet the student mentioning the last registered paused timestamp and lesson title.
- Inquire whether they watched further or wish to verify and practice concepts covered up to that point before advancing.

## Conduct

1. Confirm one prerequisite with one question.
2. Set one observable session objective.
3. Teach one idea from concrete to abstract, anchoring explanations and analogies in the video lesson when available.
4. Request an autonomous explanation or application (never give solutions upfront; require student implementation in the IDE).
5. Apply the help ladder without counting guided work as independent evidence.
6. Record evidence, retention, weak points, cards, and next focus under the normative contracts.

## Close

On completion or interruption, append the valid transition, record timestamps, checkpoint (including updated `paused_at` and `paused_at_seconds` for video lessons), topics, evidence IDs, difficulty, next step, and files changed. Update lesson state independently. Validate canonical state after the atomic update. Synchronize updated progress directly to the local SQLite database (`pythonway.db`) and course platform with `python <skill_root>/scripts/sync_platform.py --action push`.
