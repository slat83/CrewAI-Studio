# CrewAI Studio

[![GitHub Stars](https://img.shields.io/github/stars/strnad/CrewAI-Studio)](https://github.com/strnad/CrewAI-Studio/stargazers)
[![License](https://img.shields.io/github/license/strnad/CrewAI-Studio)](https://github.com/strnad/CrewAI-Studio/blob/main/LICENSE)

CrewAI Studio is a user-friendly graphical interface that helps you create and manage AI agent teams (crews) without writing code. Built with Streamlit, it provides an intuitive way to leverage the power of CrewAI for task automation and AI orchestration.

## Features

### Core Capabilities
- **No-Code Interface**: Build and manage AI crews through an intuitive graphical interface
- **Multi-Platform**: Works seamlessly on Windows, Linux, and MacOS
- **Background Processing**: Run crews in separate threads with the ability to stop them
- **Single-Page Export**: Export your crew as a standalone Streamlit application

### AI Integration
- **Multiple AI Backends**: Support for:
  - OpenAI
  - Groq
  - Anthropic
  - LM Studio (remember to load embedding models)
- **CrewAI Tools**: Integrate with external services and real-world interactions
- **Custom Tools**: API calling and file writing capabilities, with more coming soon

## Prerequisites

Before installation, ensure you have:
- Python 3.8 or higher
- Git (for cloning the repository)
- Internet connection for downloading dependencies
- API keys for your chosen AI provider(s)

## System Requirements

- Memory: Minimum 4GB RAM (8GB recommended)
- Storage: 2GB free disk space
- CPU: Dual-core processor or better
- Internet: Broadband connection required for AI API calls

## Quick Start

1. **Install using your preferred method** (see Installation section below)
2. **Set up your environment**:
   ```bash
   cp .env_example .env
   # Edit .env with your API keys
   ```
3. **Launch the application** and open http://localhost:8501
4. **Create your first crew**:
   - Click "New Crew" 
   - Add agents and define their roles
   - Set up the execution task
   - Click "Run" to start your crew

## Basic Usage

1. **Managing Crews**:
   - Create new crews from the main dashboard
   - Save crews for later use
   - Export crews as standalone applications

2. **Working with Agents**:
   - Define agent roles and capabilities
   - Set agent personalities and expertise levels
   - Configure AI model settings per agent

3. **Running Tasks**:
   - Start/stop crew operations
   - Monitor execution progress
   - View task results and agent interactions

## Screenshots

<img src="https://raw.githubusercontent.com/strnad/CrewAI-Studio/main/img/crews.png" alt="crews definition" style="width:50%;"/>
<img src="https://raw.githubusercontent.com/strnad/CrewAI-Studio/main/img/kickoff.png" alt="kickoff" style="width:50%;"/>

## Installation

### Using Virtual Environment

**For Virtual Environment**: Ensure you have Python installed. If you dont have python instaled, you can simply use the conda installer.

#### On Linux or MacOS

1. **Clone the repository (or use downloaded ZIP file)**:

   ```bash
   git clone https://github.com/strnad/CrewAI-Studio.git
   cd CrewAI-Studio
   ```

2. **Run the installation script**:

   ```bash
   ./install_venv.sh
   ```

3. **Run the application**:
   ```bash
   ./run_venv.sh
   ```

#### On Windows

1. **Clone the repository (or use downloaded ZIP file)**:

   ```powershell
   git clone https://github.com/strnad/CrewAI-Studio.git
   cd CrewAI-Studio
   ```

2. **Run the Conda installation script**:

   ```powershell
   ./install_venv.bat
   ```

3. **Run the application**:
   ```powershell
   ./run_venv.bat
   ```

### Using Conda

Conda will be installed locally in the project folder. No need for a pre-existing Conda installation.

#### On Linux

1. **Clone the repository (or use downloaded ZIP file)**:

   ```bash
   git clone https://github.com/strnad/CrewAI-Studio.git
   cd CrewAI-Studio
   ```

2. **Run the Conda installation script**:

   ```bash
   ./install_conda.sh
   ```

3. **Run the application**:
   ```bash
   ./run_conda.sh
   ```

#### On Windows

1. **Clone the repository (or use downloaded ZIP file)**:

   ```powershell
   git clone https://github.com/strnad/CrewAI-Studio.git
   cd CrewAI-Studio
   ```

2. **Run the Conda installation script**:

   ```powershell
   ./install_conda.bat
   ```

3. **Run the application**:
   ```powershell
   ./run_conda.bat
   ```

### One-Click Deployment

[![Deploy to RepoCloud](https://d16t0pc4846x52.cloudfront.net/deploylobe.svg)](https://repocloud.io/details/?app_id=318)

## Running with Docker Compose

To quickly set up and run CrewAI-Studio using Docker Compose, follow these steps:

### Prerequisites

- Ensure [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed on your system.

### Steps

1. Clone the repository:
```
git clone https://github.com/chadsly/CrewAI-Studio.git
cd CrewAI-Studio
```

2. Create a .env file for configuration.  Edit for your own configuration:
```
cp .env_example .env
```

3. Start the application with Docker Compose:
```
docker-compose up --build
```

4. Access the application: http://localhost:8501

## Configuration

Before running the application, ensure you update the `.env` file with your API keys and other necessary configurations. An example `.env` file is provided for reference.

## Running Tests

CrewAI Studio includes a comprehensive test suite to ensure code quality and functionality. To run the tests:

### Prerequisites

Ensure you have the testing dependencies installed:
```bash
pip install pytest pytest-cov pytest-mock coverage
```

Or simply install all dependencies including test requirements:
```bash
pip install -r requirements.txt
```

### Running the Tests

1. **Run all tests**:
   ```bash
   pytest
   ```

2. **Run tests with coverage report**:
   ```bash
   pytest --cov=app
   ```

3. **Generate HTML coverage report**:
   ```bash
   pytest --cov=app --cov-report=html
   ```
   This will create a `htmlcov` directory with an HTML report that you can open in your browser.

4. **Run specific test file**:
   ```bash
   pytest test/test_app.py
   ```

5. **Run tests with verbose output**:
   ```bash
   pytest -v
   ```

### Test Structure

The test suite is organized as follows:
- `test/test_app.py`: Unit tests for the main application
- `test/test_app_integration.py`: Integration tests for app dependencies
- `test/test_app_ui.py`: UI-specific tests for Streamlit components

### Troubleshooting Tests

If you encounter test failures:
1. Ensure all dependencies are correctly installed
2. Check that your Python version is compatible
3. Verify that the app structure hasn't changed significantly since the tests were written

## Troubleshooting
In case of problems:
- Delete the `venv/miniconda` folder and reinstall `crewai-studio`.
- Rename `crewai.db` (it contains your crews but sometimes new versions can break compatibility).
- Raise an issue and I will help you.

## Common Issues

1. **API Connection Errors**:
   - Verify API keys in .env file
   - Check internet connection
   - Ensure API service is available

2. **Installation Problems**:
   - Clear Python cache: `pip cache purge`
   - Update pip: `python -m pip install --upgrade pip`
   - Check Python version compatibility

3. **Runtime Errors**:
   - Verify all dependencies are installed
   - Check logs for detailed error messages
   - Ensure sufficient system resources

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a Pull Request

Please ensure your code follows our style guidelines and includes appropriate tests.

## Video tutorial
Video tutorial on CrewAI Studio made by Josh Poco

[![FREE CrewAI Studio GUI EASY AI Agent Creation!🤖 Open Source AI Agent Orchestration Self Hosted](https://img.youtube.com/vi/3Uxdggt88pY/hqdefault.jpg)](https://www.youtube.com/watch?v=3Uxdggt88pY)

## Star History

<a href="https://star-history.com/#strnad/CrewAI-Studio&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=strnad/CrewAI-Studio&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=strnad/CrewAI-Studio&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=strnad/CrewAI-Studio&type=Date" />
 </picture>   
</a>
