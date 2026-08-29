# Media Providers: Local, NotebookLM, and Gemini

Always create a local learning pack first. External generation is optional and cannot block study.

## Capability order

1. Produce local sources, prompts, manifests, and fallbacks.
2. Determine whether an authenticated browser and the requested feature are available.
3. List the exact files and request consent immediately before upload.
4. If consented, use the existing authenticated session; never request, store, or type credentials.
5. Record generated URLs/downloads without publishing or changing sharing settings.
6. Verify the artifact against sources and preserve a transcript or accessible alternative.

## Provider split

NotebookLM is the grounded provider for Studio artifacts: cards, quizzes, mind maps, study guides, audio overviews, video overviews, infographics, and slide decks when available to the account.

Notebooks in Gemini may be used to chat with the synchronized notebook and use broader Gemini tools. Gemini chat can include web/tool context; it is not equivalent to NotebookLM's source-only grounding. Studio artifacts such as audio, video, infographics, and slide decks must be requested in NotebookLM.

Feature availability, quotas, language support, and account rules may change. Detect them at use time and fall back instead of claiming generation succeeded.

## Privacy gate

Do not upload credentials, personal identifiers, restricted coursework, proprietary material, or copyrighted content without clear rights and specific consent. Generating an artifact does not authorize public sharing. Sharing is a separate external action.

## Learning pack

`scripts/create_learning_pack.py` creates:

```text
media/<lesson-id>/notebooklm/
├── source-pack.md
├── prompts.md
├── manifest.json
└── exports/
```

The manifest begins with consent false. The manual fallback supplies the same source pack and prompts when browser automation is unavailable.

Official capability references:

- https://support.google.com/notebooklm/answer/16164461
- https://support.google.com/notebooklm/answer/16215270
- https://support.google.com/notebooklm/answer/17003757
- https://support.google.com/notebooklm/answer/16212820
- https://support.google.com/notebooklm/answer/16454555
