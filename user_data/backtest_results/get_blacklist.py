import json
import os, sys

file = ''

with open(os.path.join(sys.path[0], '.last_result.json'), "r") as last_result_file:
  last = json.load(last_result_file)
  file = last['latest_backtest']

coins = []

with open(os.path.join(sys.path[0], file), "r") as jsonfile:
  data = json.load(jsonfile)
  strategies = data["strategy"]
  for strategy_name in strategies:
    strategy = strategies[strategy_name]
    results_per_pair = strategy["results_per_pair"]
    for pair_result in results_per_pair:
      if pair_result["profit_mean"] < 0.008:
        pair = pair_result["key"]
        coin = pair.split("/", 1)
        coins.append(coin[0])

coins.sort()
coinstring = ''

for c in coins:
  coinstring += c + '|'

coinstring = coinstring[:-1]

file_object = open(os.path.join(sys.path[0], 'to_blacklist.txt'), 'a')
file_object.write(coinstring)
jsonfile.close()
file_object.close()