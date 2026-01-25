# Condenser

## Setting up SSH certificates

1. Connect to UCL VPN (see [here](https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn) for details)

2. Upload (or generate) an SSH key > https://ssh.condenser.arc.ucl.ac.uk/ssh-keys (`id_condenser` and `id_condenser.pub`)

3. Generate SSH Certificates > https://ssh.condenser.arc.ucl.ac.uk/ssh-certificates (e.g., `id_condenser.signed`)

4. Create `~/.ssh/config`
```bash
Host condenser
  HostName ssh.condenser.arc.ucl.ac.uk
  User cloud-user
  CertificateFile ~/.ssh/id_condenser.signed
  IdentityFile ~/.ssh/id_condenser
```

## Available VMs
To connect to the VMs, you need to define the required details as local environment variables in your shell. 

:warning: It is important to note that IP addresses must not be shared publicly, as this can introduce security risks such as targeted attacks, denial-of-service (DoS/DDoS) attacks, geolocation tracking, network mapping, brute-force attacks, and identification or social engineering.

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
IMAGE="ghcr.io/mxochicale/ros2condenser:0.0.2"
docker pull $IMAGE

docker images
#REPOSITORY                         TAG       IMAGE ID       CREATED       SIZE
#ghcr.io/mxochicale/ros2condenser   0.0.1     4594077c8331   2 hours ago   6.4GB

[ -z "$DISPLAY" ] && export DISPLAY=:0 # Set DISPLAY if not set
docker run -it --rm --net=host --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/workspace $IMAGE  

#[rosuser@cyber-physical-lab-2:~][humble][Rust]$ ros2
#usage: ros2 [-h] [--use-python-default-buffering] Call `ros2 <command> -h` for more detailed usage. ...
#ros2 is an extensible command-line tool for ROS 2.
# ...
```


## Known issues and potential solutions 

### `rqt: could not connect to display`
* install x11 utils and restart VM to make effect
```
sudo apt install x11-xserver-utils 
#xhost +local:root  # Allow local connections (temporary security relaxation)
#xhost -local:root  # Restrict access when done
sudo apt install xvfb

```
* Check display manager
```
echo $XDG_SESSION_TYPE  # Should be 'x11' or 'wayland'
tty
```

### `cloud-user@ssh.condenser.arc.ucl.ac.uk: Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`

SSH certificates are valid for 7 days. Once a certificate expires, you will need to generate a new one by visiting:
https://ssh.condenser.arc.ucl.ac.uk/ssh-certificates (remember to be connected to the UCL VPN).

After downloading the certificate file (`id_condenser.signed`), place it in your home SSH directory (on macOS/Linux: `~/.ssh/`) and set the correct permissions:

```bash
chmod 600 ~/.ssh/id_condenser.signed
```

Example certificate file (`id_condenser.signed`)
```bash
ssh-ed25519-cert-v01@openssh.com <KEY>
```



## Deploying with Terraform
In the case you want to destroy and create a new VM, it is recommended to see https://condenser.arc.ucl.ac.uk/documentation/deploying_resources/deploying_terraform/
