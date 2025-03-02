"""Test fixtures for CrewAI-Studio tests."""

import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add app directory to path for importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit to prevent UI interactions during testing."""
    with patch('streamlit.sidebar') as mock_sidebar:
        with patch('streamlit.image') as mock_image:
            with patch('streamlit.radio') as mock_radio:
                with patch('streamlit.set_page_config') as mock_page_config:
                    with patch('streamlit.rerun') as mock_rerun:
                        with patch('streamlit.session_state') as mock_session_state:
                            mock_session_state.__getitem__ = MagicMock()
                            mock_session_state.__setitem__ = MagicMock()
                            mock_session_state.get = MagicMock(return_value=False)
                            yield {
                                'sidebar': mock_sidebar,
                                'image': mock_image,
                                'radio': mock_radio,
                                'set_page_config': mock_page_config,
                                'rerun': mock_rerun,
                                'session_state': mock_session_state
                            }

@pytest.fixture
def mock_db_utils():
    """Mock database utilities to prevent actual database operations during testing."""
    with patch('db_utils.initialize_db') as mock_init_db:
        with patch('db_utils.load_agents') as mock_load_agents:
            with patch('db_utils.load_tasks') as mock_load_tasks:
                with patch('db_utils.load_crews') as mock_load_crews:
                    with patch('db_utils.load_tools') as mock_load_tools:
                        with patch('db_utils.load_tools_state') as mock_load_tools_state:
                            yield {
                                'initialize_db': mock_init_db,
                                'load_agents': mock_load_agents,
                                'load_tasks': mock_load_tasks,
                                'load_crews': mock_load_crews,
                                'load_tools': mock_load_tools,
                                'load_tools_state': mock_load_tools_state
                            }

@pytest.fixture
def mock_pages():
    """Mock page classes to prevent actual page rendering during testing."""
    with patch('pg_agents.PageAgents') as mock_page_agents:
        with patch('pg_tasks.PageTasks') as mock_page_tasks:
            with patch('pg_crews.PageCrews') as mock_page_crews:
                with patch('pg_tools.PageTools') as mock_page_tools:
                    with patch('pg_crew_run.PageCrewRun') as mock_page_crew_run:
                        with patch('pg_results.PageResults') as mock_page_results:
                            with patch('pg_export_crew.PageExportCrew') as mock_page_export_crew:
                                # Create mock instances for each page class
                                mock_page_agents.return_value = MagicMock()
                                mock_page_tasks.return_value = MagicMock()
                                mock_page_crews.return_value = MagicMock()
                                mock_page_tools.return_value = MagicMock()
                                mock_page_crew_run.return_value = MagicMock()
                                mock_page_results.return_value = MagicMock()
                                mock_page_export_crew.return_value = MagicMock()
                                
                                # Add maintain_session_state method to PageCrewRun
                                mock_page_crew_run.maintain_session_state = MagicMock()
                                
                                yield {
                                    'PageAgents': mock_page_agents,
                                    'PageTasks': mock_page_tasks,
                                    'PageCrews': mock_page_crews,
                                    'PageTools': mock_page_tools,
                                    'PageCrewRun': mock_page_crew_run,
                                    'PageResults': mock_page_results,
                                    'PageExportCrew': mock_page_export_crew
                                }

@pytest.fixture
def mock_env():
    """Mock environment-related functions."""
    with patch('dotenv.load_dotenv') as mock_load_dotenv:
        with patch('llms.load_secrets_fron_env') as mock_load_secrets:
            with patch('os.getenv') as mock_getenv:
                mock_getenv.return_value = 'false'  # Default value for most env vars
                yield {
                    'load_dotenv': mock_load_dotenv,
                    'load_secrets_fron_env': mock_load_secrets,
                    'getenv': mock_getenv
                }