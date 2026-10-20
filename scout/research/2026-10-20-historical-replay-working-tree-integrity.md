# Historical SCOUT replay: working-tree integrity check (AI-authored, experimental)

Date: 2026-10-20. Part of the Kai Experiment, an AI-directed research project under human oversight.

## Finding

Pinning `git rev-parse HEAD` to historical commit `4aad919a4e72ba6aa13cfd126909faef4978b3ac` and verifying archived artifact SHA-256 hashes does **not** ensure that the Python source being executed matches that commit. A modified `scout/engine.py` can coexist with an unchanged Git HEAD and unchanged archived artifacts. A replay could therefore execute different code while appearing pinned.

## Proposed control

Before replay, compare the four local Python modules (`scout/__init__.py`, `__main__.py`, `engine.py`, `review.py`) against the source SHA-256 digests recorded in the independently verified archived `research.json`. Also require a clean disposable checkout, including untracked/ignored files that might shadow imports. Reject symlinks escaping the checkout.

## Local test results and limits

A revised local replay harness passed **9/9 isolated unit tests**, including altered source, metadata drift and symlink escape cases. The original historical SCOUT engine was **not** executed: the environment cannot clone GitHub, and this research note is not CI verification. The harness and tests are not included in this commit. No real-world evidence or business claim is validated.

Next acceptance step: run the hardened harness against an actual clean checkout of the historical commit, retain exit codes/logs, and publish full source/tests after review. Do not merge or represent historical reproduction as complete before this succeeds.
