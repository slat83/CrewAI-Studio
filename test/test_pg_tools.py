import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Mock modules that would be imported by pg_tools
sys.modules['utils'] = MagicMock()
sys.modules['utils'].rnd_id = MagicMock(return_value='test_id')
sys.modules['my_tools'] = MagicMock()
sys.modules['my_tools'].TOOL_CLASSES = {'MockTool': MagicMock()}
sys.modules['db_utils'] = MagicMock()
sys.modules['streamlit'] = MagicMock()
sys.modules['streamlit'].session_state = MagicMock()

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

# Now import the module directly
from pg_tools import PageTools

class TestPageTools(unittest.TestCase):
    @patch('pg_tools.st')
    @patch('pg_tools.db_utils')
    @patch('pg_tools.ss')
    @patch('pg_tools.rnd_id', return_value='mock_id')
    def setUp(self, mock_rnd_id, mock_ss, mock_db_utils, mock_st):
        self.mock_st = mock_st
        self.mock_db_utils = mock_db_utils
        self.mock_ss = mock_ss
        self.mock_rnd_id = mock_rnd_id

        # Create a mock tool class and instance
        self.mock_tool_class = MagicMock()
        self.mock_tool_instance = MagicMock()
        self.mock_tool_class.return_value = self.mock_tool_instance
        self.mock_tool_instance.tool_id = 'mock_id'
        self.mock_tool_instance.name = 'MockTool'
        self.mock_tool_instance.description = 'Mock tool description'
        self.mock_tool_instance.get_parameter_names.return_value = ['param1', 'param2']
        self.mock_tool_instance.parameters = {'param1': 'value1', 'param2': 'value2'}
        self.mock_tool_instance.is_valid.return_value = True
        self.mock_tool_instance.is_parameter_mandatory.return_value = True

        # Create PageTools instance with mock tool classes
        self.page_tools = PageTools()
        self.page_tools.available_tools = {'MockTool': self.mock_tool_class}
        
        # Set up mock session state
        self.mock_ss.tools = []

    def test_init(self):
        """Test initialization of PageTools class"""
        self.assertEqual(self.page_tools.name, "Tools")
        self.assertIsNotNone(self.page_tools.available_tools)

    @patch('pg_tools.ss')
    @patch('pg_tools.db_utils')
    @patch('pg_tools.rnd_id', return_value='new_id')
    def test_create_tool(self, mock_rnd_id, mock_db_utils, mock_ss):
        """Test creating a new tool"""
        mock_tool_class = MagicMock()
        mock_tool_instance = MagicMock()
        mock_tool_class.return_value = mock_tool_instance
        
        page_tools = PageTools()
        page_tools.available_tools = {'TestTool': mock_tool_class}
        
        # Test with empty session state
        mock_ss.get = MagicMock(return_value=None)
        mock_ss.tools = []
        
        page_tools.create_tool('TestTool')
        
        # Verify the tool was created with the right ID
        mock_tool_class.assert_called_once_with('new_id')
        # Verify the tool was added to session state
        self.assertEqual(mock_ss.tools, [mock_tool_instance])
        # Verify the tool was saved to the database
        mock_db_utils.save_tool.assert_called_once_with(mock_tool_instance)

    def test_remove_tool(self):
        """Test removing a tool"""
        # Add a mock tool to the session state
        mock_tool = MagicMock()
        mock_tool.tool_id = 'tool_to_remove'
        self.mock_ss.tools = [mock_tool]
        
        self.page_tools.remove_tool('tool_to_remove')
        
        # Verify the tool was removed from session state
        self.assertEqual(self.mock_ss.tools, [])
        # Verify the tool was deleted from the database
        self.mock_db_utils.delete_tool.assert_called_once_with('tool_to_remove')
        # Verify streamlit rerun was called
        self.mock_st.rerun.assert_called_once()

    def test_set_tool_parameter(self):
        """Test setting a tool parameter"""
        # Add a mock tool to the session state
        mock_tool = MagicMock()
        mock_tool.tool_id = 'test_tool'
        self.mock_ss.tools = [mock_tool]
        
        self.page_tools.set_tool_parameter('test_tool', 'test_param', 'test_value')
        
        # Verify the tool parameter was set
        mock_tool.set_parameters.assert_called_once_with(test_param='test_value')
        # Verify the tool was saved to database
        self.mock_db_utils.save_tool.assert_called_once_with(mock_tool)
        
        # Test with empty string value (should convert to None)
        mock_tool.set_parameters.reset_mock()
        self.mock_db_utils.save_tool.reset_mock()
        
        self.page_tools.set_tool_parameter('test_tool', 'empty_param', '')
        
        mock_tool.set_parameters.assert_called_once_with(empty_param=None)
        self.mock_db_utils.save_tool.assert_called_once_with(mock_tool)

    def test_get_tool_display_name_with_param(self):
        """Test getting a tool display name with a parameter"""
        mock_tool = MagicMock()
        mock_tool.name = 'MockTool'
        mock_tool.tool_id = 'mock_id'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': 'value1'}
        
        result = self.page_tools.get_tool_display_name(mock_tool)
        
        # Verify the correct display name was returned
        self.assertEqual(result, 'MockTool (value1)')

    def test_get_tool_display_name_no_param(self):
        """Test getting a tool display name without parameters"""
        mock_tool = MagicMock()
        mock_tool.name = 'MockTool'
        mock_tool.tool_id = 'mock_id'
        mock_tool.get_parameter_names.return_value = []
        mock_tool.parameters = {}
        
        result = self.page_tools.get_tool_display_name(mock_tool)
        
        # Verify the correct display name was returned
        self.assertEqual(result, 'MockTool (mock_id)')
        
    def test_get_tool_display_name_empty_param(self):
        """Test getting a tool display name with an empty parameter value"""
        mock_tool = MagicMock()
        mock_tool.name = 'MockTool'
        mock_tool.tool_id = 'mock_id'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': ''}
        
        result = self.page_tools.get_tool_display_name(mock_tool)
        
        # Verify the correct display name was returned
        self.assertEqual(result, 'MockTool (mock_id)')

    @patch('pg_tools.st')
    def test_draw_tools_available(self, mock_st):
        """Test drawing available tools"""
        # Setup mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]
        
        # Setup mock button
        mock_col1.__enter__ = MagicMock()
        mock_col1.__exit__ = MagicMock()
        mock_col1.button.return_value = True
        
        # Mock the create_tool method
        self.page_tools.create_tool = MagicMock()
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify columns were created
        mock_st.columns.assert_called_once_with([1, 3])
        
        # Verify create_tool was called when button was clicked
        self.page_tools.create_tool.assert_called_once_with('MockTool')
    
    @patch('pg_tools.st')
    def test_draw_tools_enabled(self, mock_st):
        """Test drawing enabled tools"""
        # Setup mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]
        
        # Setup return values for context managers
        mock_col1.__enter__ = MagicMock()
        mock_col1.__exit__ = MagicMock()
        mock_col2.__enter__ = MagicMock()
        mock_col2.__exit__ = MagicMock()
        
        # Add a mock tool to session state
        mock_tool = MagicMock()
        mock_tool.tool_id = 'enabled_tool'
        mock_tool.name = 'EnabledTool'
        mock_tool.description = 'Enabled tool description'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': 'value1'}
        mock_tool.is_valid.return_value = True
        mock_tool.is_parameter_mandatory.return_value = False
        
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock()
        
        # Mock the set_tool_parameter and remove_tool methods
        self.page_tools.set_tool_parameter = MagicMock()
        self.page_tools.remove_tool = MagicMock()
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify write was called for the enabled tools section
        mock_col2.write.assert_called_with("##### Enabled Tools")
        
        # Verify expander was created with the right title
        mock_col2.expander.assert_called_once()
        
        # Verify description was written
        mock_expander.write.assert_called_once_with('Enabled tool description')
    
    @patch('pg_tools.st')
    def test_draw_tools_invalid_tool(self, mock_st):
        """Test drawing an invalid tool (missing required parameters)"""
        # Setup mock columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]
        
        # Setup return values for context managers
        mock_col1.__enter__ = MagicMock()
        mock_col1.__exit__ = MagicMock()
        mock_col2.__enter__ = MagicMock()
        mock_col2.__exit__ = MagicMock()
        
        # Add an invalid mock tool to session state
        mock_tool = MagicMock()
        mock_tool.tool_id = 'invalid_tool'
        mock_tool.name = 'InvalidTool'
        mock_tool.description = 'Invalid tool description'
        mock_tool.get_parameter_names.return_value = ['required_param']
        mock_tool.parameters = {'required_param': ''}
        mock_tool.is_valid.return_value = False
        mock_tool.is_parameter_mandatory.return_value = True
        
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock()
        
        # Get the display name for the invalid tool
        display_name = self.page_tools.get_tool_display_name(mock_tool)
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify expander was created with warning indicator
        mock_col2.expander.assert_called_once_with(f"❗ {display_name}")

    @patch('pg_tools.st')
    def test_draw(self, mock_st):
        """Test the draw method"""
        # Mock the draw_tools method
        self.page_tools.draw_tools = MagicMock()
        
        # Call draw
        self.page_tools.draw()
        
        # Verify subheader was set
        mock_st.subheader.assert_called_once_with("Tools")
        
        # Verify draw_tools was called
        self.page_tools.draw_tools.assert_called_once()

if __name__ == '__main__':
    unittest.main()