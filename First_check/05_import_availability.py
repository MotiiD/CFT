import importlib

MODULES = [
    "os",
    "sys",
    "json",
    "socket",
]

results = {}

for module in MODULES:
    try:
        importlib.import_module(module)
        results[module] = True
    except Exception:
        results[module] = False

print(results)
