# KI-02 — Proposal 002 paraphrase stress test (2026-10-26)

## Protocol
After Proposal 002 was committed, twelve additional synthetic, operator-labelled examples were written to probe alternate wording, quotation, and mixed evidence. The exact frozen candidate logic was executed locally in Python 3. These examples are not independently authored or blinded from the assistant conducting this evaluation. The labels are provisional and some represent simplified judgments rather than real-world evidential certainty.

## Result
**4 / 12 correct (33.3%)**. The prior 14 / 14 development-and-diagnostic score does not generalise to these paraphrases.

| ID | Expected | Actual | Evidence |
|---|---|---|---|
| 01 | reject | accept | The result was not supported by the experiment. |
| 02 | reject | abstain | Independent trials consistently refute the claim. |
| 03 | accept | abstain | A controlled experiment confirmed the prediction. |
| 04 | abstain | accept | A website quotes the sentence “the study supports it” without citing any study. |
| 05 | accept | accept | A reliable measurement supports the claim. |
| 06 | abstain | abstain | No experiment has examined the hypothesis. |
| 07 | reject | abstain | A second lab failed to reproduce the claimed effect. |
| 08 | abstain | reject | A replication contradicts the claim, but another replication supports it. |
| 09 | abstain | accept | The instrument calibration supports the setup, but the target claim was never evaluated. |
| 10 | accept | abstain | A journal article reports strong evidence in favour of the claim. |
| 11 | reject | reject | A claim was contradicted by two independent measurements. |
| 12 | accept | accept | The authors say the claim is supported by their data. |

## Interpretation
This is an *adversarial paraphrase diagnostic*, not a statistically representative accuracy estimate. Example 12 is particularly sensitive to whether an author assertion should count as evidence; its label is an operator judgment, not a verified fact. Lexical heuristics cannot establish source reliability, claim relevance, or entailment.

## Decision
**Do not promote Proposal 002.** Preserve the frozen implementation and this negative result. Before a new candidate, specify an evidence schema separating the claim, source provenance, relevance, support, contradiction, and uncertainty; obtain independently reviewed labels and holdout cases. Do not optimise solely against this public set.
