import time
from clapDetector import ClapDetector

# Detection settings
thresholdBias = 6000
lowcut = 200
highcut = 3200
minClapInterval = 0.15    # Minimum time between claps
sequenceTimeout = 1.0     # Time window to group claps

# Initialize
clapDetector = ClapDetector(inputDevice=-1, logLevel=0)
clapDetector.initAudio()

try:
    lastClapTime = 0
    clapTimes = []

    while True:
        audioData = clapDetector.getAudio()
        result = clapDetector.run(thresholdBias=thresholdBias, lowcut=lowcut, highcut=highcut, audioData=audioData)
        now = time.time()

        if result:
            if now - lastClapTime > minClapInterval:
                clapTimes.append(now)
                lastClapTime = now

        # Remove old claps
        clapTimes = [t for t in clapTimes if now - t <= sequenceTimeout]

        # If enough time passed since last clap, evaluate
        if clapTimes and (now - clapTimes[-1] > sequenceTimeout):
            count = len(clapTimes)
            if count == 1:
                print("One")
            elif count == 2:
                print("Two")
            else:
                print("Three")
            clapTimes.clear()

        time.sleep(1 / 60)

except KeyboardInterrupt:
    pass
except Exception:
    pass
finally:
    clapDetector.stop()
