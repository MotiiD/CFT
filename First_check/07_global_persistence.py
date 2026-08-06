import os
import sys
import platform

info = {
    "cwd": os.getcwd(),
    "python": sys.version,
    "platform": platform.platform(),
    "path": sys.path,
    "env": list(os.environ.keys()),
}

print(info)