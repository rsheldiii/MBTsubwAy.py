#!/usr/bin/python

import time, datetime, requests, yaml
from dateutil import parser

class API:
  url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D=70180&api_key=40e710800b80496ebe17d584b103dab5"

  def __init__(self):
    self.loadSettings()

  def loadSettings(self):
    with open("./settings.yaml", 'r') as stream:
      settings = yaml.load(stream)
      self.settings = settings

  def formatted_url(self):
    return self.url.format(self.settings['api_key'], self.settings['stop_id'])

  def get_next_prediction(self):
    next_prediction = None

    try:
      data = requests.get(self.formatted_url()).json()
    except:
      data = {}
      print("failed to get data from API")


    print(data)
      
    if len(data['data']) > 0:
      now = datetime.datetime.now(datetime.timezone.utc)
      predictions = [parser.parse(x['attributes']['arrival_time']) for x in data['data']]
      filtered_predictions = [x for x in predictions if (x - now).seconds > self.settings['delay']]
      filtered_predictions.sort
      if len(filtered_predictions) > 0:
        return (filtered_predictions[0] - now).seconds
      else: return False
    else: return False


if __name__ == '__main__':
  api = API()

  print(api.get_next_prediction())
