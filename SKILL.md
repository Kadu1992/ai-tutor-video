---
name: ai-tutor
description: Use when the user wants a persistent, evidence-based learning program with curriculum, sessions, practice, review, and durable progress tracking; do not use for a one-off explanation that does not need saved state.
---

# AI Tutor

Build durable understanding through autonomous evidence, not content consumption.

## Boundary

A one-off educational question is answered directly without creating files. For a persistent program, establish two roots before any write:

- `skill_root`: this installed skill; read-only source of references, assets, and scripts.
- `study_root`: an explicit user-selected directory that stores one study program.

Read `references/architecture.md` before setup or migration. Before changing progress, sessions, lessons, cards, or media, read both `references/state-contract.md` and `references/learning-contract.md`.

## Routing

Load only the workflow needed for the current intent.

| Intent or conversational shortcut | Read |
| --- | --- |
| Start a persistent program, `/setup` | `references/workflows/setup.md` |
| Continue, resume, or conduct a session | `references/workflows/session.md` |
| Create or revise the roadmap, `/curriculum` | `references/workflows/curriculum.md` |
| Create the next eligible lesson, `/licao` | `references/workflows/lesson.md` |
| Review weak points or due practice, `/review` | `references/workflows/review.md` |
| Verify an explanation, `/feynman` | `references/workflows/feynman.md` |
| Create or review cards, `/flashcards` | `references/workflows/flashcards.md` |
| Inspect measured progress, `/progress` | `references/workflows/progress.md` |
| Find and register trustworthy sources, `/sources` | `references/workflows/sources.md` |
| Create cards, images, diagrams, charts, audio, video, or NotebookLM material, `/media` or `/notebooklm` | `references/workflows/media.md` |

For programming, also read `references/programming.md`. For output formats, read `references/output-contract.md`. For Google media generation, read `references/media-providers.md`.

## Non-negotiable invariants

- Ask for an autonomous attempt before revealing a solution.
- Never count tutor-provided content or generated media as evidence.
- Ask one learning question at a time, but allow setup answers in one batch.
- Use the normative mastery matrix; workflows cannot create their own thresholds.
- Resume active or resumable interrupted work before advancing.
- Validate structured state after every state-changing turn.
- Close or interrupt every session explicitly and preserve its checkpoint.
- Obtain specific consent immediately before uploading study content externally.
