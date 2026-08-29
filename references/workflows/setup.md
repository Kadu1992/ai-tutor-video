# Setup Workflow

Read `references/architecture.md`, `references/state-contract.md`, and `references/learning-contract.md`.

Collect only persisted fields: topic, concrete goal, initial level, weekly hours, preferred times, deadline, language, accessibility needs, source preferences, and explicit study root. Accept one complete answer or ask one missing field at a time.

Summarize the proposed configuration and obtain confirmation before writing. Run `scripts/init_study.py` using the absolute study root and structured JSON. Never overwrite an existing `.ai-tutor/`; use migration when v1 state exists.

After initialization, create an initial curriculum with observable outcomes but do not mark evidence or mastery. Validate the study and show created paths.
