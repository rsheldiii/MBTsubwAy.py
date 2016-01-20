class SubwayFormatter:
    # formats time into 4 numbers/letters [0-9noe] for use with display code
  @staticmethod
  def clock_time(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    if minutes > 99:
      return "none"
    else:
      return "{:0>2d}{:0>2d}".format(minutes,seconds)

  @staticmethod
  def human_time(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    if minutes > 99:
      return "No current trains scheduled"
    else:
      return "{:0>2d}:{:0>2d}".format(minutes,seconds)
