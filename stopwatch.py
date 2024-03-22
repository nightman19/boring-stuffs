#! python3
# stopwatch.py - A simple stopwatch program.


import time


starter_message = 'Press ENTER to begin. \n' \
                  'Afterwards, press ENTER to "click" the stopwatch.\n' \
                  'Press Ctrl-C to quit.'
print(starter_message)          # Displays the program's instructions.
input()                         # Listening for user input.
print('Started...')
startTime = time.time()         # get the first lap's start time
lastTime = startTime
lapNum = 1


# Start tracking the lap times.
try:
    while True:
        input()
        lapTime = round(time.time() - lastTime, 2)
        totalTime = round(time.time() - startTime, 2)
        print('Lap #%s: %s (%s)' % (lapNum, totalTime, lapTime), end='')
        lapNum += 1
        lastTime = time.time()          #reset the last lap time
except KeyboardInterrupt:
    # Handle the Ctrl-C exception to keep its error message from displaying.
    print('\nDone!')
