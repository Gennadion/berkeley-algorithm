import threading

from core.nodes import Master, Slave


class NodeManager:
    def __init__(self):
        self.nodes = []
        self.node_threads = []

    def add_node(self, node):
        self.nodes.append(node)
        thread = threading.Thread(target=node.start)
        self.node_threads.append(thread)
        thread.start()

    def remove_node(self, node):
        node.socket.close()
        self.nodes.remove(node)

    def add_slave(self, master_addr):
        slave = Slave(master_addr)
        self.add_node(slave)
        print(f"Slave started at port {slave.get_port()}.")

    def remove_slave(self, port):
        for node in self.nodes:
            if node.get_port() == port and node.get_role() == "slave":
                self.remove_node(node)
                print(f"Slave at port {port} removed.")
                return
        print(f"No slave found at port {port}.")