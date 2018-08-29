#!/usr/bin/python

import time, datetime, requests, yaml

class API:
  url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D=70180&api_key=40e710800b80496ebe17d584b103dab5"
  datetime_format = '%FT%T%z'
  time_format = "{:0>2d}{:0>2d}"

  def __init__(self):
    self.timestamp = time.time()
    self.prediction = 0
    self.exit = False
    self.loadSettings()

  def loadSettings(self):
    with open("./settings.yaml", 'r') as stream:
      settings = yaml.load(stream)
      self.settings = settings

  def formatted_url(self):
    return self.url.format(self.settings['api_key'], self.settings['stop_id'])

  def formatted_time_string(self):
    next_prediction = max(self.formatted_time(), 0)
    return self.time_format.format(next_prediction/60,next_prediction%60)

  # the time into the negatives. used to be used for blinking colon but that's annoying
  def formatted_time(self):
    return int(self.prediction - (time.time() - self.timestamp))

  def get_next_prediction(self):
    next_prediction = None

    try:
      data = requests.get(self.formatted_url()).json()
    except:
      data = {}
      print("failed to get data from API")

    if data.length > 0:
      predictions = [datetime.datetime.strptime(x['attributes']['arrival_time']) for x in data if x > (time.time() + self.delay)]
      if len(predictions) > 0:
        next_prediction = predictions[0]

    return next_prediction

api = API()

print(api.get_next_prediction())
