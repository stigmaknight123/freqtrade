# tested on VM.Standard.A1.Flex with Ubuntu 20.04

# Prepare VPS
sudo su
apt update && apt -y install build-essential pkg-config libblosc-dev  libhdf5-dev libssl-dev

# Install mambaforge (has most ARM ready packages, further details at https://github.com/conda-forge/miniforge )
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-pypy3-Linux-aarch64.sh
bash Mambaforge-pypy3-Linux-aarch64.sh
# just press enter a few times at license, and yes for default location

# need to exit terminal and re-enter to activate base environment
exit