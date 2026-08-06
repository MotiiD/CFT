import os
import getpass

info = {
    "user": getpass.getuser(),
    "uid": getattr(os, "getuid", lambda: None)(),
    "gid": getattr(os, "getgid", lambda: None)(),
    "pid": os.getpid(),
    "ppid": os.getppid(),
}

print(info)