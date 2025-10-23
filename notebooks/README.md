# Notebooks

## Local development
### Install dependencies
* Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
* Install dependencies
```bash
uv venv --python 3.9 #seems to work with /usr/local/lib/python3.10 from the colabs notebook
source .venv/bin/activate
uv pip install pip jupyterlab

uv run jupyter lab 
uv pip list --verbose
```

## Notebook

* [potential_motion_plan_eval_maze2d_demo.ipynb](potential_motion_plan_eval_maze2d_demo.ipynb) 
![animation](animation-potential-motion-plan-release.gif)


