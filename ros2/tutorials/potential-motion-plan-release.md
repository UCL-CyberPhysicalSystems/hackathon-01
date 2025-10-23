# Potential Based Diffusion Motion Planning

## Run example
* Create env
```bash

python3 -m venv .env.ros2cuda --system-site-packages
source .env.ros2cuda/bin/activate
```

* Install dependencies
```bash
cd /home/diffusion_path_plannig/diffusion

python3 -m pip install setuptools==58.2.0 numpy==1.23.4 
#python3 -m pip install opencv-python==4.5.1.48 #build errors
#python3 -m pip install opencv-python==4.11.0.86 #from notebook works
python3 -m pip install opencv-python==4.12.0.88 #works
python3 -m pip install PyQt5 h5py tqdm gym==0.17.3 typed-argument-parser==1.10.0 
python3 -m pip install termcolor==2.4.0 GitPython==3.1.37 matplotlib==3.7.2 pybullet==3.2.5 colorama==0.4.6 pandas imageio scipy==1.11.1 
python3 -m pip install scipy==1.11.1 torch torchvision einops wandb==0.14.2

# pip list --verbose #see all installed packages

#TORUN? pip install -U pip argcomplete setuptools==58.2.0 bloom colcon-common-extensions rosdep vcstool lark 
```
* Build ROS2 package
```bash
cd diffusion_path_plannig
colcon build --base-paths src

cd pb_diff_envs 
pip install -e .
```
* Run visualization
```bash
python3 path_visualization_simulator.py --config "config/rm2d/rSmaze_nw3_hExt07_exp.py"
```


* ROS2
```bash
# In your running terminal
#?source <venv_name>/bin/activate
#?python3 -m colcon build
#? source install/setup.bash
#? <run stuff>
```


## Notes

* `path_visualization_simulator.py`
```bash
[ utils/serialization ] Loading model epoch: 1900000
load datafile: 100%|█████████████████| 5/5 [00:00<00:00, 365.66it/s]
```


## References
* https://github.com/ros2/ros2/issues/1094#issuecomment-2916700723

