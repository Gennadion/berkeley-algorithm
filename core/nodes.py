import datetime
import socket
import time


def get_time():
    return datetime.datetime.now()


class Node:
    def __init__(self, role, port, soc=None, time=datetime.datetime.now()):
        self.role = role
        self.port = port
        self.socket = soc
        self.time = time

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while self.port < 65535:
            try:
                self.socket.bind(("", self.port))
                break
            except Exception as e:
                print(f"{self.role}: Error occurred while binding to port {self.port}")
                print(f"{self.role}: Error: {e}")
                self.port += 1

        print(f"{self.role}: Server is listening at port {self.port}")

    def send_time(self, dest):
        pass

    def receive_time(self):
        pass

    def update_time(self):
        pass

    def get_port(self):
        return self.port

    def get_role(self):
        return self.role

    def set_time(self, time):
        self.time = time


class Master(Node):
    def __init__(self):
        super().__init__("master", 8000)
        self.offsets = []

    def update_time(self):
        self.time = get_time()
        print(f"{self.role}: Time updated to {self.time}")

    def send_offset(self, slaves):
        try:
            offset = self.get_average_offset()
            # Broadcast offset to all slaves
            for port in range(slaves[0].get_port(), slaves[-1].get_port() + 1):
                self.socket.sendto(str(offset).encode(), ("localhost", port))
            self.offsets = []
        except Exception as e:
            print(f"{self.role}: Error occurred while sending time")
            print(f"{self.role}: Error: {e}")

    def receive_time(self):
        try:
            data = self.socket.recvfrom(1024)
            return datetime.datetime.strptime(data[0].decode(), "%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            print(f"{self.role}: Error occurred while receiving time")
            print(f"{self.role}: Error: {e}")

    def get_offsets(self, slaves):
        for _ in slaves:
            slave_time = self.receive_time()
            offset = (get_time().second - slave_time.second) / 2
            self.offsets.append(offset)

    def get_average_offset(self):
        average_offset = sum(self.offsets) / len(self.offsets)
        print(f"\nAverage Offset: {average_offset}\n")
        return average_offset


class Slave(Node):
    def __init__(self, master_addr):
        super().__init__("slave", 8001)
        self.master_addr = master_addr
        self.offset = 0

    def send_time(self, dest=None):
        self.socket.sendto(str(self.time).encode(), self.master_addr)
        print(f"{self.role}: Time sent to {self.master_addr[0]} : {self.master_addr[1]}")

    def receive_offset(self):
        try:
            data = self.socket.recvfrom(1024)
            self.offset = float(data[0].decode())
            print(f"{self.role}: Offset received: {self.offset}")
        except Exception as e:
            print(f"{self.role}: Error occurred while receiving offset")
            print(f"{self.role}: Error: {e}")

    def update_time(self):
        self.time = get_time() + datetime.timedelta(seconds=self.offset)
        print(f"{self.role}: Time updated to {self.time}")


