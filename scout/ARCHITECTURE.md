# KI-01 architecture

`python3 -m scout` calls a small standard-library pipeline. `engine.ingest` validates the dossier and snapshots; `evaluate` matches opportunity rules, audits exact quotes, distinguishes claim kinds, scores, applies abstention gates and performs source-removal challenges; `analyse` ranks and hashes the complete record; `run` freezes JSON, Markdown, inputs and the initial queue. `verify` replays from frozen inputs. `review` records a separate state transition and executes nothing.

The implementation is synchronous and deterministic once inputs and timestamp are fixed. A single run ID binds question, full input, source text/hashes, software hashes, decisions and timestamp. Full source snapshots make quotes inspectable after the original website changes. A missing source remains explicit and can weaken or block a recommendation. JSON is the authoritative structured report; Markdown is rendered from it.

Data flow:

```text
question + attributed snapshots + operator opportunity rules
  -> input validation and source hashes
  -> lexical candidate matching and claim/quote audit
  -> evidence-capped scores and abstention gates
  -> source-removal challenge
  -> ranked JSON + readable report + frozen initial queue
  -> Kai select/reject -> Obe approve/reject (new local files)
  -> STOP: no real-world executor
```

This workflow supports arbitrary questions and user-authored rules, but its reasoning and coverage are bounded by those inputs. No LLM or fictional specialist agents are hiding behind role names. The prototype cannot independently recognise an opportunity, judge truth, establish novelty, conduct live research, estimate actual market size, recruit customers, perform physical science or guarantee a safe action. Scores can be manipulated through weak annotations. Quote matching catches missing citations, not misleading citations. Independence and source quality are declared judgments; copied/related sources may evade deduplication.

Extension points are deliberately ordinary Python functions and versioned JSON:

- An optional read-only collector could write snapshots and provenance into the existing dossier format. It would need explicit network availability, truthful fetch/error logging, access timestamps and source licensing/privacy handling. No such collector exists today.
- A future specialist could propose rules/claims; all suggestions must retain attribution and remain visibly distinct from verified observations. Keep deterministic checks and baseline tests independent of that specialist.
- A semantic reviewer could add contradiction annotations and alternative hypotheses, with saved inputs/outputs and evaluation against labelled cases. It must not silently replace the existing evidence.
- An authenticated approval service could replace local actor strings. Execution must be a separately authorised subsystem with exact action scopes and budgets, never an automatic consequence of ranking or a local queue edit.

The repository integration is additive under `scout/`. Existing website, calculator, Prometheus code/results and research records are untouched. Mission 004 branches and PR #4 remain separate. No runtime dependency, build step, server, workflow, hosting setting or site navigation change was introduced.
