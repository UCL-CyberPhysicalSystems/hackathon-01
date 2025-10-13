# Handling Data with the Research Data Storage Service (rdss)

## Connect to VPN

You can find instructions for connecting to the UCL Virtual Private Network (VPN) for your operating system here:
<https://www.ucl.ac.uk/isd/services/get-connected/ucl-virtual-private-network-vpn>

## Mounting/Umounting paths

### Linux

Use the following bash scripts [mount_rdss.bash](mount_rdss.bash) and [umount_rdss.bash](umount_rdss.bash) to mount and unmount the paths.
Be sure to replace UCL_USER with your own UCL username (e.g. a seven-character username), and DESTINATION with your chosen destination path (e.g. $HOME/datasets/rdss).
And of course, enter your password securely to gain access to the data in the respective locations.

```bash
cd github_project_root_path
cd scripts/data/
UCL_USER="put_your_user_name" (e.g. "cc12345")
DESTINATION="set_your_dataset_path" (e.g. "$HOME/datasets/rdss")
bash mount_rdss.bash $UCL_USER $DESTINATION
bash umount_rdss.bash $DESTINATION
```


