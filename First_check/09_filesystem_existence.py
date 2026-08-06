import socket

results = {}

try:
    socket.gethostbyname("example.com")
    results["dns"] = True
except Exception:
    results["dns"] = False

try:
    socket.socket()
    results["socket"] = True
except Exception:
    results["socket"] = False

print(results)