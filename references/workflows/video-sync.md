# Video Sync Workflow

Use when the user invokes `/video-sync`, `/video`, provides a YouTube link or video ID, or wants to ingest video classes for study.

Read `references/architecture.md`, `references/state-contract.md`, and `references/learning-contract.md`.

## 1. Transcript ingestion via yt-tool

1. Run the terminal command:
   `yt-tool transcript "<URL_or_ID>"`
2. Verify the generated transcript Markdown in the `transcripts/` directory (`transcripts/<id>_<slug>.md`). Ensure the file is preserved in `<study_root>/transcripts/`.

## 2. Transcript parsing

1. Execute the parser utility:
   `python <skill_root>/scripts/parse_transcript.py --file <path_to_transcript> --pretty`
2. Extract the structured representation:
   - Video metadata: title, channel, duration, duration in seconds, and video ID.
   - Key topics and concepts in chronological order with timestamps (`paused_at`).
   - Real analogies and code examples used by the instructor.
   - Specific challenges, exercises, or homework proposed during the class.

## 3. Curriculum and state integration

1. Map the video to a structured topic and planned lesson in `curriculum.md` and `.ai-tutor/state.json`.
2. Populate the `video_metadata` and `checkpoint` object for the corresponding lesson:
   - Initialize `checkpoint` with `paused_at: "00:00"`, `paused_at_seconds: 0`, and `status: "not_started"`.
   - List extracted concepts under `concepts_pending`.
3. For playlists or sequential modules, organize the classes in chronological order, respecting prerequisites.
4. Validate canonical state with `scripts/validate_study.py`.
