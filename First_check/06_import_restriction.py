from pathlib import Path

paths = [
    ".",
    "/",
    "/tmp",
]

results = {}

for p in paths:
    try:
        results[p] = {
            "exists": Path(p).exists(),
            "dir": Path(p).is_dir(),
        }
    except Exception as e:
        results[p] = str(e)

print(results)