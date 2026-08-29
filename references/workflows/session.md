# Session Workflow

Read and validate canonical state before the first learning question.

## Resume

Resume the latest `in_progress` session. If none exists, resume the latest `interrupted` session whose `resumable` field is true by adding the `resumed` transition. Recover its checkpoint, lesson IDs, weak points, and next action. Open a new session only when no resumable work exists.

## Conduct

1. Confirm one prerequisite with one question.
2. Set one observable session objective.
3. Teach one idea from concrete to abstract.
4. Request an autonomous explanation or application.
5. Apply the help ladder without counting guided work as independent evidence.
6. Record evidence, retention, weak points, cards, and next focus under the normative contracts.

## Close

On completion or interruption, append the valid transition, record timestamps, checkpoint, topics, evidence IDs, difficulty, next step, and files changed. Update lesson state independently. Validate canonical state after the atomic update.
