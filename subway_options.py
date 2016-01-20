import argparse, sys

class SubwayOptions:
  default_options = {
    'delay': 7 * 60,
    'stop_id': 0 # YOUR STOP HERE
  }

  def __init__(self, options={}):
    self.options = self.default_options
    self.options.update(self.load_from_argv())
    self.options.update(options)

  def __repr__(self):
    return self.options.__repr__()

  def load_from_file(self):
    return {}

  def load_from_argv(self):
    parser = argparse.ArgumentParser(description='get the next Subway train based on stop id')
    parser.add_argument('--delay', action="store", dest="delay", type=int, help="delay", default=None)
    parser.add_argument('--stop_id', action="store", dest="stop_id", type=int, help="stop id", default=None)
    parser.add_argument('-', action="store", dest="options_file", help="options file location", default=None)
    result = parser.parse_args(sys.argv[1:])

    ret = {}
    if result.options_file is not None:
      ret.update(self.load_from_file(result.options_file))
    if result.delay is not None:
      ret['delay'] = result.delay
    if result.stop_id is not None:
      ret['stop_id'] = result.stop_id

    return ret

  def get(self, key):
    return self.options.get(key, None)
