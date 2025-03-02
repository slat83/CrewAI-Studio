import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import warnings

# Filter warnings for testing
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=ResourceWarning)

# Create mock streamlit and its submodules
mock_streamlit = MagicMock()
mock_emojis = MagicMock()
mock_streamlit.emojis = mock_emojis

# Mock modules that would be imported by pg_tools
sys.modules['streamlit'] = mock_streamlit
sys.modules['streamlit.emojis'] = mock_emojis
sys.modules['utils'] = MagicMock()
sys.modules['utils'].rnd_id = MagicMock(return_value='test_id')
sys.modules['my_tools'] = MagicMock()
sys.modules['my_tools'].TOOL_CLASSES = {'TestTool': MagicMock()}
sys.modules['db_utils'] = MagicMock()

# Add the parent directory to sys.path so we can import the app modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.pg_tools import PageTools

class TestPageToolsUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up any test fixtures that are shared across test methods"""
        # Suppress warnings for the entire test class
        warnings.simplefilter('ignore')
    
    @patch('app.pg_tools.st')
    @patch('app.pg_tools.db_utils')
    @patch('app.pg_tools.ss')
    def setUp(self, mock_ss, mock_db_utils, mock_st):
        self.mock_st = mock_st
        self.mock_db_utils = mock_db_utils
        self.mock_ss = mock_ss
        
        # Create a PageTools instance
        self.page_tools = PageTools()
        
        # Setup mock column context managers
        self.mock_col1 = MagicMock()
        self.mock_col2 = MagicMock()
        self.mock_st.columns.return_value = [self.mock_col1, self.mock_col2]
        
        self.mock_col1.__enter__ = MagicMock()
        self.mock_col1.__exit__ = MagicMock(return_value=False)
        self.mock_col2.__enter__ = MagicMock()
        self.mock_col2.__exit__ = MagicMock(return_value=False)
        
    def test_ui_layout(self):
        """Test the basic UI layout structure"""
        # Call the draw method
        self.page_tools.draw()
        
        # Verify subheader was set with correct name
        self.mock_st.subheader.assert_called_once_with("Tools")
        
        # Verify columns were created with correct ratio
        self.mock_st.columns.assert_called_once_with([1, 3])
    
    def test_tool_button_click(self):
        """Test what happens when a tool button is clicked"""
        # Configure mock tool class
        mock_tool_class = MagicMock()
        mock_tool_instance = MagicMock()
        mock_tool_class.return_value = mock_tool_instance
        mock_tool_instance.name = 'TestTool'
        mock_tool_instance.description = 'Test tool description'
        
        # Set up our page with the mock tool
        self.page_tools.available_tools = {'TestTool': mock_tool_class}
        
        # Setup button return value (clicked)
        self.mock_col1.button.return_value = True
        
        # Setup session state
        self.mock_ss.tools = []
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify button was created with correct name
        self.mock_col1.button.assert_called_once_with("TestTool", key="enable_TestTool", help=mock_tool_instance.description)
        
        # Verify tool was added to session state
        self.assertEqual(len(self.mock_ss.tools), 1)
        
        # Verify tool was saved to database
        self.mock_db_utils.save_tool.assert_called_once()

    def test_expander_display_valid_tool(self):
        """Test displaying a valid tool in an expander"""
        # Create a mock tool
        mock_tool = MagicMock()
        mock_tool.name = 'ValidTool'
        mock_tool.tool_id = 'valid_id'
        mock_tool.description = 'Valid tool description'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': 'value1'}
        mock_tool.is_valid.return_value = True
        mock_tool.is_parameter_mandatory.return_value = False
        
        # Add the tool to session state
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        self.mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock(return_value=False)
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify expander was created with correct title
        display_name = self.page_tools.get_tool_display_name(mock_tool)
        self.mock_col2.expander.assert_called_once_with(display_name)
        
        # Verify description was written
        mock_expander.write.assert_called_once_with('Valid tool description')
        
        # Verify text input was created
        mock_expander.text_input.assert_called_once_with('param1', value='value1', key='valid_id_param1', placeholder='Optional')
        
    def test_expander_display_invalid_tool(self):
        """Test displaying an invalid tool in an expander (with warning indicator)"""
        # Create a mock tool with invalid state (missing required parameter)
        mock_tool = MagicMock()
        mock_tool.name = 'InvalidTool'
        mock_tool.tool_id = 'invalid_id'
        mock_tool.description = 'Invalid tool description'
        mock_tool.get_parameter_names.return_value = ['required_param']
        mock_tool.parameters = {'required_param': ''}
        mock_tool.is_valid.return_value = False
        mock_tool.is_parameter_mandatory.return_value = True
        
        # Add the tool to session state
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        self.mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock(return_value=False)
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify expander was created with warning indicator
        display_name = self.page_tools.get_tool_display_name(mock_tool)
        self.mock_col2.expander.assert_called_once_with(f"❗ {display_name}")
        
        # Verify text input was created with 'Required' placeholder
        mock_expander.text_input.assert_called_once_with('required_param', value='', key='invalid_id_required_param', placeholder='Required')
    
    def test_parameter_update_via_ui(self):
        """Test updating a parameter through the UI"""
        # Create a mock tool
        mock_tool = MagicMock()
        mock_tool.name = 'TestTool'
        mock_tool.tool_id = 'test_id'
        mock_tool.description = 'Test tool description'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': 'old_value'}
        mock_tool.is_valid.return_value = True
        mock_tool.is_parameter_mandatory.return_value = False
        
        # Add the tool to session state
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        self.mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock(return_value=False)
        
        # Setup text input return value (user entered a new value)
        mock_expander.text_input.return_value = 'new_value'
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify parameter was updated
        mock_tool.set_parameters.assert_called_once_with(param1='new_value')
        
        # Verify tool was saved to database
        self.mock_db_utils.save_tool.assert_called_once_with(mock_tool)
    
    def test_tool_removal_via_ui(self):
        """Test removing a tool through the UI"""
        # Create a mock tool
        mock_tool = MagicMock()
        mock_tool.name = 'TestTool'
        mock_tool.tool_id = 'test_id'
        mock_tool.description = 'Test tool description'
        mock_tool.get_parameter_names.return_value = ['param1']
        mock_tool.parameters = {'param1': 'value1'}
        mock_tool.is_valid.return_value = True
        mock_tool.is_parameter_mandatory.return_value = False
        
        # Add the tool to session state
        self.mock_ss.tools = [mock_tool]
        
        # Setup mock expander
        mock_expander = MagicMock()
        self.mock_col2.expander.return_value = mock_expander
        mock_expander.__enter__ = MagicMock()
        mock_expander.__exit__ = MagicMock(return_value=False)
        
        # Setup button return value (clicked)
        mock_expander.button.return_value = True
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify removal button was created
        mock_expander.button.assert_called_once_with("Remove", key="remove_test_id")
        
        # Verify tool was removed
        self.assertEqual(self.mock_ss.tools, [])
        self.mock_db_utils.delete_tool.assert_called_once_with('test_id')
        
        # Verify streamlit rerun was called
        self.mock_st.rerun.assert_called_once()
    
    def test_no_enabled_tools(self):
        """Test UI when no tools are enabled"""
        # Setup empty tools list
        self.mock_ss.tools = []
        
        # Call draw_tools
        self.page_tools.draw_tools()
        
        # Verify "Enabled Tools" header not written
        self.mock_col2.write.assert_not_called()
        
        # Verify no expanders were created
        self.mock_col2.expander.assert_not_called()

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        unittest.main()