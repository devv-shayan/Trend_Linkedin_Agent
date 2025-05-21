# Trend LinkedIn Agent

A powerful AI agent that identifies trending topics, analyzes them, and generates engaging LinkedIn posts with user input.

## Overview

This project automates the process of creating trend-driven LinkedIn content using multiple specialized AI agents. The Agentic Workflow:

1. Identifies current trending topics in your specified niche
2. Selects the most promising trend
3. Analyzes the trend in detail
4. Generates thought-provoking questions for user input
5. Creates a brief incorporating trend analysis and user perspective
6. Transforms the brief into a polished LinkedIn post

## Prerequisites

- Python 3.13+
- UV package manager
- Required API keys:
  - Gemini API key (for AI model access and search functionality)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Trend_Linkedin_Agent.git
   cd Trend_Linkedin_Agent
   ```

2. Install UV package manager (if not already installed):
   ```
   pip install uv
   ```


3. Initialize the project:
   ```
   uv init
   ```

4. Create and activate a virtual environment:
   ```
   uv venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

5. Install dependencies from pyproject.toml:
   ```
   uv sync
   ```

## Configuration

Create a `.env` file in the project root with your API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

Run the agent pipeline:

```
python main.py
```

Follow the interactive prompts to:
1. Enter the current date
2. Specify your niche (e.g., "digital marketing", "software development", "leadership")
3. Choose from AI-generated questions to personalize the content
4. Provide your answers to shape the final LinkedIn post

## Project Structure

- `main.py`: Orchestrates the agent pipeline workflow
- `agent.py`: Defines specialized agents for each pipeline stage
- `model.py`: Configures the Gemini LLM with OpenAI-compatible interface
- `prompts.py`: Contains prompt templates for each agent
- `tools.py`: Implements search functionality using Gemini API with Google Search grounding

## Agent Pipeline Steps

1. **Trend Spotting**: Identifies current trending topics in your niche
2. **Trend Selection**: Analyzes and selects the most promising trend
3. **Trend Analysis**: Performs in-depth analysis of the selected trend
4. **Question Generation**: Creates thought-provoking questions for user input
5. **Brief Writing**: Combines trend analysis with user perspective
6. **LinkedIn Post Generation**: Transforms the brief into an engaging post

## Example Output

The final LinkedIn post follows a structured template designed for maximum engagement:
- Opening hook or question
- Quick answer
- Transition to reflection
- Core insight
- Origin story
- Plot twist
- Lesson learned
- Call to action
- Recent example or anecdote
- P.S. with a fun aside or safety joke

## License

[Include your license information here]

## Acknowledgements

- Uses OpenAI's Agent SDK for orchestration
- Powered by Google's Gemini AI model with Google Search grounding
