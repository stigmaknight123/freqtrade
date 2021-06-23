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
DIRECTORY=/logs/
if [ ! -d "$DIRECTORY" ]; then
  mkdir logs
fi
DIRECTORY=/strategies/
if [ ! -d "$DIRECTORY" ]; then
  mkdir strategies
fi
cd strategies/
sudo wget https://raw.githubusercontent.com/froggleston/cryptofrog-strategies/main/CryptoFrog.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/DevilStra.py
sudo wget https://raw.githubusercontent.com/freqtrade/freqtrade-strategies/master/user_data/strategies/GodStra.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/GodStraNew.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/GodStraNewOpt.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/GodStraNewOptQuick.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHAndClucV8.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/MultiOffsetLamboV0.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NostalgiaForInfinityV3.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NostalgiaForInfinityV4.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NostalgiaForInfinityV5.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NostalgiaForInfinityV5_ProfitOnly.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/NormalizerStrategy.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHAndClucV8XH.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/SMAOffsetProtectOptV1.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/SMAOffsetProtectOptV1_opt.py
sudo wget https://raw.githubusercontent.com/stash86/freqtrade/develop/user_data/strategies/CombinedBinHClucAndMADV9.py
