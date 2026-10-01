# Setup Workflow

Read `references/architecture.md`, `references/state-contract.md`, and `references/learning-contract.md`.

Collect persisted fields: topic, concrete goal, initial level, weekly hours, preferred times, deadline, language, accessibility needs, source preferences, and explicit study root. When run inside a workspace or course project repository, default `study_root` to `<workspace>/ai-tutor` so that all generated files and folders are encapsulated in one clean directory. When starting from a video course or YouTube playlist, optionally collect `playlist_url`, `course_id`, and `platform_api_url` (defaults to `http://localhost:8000`). When `pythonway.db` exists in the workspace, automatically detect course catalog and baseline progress using `scripts/sync_platform.py --action pull`. Accept one complete answer or ask one missing field at a time.

Summarize the proposed configuration and obtain confirmation before writing. Run `scripts/init_study.py` using the absolute study root (`<workspace>/ai-tutor`) and structured JSON to generate the complete directory tree (`.ai-tutor/`, `curriculum.md`, `session-log.md`, `flashcards.md`, `lessons/`, `projects/`, `transcripts/`, `media/`). Never overwrite an existing `.ai-tutor/`; use migration when v1 state exists.

After initialization, create an initial curriculum with observable outcomes (organizing video lessons if a playlist was provided) but do not mark evidence or mastery. Validate the study with `scripts/validate_study.py` and show created paths.
