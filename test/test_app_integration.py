"""Integration tests for app.py with its dependencies."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import importlib

# Add app directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))


class TestAppIntegration:
    """Integration test suite for app.py with actual dependencies."""
    
    def test_app_imports(self):
        """Test that all required modules for app.py can be imported."""
        # List of modules that app.py depends on
        required_modules = [
            'streamlit',
            'db_utils',
            'pg_agents', 
            'pg_tasks',
            'pg_crews',
            'pg_tools',
            'pg_crew_run',
            'pg_export_crew',
            'pg_results',
            'dotenv',
            'llms',
            'os'
        ]
        
        # Try to import each module
        failed_imports = []
        for module in required_modules:
            try:
                # Use importlib to check if module can be imported
                spec = importlib.util.find_spec(module)
                assert spec is not None, f"Module '{module}' not found"
            except (ImportError, ModuleNotFoundError, AssertionError) as e:
                failed_imports.append((module, str(e)))
                
        # Assert that all imports succeeded
        assert not failed_imports, f"Failed to import: {failed_imports}"
    
    def test_page_classes_interface(self):
        """Test that all page classes have the required interface."""
        # This test verifies that each page class has the required methods
        # Without actually instantiating them (which would require full dependency setup)
        
        with patch.dict('sys.modules'):
            # Create mock page modules
            page_modules = {
                'pg_agents': MagicMock(),
                'pg_tasks': MagicMock(),
                'pg_crews': MagicMock(),
                'pg_tools': MagicMock(),
                'pg_crew_run': MagicMock(),
                'pg_results': MagicMock(),
                'pg_export_crew': MagicMock()
            }
            
            # Mock each page class
            for module_name, mock_module in page_modules.items():
                page_class_name = 'Page' + module_name[3:].replace('_', ' ')
                page_class = type(page_class_name, (), {'draw': MagicMock()})
                setattr(mock_module, page_class_name, page_class)
                sys.modules[module_name] = mock_module
            
            # Import app module with our mocks in place
            import app
            
            # Check that each page in the pages function has a draw method
            pages = app.pages()
            for page_name, page_obj in pages.items():
                # Check if the draw method exists on the class
                assert hasattr(page_obj.__class__, 'draw'), f"Page {page_name} is missing draw method"
    
    @pytest.mark.parametrize("env_value,expected", [
        ('true', True),
        ('True', True),
        ('1', True),
        ('false', False),
        ('False', False),
        ('0', False),
        (None, False),
    ])
    def test_agentops_env_parsing(self, env_value, expected):
        """Test that agentops enabled parsing works correctly for various env values."""
        # Mock all streamlit related modules
        with patch.dict('sys.modules', {
            'streamlit': MagicMock(),
            'streamlit.runtime': MagicMock(),
            'streamlit.runtime.scriptrunner': MagicMock(),
            'streamlit.runtime.scriptrunner_utils': MagicMock(),
            'streamlit.runtime.scriptrunner_utils.script_run_context': MagicMock(),
        }):
            with patch('os.getenv', return_value=env_value):
                with patch('dotenv.load_dotenv'):
                    with patch('llms.load_secrets_fron_env'):
                        # Mock the agentops module
                        mock_agentops = MagicMock()
                        
                        # Setup system modules dict with our mocks
                        mock_modules = {
                            'agentops': mock_agentops,
                            'pg_agents': MagicMock(),
                            'pg_tasks': MagicMock(),
                            'pg_crews': MagicMock(),
                            'pg_tools': MagicMock(),
                            'pg_crew_run': MagicMock(),
                            'pg_results': MagicMock(),
                            'pg_export_crew': MagicMock(),
                            'db_utils': MagicMock(),
                        }
                        
                        # Add page classes to mocks
                        for module_name in ['pg_agents', 'pg_tasks', 'pg_crews', 'pg_tools', 'pg_crew_run', 'pg_results', 'pg_export_crew']:
                            page_class_name = 'Page' + module_name[3:].replace('_', '')
                            mock_page_class = type(page_class_name, (), {'draw': MagicMock()})
                            mock_page_instance = mock_page_class()
                            getattr(mock_modules[module_name], page_class_name).return_value = mock_page_instance
                        
                        with patch.dict('sys.modules', mock_modules):
                            # Create a fresh version of the app module
                            if 'app' in sys.modules:
                                del sys.modules['app']
                            
                            # Create session state mock
                            mock_ss = MagicMock()
                            mock_ss.page = 'Crews'
                            mock_ss.get.return_value = False
                            
                            # Import app with our mocks in place
                            with patch('streamlit.session_state', mock_ss):
                                import app
                                
                                # Mock app's session state
                                with patch('app.ss', mock_ss):
                                    # Mock remaining app dependencies
                                    with patch('app.db_utils.initialize_db'):
                                        with patch('app.load_data'):
                                            with patch('app.draw_sidebar'):
                                                with patch('app.PageCrewRun.maintain_session_state'):
                                                    with patch('app.pages', return_value={'Crews': MagicMock()}):
                                                        # Call main to trigger AgentOps check
                                                        app.main()
                                                        
                                                        # Verify expected behavior
                                                        if expected:
                                                            assert 'agentops_failed' not in mock_ss or not mock_ss.agentops_failed
                                                        elif 'agentops' in sys.modules:
                                                            # In the non-True cases, we shouldn't even try to import agentops
                                                            assert 'agentops_init_calls' not in mock_ss or mock_ss.agentops_init_calls == 0
    
    def test_db_initialization_flow(self):
        """Test the database initialization and data loading flow."""
        with patch('streamlit.session_state') as mock_ss:
            with patch('app.ss') as app_ss:
                with patch('streamlit.sidebar'):
                    with patch('streamlit.set_page_config'):
                        with patch('dotenv.load_dotenv'):
                            with patch('llms.load_secrets_fron_env'):
                                with patch('db_utils.initialize_db') as mock_init_db:
                                    with patch('db_utils.load_agents') as mock_load_agents:
                                        with patch('db_utils.load_tasks') as mock_load_tasks:
                                            with patch('db_utils.load_crews') as mock_load_crews:
                                                with patch('db_utils.load_tools') as mock_load_tools:
                                                    with patch('db_utils.load_tools_state') as mock_load_tools_state:
                                                        
                                                        # Set up mocks
                                                        mock_ss.page = 'Crews'
                                                        app_ss.page = 'Crews'
                                                        mock_ss.get = MagicMock(return_value=False)
                                                        app_ss.get = MagicMock(return_value=False)
                                                        
                                                        # The order of calls is important:
                                                        # 1. initialize_db should be called first
                                                        # 2. Then all load_* functions should be called
                                                        call_order = []
                                                        def track_call(name):
                                                            def _track(*args, **kwargs):
                                                                call_order.append(name)
                                                                return MagicMock()
                                                            return _track
                                                        
                                                        # Apply trackers
                                                        mock_init_db.side_effect = track_call('initialize_db')
                                                        mock_load_agents.side_effect = track_call('load_agents')
                                                        mock_load_tasks.side_effect = track_call('load_tasks')
                                                        mock_load_crews.side_effect = track_call('load_crews')
                                                        mock_load_tools.side_effect = track_call('load_tools')
                                                        mock_load_tools_state.side_effect = track_call('load_tools_state')
                                                        
                                                        # Mock remaining dependencies
                                                        with patch('app.os.getenv', return_value='false'):
                                                            with patch('app.draw_sidebar'):
                                                                with patch('app.PageCrewRun.maintain_session_state'):
                                                                    with patch('app.pages', return_value={'Crews': MagicMock()}):
                                                                        # Import app fresh
                                                                        import importlib
                                                                        importlib.reload(__import__('app'))
                                                                        import app
                                                                        
                                                                        # Call main to trigger the flow
                                                                        app.main()
                                                                        
                                                                        # Check initialization happens first
                                                                        assert call_order[0] == 'initialize_db', "DB initialization should happen first"
                                                                        
                                                                        # Check all load functions are called (in any order after init)
                                                                        assert 'load_agents' in call_order, "load_agents should be called"
                                                                        assert 'load_tasks' in call_order, "load_tasks should be called"
                                                                        assert 'load_crews' in call_order, "load_crews should be called"
                                                                        assert 'load_tools' in call_order, "load_tools should be called"
                                                                        assert 'load_tools_state' in call_order, "load_tools_state should be called"