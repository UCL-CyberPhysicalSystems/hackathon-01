# Notebooks

## Local development
### Install dependencies

Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create a virtual environment with respective python version 

```bash
# Using python3.9
uv venv python309 --python 3.9
source .venv/bin/activate

# Using python3.10
uv venv .venv.python310 --python 3.10
source .venv.python310/bin/activate

# Using python3.11
uv venv .venv.python311 --python 3.11
source .venv.python311/bin/activate

# Using python3.12
uv venv .venv.python312 --python 3.12
source .venv.python312/bin/activate
```


Install dependencies
```bash
uv pip install --upgrade pip
uv pip install pip jupyterlab
```

Launch notebooks
```bash
uv run jupyter lab 
uv pip list --verbose
```


