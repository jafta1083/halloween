# AI Agent Instructions for Halloween Project

This document provides essential guidance for AI agents working with this Python codebase.

## Project Overview
This is a Python project currently in its initial setup phase. The project uses modern Python development practices as evidenced by the comprehensive `.gitignore` configuration.

## Development Environment
- This is a Python project with support for various Python package management tools:
  - Poetry (optional)
  - pipenv (optional)
  - UV (optional)
  - pdm (optional)
  - pixi (optional)
  - virtualenv/venv (standard)

## Key Files and Directories
- `.gitignore` - Comprehensive Python-specific ignore patterns
- Important development tool configurations are supported:
  - Ruff for linting (`.ruff_cache/`)
  - mypy for type checking (`.mypy_cache/`)
  - pytest for testing (`.pytest_cache/`)
  - Jupyter notebooks (`.ipynb_checkpoints/`)

## Conventions and Patterns
1. Python Package Structure:
   - Use standard Python package layout with `src/` directory (when implemented)
   - Follow PEP guidelines for Python code organization

2. Testing:
   - Tests should be placed in a `tests/` directory (when implemented)
   - Use pytest as the testing framework

3. Documentation:
   - Maintain documentation in markdown format
   - Keep README.md updated with project overview and setup instructions

## Development Workflow
1. Environment Setup:
   - Create and activate a virtual environment
   - Install development dependencies
   - Follow PEP standards for Python code

2. Code Quality:
   - Use Ruff for linting Python code
   - Run mypy for type checking
   - Ensure tests pass before committing

## Integration Points
- CI/CD: Not yet configured, but project structure supports common Python CI tools
- Dependencies: Use requirements.txt or modern Python package management tools

## Notes for AI Agents
1. Always respect the `.gitignore` patterns when creating new files
2. Maintain Python best practices (PEP 8, PEP 517, etc.)
3. Use appropriate tool configurations based on the development task:
   - Linting: Ruff
   - Type checking: mypy
   - Testing: pytest
   - Package management: Multiple options supported

*This document will be updated as the project evolves and new patterns emerge.*