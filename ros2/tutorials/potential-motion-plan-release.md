# Potential Based Diffusion Motion Planning

## Download project
https://drive.google.com/drive/folders/1gl_Si7PU6t0VxISdwS_mSCWJH9jU8hL7


## Run example
* Create env
```bash
cd /home/diffusion_path_planning/diffusion

python3 -m venv .env.ros2cuda --system-site-packages
source .env.ros2cuda/bin/activate
```

* Install dependencies
```bash
cd /home/diffusion_path_planning/diffusion

python3 -m pip install --upgrade pip


#python3 -m pip install setuptools==58.2.0 numpy==1.23.4 
#python3 -m pip install opencv-python==4.5.1.48 #build errors
#python3 -m pip install opencv-python==4.11.0.86 #from notebook works
#python3 -m pip install opencv-python==4.12.0.88 #works
python3 -m pip install PyQt5 h5py tqdm gym==0.17.3 typed-argument-parser==1.10.0 
python3 -m pip install termcolor==2.4.0 GitPython==3.1.37 matplotlib==3.7.2 pybullet==3.2.5 colorama==0.4.6 pandas imageio scipy==1.11.1 
python3 -m pip install torch torchvision einops wandb==0.14.2

# without versions
python3 -m pip install numpy 
python3 -m pip install opencv-python
python3 -m pip install PyQt5 h5py tqdm gym typed-argument-parser 
python3 -m pip install termcolor GitPython matplotlib pybullet colorama pandas imageio scipy
python3 -m pip install torch torchvision einops wandb


#Successfully installed numpy-2.2.6 opencv-python-4.12.0.88
#Successfully installed cloudpickle-3.1.1 docstring-parser-0.17.0 gym-0.26.2 gym_notices-0.1.0 h5py-3.15.1 mypy-extensions-1.1.0 tqdm-4.67.1 typed-argument-parser-1.11.0 typing-extensions-4.15.0 typing-inspect-0.9.0
#Successfully installed GitPython-3.1.45 colorama-0.4.6 gitdb-4.0.12 imageio-2.37.0 numpy-1.26.4 pandas-2.3.3 pybullet-3.2.7 smmap-5.0.2 termcolor-3.2.0 tzdata-2025.2
#Successfully installed annotated-types-0.7.0 certifi-2025.10.5 charset_normalizer-3.4.4 click-8.3.0 einops-0.8.1 fsspec-2025.9.0 idna-3.11 mpmath-1.3.0 networkx-3.5 nvidia-cublas-cu12-12.8.4.1 nvidia-cuda-cupti-cu12-12.8.90 nvidia-cuda-nvrtc-cu12-12.8.93 nvidia-cuda-runtime-cu12-12.8.90 nvidia-cudnn-cu12-9.10.2.21 nvidia-cufft-cu12-11.3.3.83 nvidia-cufile-cu12-1.13.1.3 nvidia-curand-cu12-10.3.9.90 nvidia-cusolver-cu12-11.7.3.90 nvidia-cusparse-cu12-12.5.8.93 nvidia-cusparselt-cu12-0.7.1 nvidia-nccl-cu12-2.27.5 nvidia-nvjitlink-cu12-12.8.93 nvidia-nvshmem-cu12-3.3.20 nvidia-nvtx-cu12-12.8.90 platformdirs-4.5.0 pydantic-2.12.3 pydantic-core-2.41.4 requests-2.32.5 sentry-sdk-2.42.1 sympy-1.14.0 torch-2.9.0 torchvision-0.24.0 triton-3.5.0 typing-inspection-0.4.2 wandb-0.22.2

# pip list --verbose #see all installed packages

#TORUN? pip install -U pip argcomplete? bloom? vcstool? lark? 
```
* Build ROS2 package
```bash
cd /home/diffusion_path_planning
colcon build --base-paths src


cd /home/diffusion_path_planning/diffusion/pb_diff_envs
pip install -e .
```
* Run visualization
```bash
cd /home/diffusion_path_planning/diffusion

python3 path_visualization_simulator.py --config "config/rm2d/rSmaze_nw3_hExt07_exp.py"

#?export QT_QPA_PLATFORM=offscreen
#[ utils/serialization ] Loading model epoch: 1900000
#load datafile: 100%|█████████████████| 5/5 [00:00<00:00, 365.66it/s]


error:
    from pb_diff_envs.utils.maze2d_utils import get_is_collision_static, get_is_connected, compute_dist_sum
ImportError: cannot import name 'get_is_collision_static' from partially initialized module 'pb_diff_envs.utils.maze2d_utils' (most likely due to a circular import) (/home/diffusion_path_planning/diffusion/pb_diff_envs/pb_diff_envs/utils/maze2d_utils.py)


```


* ROS2
```bash
# In your running terminal
#?source <venv_name>/bin/activate
#?python3 -m colcon build
#? source install/setup.bash
#? <run stuff>
```
* launch gazebo simulation
```bash
source /home/diffusion_path_planning/install/setup.bash 
ros2 launch robot_gazebo main.launch.py  
```

## Notes


## References
* [Setting up python environment in ros2](https://github.com/ros2/ros2/issues/1094#issuecomment-2916700723)
* [Docker for GUI-based environments?](https://stackoverflow.com/questions/24095968/docker-for-gui-based-environments)

