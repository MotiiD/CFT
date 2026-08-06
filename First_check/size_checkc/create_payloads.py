#!/usr/bin/env python3

from pathlib import Path


OUTPUT_DIR = Path("payload_sizes")

sizes = [
    ("100KB", 100 * 1024),
    ("500KB", 500 * 1024),
    ("1MB", 1024 * 1024),
    ("5MB", 5 * 1024 * 1024),
    ("10MB", 10 * 1024 * 1024),
]


OUTPUT_DIR.mkdir(exist_ok=True)


for name, size in sizes:

    filename = OUTPUT_DIR / f"payload_{name}.py"

    # Base valid Python code
    header = """\
# Payload size test
# Generated automatically

TEST_NAME = "payload_size_test"

pass

"""

    # Fill remaining space with comments
    padding_size = size - len(header.encode("utf-8"))

    if padding_size < 0:
        padding_size = 0

    padding = "#" * padding_size


    content = header + padding


    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


    actual_size = filename.stat().st_size


    print(
        f"{filename}: {actual_size / 1024:.2f} KB"
    )


print("\nDone")