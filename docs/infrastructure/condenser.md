# Condenser

## Setting up SSH certificates

1. Connect to UCL VPN (see [here](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn) for details)

2. Upload (or generate) an SSH key > https://ssh.condenser.arc.ucl.ac.uk/ssh-keys

3. Generate SSH Certificates > https://ssh.condenser.arc.ucl.ac.uk/ssh-certificates

4. Create `~/.ssh/config`
```bash
Host condenser
  HostName ssh.condenser.arc.ucl.ac.uk
  User cloud-user
  CertificateFile ~/.ssh/id_condenser.signed
  IdentityFile ~/.ssh/id_condenser
```

## Available VMs
```bash
IP0=00.000.00.2
IP1=00.000.00.3
IP2=00.000.00.4
ssh -J condenser ubuntu@${IP0} # for cyber-physical-lab-0 
ssh -J condenser ubuntu@${IP1} # for cyber-physical-lab-1
ssh -J condenser ubuntu@${IP2} # for cyber-physical-lab-2
```

## Pull image
```bash
# install docker
sudo apt install docker.io
sudo usermod -aG docker $USER # Log out and log back in for changes to take effect
#setup image, pull and run it
IMAGE="ghcr.io/mxochicale/ros2condenser:0.0.1"
docker pull $IMAGE

docker images
#REPOSITORY                         TAG       IMAGE ID       CREATED       SIZE
#ghcr.io/mxochicale/ros2condenser   0.0.1     4594077c8331   2 hours ago   6.4GB

docker run -it --rm   --net=host   --privileged   -v $(pwd):/workspace   $IMAGE  

#[rosuser@cyber-physical-lab-2:~][humble][Rust]$ ros2
#usage: ros2 [-h] [--use-python-default-buffering] Call `ros2 <command> -h` for more detailed usage. ...
#ros2 is an extensible command-line tool for ROS 2.
# ...
```

## Deploying with Terraform
In the case you want to destroy and create a new VM, it is recommended to see https://condenser.arc.ucl.ac.uk/documentation/deploying_resources/deploying_terraform/