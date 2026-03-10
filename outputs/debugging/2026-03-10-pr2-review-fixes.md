# PR #2 Review Fixes

- Timestamp: 2026-03-10
- Branch: `codex/examples-finetune-cleanup`
- Scope: Address PR review findings on `randyy179/Kronos#2`

## Commands

```bash
rg -n "load_data_file|/api/load-data|/api/predict|file_path|load_data_files|result_name|run-name|batch_size|to_dict\\(|Config\\(overrides=config\\)" webui/app.py finetune/config.py finetune/qlib_test.py finetune/train_predictor.py finetune/train_tokenizer.py examples/prediction_batch_example.py examples/prediction_cn_markets_day.py
/bin/zsh -lc 'PYTHONPATH=. uv run pytest tests/test_review_fixes.py tests/test_kronos_regression.py'
```

## Parameters And Inputs

- Web UI data files constrained to repository-local `data/` and `examples/data/`
- Config overrides checked against `finetune/config.py`
- Example CLI validation checked for `symbol`, `--batch-size`, `--plot-series`, and `--run-name`

## Changes

- Replaced absolute-path exposure in `webui/app.py` API responses with repo-relative file references and added server-side allowlist validation for file reads.
- Fixed `Config.to_dict()` / `Config(overrides=...)` round-trip behavior by excluding derived fields and restoring auto-derived `n_train_iter` / `n_val_iter`.
- Added input validation for `finetune/qlib_test.py` run names and safe artifact naming in `examples/prediction_cn_markets_day.py`.
- Added bounds checks for sequential batch windows in `examples/prediction_batch_example.py`.
- Added regression coverage in `tests/test_review_fixes.py`.

## Verification

- `tests/test_review_fixes.py`: 5 passed
- `tests/test_kronos_regression.py`: 4 passed
- Total: 9 passed in 14.36s

## Failures Encountered

- Initial sandboxed `uv run pytest ...` failed because `uv` could not read its local cache due to a permission issue.
- Re-ran the same test command with the required local permissions and it completed successfully.

## Conclusion

The actionable review findings were addressed in code and covered with targeted regression tests. The remaining non-blocking bot suggestions were either subsumed by these fixes or left as optional performance/style follow-ups.
