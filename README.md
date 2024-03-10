Certainly! Here's a concise README based on the provided information:

---

# Berkeley Time Synchronization Algorithm

This project implements a time synchronization system consisting of master and slave nodes. It allows for dynamic addition and removal of nodes without interrupting any of the procedures.

## Background

The Berkeley Algorithm is a time synchronization algorithm that was developed by Gustave Berkeley in 1989. It is used to synchronize the time of different nodes in a distributed system. The algorithm works by calculating the time difference between the master node and each slave node, and then adjusting the time of the slave nodes accordingly.

## Features

- **Dynamic Node Management**: The system supports adding and removing nodes dynamically.
- **Master-Slave Architecture**: The system follows a master-slave architecture for time synchronization.
- **Master Node Election**: The system automatically elects a master node from available slave nodes when the current master node goes offline.
- **Time Synchronization**: Slave nodes synchronize their time with the master node periodically.
- **Error Handling**: Error handling mechanisms are in place for network communication and node operations.

## Usage

1. **Installation**: No installation is required. Simply clone the repository to your local machine.

    ```git clone https://github.com/Gennadion/berkeley-algorithm.git```


2. **Running the System**:
   - Execute `runner.py` to start the system.
   
        ```python runner.py```

   - The master node will be started automatically, while slave nodes can be added dynamically during runtime.

3. **Dynamic Node Management**:
   - Current logic adds a Slave Node every 20 seconds and removes a Slave Node every 30 seconds.
   - You can modify the logic in `runner.py` to add or remove nodes at different intervals.
   - You can also add or remove nodes manually using the `add_node` and `remove_node` methods in `runner.py`.

## Contributing

Contributions to the project are welcome! Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---