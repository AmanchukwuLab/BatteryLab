import socket

# Establish a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.107", 29999))

def send(cmd: str):
    s.send((cmd + "\n").encode())

def recv():
    return s.recv(1024).decode()

# Socket is already connected to port 29999
for cmd in ["EnableRobot()", "EnableRobot(0.1)", "EnableRobot(0.5)"]:
    send(cmd)
    resp = recv().strip()
    print(f"{cmd} → {resp}")
    if resp.startswith("0"):
        print("Robot enabled successfully")
        break
else:
    # If all attempts fail, try troubleshooting
    send("GetErrorID()")
    err = recv().strip()
    print("GetErrorID →", err)

    send("ResetRobot()")
    _ = recv()
    print("Robot state has been reset; you can try enabling it again")
