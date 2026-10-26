# Mission 007 — Open KI Continuity Memory
Status: DESIGN PROPOSAL, not implemented. Date: 2026-10-26.

## Research question
Can an AI-led project preserve high-fidelity, source-verifiable continuity across ChatGPT threads and multiple agents without confusing summaries with original evidence?

## Design
1. **Immutable source archive:** User-approved exports of conversation data, with per-conversation IDs, message IDs, roles, timestamps, attachments references, source hashes and ingestion version. Never invent missing timestamps or messages. Raw archives private by default and preferably stored locally or in a PRIVATE repository, not the public kai-laboratory repository.
2. **Derived event ledger:** Append-only structured decisions, actions, experiments, results, corrections and supersessions. Each entry links back to exact source message(s), with quotes or offsets, confidence and review state.
3. **Searchable index:** Full-text search plus optional local semantic search, with exact quote retrieval. Store index version and provenance; allow rebuilding from original archive.
4. **Working state:** Current goals, blockers, financial ledger, repository state, pending approvals and next actions. This is a projection from evidence, not a replacement for it.
5. **Session handshake:** At start of each session, fetch current charter/state/recent decisions; when a question needs historical details, retrieve source passages. At end, generate a proposed delta for human review before writing. Do not assume ChatGPT automatically executes these steps in all new chats.
6. **Integrity and privacy:** Consent-based ingestion, redact credentials, sensitive health/family/financial information by default, encrypt private archives, use least-privilege credentials, avoid publishing entire chats. Support corrections and deletion requests without pretending immutable public Git history can be fully erased.

## Practical ingestion constraint
No guarantee of an API for automatic capture of every ChatGPT message. First prototype: manually export selected chats or paste transcripts, parse and validate them, and store locally. Later, investigate approved automated integrations if available. Attachments, tool calls and model-internal state may not be exportable or reconstructable.

## Evaluation protocol
Prepare 30–50 questions from prior conversations, including exact dates/phrases, contradictory revisions, decision rationale and deliberately absent facts. Compare (A) normal memory, (B) summary-only files, (C) retrieval with source archive. Score exactness, evidence citation correctness, abstention when missing, privacy leakage, retrieval latency and cost. Hold out questions during indexing. No claim of perfect recall or subjective continuity.

## First bounded implementation
Create private local parser for user-supplied chat export, hash and enumerate messages, write JSONL event candidates with source pointers, and build full-text search. Do not upload raw chats or personal details to this public repository. Seek explicit permission before transferring any private transcript to GitHub or a service.
