# Medium execution and recovery

Use the shared workspace `.venv/bin/python` directly. No packages are installed by these scripts. Check existing processes before executing; never launch a duplicate worker.

- `benchmark.py`: original gated runner adapted only for three Medium models and owning-repository archival paths. Frozen evaluator, preprocessing and timing semantics are preserved.
- `audit_resume_state.py <run_id>`: inspect atomic saved records, contiguous IDs, RLE readability and frozen config/checkpoint identity without model inference.
- `resume_medium.py <run_id>`: singleton durable supervisor. It retains active original workers, detects completed records, resumes only missing frames if necessary, reuses aggregates and accepted timing rounds, and validates canonical outputs. Launch with detached session and logs redirected to this experiment. Progress is persisted in manifests/<run_id>_RESUME_PROGRESS.json. Valid saved predictions are never overwritten.
- `build_medium_results.py <run_id>`: validate completed scientific artifacts and normalize canonical CSVs without running inference or recalculating accuracy metrics.
- `report_medium.py <run_id>`: render the common templates and plots from canonical CSVs; validate numbers/headings/links. Presentation summary stays neutral.

Recovery drivers/reporting sources are post-freeze additions recorded separately. They do not modify the archived runtime sources. Source hashes, reused versus new work and session-interruption details are in RESUME_PROVENANCE.json and final_integrity.json. A future restart requires the same frozen run config/protocol and checkpoint hashes. Stop on a gap/corrupt nonterminal record; only an incomplete terminal record can be quarantined with preserved evidence. Do not launch another tier from these scripts.
