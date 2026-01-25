# zcam-python -- Streaming video with zenoh-python
https://github.com/eclipse-zenoh/zenoh-demos/tree/main/computer-vision/zcam/zcam-python

## Dependencies
```
pip3 install eclipse-zenoh opencv-python numpy imutils
```

## Running zcam-python
* Terminal 1
```
python3 zcapture.py -k 'demo/zcam/yourname'
```
* Terminal 2
```
python3 zdisplay.py -k 'demo/zcam/*'
```

## Shared Memory (SHM) transport
```
# Check current size
df -h /dev/shm
# Mount with larger size temporarily
sudo mount -o remount,size=2G /dev/shm

# TO HACK!
# Or make permanent in /etc/fstab
# Add: tmpfs /dev/shm tmpfs defaults,size=2G 0 0
```
