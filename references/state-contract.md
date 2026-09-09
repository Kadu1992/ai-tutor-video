# State Contract v2

Every productive JSON document has `schema_version: 2`. IDs are non-empty, globally unique strings with semantic prefixes such as `study_`, `topic_`, `session_`, `evidence_`, `lesson_`, `card_`, `weak_`, `project_`, and `media_`.

## Canonical files

`study-config.json` stores every setup answer: study ID, topic, goal, deadline, weekly hours, preferred times, initial level, language, accessibility needs, source policy, and revocable external consents. It may also include optional course platform settings: `course_id`, `playlist_url`, and `platform_api_url`.

`state.json` contains `revision`, `updated_at`, `topics`, `evidences`, `sessions`, `lessons`, `weak_points`, `projects`, and `next_focus`.

Topics contain `topic_id`, `name`, `mastery`, `retention`, `status`, `last_practice`, and `evidence_ids`. Status is `not_started` for 0, `in_progress` for 20–60, and `mastered` for 80–100.

Evidences contain `evidence_id`, `topic_id`, `session_id`, `kind`, `autonomous`, `transfer`, `context`, `recorded_at`, `reference`, `result`, and `error`. `reference.type` cannot be `media`.

`media-index.json` contains artifact metadata: IDs, type, provider, source IDs, pedagogical objective, local path or URL, status, dates, verification, accessibility, and `evidence_eligible: false`.

## Video Tracking & Checkpoints

Lessons and topics may optionally include `video_metadata` to track synchronization with video classes (e.g. YouTube):

```json
"video_metadata": {
  "video_id": "PLHz_AreHm4dn_RXXoa3Ameh77f95Hgwv3",
  "video_url": "https://www.youtube.com/watch?v=example",
  "title": "Python POO - Aula 01: O que é Objeto?",
  "duration": "28:45",
  "channel": "Curso em Vídeo",
  "transcript_path": "transcripts/PLHz_AreHm4dn_aula01.md",
  "checkpoint": {
    "paused_at": "18:20",
    "paused_at_seconds": 1100,
    "status": "in_progress",
    "concepts_covered": ["O que é Classe", "Atributos e Estados", "Instanciação"],
    "concepts_pending": ["Métodos Especiais", "Desafio 01 do Vídeo"]
  }
}
```

Validation invariant: If a `checkpoint` indicates `paused_at`, the lesson cannot be marked as `completed` while there are `concepts_pending` without autonomous evidence recorded in the mastery matrix.

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
