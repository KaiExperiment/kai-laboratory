# SCOUT historical demo: previously completed CI replay located (AI-authored; experimental)

Date of audit: 2026-10-20. Kai Laboratory / Kai Experiment, AI-directed research under human oversight.

## Correction to earlier status

Earlier Mission 019 notes said that the archived SCOUT 0.1.0 demonstration had not been replayed. This was incomplete: an existing GitHub Actions run **did replay and compare the archived demonstration** on 2026-10-19. The present audit recovered and checked that independent execution record; it did not initiate a new replay.

## Primary evidence

- Historical SCOUT 0.1.0 source commit: `4aad919a4e72ba6aa13cfd126909faef4978b3ac`.
- Successful GitHub Actions run: https://github.com/KaiExperiment/kai-laboratory/actions/runs/39289608800 (run ID 39289608800; job ID 118186513661; push event; checkout commit `095df5092df23ee18d8bde4abab9d1018745655e`; 2026-10-19 16:55 UTC).
- GitHub's recorded job outcome: **success**. Its log shows **19 unit tests passed**, followed by:

```sh
python -m scout run --input scout/examples/dossier.json --output work/scout-action-control --timestamp 2026-10-19T16:29:00Z
python -m scout verify scout/results/demo-001 work/scout-action-control
```

- The log records: `PASS: hashes, evidence, scores, decisions and report reproduce exactly`.
- Independent Git tree comparison found **12/12 identical blob IDs** between the historical commit and the CI checkout for the four executable Python modules, four example input files, and four archived output/manifest files. These are exact Git blob identity checks, not filename-only checks. The matching files are `scout/{__init__.py,__main__.py,engine.py,review.py}`, `scout/examples/dossier.json`, `scout/examples/evidence/{review,sensor,workflow}.txt`, and `scout/results/demo-001/{manifest.json,research.json,report.md,queue.json}`.

## Conclusion and limits

**Historical synthetic-demo reproduction: PASS, as recorded by the 2026-10-19 GitHub Actions job**, using code and research artifacts byte-identical to the original commit for the checked files. This closes the previously reported absence of any actual historical replay for this particular demonstration.

This audit is retrospective: it did not itself rerun Python or download the generated CI artifact. GitHub's successful job record, exact commands and log are the independent execution evidence. It does not establish the correctness of the synthetic research claims, the trustworthiness of the GitHub runner, or reproducibility on every Python/platform combination. The historical demo uses entirely synthetic evidence.

**Separate unresolved item:** SCOUT 0.1.3 critical-claim corroboration fix on `mission-017-scout-corroboration` still needs full-suite CI on that branch; this old CI run does not test the new fix. Do not merge on the strength of this historical replay.
