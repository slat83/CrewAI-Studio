# Project Structure and File Explanations

## Root Directory

- **crewai.db**: The database file where the application stores its data.
- **docker-compose-no_env.yaml**: Docker Compose configuration file without environment variables.
- **docker-compose.yaml**: Docker Compose configuration file for setting up and running the application in a Docker environment.
- **Dockerfile**: Instructions for building a Docker image for the application.
- **install_conda.bat**: Batch script for installing the application using Conda on Windows.
- **install_conda.sh**: Shell script for installing the application using Conda on Linux/MacOS.
- **install_venv.bat**: Batch script for setting up a virtual environment on Windows.
- **install_venv.sh**: Shell script for setting up a virtual environment on Linux/MacOS.
- **LICENCE**: License file for the project.
- **README.md**: Documentation file providing an overview of the project, installation instructions, and usage guidelines.
- **requirements.txt**: List of Python dependencies required by the project.
- **run_conda.bat**: Batch script for running the application using Conda on Windows.
- **run_conda.sh**: Shell script for running the application using Conda on Linux/MacOS.
- **run_venv.bat**: Batch script for running the application in a virtual environment on Windows.
- **run_venv.sh**: Shell script for running the application in a virtual environment on Linux/MacOS.

## `app/` Directory

- **app.py**: The main application file that sets up the Streamlit interface, loads data, and manages the different pages of the application. It initializes the database, loads environment variables, and handles the navigation between different pages such as Crews, Tools, Agents, Tasks, Kickoff, Results, and Import/Export. The file uses Streamlit to create a sidebar for navigation and to render different pages based on user selection. It also includes functions to load data from the database and maintain session state.
- **console_capture.py**: Utility for capturing console output, useful for debugging and logging purposes. This file helps in redirecting the standard output and error streams to capture logs that can be displayed within the Streamlit interface or saved for later analysis.
- **db_utils.py**: Utilities for interacting with the database, including functions to load and save agents, tasks, crews, and tools. This file contains functions to initialize the database, load data into session state, and perform CRUD operations on various entities.
- **llms.py**: Functions for loading secrets and managing language models, including loading API keys and other secrets from environment variables. This file ensures that the necessary API keys and configurations are loaded from environment variables to interact with different AI backends.
- **my_agent.py**: Definitions and utilities related to agents, including agent roles, capabilities, and configurations. This file defines the structure and behavior of agents, including their roles, goals, and the tools they can use.
- **my_crew.py**: Definitions and utilities related to crews, including crew composition, roles, and execution tasks. This file manages the composition of crews, assigning agents to specific roles and defining the tasks they need to perform.
- **my_task.py**: Definitions and utilities related to tasks, including task creation, management, and execution. This file handles the creation and management of tasks that agents need to execute as part of their roles in a crew.
- **my_tools.py**: Definitions and utilities related to tools, including tool configurations and interactions. This file defines various tools that agents can use to perform their tasks, including custom tools for API interactions, file writing, and web scraping.
- **pg_agents.py**: Page for managing agents, including adding, editing, and deleting agents. This file uses Streamlit to create a user interface for managing agents, allowing users to define agent roles, capabilities, and configurations.
- **pg_crew_run.py**: Page for running crews, including starting, stopping, and monitoring crew operations. This file provides a Streamlit interface for executing and monitoring the operations of a crew, displaying real-time progress and results.
- **pg_crews.py**: Page for managing crews, including creating, editing, and deleting crews. This file uses Streamlit to create a user interface for managing crews, allowing users to define the composition and roles of different crews.
- **pg_export_crew.py**: Page for exporting crews, including exporting crew configurations as standalone applications. This file provides functionality to export crew configurations into a standalone Streamlit application, including generating necessary environment files and scripts for deployment.
- **pg_results.py**: Page for viewing results, including task results and agent interactions. This file uses Streamlit to display the results of tasks executed by agents, providing insights into their performance and interactions.
- **pg_tasks.py**: Page for managing tasks, including adding, editing, and deleting tasks. This file provides a Streamlit interface for managing tasks, allowing users to define and configure tasks that agents need to perform.
- **pg_tools.py**: Page for managing tools, including adding, editing, and deleting tools. This file uses Streamlit to create a user interface for managing tools, allowing users to configure and assign tools to agents.
- **result.py**: Utilities for handling results, including saving and loading task results. This file manages the storage and retrieval of task results, ensuring that results are saved and can be accessed for analysis.
- **utils.py**: General utility functions, including common helper functions used throughout the application. This file contains various helper functions that are used across different parts of the application to perform common tasks.

## `tools/` Directory

- **CSVSearchToolEnhanced.py**: Tool for enhanced CSV search capabilities, allowing for advanced search operations on CSV files.
- **CustomApiTool.py**: Tool for custom API interactions, allowing for integration with external APIs.
- **CustomCodeInterpreterTool.py**: Tool for interpreting custom code, allowing for execution of custom scripts and code snippets.
- **CustomFileWriteTool.py**: Tool for custom file writing operations, allowing for writing data to files in various formats.
- **ScrapeWebsiteToolEnhanced.py**: Tool for enhanced website scraping capabilities, allowing for extracting data from web pages.

## `docs/` Directory

- **Documentation files**: Contains additional documentation for the project.
- **PROJECT_STRUCTURE.md**: Detailed documentation explaining the project structure and the purpose of each file.

## `img/` Directory

- **crewai_logo.png**: Logo image for the application.
- **crews.png**: Image related to crew definitions.
- **favicon.ico**: Favicon for the application.
- **kickoff.png**: Image related to the kickoff process.
