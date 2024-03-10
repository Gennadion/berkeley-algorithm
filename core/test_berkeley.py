import unittest
from unittest.mock import patch, MagicMock
from runner import main, elect_new_master, MASTER_TIMEOUT
from nodes import Master, Slave
import time


class TestMasterElection(unittest.TestCase):
    def test_master_election(self):
        # Create a mock master and slave nodes
        master = Master()
        master.start()
        slaves = [Slave(("localhost", 8000)) for _ in range(5)]

        # Mocking methods for the slave nodes
        for slave in slaves:
            slave.get_role = MagicMock(return_value="slave")

        # Set up a scenario where the original master times out
        with patch('runner.time') as mock_time:
            mock_time.time.side_effect = [0, MASTER_TIMEOUT + 1]

            # Perform master election
            new_master = elect_new_master(slaves)

            # Assert that a new master is elected
            self.assertIsNotNone(new_master)
            self.assertEqual(new_master.get_role(), "slave")

    def test_main_functionality(self):
        # This test checks the main functionality of the runner script
        # It doesn't test the master election explicitly but indirectly tests it

        # Mocking time.time to control the timing
        with patch('runner.time') as mock_time:
            mock_time.side_effect = [0, 1, MASTER_TIMEOUT + 1, 10]  # Master timeout scenario

            # Mocking input/output of the main function
            with patch('builtins.print') as mock_print:
                with patch('runner.Master') as mock_master:
                    with patch('runner.Slave') as mock_slave:
                        # Mock master and slave instances
                        mock_master_instance = MagicMock()
                        mock_master_instance.get_role.return_value = "master"
                        mock_master.return_value = mock_master_instance
                        mock_slave_instance = MagicMock()
                        mock_slave.return_value = mock_slave_instance

                        # Call the main function
                        main()

                        # Assert that the new master election happened
                        self.assertTrue(mock_master_instance.update_time.called)
                        self.assertTrue(mock_master_instance.get_offsets.called)
                        self.assertTrue(mock_master_instance.send_offset.called)
                        self.assertTrue(mock_slave_instance.receive_offset.called)
                        self.assertTrue(mock_slave_instance.update_time.called)
