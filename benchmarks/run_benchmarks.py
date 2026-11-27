#!/usr/bin/env python3
"""run_benchmarks.py — time the validators on both example specs.

Writes benchmarks/results.json with per-example timings and verdicts.
Standard library only.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXAMPLES = ["spec_5inch_freestyle.json", "spec_hexacopter_inspection.json"]


def main():
    results = {"addon": "ai-fpv-drone-pcbs-design-skill-addon",
               "version": "0.0.1", "examples": {}}
    for name in EXAMPLES:
        spec = ROOT / "examples" / name
        start = time.perf_counter()
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_all.py"),
             "--spec", str(spec), "--base-skill",
             str(ROOT.parent / "ai-pcb-design-skill")],
            capture_output=True, text=True)
        elapsed = round(time.perf_counter() - start, 3)
        results["examples"][name] = {
            "exit_code": r.returncode,
            "verdict": "PASS" if r.returncode == 0 else "FAIL",
            "seconds": elapsed,
        }
        print(f"{name}: {results['examples'][name]['verdict']} "
              f"in {elapsed} s (exit {r.returncode})")
    out = HERE / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0 if all(v["verdict"] == "PASS"
                    for v in results["examples"].values()) else 1


if __name__ == "__main__":
    sys.exit(main())
