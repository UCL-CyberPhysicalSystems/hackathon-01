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
To host and distribute container images, you can use the [Github Container Registry (GHCR)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
This registry allows you to store, manage, and version Docker images directly through GitHub for seamless integration with your CI/CD workflows. 

Build Dockerfile container
```bash
docker build -t unifiedai:diffusion-motion-planning -f Dockerfile .
```

Docker Management Commands
```bash
docker images && docker ps
docker exec -it <container_id> bash
docker exec -it $(docker container ls  | grep 'unifiedai:diffusion-motion-planning' | awk '{print $1}') bash
docker stop $(docker ps -q)
docker system prune -f --volumes
```
