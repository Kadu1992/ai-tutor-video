# Educational Output Contract

Every artifact records `artifact_id`, `lesson_id`, pedagogical objective, topic/source IDs, audience level, format, path or URL, accessibility data, and a retrieval or transfer prompt. Every artifact has `evidence_eligible: false`.

## Format selection

| Learning need | Preferred output | Local canonical form | Fallback |
| --- | --- | --- | --- |
| Recall atomic facts | Cards | JSON + Markdown | Markdown |
| Check discrimination and misconceptions | Quiz | JSON with separate answer key | Markdown |
| Understand relationships | Concept map | Mermaid `.mmd` | Hierarchical Markdown |
| Compare quantitative values | Chart | CSV + chart specification | Markdown table |
| See a concrete system or object | Didactic image | Image + prompt + alt text | Mermaid or ASCII sketch |
| Combine overview and visual hierarchy | Infographic | Brief + image/PDF | Structured Markdown |
| Teach a sequence to an audience | Slides | Outline + PPTX/PDF when available | Markdown outline |
| Review while away from screen | Audio | File/URL + transcript | Script |
| Explain a visual process | Video | File/URL + transcript | Storyboard |

Do not use a decorative image where a chart is needed. Do not create a chart without identifiable data. Separate objective correctness from visual polish.

## Cards and quizzes

Cards contain stable ID, front, back, topic ID, source IDs, difficulty, spaced-repetition step, due date, objective correctness, confidence, and status. Keep one retrievable fact or decision per card.

Quiz answers and explanations remain hidden until the learner attempts the question. Each distractor targets a documented misconception.

## Accessibility and verification

Images, diagrams, charts, infographics, and slides require alt text. Audio and video require a transcript or equivalent notes. Color cannot be the only carrier of meaning.

Before status becomes `ready`, compare claims and labels with source material. After consumption, ask for a new autonomous explanation or application; that response, not the artifact, may become evidence.
