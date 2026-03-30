import requests
import time
BASE_URL = "http://localhost:3080/v2"

# ========================
# BASIC REQUEST
# ========================
def get(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("ERROR:", r.status_code, r.text)
        exit()
    return r.json()

def post(url, data=None):
    r = requests.post(url, json=data)
    if r.status_code not in [200, 201]:
        print("ERROR:", r.status_code, r.text)
        exit()
    return r.json()

def delete(url):
    requests.delete(url)

# ========================
# PROJECT
# ========================
def get_all_projects():
    return get(f"{BASE_URL}/projects")

def find_project(name):
    for p in get_all_projects():
        if p["name"] == name:
            return p["project_id"]
    return None

def create_project(name):
    return post(f"{BASE_URL}/projects", {"name": name})["project_id"]

# ========================
# RESET PROJECT
# ========================
def reset_project(project_id):
    print("Resetting project...")

    requests.post(f"{BASE_URL}/projects/{project_id}/open")
    try:
        nodes = requests.get(f"{BASE_URL}/projects/{project_id}/nodes").json()
    except Exception:
        nodes = []

    # stop node trước
    for n in nodes:
        requests.post(f"{BASE_URL}/projects/{project_id}/nodes/stop")

    time.sleep(1)
    # xóa node
    for n in nodes:
        res = requests.delete(f"{BASE_URL}/projects/{project_id}/nodes/{n['node_id']}")
    
    requests.post(f"{BASE_URL}/v2/projects/{project_id}/nodes/clean")

    print("Project cleared.")

# ========================
# GET OR CREATE PROJECT
# ========================
def open_project(project_id):
    requests.post(f"{BASE_URL}/projects/{project_id}/open")
    
def get_or_create_project(name):
    pid = find_project(name)

    if pid:
        print(f"Project '{name}' exists → reset")
        reset_project(pid)
        return pid
    else:
        print(f"Creating project '{name}'")
        return create_project(name)

# ========================
# NODE
# ========================
def create_vpcs(project_id, name, x, y):
    return post(f"{BASE_URL}/projects/{project_id}/nodes", {
        "name": name,
        "node_type": "vpcs",
        "compute_id": "local",
        "x": x,
        "y": y
    })["node_id"]

def create_switch(project_id, name, x, y):
    return post(f"{BASE_URL}/projects/{project_id}/nodes", {
        "name": name,
        "node_type": "iou",
        "compute_id": "vm",
        "symbol": ":/symbols/ethernet_switch.svg",
        "x": x,
        "y": y,
        "properties": {
            "path": "i86bi-linux-l3-tpgen-adventerprisek9-12.4.bin",
            "ram": 512,
            "nvram": 128,
            "ethernet_adapters": 2
        },
        "template_id": "d26ce2e9-3fd3-4ae1-8ad9-a2b06fe2384f",
    })["node_id"]

def create_router(project_id, name, x, y):
    return post(f"{BASE_URL}/projects/{project_id}/nodes", {
        "name": name,
        "node_type": "dynamips",   
        "compute_id": "local",
        "x": x,
        "y": y,
        "properties": {
            "platform": "c7200",
            "image": "c7200-adventerprisek9-mz.153-3.XB12.image",
            "ram": 512,
            "slot0": "C7200-IO-2FE",
            "slot1": "PA-2FE-TX"
        },
        "symbol": ":/symbols/router.svg"
    })["node_id"]

# ========================
# LINK
# ========================
def connect(project_id, n1, a1, p1, n2, a2, p2):
    post(f"{BASE_URL}/projects/{project_id}/links", {
        "nodes": [
            {
                "node_id": n1,
                "adapter_number": a1,
                "port_number": p1
            },
            {
                "node_id": n2,
                "adapter_number": a2,
                "port_number": p2
            }
        ]
    })

# ========================
# START
# ========================
def start_node(project_id, node_id):
    requests.post(f"{BASE_URL}/projects/{project_id}/nodes/{node_id}/start")