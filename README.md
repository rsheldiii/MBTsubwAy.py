# MBTsubwAy.py, the terribly named library for interfacing with only the MBTA Subway application
## Specifically only for ETAs of subway trains so it's kinda bad
### Also it has a really long name

code is pretty self-documenting, there's an autogenerated help for command-line arguments that's probably not that helpful. Basically just look for your stop id by derping around the MBTA API and plug that puppy in and it should tell you when the next train is coming for that stop, AFTER the buffer window - which is currently 7 minutes but you can set it to whatever. Running the code will run that once.


This is not currently intended to be used by anyone so if you're reading this right now I'm quite impressed