"""Unit tests for the app.py file."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Import the app module for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
import app


class TestApp:
    """Test suite for app.py."""
    
    def test_pages_function(self, mock_pages):
        """Test that the pages function returns all expected pages."""
        pages_dict = app.pages()
        
        # Check that all expected page keys exist
        expected_pages = ['Crews', 'Tools', 'Agents', 'Tasks', 'Kickoff!', 'Results', 'Import/export']
        for page in expected_pages:
            assert page in pages_dict
    
    def test_load_data(self, mock_db_utils):
        """Test that load_data calls all the expected database functions."""
        with patch('app.ss', new=MagicMock()) as mock_ss:
            app.load_data()
            
            # Assert that all database loading functions are called
            mock_db_utils['load_agents'].assert_called_once()
            mock_db_utils['load_tasks'].assert_called_once()
            mock_db_utils['load_crews'].assert_called_once()
            mock_db_utils['load_tools'].assert_called_once()
            mock_db_utils['load_tools_state'].assert_called_once()
    
    def test_draw_sidebar(self):
        """Test the sidebar creation and page selection functionality."""
        with patch('app.st') as mock_st:
            with patch('app.ss') as mock_ss:
                # Configure sidebar to return a context manager
                sidebar_context = MagicMock()
                mock_st.sidebar.__enter__ = MagicMock(return_value=sidebar_context)
                mock_st.sidebar.__exit__ = MagicMock(return_value=None)
                
                # Set up session state
                mock_ss.__contains__ = MagicMock(return_value=True)
                mock_ss.page = 'Crews'
                
                # Configure radio to return a different page
                mock_st.radio = MagicMock(return_value='Agents')
                
                # Call the function to test
                app.draw_sidebar()
                
                # Check that the image is displayed
                mock_st.image.assert_called_once_with("img/crewai_logo.png")
                
                # Check that the radio button is created with all pages
                mock_st.radio.assert_called_once()
                
                # With our mock returning 'Agents', page should switch
                assert mock_ss.page == 'Agents'

    def test_main_function(self, mock_streamlit, mock_db_utils, mock_env, mock_pages):
        """Test the main function that initializes the app."""
        # Mock session_state globally for this test
        with patch('app.ss') as mock_ss:
            mock_ss.page = 'Crews'
            mock_ss.get = MagicMock(return_value=False)
            
            # Mock function dependencies to prevent actual execution
            with patch('app.load_dotenv') as mock_load_dotenv:
                with patch('app.load_secrets_fron_env') as mock_load_secrets:
                    with patch('app.db_utils.initialize_db') as mock_init_db:
                        with patch('app.load_data') as mock_load_data:
                            with patch('app.draw_sidebar') as mock_draw_sidebar:
                                with patch('app.PageCrewRun.maintain_session_state') as mock_maintain_state:
                                    with patch('app.pages') as mock_pages_func:
                                        # Set up page mocks
                                        mock_pages_dict = {
                                            'Crews': MagicMock(),
                                            'Tools': MagicMock(),
                                            'Agents': MagicMock(),
                                            'Tasks': MagicMock(),
                                            'Kickoff!': MagicMock(),
                                            'Results': MagicMock(),
                                            'Import/export': MagicMock()
                                        }
                                        mock_pages_func.return_value = mock_pages_dict
                                        
                                        # Execute the main function
                                        app.main()
                                        
                                        # Check function calls
                                        mock_load_dotenv.assert_called_once()
                                        mock_load_secrets.assert_called_once()
                                        mock_init_db.assert_called_once()
                                        mock_load_data.assert_called_once()
                                        mock_draw_sidebar.assert_called_once()
                                        mock_maintain_state.assert_called_once()
                                        
                                        # Check that the correct page is drawn
                                        mock_pages_dict[mock_ss.page].draw.assert_called_once()

    def test_agentops_initialization(self):
        """Test AgentOps initialization when enabled."""
        # Mock environment variables
        with patch('app.os.getenv', return_value='true'):
            # Mock app dependencies
            with patch('app.ss') as mock_ss:
                mock_ss.get = MagicMock(return_value=False)
                mock_ss.page = 'Crews'
                
                # Mock agentops module and initialization
                mock_agentops = MagicMock()
                with patch.dict('sys.modules', {'agentops': mock_agentops}):
                    with patch('app.load_dotenv'):
                        with patch('app.load_secrets_fron_env'):
                            with patch('app.db_utils.initialize_db'):
                                with patch('app.load_data'):
                                    with patch('app.draw_sidebar'):
                                        with patch('app.PageCrewRun.maintain_session_state'):
                                            with patch('app.pages', return_value={'Crews': MagicMock()}):
                                                # Call main to trigger AgentOps check
                                                app.main()
                                                
                                                # Check that agentops.init was called
                                                mock_agentops.init.assert_called_once()

    def test_agentops_failure_handling(self):
        """Test handling of AgentOps initialization failure."""
        # Mock environment variables
        with patch('app.os.getenv', return_value='true'):
            # Mock app dependencies
            with patch('app.ss') as mock_ss:
                mock_ss.get = MagicMock(return_value=False)
                mock_ss.page = 'Crews'
                
                # Force an import error for agentops
                def mock_import_function(name, *args, **kwargs):
                    if name == 'agentops':
                        raise ModuleNotFoundError("No module named 'agentops'")
                    return MagicMock()
                
                with patch('builtins.__import__', side_effect=mock_import_function):
                    with patch('app.load_dotenv'):
                        with patch('app.load_secrets_fron_env'):
                            with patch('app.db_utils.initialize_db'):
                                with patch('app.load_data'):
                                    with patch('app.draw_sidebar'):
                                        with patch('app.PageCrewRun.maintain_session_state'):
                                            with patch('app.pages', return_value={'Crews': MagicMock()}):
                                                # Call main which should handle the exception
                                                app.main()
                                                
                                                # Check that the agentops_failed flag is set
                                                assert mock_ss.agentops_failed is True

    def test_main_with_different_pages(self):
        """Test the main function with different selected pages."""
        # Test for each page
        for page_name in ['Crews', 'Tools', 'Agents', 'Tasks', 'Kickoff!', 'Results', 'Import/export']:
            with patch('app.ss') as mock_ss:
                mock_ss.page = page_name
                mock_ss.get = MagicMock(return_value=False)
                
                # Mock function dependencies
                with patch('app.load_dotenv'):
                    with patch('app.load_secrets_fron_env'):
                        with patch('app.db_utils.initialize_db'):
                            with patch('app.load_data'):
                                with patch('app.draw_sidebar'):
                                    with patch('app.PageCrewRun.maintain_session_state'):
                                        # Create mock pages
                                        mock_pages_dict = {}
                                        for p_name in ['Crews', 'Tools', 'Agents', 'Tasks', 'Kickoff!', 'Results', 'Import/export']:
                                            mock_pages_dict[p_name] = MagicMock()
                                        
                                        with patch('app.pages', return_value=mock_pages_dict):
                                            # Execute main
                                            app.main()
                                            
                                            # Check that the correct page is drawn
                                            mock_pages_dict[page_name].draw.assert_called_once()
                                            
                                            # Reset all mocks for next iteration
                                            for p_name, mock_page in mock_pages_dict.items():
                                                mock_page.draw.reset_mock()