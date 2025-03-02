import unittest
from unittest.mock import MagicMock, patch
from langchain_integration.agent_monitor_adapter import AgentMonitorCallback

class TestAgentMonitor(unittest.TestCase):
    def setUp(self):
        self.update_callback = MagicMock()
        self.monitor = AgentMonitorCallback(
            agent_id="test_agent",
            agent_name="Test Agent",
            agent_role="Tester",
            update_callback=self.update_callback
        )
    
    def test_on_llm_start(self):
        self.monitor.on_llm_start({}, ["test prompt"])
        self.assertEqual(self.monitor.status, "Procesando consulta...")
        self.update_callback.assert_called_once()
    
    def test_update_progress(self):
        self.monitor.update_progress(50)
        self.assertEqual(self.monitor.progress, 50)
        self.update_callback.assert_called_once()
        
        # Test boundary values
        self.monitor.update_progress(-10)
        self.assertEqual(self.monitor.progress, 0)
        
        self.monitor.update_progress(150)
        self.assertEqual(self.monitor.progress, 100)

if __name__ == '__main__':
    unittest.main()