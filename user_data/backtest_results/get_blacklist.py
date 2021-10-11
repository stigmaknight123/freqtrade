import json
import os, sys

file = ''

with open(os.path.join(sys.path[0], '.last_result.json'), "r") as last_result_file:
    last = json.load(last_result_file)
    file = last['latest_backtest']

coins = []

with open(os.path.join(sys.path[0], file), "r") as jsonfile:
  data = json.load(jsonfile)
  for x in data:
      if x == 'strategy':
          y = data[x]
          for z in y:
              q = y[z]
              for r in q:
                  if r == 'results_per_pair':
                      s = q[r]
                      for t in s:
                          if t['profit_mean'] < 0.08:
                              string = t['key']
                              coin = string.split("/", 1)
                              #print(coin[0] + ' avg profit: ' + str(t['profit_mean']))
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