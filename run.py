import sounddevice as sd
import numpy as np
import time
import keyboard

# Configuration
SAMPLE_RATE = 44100
DURATION = 0.3
CLAP_THRESHOLD = 0.5
CLAP_GROUP_WINDOW = 2  # Time window to group claps (seconds)

def record_audio():
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    return np.squeeze(audio)

def detect_clap(audio):
    volume = np.max(np.abs(audio))
    return volume > CLAP_THRESHOLD

def get_letter_from_claps(clap_count):
    mapping = {
        1: 'A',
        2: 'B',
        3: 'C'
    }
    return mapping.get(clap_count, '?')

def main():
    print("👂 Listening for claps... (Press Ctrl+C to stop)")
    clap_times = []
    group_start_time = None

    try:
        while True:
            audio = record_audio()
            if detect_clap(audio):
                now = time.time()
                print("👏 Clap detected!")
                if group_start_time is None:
                    group_start_time = now
                    clap_times = [now]
                else:
                    clap_times.append(now)

            # Check if grouping time is over
            if group_start_time and (time.time() - group_start_time > CLAP_GROUP_WINDOW):
                clap_count = len(clap_times)
                letter = get_letter_from_claps(clap_count)
                if letter != '?':
                    keyboard.write(letter)
                    print(f"✅ Typed: {letter}")
                else:
                    print(f"❌ Unknown pattern: {clap_count} claps")

                # Reset for next group
                group_start_time = None
                clap_times = []

    except KeyboardInterrupt:
        print("\n🛑 Exiting. Bye!")

if __name__ == "__main__":
    main()
