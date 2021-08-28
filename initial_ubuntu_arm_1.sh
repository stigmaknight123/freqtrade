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
ssh back into VPS
sudo su # check if (base) activated

# install TA-Lib library first ( second half of https://mikestaszel.com/2021/01/23/install-ta-lib-on-m1/ for ARM linux)
apt install -y build-essential automake
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
cp /usr/share/automake-1.16/config.guess .
./configure --prefix=/usr
make
make install

# install Freqtrade
mkdir /freqtrade
cd /freqtrade

nano ftc.yml # paste contents of file that was sent separately
mamba env create -n ftc -f ftc.yml
conda activate ftc
freqtrade -V
freqtrade create-userdir --userdir user_data
freqtrade install-ui

# now freqtrade should be ready to run
# ftc.yml is based on stable version, see notes in file if dev is preferred

# suggest to set strategy inside the config file, then easy to swith strategy by editing config and reload_config. Easier for autostart, else need to reboot if want to swith strategy, see notes below.
  "strategy": "MyStrategy"


# for autostart at boot (did not test this on Oracle, but have used before on Ubuntu with Vultr)
nano /freqtrade/autostart.sh

# contents of autostart.sh
cd /freqtrade && \
source /root/mambaforge/etc/profile.d/conda.sh && \
conda run --no-capture-output -n ftc freqtrade trade --logfile user_data/logs/freqtrade.log --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite --config user_data/config.json

# make executable
chmod +x /freqtrade/autostart.sh

# load at boat with cron
crontab -e

# add this line in cron file
@reboot bash /freqtrade/autostart.sh
