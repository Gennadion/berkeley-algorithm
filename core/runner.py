import time

from core.manager import NodeManager
from core.nodes import Master, Slave

MASTER_TIMEOUT = 10  # Master timeout in seconds


def elect_new_master(slaves):
    print("Electing a new master...")
    for slave in slaves:
        if slave.get_role() == "slave":
            return slave  # Return the first slave node found
    return None


def main():
    node_manager = NodeManager()

    master = Master()
    node_manager.add_node(master)
    print("Master started.")

    slaves = []
    for i in range(5):  # Create 5 slave nodes
        slave = Slave(("localhost", 8000))  # Pass the master address
        slaves.append(slave)
        node_manager.add_node(slave)
        print(f"Slave {i+1} started.")

    # Synchronize time every 5 seconds
    while True:

        # Add a slave every 20 seconds
        if time.time() % 20 == 0:
            node_manager.add_slave(("localhost", 8000))

        # Remove a slave every 30 seconds
        if time.time() % 30 == 0:
            node_manager.remove_slave(8001)

        for slave in slaves:
            slave.send_time()  # Send slave time to master

        start_time = time.time()

        master.update_time()  # Update master time
        master.get_offsets(slaves)  # Get the offsets from all slaves (round trip time / 2)
        master.send_offset(slaves)    # Send the offset to all slaves

        # Check if master response time exceeds the threshold
        if int(time.time() - start_time) > MASTER_TIMEOUT:
            print("Master response timeout reached.")
            new_master = elect_new_master(slaves)
            if new_master:
                print(f"New master elected: {new_master.get_role()} at port {new_master.get_port()}")
                master = new_master  # Assign the new master node
            else:
                print("No suitable slave found for election. Exiting.")
                break

        for slave in slaves:
            slave.receive_offset()  # Receive offset from master
            slave.update_time()  # Update time based on the offset

        time.sleep(5)  # Wait for 5 seconds before syncing again
        print("\n\n")


if __name__ == "__main__":
    main()