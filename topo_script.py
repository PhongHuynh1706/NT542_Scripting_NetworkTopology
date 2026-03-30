from gns3_api import *
import time
if __name__ == "__main__":

    project_id = get_or_create_project("Enterprise_Network")
    time.sleep(1)

    # ========================
    # CORE LAYER
    # ========================
    
    r1 = create_router(project_id, "R1", -200, -300)
    r2 = create_router(project_id, "R2", 200, -300)

    # ========================
    # DISTRIBUTION LAYER
    # ========================
    sw1 = create_router(project_id, "R3", -200, -100)
    sw2 = create_router(project_id, "R4", 200, -100)

    # ========================
    # ACCESS LAYER
    # ========================
    sw3 = create_switch(project_id, "SW3", -300, 100)
    sw4 = create_switch(project_id, "SW4", -100, 100)
    sw5 = create_switch(project_id, "SW5", 100, 100)
    sw6 = create_switch(project_id, "SW6", 300, 100)

    # ========================
    # END DEVICES
    # ========================
    pc1 = create_vpcs(project_id, "PC1", -300, 250)
    pc2 = create_vpcs(project_id, "PC2", -100, 250)
    pc3 = create_vpcs(project_id, "PC3", 100, 250)
    pc4 = create_vpcs(project_id, "PC4", 300, 250)


    # ========================
    # CORE <-> CORE
    # ========================
    connect(project_id, r1, 0, 0, r2, 0, 0)  # Fa0/0 ↔ Fa0/0

    # ========================
    # CORE <-> DISTRIBUTION
    # ========================
    connect(project_id, r1, 0, 1, sw1, 0, 0)  # Fa0/1 → DSW1
    connect(project_id, r1, 1, 0, sw2, 0, 0)  # Fa1/0 → DSW2
    connect(project_id, r2, 0, 1, sw1, 0, 1)  # Fa0/1 → DSW1
    connect(project_id, r2, 1, 0, sw2, 0, 1)  # Fa1/0 → DSW2

    # ========================
    # DISTRIBUTION <-> ACCESS
    # ========================
    # SW1
    connect(project_id, sw1, 1, 0, sw3, 0, 0)
    connect(project_id, sw1, 1, 1, sw4, 0, 0)

    # SW2
    connect(project_id, sw2, 1, 0, sw5, 0, 0)
    connect(project_id, sw2, 1, 1, sw6, 0, 0)
    # ========================
    # ACCESS <-> PC
    # ========================
    connect(project_id, sw3, 0, 1, pc1, 0, 0)
    connect(project_id, sw4, 0, 1, pc2, 0, 0)
    connect(project_id, sw5, 0, 1, pc3, 0, 0)
    connect(project_id, sw6, 0, 1, pc4, 0, 0)
    # ========================
    # START DEVICES
    # ========================
    for router in [r1, r2]:
        start_node(project_id, router)

    for sw in [sw1, sw2, sw3, sw4, sw5, sw6]:
        start_node(project_id, sw)

    for pc in [pc1, pc2, pc3, pc4]:
        start_node(project_id, pc)

    print("Enterprise 3-layer topology created.")