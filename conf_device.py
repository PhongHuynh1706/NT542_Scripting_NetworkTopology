import json
import time
from netmiko import ConnectHandler

# =========================
# LOAD INVENTORY
# =========================
def load_inventory(file="inventory/inventory.json"):
    with open(file) as f:
        return json.load(f)

# =========================
# CONNECT (NO AUTH)
# =========================
def connect_device(device):
    return ConnectHandler(
        device_type=device["device_type"],
        host=device["host"],
        port=device["port"],
        username="",   
        password="",   
        secret="",     
        fast_cli=False
    )

# =========================
# PUSH CONFIG
# =========================
def push_config(device):
    print(f"\n=== Configuring {device['name']} ===")

    try:
        if device.get("type") == "pc":
            tn = telnetlib3.Telnet(device["host"], device["port"])
            tn.write(b"\n")
            tn.write(b"show ip\n")
            output = tn.read_very_eager().decode()
            print(output)
            tn.close()
            return
        
        conn = connect_device(device)

        # vào enable nếu có (nếu không có thì ignore)
        try:
            conn.enable()
        except:
            pass

        output = conn.send_config_set(device["config"])
        print(output)

        # save nếu có hỗ trợ
        try:
            conn.save_config()
        except:
            pass

        conn.disconnect()

    except Exception as e:
        print(f"ERROR {device['name']}: {e}")

# =========================
# VERIFY
# =========================
def verify(device):
    print(f"\n=== Verifying {device['name']} ===")

    try:
        conn = connect_device(device)

        try:
            conn.enable()
        except:
            pass

        print(conn.send_command("show ip interface brief"))
        print(conn.send_command("show ip route"))

        conn.disconnect()

    except Exception as e:
        print(f"VERIFY ERROR {device['name']}: {e}")


import socket
import time

def config_pc(device):
    print(f"\n=== Configuring {device['name']} ===")

    s = socket.socket()
    s.connect((device["host"], device["port"]))

    time.sleep(1)

    # kick start prompt
    s.send(b"\n")
    time.sleep(0.5)

    # lấy config từ inventory
    for cmd in device["config"]:
        print(f"{cmd}")
        s.send((cmd + "\n").encode())
        time.sleep(0.5)

    # verify luôn
    s.send(b"show ip\n")
    time.sleep(1)

    output = s.recv(4096).decode(errors="ignore")
    print(output)

    s.close()
# =========================
# MAIN
# =========================
def main():
    inventory = load_inventory()

    # đợi thiết bị boot xong (rất quan trọng)
    print("Waiting devices to be ready...")
    time.sleep(1)

    # =========================
    # CONFIG
    # =========================
    for dev in inventory["devices"]:
        if dev.get("type") == "pc":
            config_pc(dev)
        else:
            push_config(dev)

    # =========================
    # VERIFY
    # =========================
    # for device in inventory["devices"]:
    #     verify(device)

    print("\nDONE.")

# =========================
if __name__ == "__main__":
    main()