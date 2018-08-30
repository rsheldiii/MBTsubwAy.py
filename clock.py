#!/usr/bin/python

import time, datetime, signal, sys, requests, yaml
from Adafruit_7Segment import SevenSegment
from threading import Thread, Lock
from api import API

print("Press CTRL+C to power down")

class Clock:
  segment = SevenSegment(address = 0x70)
  mutex = Lock()
  time_format = "{:0>2d}{:0>2d}"

  def __init__(self):
    self.timestamp = time.time()
    self.prediction = 0
    self.exit = False
    self.api = API()

  def formatted_time_string(self):
    next_prediction = max(self.formatted_time(), 0)
    return self.time_format.format(next_prediction//60,next_prediction%60)

  # the time into the negatives. used to be used for blinking colon but that's annoying
  def formatted_time(self):
    return int(self.prediction - (time.time() - self.timestamp))

  def get_next_prediction(self):
    next_prediction = self.api.get_next_prediction()
    next_timestamp = int(time.time())
 
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

    print(self.prediction)

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
    if int(time.time() - self.timestamp) > 65: #TODO self.delta was here but splitting out settings put it in the api lol
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
