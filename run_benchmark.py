# ============================================================
# C8 COHERENCE BENCHMARK — RUNNER
# Executes full benchmark and exports verifiable artefact
# ============================================================

import json
from datetime import datetime
from c8_core import run_core

def main():
    result = run_core()

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    output_file = f"benchmark_output_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("C8 Coherence Benchmark executed successfully.")
    print(f"Output saved to: {output_file}")
    print(f"SHA256: {result.get('sha256', 'N/A')}")

if __name__ == "__main__":
    main()