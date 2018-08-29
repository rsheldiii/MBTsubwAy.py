#!/usr/bin/python

import time, datetime, signal, sys, requests, yaml
from Adafruit_7Segment import SevenSegment
from threading import Thread, Lock

print "Press CTRL+C to power down"

class Clock:
  url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D=70180&api_key=40e710800b80496ebe17d584b103dab5"
  segment = SevenSegment(address = 0x70)
  mutex = Lock()
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
    return self.url.format(self.settings['stop_id'])

  def formatted_time_string(self):
    next_prediction = max(self.formatted_time(), 0)
    return self.time_format.format(next_prediction/60,next_prediction%60)

  # the time into the negatives. used to be used for blinking colon but that's annoying
  def formatted_time(self):
    return int(self.prediction - (time.time() - self.timestamp))

  def get_next_prediction(self):
    next_timestamp = None
    next_prediction = None

    try:
      data = requests.get(self.formatted_url()).json()
      next_timestamp = int(time.time())
    except:
      data = {}
      print "failed to get data from API"

    if data.get("mode", False):
      #TODO this might fail if there are no routes, or if a direction is disabled.
      raw_trips = data["mode"][0]["route"][0]["direction"][0]["trip"]
      predictions = [int(x['pre_away']) for x in raw_trips]
      predictions.sort # not strictly necessary I dont think
      filtered_predictions = [x for x in predictions if x > self.delay]
      if len(filtered_predictions) > 0:
        next_prediction = filtered_predictions[0]

    self.mutex.acquire()
    try:
      if next_timestamp and next_prediction:
        self.timestamp = next_timestamp
        self.prediction = next_prediction
    finally:
      self.mutex.release()

  def step(self):
    #TODO "none" shown on clock when no trains?
    character_string = self.formatted_time_string()

    print self.prediction

    if int(character_string[0]) != 0:
      self.segment.writeDigit(0, int(character_string[0])) # Tens
    else:
      self.segment.writeDigitRaw(0, 0)

    self.segment.writeDigit(1, int(character_string[1])) # Ones

    self.handle_colon()

    self.segment.writeDigit(3, int(character_string[2]))   # Tens
    self.segment.writeDigit(4, int(character_string[3]))        # Ones
    # Toggle colon

  def handle_colon(self):
    code = 2
    if int(time.time() - self.timestamp) > self.delta:
      code |= 4

    self.segment.writeDigitRaw(2, code)

  def clock_loop(self):
    while not self.exit:
      self.step()
      time.sleep(0.125)

  def worker_loop(self):
    while not self.exit: #TODO is it worth looping a bunch in order to check for exit flags
      self.get_next_prediction()
      time.sleep(30)
    self.clear() # so clock clears on exit

  def run(self):
    worker_thread = Thread(target = self.worker_loop)
    worker_thread.start()
    self.clock_loop()

  def exit_gracefully(self, a, b):
    print("beginning exit...")

    self.mutex.acquire()
    try:
      self.exit = True
    finally:
      self.mutex.release()

  def clear(self):
    for i in range(0,5):
      self.segment.writeDigitRaw(i, 0)

c = Clock()
signal.signal(signal.SIGINT, c.exit_gracefully) # should probably leave out here. don't want each instance setting one for itself
c.run()
