# Notebooks

## Local development
### Install dependencies
* Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
* Install dependencies
```bash
# Create a virtual environment with Python 3.9 or 3.10 (both are supported)
uv venv --python 3.9  # or use 3.10 if available (e.g., Colab uses Python 3.10)
source .venv/bin/activate
uv pip install pip jupyterlab

uv run jupyter lab 
uv pip list --verbose
```

## Notebook

* [potential_motion_plan_eval_maze2d_demo.ipynb](potential_motion_plan_eval_maze2d_demo.ipynb) 
![animation](animation-potential-motion-plan-release.gif)


