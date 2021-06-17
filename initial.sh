sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose python3-pip
mkdir ft_userdata
cd ft_userdata/
mkdir docker
cd docker/
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/docker/Dockerfile.custom
cd ..
curl https://raw.githubusercontent.com/stash86/freqtrade/develop/docker-compose.yml -o docker-compose.yml
sudo docker-compose pull
sudo docker-compose run --rm freqtrade create-userdir --userdir user_data
DIRECTORY=/user_data/
if [ ! -d "$DIRECTORY" ]; then
  mkdir user_data
fi
cd user_data/
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/atur-telegram.json
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/atur-binance.json
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/config-static.json
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/config.json
DIRECTORY=/strategies/
if [ ! -d "$DIRECTORY" ]; then
  mkdir strategies
fi
cd strategies/
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/DevilStra.py
sudo wget https://raw.githubusercontent.com/freqtrade/freqtrade-strategies/master/user_data/strategies/GodStra.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/GodStraNew.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHAndClucV8.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NostalgiaForInfinityV4.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHAndClucV8XH.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHClucAndMADV6.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/SMAOffsetProtectOptV1.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/SMAOffsetProtectOptV1_opt.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHClucAndMADV9.py
