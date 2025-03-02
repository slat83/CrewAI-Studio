import unittest
from unittest.mock import patch, MagicMock, call, ANY
import sys
import os

# Mock modules that would be imported by pg_tools
sys.modules['utils'] = MagicMock()
sys.modules['utils'].rnd_id = MagicMock(return_value='test_id')
sys.modules['my_tools'] = MagicMock()
sys.modules['my_tools'].TOOL_CLASSES = {
    'ScrapeWebsiteTool': MagicMock(),
    'FileReadTool': MagicMock(),
}
sys.modules['db_utils'] = MagicMock()
sys.modules['streamlit'] = MagicMock()
sys.modules['streamlit'].session_state = MagicMock()

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the modules directly
from pg_tools import PageTools
from my_tools import MyTool

# Replace imported TOOL_CLASSES with our mock version
TOOL_CLASSES = {
    'ScrapeWebsiteTool': MagicMock(),
    'FileReadTool': MagicMock(),
    'MockTool1': MagicMock(),
    'MockTool2': MagicMock()
}

class TestPageToolsIntegration(unittest.TestCase):
    def setUp(self):
        # Create real instances with mocked dependencies
        self.patcher1 = patch('pg_tools.st')
        self.patcher2 = patch('pg_tools.db_utils')
        self.patcher3 = patch('pg_tools.ss')
        self.patcher4 = patch('pg_tools.rnd_id', return_value='test_id')
        
        self.mock_st = self.patcher1.start()
        self.mock_db_utils = self.patcher2.start()
        self.mock_ss = self.patcher3.start()
        self.mock_rnd_id = self.patcher4.start()
        
        # Create a real PageTools instance
        self.page_tools = PageTools()
        
    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
        self.patcher4.stop()
        
    def test_tool_lifecycle(self):
        """Test the full lifecycle of a tool (create, update, remove)"""
        # Mock the tools in session state
        self.mock_ss.tools = []
        
        # Setup TOOL_CLASSES with our mock
        mock_tool_class = MagicMock()
        mock_tool_instance = MagicMock()
        mock_tool_class.return_value = mock_tool_instance
        mock_tool_instance.tool_id = 'test_id'
        mock_tool_instance.name = 'ScrapeWebsiteTool'
        mock_tool_instance.parameters = {}
        
        self.page_tools.available_tools = {'ScrapeWebsiteTool': mock_tool_class}
        
        # Create a real tool instance for testing
        self.page_tools.create_tool('ScrapeWebsiteTool')
        
        # Verify tool was created and added to session state
        self.assertEqual(len(self.mock_ss.tools), 1)
        created_tool = self.mock_ss.tools[0]
        self.assertEqual(created_tool.tool_id, 'test_id')
        self.assertEqual(created_tool.name, 'ScrapeWebsiteTool')
        
        # Verify tool was saved to database
        self.mock_db_utils.save_tool.assert_called_once_with(created_tool)
        self.mock_db_utils.save_tool.reset_mock()
        
        # Update a parameter
        self.page_tools.set_tool_parameter('test_id', 'website_url', 'https://example.com')
        
        # Verify parameter was updated
        self.assertEqual(created_tool.parameters.get('website_url'), 'https://example.com')
        self.mock_db_utils.save_tool.assert_called_once_with(created_tool)
        self.mock_db_utils.save_tool.reset_mock()
        
        # Remove the tool
        self.page_tools.remove_tool('test_id')
        
        # Verify tool was removed from session state
        self.assertEqual(len(self.mock_ss.tools), 0)
        self.mock_db_utils.delete_tool.assert_called_once_with('test_id')
        
    def test_session_state_initialization(self):
        """Test handling when session state isn't initialized"""
        # Simulate session state without 'tools' key
        del self.mock_ss.tools
        
        # Setup TOOL_CLASSES with our mock
        mock_tool_class = MagicMock()
        mock_tool_instance = MagicMock()
        mock_tool_class.return_value = mock_tool_instance
        
        self.page_tools.available_tools = {'FileReadTool': mock_tool_class}
        
        # Create a tool - should initialize session state
        self.page_tools.create_tool('FileReadTool')
        
        # Verify session state was initialized
        self.assertTrue(hasattr(self.mock_ss, 'tools'))
        self.assertEqual(len(self.mock_ss.tools), 1)
        
    def test_draw_tools_with_multiple_tools(self):
        """Test drawing tools UI with multiple tools"""
        # Mock column and expander context managers
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        self.mock_st.columns.return_value = [mock_col1, mock_col2]
        
        mock_col1.__enter__ = MagicMock()
        mock_col1.__exit__ = MagicMock(return_value=False)
        mock_col2.__enter__ = MagicMock()
        mock_col2.__exit__ = MagicMock(return_value=False)
        
        # Set up available tools with mocks
        self.page_tools.available_tools = TOOL_CLASSES
        
        # Create mock buttons for each tool
        button_values = [True] + [False] * (len(TOOL_CLASSES) - 1)  # First button True, others False
        mock_col1.button.side_effect = button_values
        
        # Create mock tools in session state
        mock_tool1 = MagicMock()
        mock_tool1.tool_id = 'tool1'
        mock_tool1.name = 'Tool1'
        mock_tool1.description = 'Tool 1 description'
        mock_tool1.get_parameter_names.return_value = ['param1']
        mock_tool1.parameters = {'param1': 'value1'}
        mock_tool1.is_valid.return_value = True
        
        mock_tool2 = MagicMock()
        mock_tool2.tool_id = 'tool2'
        mock_tool2.name = 'Tool2'
        mock_tool2.description = 'Tool 2 description'
        mock_tool2.get_parameter_names.return_value = ['param1', 'param2']
        mock_tool2.parameters = {'param1': 'value1', 'param2': ''}
        mock_tool2.is_valid.return_value = False
        
        self.mock_ss.tools = [mock_tool1, mock_tool2]
        
        # Mock expanders
        mock_expander1 = MagicMock()
        mock_expander2 = MagicMock()
        mock_col2.expander.side_effect = [mock_expander1, mock_expander2]
        
        mock_expander1.__enter__ = MagicMock()
        mock_expander1.__exit__ = MagicMock(return_value=False)
        mock_expander2.__enter__ = MagicMock()
        mock_expander2.__exit__ = MagicMock(return_value=False)
        
        # Mock input fields
        mock_expander1.text_input.return_value = 'new_value1'
        mock_expander2.text_input.side_effect = ['new_value2', 'new_param2']
        
        # Mock remove buttons
        mock_expander1.button.return_value = False
        mock_expander2.button.return_value = True
        
        # Create a spy on methods we want to verify
        self.page_tools.set_tool_parameter = MagicMock(wraps=self.page_tools.set_tool_parameter)
        self.page_tools.remove_tool = MagicMock(wraps=self.page_tools.remove_tool)
        self.page_tools.create_tool = MagicMock()
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify appropriate UI elements were created
        self.mock_st.columns.assert_called_once_with([1, 3])
        
        # Verify create_tool was called for the first button (True)
        first_tool_name = list(TOOL_CLASSES.keys())[0]
        self.page_tools.create_tool.assert_called_once_with(first_tool_name)
        
        # Verify parameter update logic
        self.page_tools.set_tool_parameter.assert_any_call('tool1', 'param1', 'new_value1')
        self.page_tools.set_tool_parameter.assert_any_call('tool2', 'param1', 'new_value2')
        self.page_tools.set_tool_parameter.assert_any_call('tool2', 'param2', 'new_param2')
        
        # Verify remove button logic
        self.page_tools.remove_tool.assert_called_once_with('tool2')

    def test_edge_cases(self):
        """Test edge cases in the tools page"""
        # Test setting parameter on non-existent tool
        self.mock_ss.tools = []
        self.page_tools.set_tool_parameter('non_existent', 'param', 'value')
        # Should not throw an error
        
        # Test with None values
        mock_tool = MagicMock()
        mock_tool.tool_id = 'test_tool'
        mock_tool.parameters = {}
        mock_tool.get_parameter_names.return_value = ['param1']
        self.mock_ss.tools = [mock_tool]
        
        # Parameter is None
        self.page_tools.set_tool_parameter('test_tool', None, 'value')
        mock_tool.set_parameters.assert_not_called()
        
        # Value is None
        mock_tool.set_parameters.reset_mock()
        self.page_tools.set_tool_parameter('test_tool', 'param1', None)
        mock_tool.set_parameters.assert_called_once_with(param1=None)
        
        # Test display name with None values
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': None}
        display_name = self.page_tools.get_tool_display_name(mock_tool)
        self.assertEqual(display_name, f"{mock_tool.name} ({mock_tool.tool_id})")
        
    def test_tools_database_sync(self):
        """Test that tools are properly synced with database"""
        # Setup tool class and instance
        mock_tool_class = MagicMock()
        mock_tool_instance = MagicMock()
        mock_tool_class.return_value = mock_tool_instance
        mock_tool_instance.tool_id = 'test_id'
        
        self.page_tools.available_tools = {'FileReadTool': mock_tool_class}
        
        # Create a tool
        self.mock_ss.tools = []
        self.page_tools.create_tool('FileReadTool')
        created_tool = self.mock_ss.tools[0]
        
        # Verify saved to database
        self.mock_db_utils.save_tool.assert_called_once_with(created_tool)
        
        # Update parameter
        self.mock_db_utils.save_tool.reset_mock()
        self.page_tools.set_tool_parameter(created_tool.tool_id, 'file_path', '/path/to/file')
        
        # Verify updated in database
        self.mock_db_utils.save_tool.assert_called_once_with(created_tool)
        
        # Remove tool
        self.mock_db_utils.delete_tool.reset_mock()
        self.page_tools.remove_tool(created_tool.tool_id)
        
        # Verify removed from database
        self.mock_db_utils.delete_tool.assert_called_once_with(created_tool.tool_id)

if __name__ == '__main__':
    unittest.main()