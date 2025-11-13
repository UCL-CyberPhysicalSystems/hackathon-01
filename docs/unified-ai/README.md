# Unified AI

## 🧠 Kubeflow Notebooks 
The Unified-AI Kubeflow Notebooks environment provides Jupyter Notebooks for experimentation and for interacting with other components via API.  
Data within the Kubeflow platform is managed through the Research Data Storage Service (RDSS) — UCL’s official storage service for research data. 
For more information, refer to the [RDSS Live Storage Access Guide](https://www.ucl.ac.uk/advanced-research-computing/platforms-services/research-data-storage-service/live-storage-access-guide).

🔧 Setup Instructions

1. Request an Account   
Contact:  
  * silvia.ramos@ucl.ac.uk  
  * a.esterson@ucl.ac.uk

2. Connect to the UCL VPN
Follow the guide: [UCL Virtual Private Network](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn)

3. Access the Kubeflow Interface
Visit: [kubeflow.arc-unified-ai.condenser.arc.ucl.ac.uk](https://kubeflow.arc-unified-ai.condenser.arc.ucl.ac.uk)

4. Create a Jupyter Notebook
Once logged in, create and configure your Jupyter Notebook workspace. You can also use the terminal to clone public repos. For example: `git clone https://github.com/UCL-CyberPhysicalSystems/hackathon-01.git`

## 🐳 Containers
To host and distribute container images, you can use the [GitHub Container Registry (GHCR)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
This registry allows you to store, manage, and version Docker images directly through GitHub for seamless integration with your CI/CD workflows. 

### Build Dockerfile container
```bash
docker build -t ros2uai:v0.0.2 -f Dockerfile .
```

### Authenticating with a personal access token (classic)
1. Create `Personal access tokens (classic)` https://github.com/settings/tokens  
	* Select the read:packages scope to download container images and read their metadata.  
	* Select the write:packages scope to download and upload container images and read and write their metadata.  
	* Select the delete:packages scope to delete container images.  
2. Save your personal access token (classic). We recommend saving your token as an environment variable.
3. Using the CLI for your container type, sign in to the Container registry service at ghcr.io.
```
export CR_PAT=YOUR_TOKEN
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

### Pushing container images 
Tag your Docker image using the image ID and your desired image name and hosting destination.
```bash
docker tag ros2uai:v0.0.2 ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.2
```
Pushing container images
```bash
docker push ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.2
```
Go to packages https://github.com/orgs/UCL-CyberPhysicalSystems/packages and change visibility to public


### Connecting to Unified-AI Kubeflow
1. Connect to VPN to access https://kubeflow.arc-unified-ai.condenser.arc.ucl.ac.uk
2. Create new notebook and set up custom image
```bash
ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.2
```

## Docker Management Commands
```bash
docker images && docker ps
docker exec -it <container_id> bash
docker exec -it $(docker container ls  | grep 'unifiedai:diffusion-motion-planning' | awk '{print $1}') bash
docker stop $(docker ps -q)
docker system prune -f --volumes
docker rmi --force <ID>
```

## Potential errors

* Using private images at https://github.com/orgs/UCL-CyberPhysicalSystems/packages/container/package/hackathon-01%2Fros2uai
> ImagePullBackOff: Back-off pulling image "ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.1": ErrImagePull: failed to pull and unpack image "ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.1": failed to resolve reference "ghcr.io/ucl-cyberphysicalsystems/hackathon-01/ros2uai:v0.0.1": unexpected status from HEAD request to https://ghcr.io/v2/ucl-cyberphysicalsystems/hackathon-01/ros2uai/manifests/v0.0.1: 403 Forbidden

* xcb display not availble
> ros2 run turtlesim turtlesim_node
qt.qpa.xcb: could not connect to display 
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, xcb.
[ros2run]: Aborted
#SORTED
jovyan@ghcrv3-0:~$ export QT_QPA_PLATFORM=offscreen
jovyan@ghcrv3-0:~$ ros2 run turtlesim turtlesim_node
