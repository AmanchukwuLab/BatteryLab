import socket

# 建立 socket 连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.107", 29999))

def send(cmd: str):
    s.send((cmd + "\n").encode())

def recv():
    return s.recv(1024).decode()

# 已有 socket 连接到 29999
for cmd in ["EnableRobot()", "EnableRobot(0.1)", "EnableRobot(0.5)"]:
    send(cmd)
    resp = recv().strip()
    print(f"{cmd} → {resp}")
    if resp.startswith("0"):
        print("启能成功")
        break
else:
    # 若都失败，则尝试排查
    send("GetErrorID()"); err = recv().strip()
    print("GetErrorID →", err)
    send("ResetRobot()"); _ = recv()
    print("已重置机器人状态，可再次尝试启能")



