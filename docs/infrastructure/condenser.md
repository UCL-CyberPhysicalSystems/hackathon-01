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
IP0=00.000.00.0
IP1=00.000.00.0
IP2=00.000.00.0
ssh -J condenser ubuntu@${IP0} # for cyber-physical-lab-0 
ssh -J condenser ubuntu@${IP1} # for cyber-physical-lab-1
ssh -J condenser ubuntu@${IP2} # for cyber-physical-lab-2
```

## Deploying with Terraform
In the case you want to destroy and create a new VM, it is recommended to see https://condenser.arc.ucl.ac.uk/documentation/deploying_resources/deploying_terraform/