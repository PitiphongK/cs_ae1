import subprocess
import sys
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent

    for n in range(1, 8):
        script = base / f"figure{n}.py"
        if not script.exists():
            print(f"[skip] Missing: {script.name}")
            continue

        print(f"\n=== Running {script.name} ===")
        result = subprocess.run([sys.executable, str(script)], cwd=base)

        if result.returncode != 0:
            print(f"[stop] {script.name} failed with code {result.returncode}")
            break

if __name__ == "__main__":
    main()
