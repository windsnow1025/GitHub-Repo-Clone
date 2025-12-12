# GitHub Repository Clone

## Development

### Python uv

1. Install uv: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Install Python in uv: `uv python install 3.12`; upgrade Python in uv: `uv python install 3.12`
3. Configure requirements:
  ```bash
  uv sync
  ```

### Pycharm Professional

1. Add New Interpreter >> Add Local Interpreter
  - Environment: Select existing
  - Type: uv
2. Add New Configuration >> uv run >> script: `./usage/main.py`

## Usage

Before each run, remove all files in the target directory.
