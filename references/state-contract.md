# State Contract v2

Every productive JSON document has `schema_version: 2`. IDs are non-empty, globally unique strings with semantic prefixes such as `study_`, `topic_`, `session_`, `evidence_`, `lesson_`, `card_`, `weak_`, `project_`, and `media_`.

## Canonical files

`study-config.json` stores every setup answer: study ID, topic, goal, deadline, weekly hours, preferred times, initial level, language, accessibility needs, source policy, and revocable external consents.

`state.json` contains `revision`, `updated_at`, `topics`, `evidences`, `sessions`, `lessons`, `weak_points`, `projects`, and `next_focus`.

Topics contain `topic_id`, `name`, `mastery`, `retention`, `status`, `last_practice`, and `evidence_ids`. Status is `not_started` for 0, `in_progress` for 20–60, and `mastered` for 80–100.

Evidences contain `evidence_id`, `topic_id`, `session_id`, `kind`, `autonomous`, `transfer`, `context`, `recorded_at`, `reference`, `result`, and `error`. `reference.type` cannot be `media`.

`media-index.json` contains artifact metadata: IDs, type, provider, source IDs, pedagogical objective, local path or URL, status, dates, verification, accessibility, and `evidence_eligible: false`.

## Sessions

Allowed transitions:

```text
in_progress → completed
in_progress → interrupted
interrupted → resumed
resumed → completed
resumed → interrupted
```

Resume the most recent `in_progress` session; otherwise resume the most recent `interrupted` session with `resumable: true`. Completed sessions require `ended_at` and cannot resume.

## Lessons

Lesson status is `planned`, `in_progress`, `blocked`, `completed`, or `archived`. Sessions and lessons have a many-to-many relationship. Advancing depends on lesson status and evidence, never only on session status.

## Validation

Run `scripts/validate_study.py` after changes. Never invent dates, evidence, IDs tied to nonexistent entities, or missing setup answers.
