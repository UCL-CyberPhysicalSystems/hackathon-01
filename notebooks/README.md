# Notebooks

## Local development
### Install dependencies

* Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* Install dependencies
```bash
# Create a virtual environment with respective python version 
# Note that notebooks have been tested locally with python 3.9 and 3.10

uv venv python309 --python 3.9
source .venv/bin/activate

uv venv .venv.python310 --python 3.10
source .venv.python310/bin/activate

uv pip install pip jupyterlab
uv run jupyter lab 
uv pip list --verbose
```

* Run notebook
```bash
source .venv/bin/activate
uv run jupyter lab 
```
* [potential_motion_plan_eval_maze2d_demo.ipynb](potential_motion_plan_eval_maze2d_demo.ipynb)    

![animation](animation-potential-motion-plan-release.gif)

