# Contributing to CadBridge

Thank you for your interest in contributing to **CadBridge**!

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/mdzihan0165-stack/cadbridge.git
   cd cadbridge
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

3. Run the test suite:
   ```bash
   python -m unittest discover tests/
   ```

## Architectural Guidelines

- **AIA Layer Standards:** All new geometry entities must be placed strictly on standardized layers (`A-WALL-EXTR`, `A-WALL-INTR`, `A-DOOR`, `A-GLAZ`, etc.).
- **Unit Scale:** All dimensions in JSON specifications and DXF entities must follow millimeters (`mm`) for precision.
- **Headless Compatibility:** All code must remain pure Python and headless without dependencies on Autodesk proprietary binaries.

## Pull Request Guidelines

- Ensure all existing unit tests pass.
- Include architectural visual tests where applicable.
- Follow PEP 8 style conventions.
