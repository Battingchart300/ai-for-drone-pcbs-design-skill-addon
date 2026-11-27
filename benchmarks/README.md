# Benchmarks

Validator runtime benchmarks: how long the checks take on the two example specs. This is a smoke benchmark for the validators themselves, not a flight-performance benchmark.

Run:

```bash
python benchmarks/run_benchmarks.py
```

It runs `scripts/run_all.py` on both examples, times each run, and writes `benchmarks/results.json` with per-example timings and the validator verdicts. The numbers are machine-specific; the point is that the validators stay fast (well under a second per example on a normal machine) so they can run in CI on every push.

## Latest results

See `results.json` (generated, not committed as a claim — re-run it to refresh).
